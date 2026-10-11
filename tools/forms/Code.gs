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

// 自動返信メールの下部に載せる、アキヤド（メディア）の案内。リンクには GA4 で効果を測るための utm を付ける
var PROMO = {
  title: 'ご連絡までの間に、アキヤドもご覧ください',
  lead: '空き家の売却・活用や、副業ではじめる民泊について、宿を運営する私たちが悩みに沿って解説しているメディアです。',
  links: [
    ['空き家を売りたい方へ', '/media/guide-sell.html'],
    ['空き家を活かしたい方へ', '/media/guide-use.html'],
    ['副業で宿をはじめたい方へ', '/media/guide-side.html'],
    ['空き家と民泊を、ゼロから体系的に学ぶ', '/media/learn.html']
  ],
  top: ['アキヤドのトップへ', '/media.html']
};
function promoUrl(path, formType) {
  return CONFIG.SITE_URL + path + '?utm_source=autoreply&utm_medium=email&utm_campaign=' + formType;
}

// 画面に出したくない内部用の項目
var HIDDEN_KEYS = ['_subject', '_form', '_gotcha', 'website', '_page'];
// お客様向けの自動返信には載せない項目（社内でだけ使う情報・お客様が入力していない項目）
var CUSTOMER_HIDDEN_KEYS = ['流入元', 'ご相談カテゴリ', 'プライバシーポリシーへの同意', 'privacy_agree'];
// 項目名の日本語表記
var LABELS = { name: 'お名前', email: 'メールアドレス', tel: '電話番号', company: '会社名', category: 'ご相談の種類', message: 'お問い合わせ内容', detail: '詳細', privacy_agree: 'プライバシーポリシーへの同意' };

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

// 入力された項目を [項目名, 値] の一覧にする（空欄は省く）
function fieldPairs(fields, forCustomer) {
  var out = [];
  Object.keys(fields).forEach(function (k) {
    if (HIDDEN_KEYS.indexOf(k) >= 0) return;
    if (forCustomer && CUSTOMER_HIDDEN_KEYS.indexOf(k) >= 0) return;
    var v = String(fields[k] == null ? '' : fields[k]).trim();
    if (!v) return;
    out.push([LABELS[k] || k, v]);
  });
  return out;
}

function fieldLines(fields, forCustomer) {
  return fieldPairs(fields, forCustomer).map(function (p) {
    return p[1].indexOf('\n') >= 0 ? '■ ' + p[0] + '\n' + p[1] : '■ ' + p[0] + '：' + p[1];
  });
}

function esc(t) {
  return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
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
  var name = String(fields.name).trim();
  var pairs = fieldPairs(fields, true);
  var lines = t.body.map(function (l) { return l.replace(/\{name\}/g, name); });

  // 文字だけの版（HTML を表示できないメールソフト向け）
  var text = lines.concat(['', '【お問い合わせ内容】'])
    .concat(pairs.map(function (p) { return p[1].indexOf('\n') >= 0 ? '・' + p[0] + '\n' + p[1] : '・' + p[0] + '：' + p[1]; }))
    .concat(['', '――――――――――――――', '■ ' + PROMO.title, PROMO.lead])
    .concat(PROMO.links.concat([PROMO.top]).map(function (l) { return '・' + l[0] + '\n  ' + promoUrl(l[1], formType); }))
    .concat(SIGNATURE).join('\n');

  // HTML の版（スマホでも読みやすいように、段落と表で整える）
  var notes = lines.filter(function (l) { return l.indexOf('※') === 0; });
  var paras = lines.filter(function (l) { return l.indexOf('※') !== 0; }).join('\n').split(/\n\s*\n/);
  var html = '<div style="font-family:-apple-system,BlinkMacSystemFont,\'Hiragino Sans\',\'Noto Sans JP\',sans-serif;font-size:15px;line-height:1.8;color:#111;max-width:600px;">'
    + paras.map(function (p) { return '<p style="margin:0 0 16px;">' + esc(p).replace(/\n/g, '<br>') + '</p>'; }).join('')
    + '<p style="margin:24px 0 8px;font-weight:bold;">お問い合わせ内容</p>'
    + '<table style="width:100%;border-collapse:collapse;font-size:14px;">'
    + pairs.map(function (p) {
      return '<tr><th style="text-align:left;vertical-align:top;white-space:nowrap;padding:8px 12px 8px 0;border-top:1px solid #eee;color:#555;font-weight:normal;">' + esc(p[0])
        + '</th><td style="padding:8px 0;border-top:1px solid #eee;word-break:break-all;">' + esc(p[1]).replace(/\n/g, '<br>') + '</td></tr>';
    }).join('')
    + '</table>'
    + (notes.length ? '<p style="margin:24px 0 0;font-size:13px;color:#666;">' + notes.map(esc).join('<br>') + '</p>' : '')
    + '<div style="margin:32px 0 0;padding:20px;background:#f6f7f5;border-radius:6px;">'
    + '<p style="margin:0 0 6px;font-weight:bold;font-size:15px;">' + esc(PROMO.title) + '</p>'
    + '<p style="margin:0 0 12px;font-size:13px;color:#555;">' + esc(PROMO.lead) + '</p>'
    + PROMO.links.map(function (l) {
      return '<a href="' + promoUrl(l[1], formType) + '" style="display:block;padding:10px 0;border-top:1px solid #e3e6e1;color:#1A472A;text-decoration:none;font-size:14px;">' + esc(l[0]) + ' &rarr;</a>';
    }).join('')
    + '<a href="' + promoUrl(PROMO.top[1], formType) + '" style="display:inline-block;margin-top:12px;padding:10px 18px;background:#1A472A;color:#fff;text-decoration:none;border-radius:4px;font-size:14px;">' + esc(PROMO.top[0]) + '</a>'
    + '</div>'
    + '<p style="margin:32px 0 0;padding-top:16px;border-top:1px solid #eee;font-size:13px;color:#555;">合同会社RIVIA&amp;CO.<br><a href="' + CONFIG.SITE_URL + '" style="color:#1A472A;">' + CONFIG.SITE_URL.replace('https://', '') + '</a></p>'
    + '</div>';

  MailApp.sendEmail({ to: fields.email, subject: t.subject, body: text, htmlBody: html, name: CONFIG.SENDER_NAME, replyTo: CONFIG.NOTIFY_TO });
}

// 設置したあと、Apps Script の画面で一度だけ実行する（権限の許可と、フォルダ・スプレッドシートの作成）
function setup() {
  var f = getFolder();
  var s = getSheet();
  console.log('フォルダ: ' + f.getUrl());
  console.log('スプレッドシート: ' + s.getParent().getUrl());
  console.log('今日あと送れるメール数: ' + MailApp.getRemainingDailyQuota());
}
