/**
 * アキヤド：民泊できる？1分診断（media/minpaku-check.html だけで読む）
 * 仕様は docs/tools/minpaku-check.md。判定の計算は judge() にまとめ、表示は render() が行う。
 * 計測（GA4）: tool_start（1問目に答えた）・tool_step（step 番号）・tool_complete（score_band・route）。gtag があるときだけ送る。
 */
(function () {
  'use strict';
  var root = document.getElementById('mchk');
  var dataEl = document.getElementById('mchk-data');
  if (!root || !dataEl) return;
  var D = JSON.parse(dataEl.textContent);
  var panel = document.getElementById('mchk-panel');
  var result = document.getElementById('mchk-result');
  var steps = root.querySelectorAll('.mchk__step');
  var back = root.querySelector('.mchk__back');
  var next = root.querySelector('.mchk__next');
  var count = root.querySelector('.mchk__count b');
  var bar = root.querySelector('.mchk__progress');
  var N = steps.length, cur = 1, started = false, pointer = false;

  var send = function (name, params) {
    if (typeof window.gtag !== 'function') return;
    params = params || {};
    params.tool_name = 'minpaku-check';
    window.gtag('event', name, params);
  };
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  // ------------------------------------------------------------ 判定（仕様 3章。数字は仕様の表のものだけ）
  function judge(a) {
    var condo = a.type === 'condo', z = a.zone;
    var ryokan, minpaku;
    if (z === 'unknown') ryokan = { s: 'hold', t: '判定を保留', n: '用途地域がわかると判定できます。' };
    else if (condo) ryokan = { s: 'hard', t: '難しい', n: 'マンション・アパートの1室は、旅館業は現実的に難しい扱いです。' };
    else if (z === 'res' || z === 'com') ryokan = { s: 'ok', t: 'できそう', n: '通年で営業できる制度です。' + (z === 'res' ? '第一種住居地域は3,000㎡以下です。' : '') + (a.area === 'gt200' ? '200㎡を超えるため、用途変更の確認申請が要ります。' : '') };
    else if (z === 'chosei') ryokan = { s: 'consult', t: '要相談', n: '用途の変更に許可が要り、難しいことが多いです。' };
    else ryokan = { s: 'hard', t: '難しい', n: 'この用途地域では、旅館業の営業はできません。' };

    if (z === 'unknown') minpaku = { s: 'hold', t: '判定を保留', n: '用途地域がわかると判定できます。' };
    else if (z === 'chosei') minpaku = { s: 'consult', t: '要相談', n: '自治体の判断によります。保健所・市町村への事前の相談が必要です。' };
    else if (z === 'ind') minpaku = { s: 'consult', t: '要確認', n: '工業専用地域は、住宅が建てられないため対象外です。' };
    else minpaku = { s: 'ok', t: '届出できそう', n: '条例で日数・区域が制限されることがあります。' + (condo ? '管理規約で民泊が禁止されていないことが必要です。' : '') };

    var seido = ryokan.s === 'ok' ? 'ryokan' : minpaku.s === 'ok' ? 'minpaku' : 'consult';
    var pts = {
      seido: { ryokan: 40, minpaku: 25, consult: 20 }[seido],
      hazard: { none: 20, unknown: 10, colored: 5 }[a.hazard],
      state: { ready: 25, care: 15, major: 5 }[a.state],
      area: { m60: 15, m150: 12, lt60: 8, gt200: 8 }[a.area]
    };
    var score = pts.seido + pts.hazard + pts.state + pts.area;
    var band = score >= 70 ? 'high' : score >= 45 ? 'mid' : 'low';
    var p1, p2;
    if (a.goal === 'sell') { p1 = ['sell']; p2 = ['use']; }
    else if (a.goal === 'lend') { p1 = ['use']; p2 = ['sell']; }
    else if (a.goal === 'start') { p1 = ['side']; p2 = ['use']; }
    else { p1 = band === 'high' ? ['use', 'side'] : band === 'mid' ? ['use'] : ['sell']; p2 = []; }
    return { ryokan: ryokan, minpaku: minpaku, seido: seido, pts: pts, score: score, band: band, primary: p1, secondary: p2,
             nights: Math.round(365 * D.occAvg / 100 / 10) * 10 };
  }

  // ------------------------------------------------------------ 画面の切り替え
  var answers = function () {
    var a = {};
    root.querySelectorAll('.mchk__form input:checked').forEach(function (i) { a[i.name] = i.value; });
    return a;
  };
  var stepDone = function (n) {
    var groups = steps[n - 1].querySelectorAll('.mchk__group');
    return Array.prototype.every.call(groups, function (g) { return g.querySelector('input:checked'); });
  };
  function show(n, quiet) {
    cur = n;
    steps.forEach(function (s, i) { s.hidden = i !== n - 1; });
    back.hidden = n === 1;
    count.textContent = n;
    bar.setAttribute('aria-valuenow', n);
    bar.firstElementChild.style.width = (n / N * 100) + '%';
    next.disabled = !stepDone(n);
    next.textContent = n === N ? '結果を見る' : '次へ';
    var q = steps[n - 1].querySelector('.mchk__q');
    if (q && !quiet) q.focus({ preventScroll: true });
  }
  function go() {
    if (!stepDone(cur)) return;
    send('tool_step', { step: cur });
    if (cur < N) { show(cur + 1); scrollTop(); }
    else finish();
  }
  var scrollTop = function () {
    var r = root.getBoundingClientRect();
    if (r.top < 0) window.scrollTo({ top: window.scrollY + r.top - 140, behavior: 'smooth' });
  };

  root.addEventListener('pointerdown', function () { pointer = true; });
  root.addEventListener('keydown', function () { pointer = false; });
  root.querySelector('.mchk__form').addEventListener('change', function (ev) {
    if (!started) { started = true; send('tool_start'); }
    next.disabled = !stepDone(cur);
    // 指やマウスで選んだときは、1つだけ聞く画面なら次へ進む（キーボードの矢印では進めない。「次へ」で進む）
    if (pointer && steps[cur - 1].getAttribute('data-multi') === '0' && ev.target.type === 'radio') setTimeout(go, 220);
    else if (pointer && stepDone(cur) && steps[cur - 1].getAttribute('data-multi') === '1') setTimeout(go, 220);
  });
  next.addEventListener('click', go);
  back.addEventListener('click', function () { if (cur > 1) show(cur - 1); });
  root.querySelector('.mchk__retry').addEventListener('click', function () {
    root.querySelector('.mchk__form').reset();
    result.hidden = true; panel.hidden = false; root.classList.remove('is-done'); show(1); scrollTop();
  });

  // ------------------------------------------------------------ 結果
  var out = function (k) { return result.querySelector('[data-out="' + k + '"]'); };
  var L = function (name, v) { return D.labels[name][v]; };
  function finish() {
    var a = answers(), r = judge(a);
    render(a, r);
    panel.hidden = true; result.hidden = false; root.classList.add('is-done');
    result.querySelector('.mchk-res__title').focus({ preventScroll: true });
    scrollTop();
    send('tool_complete', { score_band: r.band, route: r.primary.join('+'), score: r.score });
  }
  var BAND = { high: '宿として有望', mid: '条件しだいで有望', low: '宿以外の道も比べたい' };
  // 判定の印は文字ではなく図形で描く（docs/design-guide.md 6章）
  var svg = function (d) { return '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' + d + '</svg>'; };
  var MARK = { ok: svg('<circle cx="10" cy="10" r="7"/>'), consult: svg('<path d="M10 3.5 17 16H3z"/>'), hold: svg('<circle cx="10" cy="10" r="7" stroke-dasharray="3 3"/>'), hard: svg('<path d="M4.5 4.5l11 11M15.5 4.5l-11 11"/>') };
  function render(a, r) {
    out('score').textContent = r.score;
    out('band').textContent = BAND[r.band];
    out('band').className = 'mchk-score__band is-' + r.band;
    out('meter').style.width = r.score + '%';
    out('break').innerHTML = [['制度', r.pts.seido, 40], ['災害', r.pts.hazard, 20], ['建物の状態', r.pts.state, 25], ['広さ', r.pts.area, 15]].map(function (x) {
      return '<li><span>' + x[0] + '</span><i style="--p:' + (x[1] / x[2] * 100) + '%" aria-hidden="true"></i><b>' + x[1] + '<small>/' + x[2] + '</small></b></li>';
    }).join('');
    out('law').innerHTML = [['旅館業（簡易宿所）', '通年で営業できる', r.ryokan], ['民泊新法（住宅宿泊事業）', '年180日まで', r.minpaku]].map(function (x) {
      return '<li class="mchk-law__item is-' + x[2].s + '"><span class="mchk-law__mark" aria-hidden="true">' + MARK[x[2].s] + '</span>' +
        '<div><p class="mchk-law__name">' + x[0] + '<small>' + x[1] + '</small></p><p class="mchk-law__res">' + x[2].t + '</p><p class="mchk-law__note">' + x[2].n + '</p></div></li>';
    }).join('');
    out('cost').innerHTML = a.state === 'major'
      ? '<dt>初期費用</dt><dd class="is-text">見積が必要</dd><p>大きな修繕は、事例の範囲を超えることがあります</p>'
      : '<dt>初期費用（総予算）</dt><dd><small>約</small>350万〜450万<small>円</small></dd><p>オーナーの事例。下田の宿（賃貸・家具家電込み）は、改修 約410万円＋家具・家電・備品 約240万円</p>';
    var n180 = out('note180');
    n180.hidden = r.seido !== 'minpaku';
    n180.innerHTML = '民泊新法は、年180日が上限です。下田の宿の1年目の稼働率 約' + D.occAvg + '%は、年に約' + r.nights + '泊ぶん。同じくらい埋まる宿では、180日の上限で売上が頭打ちになります。';
    out('place').textContent = a.place === 'izu' ? '稼働率は、同じ伊豆半島の下田の宿の数字です。' : '稼働率は、静岡県下田市の宿の数字です。場所によって、数字は変わります。';

    var law = { ryokan: '旅館業（簡易宿所）で、通年で営業できそうです。', minpaku: '民泊新法なら、届出できそうです（年180日まで）。',
      consult: a.zone === 'unknown' ? '用途地域がわかると、使える制度を判定できます。' : '制度は、保健所・市町村への事前の相談で決まります。' }[r.seido];
    var haz = { none: 'ハザードマップで、浸水・土砂災害などの色が付いていません。', colored: '浸水・土砂災害などの色が付いている場所です。', unknown: 'ハザードマップは、まだ確かめていません。' }[a.hazard];
    out('found').innerHTML = [law, haz, L('type', a.type) + '（' + L('area', a.area) + '・' + L('state', a.state) + '）です。'].map(function (t) { return '<li>' + esc(t) + '</li>'; }).join('');
    var unk = ['建物の傷み・改修の見積（現地を見ないとわかりません）', '条例の日数の制限と、保健所・消防との事前の相談', 'その場所の1泊の料金の相場と、予約の入り方'];
    if (a.type === 'condo') unk.push('マンションの管理規約');
    out('unknown').innerHTML = unk.map(function (t) { return '<li>' + esc(t) + '</li>'; }).join('');

    var memo = ['【1分診断の結果】'].concat(D.order.map(function (k) { return '・' + D.short[k] + '：' + L(k, a[k]); }))
      .concat(['・点数：' + r.score + '点（' + BAND[r.band] + '）']).join('\n');
    var card = function (k, big) {
      var p = D.plans[k];
      var href = 'contact.html?category=' + k + '&from=minpaku-check&memo=' + encodeURIComponent(memo);
      return '<article class="mchk-plan' + (big ? ' is-main' : '') + '">' +
        (big ? '<p class="mchk-plan__tag">おすすめ</p>' : '') +
        '<p class="mchk-plan__who">' + esc(p.who) + '</p><h3 class="mchk-plan__name">' + esc(p.name) + '</h3>' +
        '<p class="mchk-plan__text">' + esc(p.title) + '</p>' +
        '<div class="mchk-plan__btns"><a href="' + esc(href) + '" class="mbtn' + (big ? '' : ' mbtn--sub') + '" data-cta="minpaku-check-' + k + '">この内容で無料相談する</a>' +
        '<a href="' + esc(p.href) + '" class="mchk-plan__more">プランを見る</a></div></article>';
    };
    // 中央揃えの文は、「、」「。」の区切りでだけ折る（docs/design-guide.md 3章）
    out('plead').innerHTML = (r.band === 'low' ? ['宿に向かない場合も、', '売る・任せるなど、', 'ほかの道をご相談いただけます。', '診断の答えは、', 'フォームに入れてお渡しします。'] : ['ご相談のフォームに、', '診断の答えを入れてお渡しします。'])
      .map(function (t) { return '<span class="mchk-nw">' + t + '</span>'; }).join('');
    out('plans').className = 'mchk-plans__list is-' + (r.primary.length + r.secondary.length);
    out('plans').innerHTML = r.primary.map(function (k) { return card(k, true); }).join('') + r.secondary.map(function (k) { return card(k, false); }).join('');
  }

  root.classList.add('is-ready');
  show(1, true); // ページを開いた直後は、質問にフォーカスを移さない
})();
