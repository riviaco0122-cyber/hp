/**
 * RIVIA&CO.／アキヤド お問い合わせフォームの受け口（Google Apps Script）
 *
 * できること（すべて無料。あなたの Google アカウントの中で動く）
 *   1. サイトのフォームから送られた内容を受け取る（項目はフォームごとに違ってよい）
 *   2. 添付ファイルを Google ドライブのフォルダに保存する
 *   3. 内容を Google スプレッドシートに1件1行で記録する
 *   4. 社内（NOTIFY_TO）に通知メールを送る（返信すると、お客様に直接届く）
 *   5. お客様に自動返信（お礼）メールを送る
 *
 * 設置方法は docs/forms-setup-guide.md を参照。
 * このファイルを変えたら、Apps Script の画面で「デプロイ」→「デプロイを管理」→ 編集 →
 * バージョン「新バージョン」→「デプロイ」をする（URL は変わらない）。
 */

// ===== 設定（必要に応じて書き換える） =====
var CONFIG = {
  NOTIFY_TO: 'rivia.co0122@gmail.com',          // 社内通知の送り先（カンマ区切りで複数可）
  SENDER_NAME: '合同会社RIVIA&CO.',              // 自動返信メールの差出人名
  SITE_URL: 'https://rivia-co.com',
  FOLDER_NAME: 'RIVIA_お問い合わせ_添付ファイル',  // 添付ファイルを保存するドライブのフォルダ名
  SHEET_NAME: 'RIVIA_お問い合わせ一覧',            // 記録用スプレッドシートの名前
  MAX_TOTAL_BYTES: 10 * 1024 * 1024,              // 添付ファイルの合計の上限（10MB）
  MAX_FILES: 5,
  ALLOWED_EXT: ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'heic', 'gif', 'webp'],
  RATE_LIMIT_PER_10MIN: 3                          // 同じメールアドレスから10分間に受け付ける件数
};

// フォームの種類ごとの自動返信の文面（{name} はお名前に置き換わる）
var REPLY = {
  contact: {
    subject: '【RIVIA&CO.】お問い合わせを受け付けました',
    body: [
      '{name} 様',
      '',
      'このたびは合同会社RIVIA&CO.にお問い合わせいただき、ありがとうございます。',
      '以下の内容でお問い合わせを受け付けました。',
      '内容を確認のうえ、2営業日以内に担当者よりご連絡いたします。',
      '',
      '※ このメールは、お問い合わせを受け付けた時点で自動でお送りしています。',
      '※ 2営業日を過ぎても連絡がない場合は、お手数ですがこのメールにご返信ください。'
    ]
  },
  akiyado: {
    subject: '【アキヤド】お問い合わせを受け付けました',
    body: [
      '{name} 様',
      '',
      'このたびはアキヤド（運営：合同会社RIVIA&CO.）にお問い合わせいただき、ありがとうございます。',
      '以下の内容でお問い合わせを受け付けました。',
      '内容を確認のうえ、2営業日以内に担当者よりご連絡いたします。',
      '',
      '※ このメールは、お問い合わせを受け付けた時点で自動でお送りしています。',
      '※ 2営業日を過ぎても連絡がない場合は、お手数ですがこのメールにご返信ください。'
    ]
  },
  careers: {
    subject: '【RIVIA&CO.】エントリーを受け付けました',
    body: [
      '{name} 様',
      '',
      'このたびは合同会社RIVIA&CO.の採用にご応募いただき、ありがとうございます。',
      '以下の内容でエントリーを受け付けました。',
      '内容を確認のうえ、担当者よりご連絡いたします。',
      '',
      '※ このメールは、エントリーを受け付けた時点で自動でお送りしています。'
    ]
  }
};
var SIGNATURE = [
  '',
  '────────────────',
  '合同会社RIVIA&CO.',
  'https://rivia-co.com',
  '────────────────'
];

// 画面に出したくない内部用の項目
var HIDDEN_KEYS = ['_subject', '_form', '_gotcha', 'website', '_page'];

// ===== 受け口 =====
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var fields = data.fields || {};
    var files = data.files || [];

    // 迷惑送信の対策（人には見えない項目に入力があれば、受け付けたふりをして捨てる）
    if (fields._gotcha || fields.website) return json({ ok: true });

    var email = String(fields.email || '').trim();
    var name = String(fields.name || '').trim();
    if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ ok: false, error: 'invalid' });
    if (!rateLimitOk(email)) return json({ ok: false, error: 'rate_limit' });

    var formType = ['contact', 'akiyado', 'careers'].indexOf(fields._form) >= 0 ? fields._form : 'contact';
    var saved = saveFiles(files, name);
    var row = record(formType, fields, saved);
    notify(formType, fields, saved, row);
    autoReply(formType, fields);
    return json({ ok: true });
  } catch (err) {
    console.error(err);
    try { MailApp.sendEmail(CONFIG.NOTIFY_TO, '【要確認】フォームの受け付けでエラー', String(err && err.stack || err)); } catch (e2) {}
    return json({ ok: false, error: 'server' });
  }
}

// 動作確認用（ブラウザで URL を開くと ok と出る）
function doGet() {
  return json({ ok: true, service: 'rivia-forms', quota: MailApp.getRemainingDailyQuota() });
}

