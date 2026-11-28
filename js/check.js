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
    // 用途地域（わかれば）で、旅館業と民泊新法のそれぞれが使えるかを決める。わからなければ両方を保留にし、両方の結果を出す
    var C = function (n) { return { s: 'consult', t: '個別の相談が必要', n: n }; };
    var big = a.area === 'gt200' ? 'とても大きい家は、建物の用途を変える手続き（確認申請）が要ります。' : '';
    if (condo) ryokan = { s: 'hard', t: '難しい', n: 'マンション・アパートの1室は、旅館業の許可は現実的に難しいです。' };
    else if (z === 'unknown') ryokan = { s: 'hold', t: '用途地域で決まります', n: '旅館業ができる用途地域なら、この結果になります。' + big };
    else if (z === 'both') ryokan = { s: 'ok', t: 'できそう', n: '第一種住居地域は、床面積3,000㎡以下の建物です。' + big };
    else if (z === 'chosei') ryokan = C('建物の用途を変えるのに許可が要り、難しいことが多いです。');
    else ryokan = { s: 'hard', t: '難しい', n: 'この用途地域では、旅館業の許可はとれません。' };

    if (z === 'unknown') minpaku = { s: 'hold', t: '用途地域で決まります', n: '工業専用地域でなければ、多くの地域で届け出られます。' };
    else if (z === 'indx') minpaku = { s: 'hard', t: '難しい', n: '工業専用地域は住宅が建てられないため、届け出られません。' };
    else if (z === 'chosei') minpaku = C('市町村の判断によります。保健所・市町村に、前もって相談します。');
    else minpaku = { s: 'ok', t: '届け出られそう', n: '' };
    if (minpaku.s !== 'hard') minpaku.n += '市町村の決まりで、日数や場所が限られることがあります。' + (condo ? 'マンションは、管理規約で民泊が禁止されていないことが必要です。' : '');

    var seido = ryokan.s === 'ok' ? 'ryokan' : minpaku.s === 'ok' ? 'minpaku' : (ryokan.s === 'hard' && minpaku.s === 'hard') ? 'hard' : z === 'unknown' ? 'unknown' : 'consult';
    var pts = {
      seido: { ryokan: 40, minpaku: 25, unknown: 20, consult: 20, hard: 0 }[seido],
      hazard: { none: 20, unknown: 10, colored: 5 }[a.hazard],
      state: { ready: 25, care: 15, major: 5 }[a.state],
      area: { m60: 15, m150: 12, lt60: 8, gt200: 8 }[a.area]
    };
    var score = pts.seido + pts.hazard + pts.state + pts.area;
    var band = score >= 70 ? 'high' : score >= 45 ? 'mid' : 'low';
    var p1, p2;
    if (a.goal === 'sell' || seido === 'hard') { p1 = ['sell']; p2 = ['use']; }
    else if (a.goal === 'lend') { p1 = ['use']; p2 = ['sell']; }
    else if (a.goal === 'start') { p1 = ['side']; p2 = ['use']; }
    else { p1 = band === 'high' ? ['use', 'side'] : band === 'mid' ? ['use'] : ['sell']; p2 = []; }
    return { ryokan: ryokan, minpaku: minpaku, seido: seido, pts: pts, score: score, band: band, primary: p1, secondary: p2,
             nights: Math.round(365 * D.occAvg / 100 / 10) * 10,
             // 売上の目安（万円/年）。旅館業＝事例の月の売上×12。民泊新法＝下田の宿と同じくらい埋まるとして、180泊に減らす
             yearRyokan: D.caseMonthly.map(function (m) { return m * 12; }),
             yearMinpaku: D.caseMonthly.map(function (m) { return Math.round(m * 12 * Math.min(1, 180 / (365 * D.occAvg / 100)) / 10) * 10; }) };
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
    out('break').innerHTML = [['宿にできるか', r.pts.seido, 40], ['災害', r.pts.hazard, 20], ['建物の状態', r.pts.state, 25], ['広さ', r.pts.area, 15]].map(function (x) {
      return '<li><span>' + x[0] + '</span><i style="--p:' + (x[1] / x[2] * 100) + '%" aria-hidden="true"></i><b>' + x[1] + '<small>/' + x[2] + '</small></b></li>';
    }).join('');
    var yen = function (y) { return '年 約' + y[0] + '万〜' + y[1] + '万円'; };
    out('law').innerHTML = [['旅館業の許可がとれた場合', '1年中営業できる（簡易宿所）', r.ryokan, yen(r.yearRyokan)],
                            ['民泊新法で届け出た場合', '届出で始められる。年180日まで（住宅宿泊事業）', r.minpaku, yen(r.yearMinpaku)]].map(function (x) {
      return '<li class="mchk-law__item is-' + x[2].s + '"><span class="mchk-law__mark" aria-hidden="true">' + MARK[x[2].s] + '</span>' +
        '<div><p class="mchk-law__name">' + x[0] + '<small>' + x[1] + '</small></p><p class="mchk-law__res">' + x[2].t + '</p>' +
        (x[2].s === 'hard' ? '' : '<p class="mchk-law__yen">売上の目安 <b>' + x[3] + '</b></p>') +
        '<p class="mchk-law__note">' + x[2].n + '</p></div></li>';
    }).join('');
    out('cost').innerHTML = a.state === 'major'
      ? '<dt>初期費用</dt><dd class="is-text">見積が必要</dd><p>大きな修繕は、事例の範囲を超えることがあります</p>'
      : '<dt>はじめにかかる費用（総額）</dt><dd><small>約</small>350万〜450万<small>円</small></dd><p>オーナーの事例。下田の宿（賃貸・家具家電込み）は、改修 約410万円＋家具・家電・備品 約240万円</p>';
    var n180 = out('note180');
    n180.hidden = r.minpaku.s === 'hard';
    n180.innerHTML = '売上の目安は、オーナーの事例の月の売上（約' + D.caseMonthly[0] + '万〜' + D.caseMonthly[1] + '万円）を1年分にした計算です。民泊新法は年180日までなので、下田の宿の1年目と同じくらい（泊まりが入った日 約' + D.occAvg + '%＝年 約' + r.nights + '泊）埋まるとして、180泊に減らしています。将来の売上をお約束するものではありません。';
    out('place').textContent = a.place === 'izu' ? '泊まりが入った日の割合（稼働率）は、同じ伊豆半島の下田の宿の数字です。' : '泊まりが入った日の割合（稼働率）は、静岡県下田市の宿の数字です。場所によって、数字は変わります。';

    var law = { ryokan: '旅館業（簡易宿所）で、通年で営業できそうです。', minpaku: '民泊新法なら、届出できそうです（年180日まで）。',
      unknown: '旅館業と民泊新法のどちらが使えるかは、用途地域で決まります。両方の場合の結果を出しました。',
      consult: '市街化調整区域は、保健所・市町村への事前の相談で決まります。',
      hard: 'この場所では、宿として営業するのは難しそうです。売る・任せるなど、ほかの道を比べるのがおすすめです。' }[r.seido];
    var haz = { none: 'ハザードマップで、浸水・土砂災害などの色が付いていません。', colored: '浸水・土砂災害などの色が付いている場所です。', unknown: 'ハザードマップは、まだ確かめていません。' }[a.hazard];
    out('found').innerHTML = [law, haz, '広さは「' + L('area', a.area) + '」、状態は「' + L('state', a.state) + '」の' + L('type', a.type) + 'です。'].map(function (t) { return '<li>' + esc(t) + '</li>'; }).join('');
    var unk = ['建物の傷みと、直すのにかかる費用（現地を見ないとわかりません）', '市町村の決まり（営業できる日数など）と、保健所・消防への事前の相談', 'その場所で1泊いくらにできるか、どれくらい予約が入るか'];
    if (a.zone === 'unknown') unk.unshift('用途地域（旅館業と民泊新法のどちらが使えるかが決まります）。私たちが無料で調べます');
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