// ===== 部品 =====
function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function rateLimitOk(email) {
  var cache = CacheService.getScriptCache();
  var key = 'rl_' + Utilities.base64EncodeWebSafe(email.toLowerCase()).slice(0, 200);
  var n = Number(cache.get(key) || 0);
  if (n >= CONFIG.RATE_LIMIT_PER_10MIN) return false;
  cache.put(key, String(n + 1), 600);
  return true;
}

function getFolder() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty('FOLDER_ID');
  if (id) { try { return DriveApp.getFolderById(id); } catch (e) {} }
  var folder = DriveApp.createFolder(CONFIG.FOLDER_NAME);
  props.setProperty('FOLDER_ID', folder.getId());
  return folder;
}

function getSheet() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty('SHEET_ID');
  var ss = null;
  if (id) { try { ss = SpreadsheetApp.openById(id); } catch (e) {} }
  if (!ss) {
    ss = SpreadsheetApp.create(CONFIG.SHEET_NAME);
    props.setProperty('SHEET_ID', ss.getId());
    ss.getSheets()[0].appendRow(['受付日時', 'フォーム', 'お名前', 'メール', '内容（すべての項目）', '添付ファイル', '流入元']);
  }
  return ss.getSheets()[0];
}

function saveFiles(files, name) {
  var out = [];
  if (!files.length) return out;
  if (files.length > CONFIG.MAX_FILES) files = files.slice(0, CONFIG.MAX_FILES);
  var total = 0;
  var folder = null;
  var stamp = Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyyMMdd-HHmm');
  files.forEach(function (f) {
    var ext = String(f.name || '').split('.').pop().toLowerCase();
    if (CONFIG.ALLOWED_EXT.indexOf(ext) < 0) { out.push({ name: f.name, error: '対応していない形式のため保存していません' }); return; }
    var bytes = Utilities.base64Decode(f.data || '');
    total += bytes.length;
    if (total > CONFIG.MAX_TOTAL_BYTES) { out.push({ name: f.name, error: '合計サイズの上限を超えたため保存していません' }); return; }
    folder = folder || getFolder();
    var blob = Utilities.newBlob(bytes, f.type || 'application/octet-stream', stamp + '_' + name + '_' + f.name);
    var file = folder.createFile(blob);  // 共有設定は「自分のみ」のまま（外部に公開しない）
    out.push({ name: f.name, url: file.getUrl() });
  });
  return out;
}

function fieldLines(fields) {
  var lines = [];
  Object.keys(fields).forEach(function (k) {
    if (HIDDEN_KEYS.indexOf(k) >= 0) return;
    var label = { name: 'お名前', email: 'メールアドレス', tel: '電話番号', company: '会社名', category: 'ご相談の種類', message: 'お問い合わせ内容', detail: '詳細' }[k] || k;
    lines.push('■ ' + label + '\n' + String(fields[k]));
  });
  return lines;
}

function record(formType, fields, saved) {
  var sheet = getSheet();
  var now = Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyy/MM/dd HH:mm');
  sheet.appendRow([now, formType, fields.name, fields.email, fieldLines(fields).join('\n\n'),
    saved.map(function (s) { return s.url || (s.name + '（' + s.error + '）'); }).join('\n'), fields['流入元'] || fields._page || '']);
  return sheet.getLastRow();
}

function notify(formType, fields, saved, row) {
  var label = { contact: 'お問い合わせ', akiyado: 'アキヤドのお問い合わせ', careers: '採用エントリー' }[formType];
  var subject = '【' + label + '】' + fields.name + ' 様' + (fields._subject ? '（' + fields._subject + '）' : '');
  var body = [label + 'がありました。このメールに返信すると、お客様に直接届きます。', '']
    .concat(fieldLines(fields))
    .concat(['', '■ 添付ファイル'])
    .concat(saved.length ? saved.map(function (s) { return '- ' + s.name + '：' + (s.url || s.error); }) : ['なし'])
    .concat(['', '■ 記録', 'スプレッドシート「' + CONFIG.SHEET_NAME + '」の ' + row + ' 行目'])
    .join('\n');
  MailApp.sendEmail({ to: CONFIG.NOTIFY_TO, subject: subject, body: body, replyTo: fields.email, name: 'RIVIA フォーム通知' });
}

function autoReply(formType, fields) {
  var t = REPLY[formType] || REPLY.contact;
  var summary = ['', '――― お問い合わせ内容 ―――'].concat(fieldLines(fields)).concat(['――――――――――――――']);
  var body = t.body.concat(summary).concat(SIGNATURE).join('\n').replace(/\{name\}/g, fields.name);
  MailApp.sendEmail({ to: fields.email, subject: t.subject, body: body, name: CONFIG.SENDER_NAME, replyTo: CONFIG.NOTIFY_TO });
}

// 設置したあと、Apps Script の画面で一度だけ実行する（権限の許可と、フォルダ・スプレッドシートの作成）
function setup() {
  var f = getFolder();
  var s = getSheet();
  console.log('フォルダ: ' + f.getUrl());
  console.log('スプレッドシート: ' + s.getParent().getUrl());
  console.log('今日あと送れるメール数: ' + MailApp.getRemainingDailyQuota());
}
