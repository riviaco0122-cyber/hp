/**
 * RIVIA&CO. Corporate Site
 */
(function () {
  'use strict';

  window.RIVIA_READY = true;
  var EN = document.documentElement.lang === 'en';  // 英語ページかどうか（一部の文言を切り替える）
  document.documentElement.classList.add('js');

  /**
   * Header の下線
   */
  var header = document.querySelector('.header');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('is-scrolled', y > 10);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /**
   * スマホ：右上のメニューボタン（3本線）で全画面メニューを開閉
   */
  // アキヤド：ヘッダーのボタン（3本線）でメニューを開閉する（PC・スマホ共通）
  var mmenuBtn = document.querySelector('.mmenu-btn');
  var mheader = document.querySelector('.header--media');
  if (mmenuBtn && mheader) {
    var setMmenu = function (open) {
      mheader.classList.toggle('is-mnav-open', open);
      document.documentElement.classList.toggle('is-menu-open', open);
      mmenuBtn.setAttribute('aria-expanded', String(open));
      mmenuBtn.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
    };
    mmenuBtn.addEventListener('click', function () { setMmenu(!mheader.classList.contains('is-mnav-open')); });
    mheader.querySelectorAll('.mnav a').forEach(function (a) { a.addEventListener('click', function () { setMmenu(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMmenu(false); });
    // PC：メニューの外をクリックしたら閉じる
    document.addEventListener('click', function (e) { if (mheader.classList.contains('is-mnav-open') && !mheader.contains(e.target)) setMmenu(false); });
  }
  var menuBtn = document.querySelector('.menu-btn');
  function setMenu(open) {
    if (!menuBtn || !header) return;
    header.classList.toggle('is-menu-open', open);
    document.documentElement.classList.toggle('is-menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', EN ? (open ? 'Close menu' : 'Open menu') : (open ? 'メニューを閉じる' : 'メニューを開く'));
    if (!open) closeSubnav();
  }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      setMenu(!header.classList.contains('is-menu-open'));
    });
    document.querySelectorAll('.gnav a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setMenu(false);
    });
    window.matchMedia('(min-width: 900px)').addEventListener('change', function (mq) {
      if (mq.matches) setMenu(false);
    });
  }

  /**
   * Service ドロップダウン
   * PC はホバーで開き、タップ・クリック・キーボードでも開閉できる
   */
  var subItems = document.querySelectorAll('.gnav__item--has-sub');
  subItems.forEach(function (item) {
    var trigger = item.querySelector('.gnav__link');
    trigger.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !item.classList.contains('is-open');
      item.classList.toggle('is-open', open);
      trigger.setAttribute('aria-expanded', String(open));
    });
  });

  // Serviceメニュー：お客様の立場（個人／法人・事業者）のタブ切り替え
  document.querySelectorAll('.subnav__tab').forEach(function (tab) {
    tab.addEventListener('click', function (e) {
      e.stopPropagation();
      var menu = tab.closest('.subnav');
      menu.querySelectorAll('.subnav__tab').forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        document.getElementById(t.getAttribute('aria-controls')).classList.toggle('is-active', on);
      });
    });
  });

  function closeSubnav() {
    subItems.forEach(function (item) {
      item.classList.remove('is-open');
      item.querySelector('.gnav__link').setAttribute('aria-expanded', 'false');
    });
  }
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.gnav__item--has-sub')) closeSubnav();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeSubnav();
  });

  /**
   * スクロールに応じたフェードイン
   * 画面内に入った要素、またはすでに通り過ぎた要素はすべて表示する
   * （ページ内リンクでの移動や高速スクロールでも表示抜けが起きないようにする）
   */
  var ticking = false;
  function revealInView() {
    ticking = false;
    var limit = window.innerHeight * 0.92;
    document.querySelectorAll('.reveal:not(.is-visible)').forEach(function (el) {
      if (el.getBoundingClientRect().top < limit) el.classList.add('is-visible');
    });
  }
  function requestReveal() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(revealInView);
    }
  }
  window.addEventListener('scroll', requestReveal, { passive: true });
  window.addEventListener('resize', requestReveal);
  window.addEventListener('hashchange', requestReveal);
  requestReveal();

  /**
   * Contact: 相談ボタンから遷移した場合、ご相談カテゴリを自動選択
   * 例) contact.html?category=operation
   */
  // アキヤドのお問い合わせ：押したボタンに合わせて「ご相談の内容」に先にチェックを入れる
  var mchecks = document.querySelectorAll('.mform__check input[data-keys]');
  if (mchecks.length && window.URLSearchParams) {
    var mcat = new URLSearchParams(location.search).get('category');
    var mmsg = document.getElementById('m-message');
    // 選んだご相談の内容に合わせて、詳細欄に書き方の例（テンプレート）を入れる。自分で書き換えたあとは上書きしない
    var lastTpl = '';
    var fillTemplate = function () {
      if (!mmsg || (mmsg.value && mmsg.value !== lastTpl)) return;
      lastTpl = Array.prototype.filter.call(mchecks, function (c) { return c.checked; })
        .map(function (c) { return c.getAttribute('data-template'); }).join('\n');
      mmsg.value = lastTpl;
    };
    mchecks.forEach(function (c) { c.addEventListener('change', fillTemplate); });
    if (mcat) mchecks.forEach(function (c) { if (c.getAttribute('data-keys').split(' ').indexOf(mcat) >= 0) c.checked = true; });
    fillTemplate();
  }
  // コーポレートのお問い合わせ：ご相談カテゴリを選ぶと、内容欄に書き方の例を入れる（自分で書き換えたあとは上書きしない）
  var CORP_TEMPLATES = EN ? {} : {
    operation: '【空き家再生事業について】\n・物件の所在地：\n・物件の状況（空き家・相続など）：\n・ご希望（売りたい／貸したい／まだ決めていない）：\n',
    management: '【宿泊施設の開業・運営支援について】\n・物件の有無（ある／探している）：\n・はじめたい宿のイメージ：\n・任せたい範囲（開業準備のみ／運営まで）：\n',
    partnership: '【不動産事業者様との協業について】\n・会社名・ご担当：\n・ご紹介・ご相談したい物件や案件：\n・ご希望の協業の形：\n',
    marketing: '【WEB集客支援について】\n・事業・施設の概要：\n・いまの集客の課題：\n・ご予算の目安：\n',
    recruit: '【WEB採用支援について】\n・募集したい職種・人数：\n・いまの採用の課題：\n・採用したい時期：\n',
    property: '【物件についてのご相談】\n・物件の所在地：\n・物件の種類・状況（空き家・相続・賃貸中など）：\n・気になっていること：\n',
    other: '',
    document: 'サービス資料を希望します。\n'
  };
  // ご相談カテゴリ（カードで選ぶ）：立場のタブ切り替え、選んだカテゴリに合わせた書き出し、URL の ?category= で選んだ状態にする
  var picker = document.querySelector('.catpick');
  var corpMsg = document.getElementById('message'), corpLast = '';
  var corpFill = function (key) {
    if (!corpMsg) return;
    var tpl = CORP_TEMPLATES[key] || '';
    if (corpMsg.value && corpMsg.value !== corpLast) return;
    corpMsg.value = corpLast = tpl;
  };
  if (picker) {
    var tabs = picker.querySelectorAll('.catpick__tab'), panels = picker.querySelectorAll('.catpick__panel');
    var showWho = function (who) {
      tabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.getAttribute('data-who') === who)); });
      panels.forEach(function (p) { p.hidden = p.getAttribute('data-who') !== who; });
    };
    tabs.forEach(function (t) { t.addEventListener('click', function () { showWho(t.getAttribute('data-who')); }); });
    picker.addEventListener('change', function (ev) {
      if (ev.target.name === 'category') corpFill(ev.target.getAttribute('data-key'));
    });
    showWho('personal');
    var param = window.URLSearchParams ? new URLSearchParams(window.location.search).get('category') : '';
    if (param && /^[a-z]+$/.test(param)) {
      // 個人向けにもある事業は個人のタブで、法人向けだけの事業は法人のタブで選ぶ
      var radio = picker.querySelector('.catpick__panel[data-who="personal"] input[data-key="' + param + '"]') ||
                  picker.querySelector('input[data-key="' + param + '"]');
      if (radio) {
        radio.checked = true;
        var panel = radio.closest('.catpick__panel');
        if (panel) showWho(panel.getAttribute('data-who'));
        // 資料請求から来た場合は、本文を書かなくても送れるように入れておく
        corpFill(param);
      }
    }
  }

  /**
   * Media: 公開日を迎えていない記事は表示しない（予約公開）
   * 各カードの data-date（YYYY-MM-DD）と今日の日付を比べる
   */
  var now = new Date();
  var today = now.getFullYear() + '-' + ('0' + (now.getMonth() + 1)).slice(-2) + '-' + ('0' + now.getDate()).slice(-2);
  // 確認用: URL に ?preview=1 を付けると、公開日前の記事も表示する（人がプレビューで新記事を確かめるため）。
  // スマホのアプリ内ブラウザなどで sessionStorage が使えなくても、URL に付いていれば必ず効く
  var previewOn = /[?&]preview=1(&|$)/.test(location.search);
  try {
    if (previewOn) sessionStorage.setItem('akiyadoPreview', '1');
    else if (sessionStorage.getItem('akiyadoPreview') === '1') previewOn = true;
  } catch (e) {}
  if (previewOn) today = '2999-12-31';
  // 公開日前の記事ページを直接開いた場合も、転送はしない（記事はそのまま表示する）。
  // 以前は記事一覧へ JS で転送していたが、Google が記事内のリンクからページを見つけて開くと
  // 「ページにリダイレクトがあります」と記録され、公開日を過ぎてもインデックスされにくくなるため（2026-10-22）
  document.querySelectorAll('.media-card[data-date]').forEach(function (c) {
    if (c.getAttribute('data-date') > today) {
      c.setAttribute('data-future', '');
      c.hidden = true;
    }
  });
  // アキヤドのトップ「主な事例」のカルーセル: 公開日前の事例を隠し、前後ボタンと「n / 全体」を動かす
  document.querySelectorAll('[data-carousel]').forEach(function (box) {
    var track = box.querySelector('.mtop__track');
    var slides = Array.prototype.slice.call(box.querySelectorAll('.mtop-case')).filter(function (c) {
      if (c.getAttribute('data-date') > today) { c.hidden = true; return false; }
      return true;
    });
    var cur = box.querySelector('[data-cur]'), total = box.querySelector('[data-total]');
    var prev = box.querySelector('[data-dir="-1"]'), next = box.querySelector('[data-dir="1"]');
    if (!track || !slides.length) return;
    total.textContent = slides.length;
    var index = function () {
      var x = track.scrollLeft, best = 0;
      slides.forEach(function (c, i) { if (Math.abs(c.offsetLeft - track.offsetLeft - x) < Math.abs(slides[best].offsetLeft - track.offsetLeft - x)) best = i; });
      if (track.scrollLeft + track.clientWidth >= track.scrollWidth - 4) best = slides.length - 1;
      return best;
    };
    var update = function () { var i = index(); cur.textContent = i + 1; prev.disabled = i === 0; next.disabled = i === slides.length - 1; };
    var go = function (d) { var i = Math.max(0, Math.min(slides.length - 1, index() + d)); track.scrollTo({ left: slides[i].offsetLeft - track.offsetLeft, behavior: 'smooth' }); };
    prev.addEventListener('click', function () { go(-1); });
    next.addEventListener('click', function () { go(1); });
    var t; track.addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(update, 60); }, { passive: true });
    update();
  });
  // トップ・サービス・記事下の記事一覧: 公開済みの先頭 N 件だけ表示
  document.querySelectorAll('.media-grid[data-limit]').forEach(function (grid) {
    var limit = parseInt(grid.getAttribute('data-limit'), 10) || 3;
    var published = Array.prototype.slice.call(grid.querySelectorAll('.media-card:not([data-future])'));
    published.forEach(function (c, i) { c.hidden = i >= limit; });
    if (!published.length) {
      var section = grid.closest('.section');
      if (section) section.hidden = true;
    }
  });

  // 新着記事：公開済みの先頭の1本を大きく見せる
  document.querySelectorAll('.media-grid--feature').forEach(function (grid) {
    var lead = grid.querySelector('.media-card:not([hidden])');
    if (lead) lead.classList.add('is-lead');
  });
  // よくある悩み：公開前の記事への質問は出さない
  // 基礎から学ぶ：公開前の記事は隠し、記事がひとつもない章も隠す
  document.querySelectorAll('.lchap__list li[data-date]').forEach(function (li) {
    if (li.getAttribute('data-date') > today) li.hidden = true;
  });
  document.querySelectorAll('.lchap').forEach(function (ch) {
    if (!ch.querySelector('.lchap__list li:not([hidden])')) ch.hidden = true;
  });
  // 章を隠したあとは、残った章を第1章から数え直す（番号が飛ばないように）
  document.querySelectorAll('.lchaps').forEach(function (list) {
    var n = 0;
    list.querySelectorAll('.lchap').forEach(function (ch) {
      if (ch.hidden) return;
      n += 1;
      var no = ch.querySelector('.lchap__no');
      if (no) no.textContent = '第' + n + '章';
    });
  });
  document.querySelectorAll('.mq li[data-date]').forEach(function (li) {
    if (li.getAttribute('data-date') > today) li.hidden = true;
  });
  // スマホでは、よくある悩みを先頭の5件だけ出し、残りはボタンで開く
  if (window.matchMedia('(max-width: 899px)').matches) {
    document.querySelectorAll('.mq').forEach(function (list) {
      var rest = Array.prototype.slice.call(list.querySelectorAll('li:not([hidden])')).slice(5);
      if (!rest.length) return;
      rest.forEach(function (li) { li.hidden = true; });
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'mq__more';
      btn.textContent = 'ほかの悩みも見る（' + rest.length + '件）';
      btn.addEventListener('click', function () {
        rest.forEach(function (li) { li.hidden = false; });
        btn.remove();
      });
      list.after(btn);
    });
  }
  // ガイド：公開前の記事は「公開予定」として表示し、リンクにしない
  document.querySelectorAll('.guide-step[data-date]').forEach(function (li) {
    var d = li.getAttribute('data-date');
    if (d <= today) return;
    var link = li.querySelector('a');
    var box = document.createElement('div');
    box.className = link.className;
    box.innerHTML = link.innerHTML;
    var more = box.querySelector('.guide-step__more');
    if (more) {
      more.className = 'guide-step__soon';
      more.textContent = Number(d.slice(5, 7)) + '月' + Number(d.slice(8, 10)) + '日 公開予定';
    }
    li.replaceChild(box, link);
    li.classList.add('is-upcoming');
  });
  // ガイド：1つの Step に記事が多いときは、先頭の3件だけ見せて「残りを見る」で開く
  document.querySelectorAll('.guide-steps[data-fold]').forEach(function (list) {
    var keep = parseInt(list.getAttribute('data-fold'), 10) || 3;
    var items = Array.prototype.slice.call(list.querySelectorAll('.guide-step')).slice();
    if (items.length <= keep + 1) return;
    var rest = items.slice(keep);
    rest.forEach(function (li) { li.hidden = true; });
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'guide-steps__more';
    btn.setAttribute('aria-expanded', 'false');
    btn.textContent = '残りの' + rest.length + '本を見る ＋';
    btn.addEventListener('click', function () {
      rest.forEach(function (li) { li.hidden = false; });
      btn.remove();
    });
    list.after(btn);
  });
  // 記事ページのガイド欄：公開前の記事は出さない
  // 前後の記事は、公開済みの記事の中で決める
  document.querySelectorAll('.guide-box').forEach(function (box) {
    var items = Array.prototype.slice.call(box.querySelectorAll('.guide-box__list li'));
    items.forEach(function (li) { if (li.getAttribute('data-date') > today) li.hidden = true; });
    var shown = items.filter(function (li) { return !li.hidden; });
    var i = shown.findIndex(function (li) { return li.hasAttribute('aria-current'); });
    // 5件を超えるときは、この記事とその前後の3件だけ見せ、残りは「ほかの◯本を見る」で開く
    if (shown.length <= 5 || i < 0) return;
    var rest = shown.filter(function (li, k) { return Math.abs(k - i) > 1; });
    if (rest.length < 2) return;
    rest.forEach(function (li) { li.hidden = true; });
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'guide-steps__more guide-box__more';
    btn.setAttribute('aria-expanded', 'false');
    btn.textContent = 'ほかの' + rest.length + '本を見る ＋';
    btn.addEventListener('click', function () {
      rest.forEach(function (li) { li.hidden = false; });
      btn.remove();
    });
    box.querySelector('.guide-box__list').after(btn);
  });
  // シェア：リンクをコピー
  document.querySelectorAll('.share__copy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var url = btn.getAttribute('data-url');
      var done = function () { btn.textContent = 'コピーしました'; setTimeout(function () { btn.textContent = 'リンクをコピー'; }, 2000); };
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function () { window.prompt('URLをコピーしてください', url); });
      else window.prompt('URLをコピーしてください', url);
    });
  });
  // 旧URL（media.html?cat=○○）はカテゴリ一覧へ
  if (window.URLSearchParams && document.querySelector('.mnav') && /media\.html$/.test(location.pathname)) {
    var oldCat = new URLSearchParams(location.search).get('cat');
    if (oldCat && /^[a-z]+$/.test(oldCat) && document.querySelector('a[href$="category-' + oldCat + '.html"]')) location.replace(new URL('media/category-' + oldCat + '.html', location.href).href);
  }

  /**
   * 計測（GA4）：相談ボタン・ガイド・検索の利用を記録し、どこから問い合わせにつながったかを見えるようにする
   */
  var track = function (name, params) { if (typeof window.gtag === 'function') window.gtag('event', name, params); };
  // 解説動画の再生（最初の1回だけ）と、最後まで見たか
  document.querySelectorAll('video[data-video]').forEach(function (v) {
    var started = false;
    v.addEventListener('play', function () { if (!started) { started = true; track('video_play', { video_name: v.getAttribute('data-video'), page_path: location.pathname }); } });
    v.addEventListener('ended', function () { track('video_complete', { video_name: v.getAttribute('data-video'), page_path: location.pathname }); });
  });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    if (/contact\.html/.test(href)) {
      track('cta_click', { cta_position: a.getAttribute('data-cta') || a.className || 'link', link_text: a.textContent.trim().slice(0, 40), page_path: location.pathname });
    } else if (/guide-[a-z]+\.html/.test(href)) {
      track('select_guide', { guide: href.match(/guide-([a-z]+)/)[1], page_path: location.pathname });
    }
  });
  // 記事の目次：スマホでは折りたたみ（既定）、PC幅では開いておく
  var tocDetails = document.querySelector('.toc__details');
  if (tocDetails && window.matchMedia('(min-width: 900px)').matches) tocDetails.open = true;
  var fixedMedia = document.querySelector('.fixed-cta');
  // 冒頭の入口・フォーム・相談ブロックが見えている間は、下に固定した相談ボタンを隠す（重なりを防ぐ）
  var hideTargets = document.querySelectorAll('.mfv, .qform, .mcta__box, .msv-band, .inline-cta, .article-cta');
  if (hideTargets.length && fixedMedia && 'IntersectionObserver' in window) {
    var visible = new Set();
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) visible.add(x.target); else visible.delete(x.target); });
      fixedMedia.classList.toggle('is-hidden', visible.size > 0);
    }, { threshold: 0.05 });
    hideTargets.forEach(function (t) { io.observe(t); });
  }
  // お問い合わせフォーム：流入元（例：アキヤドの記事）を一緒に送る
  var fromField = document.getElementById('from-field');
  if (fromField && window.URLSearchParams) {
    var from = new URLSearchParams(location.search).get('from');
    var ref = document.referrer && document.referrer.indexOf(location.host) >= 0 ? document.referrer.replace(/^https?:\/\/[^/]+/, '') : '';
    fromField.value = [from, ref].filter(Boolean).join(' / ');
  }

  /**
   * Media: 記事検索（media/search.html?q=…）
   * js/media-index.js の索引から、すべてのキーワードを含む公開済みの記事を探す
   */
  var results = document.getElementById('search-results');
  if (results && window.MEDIA_INDEX) {
    var norm = function (t) { return (t.normalize ? t.normalize('NFKC') : t).toLowerCase(); };
    var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    // 題名の最後の4文字を改行しないまとまりにする（最後の行が2〜3文字だけにならないように。build の n-b と同じ）
    var tailKeep = function (t) { t = String(t); return t.length > 8 ? esc(t.slice(0, -4)) + '<n-b>' + esc(t.slice(-4)) + '</n-b>' : esc(t); };
    var q = (new URLSearchParams(location.search).get('q') || '').trim();
    var words = norm(q).split(/[\s、，,・]+/).filter(Boolean);
    var input = document.querySelector('.msearch__input');
    if (input) input.value = q;
    var count = function (t, w) { return t.split(w).length - 1; };
    // タイトル・要点・見出し・テーマに含む記事、または本文でくり返し扱う記事を「関連の深い記事」とし、
    // 本文で少し触れているだけの記事は下に分けて出す
    var hits = window.MEDIA_INDEX.filter(function (a) { return a.date <= today; }).map(function (a) {
      var title = norm(a.title), key = norm(a.key), text = norm(a.text), score = 0, strong = true;
      for (var i = 0; i < words.length; i++) {
        var w = words[i], inKey = key.indexOf(w) >= 0, n = count(text, w);
        if (!inKey && !n) return null;
        if (!inKey && n < 3) strong = false;
        score += (title.indexOf(w) >= 0 ? 30 : 0) + (inKey ? 10 : 0) + Math.min(n, 10);
      }
      return { a: a, score: score, strong: strong };
    }).filter(Boolean).sort(function (x, y) { return y.score - x.score || (x.a.date < y.a.date ? 1 : -1); });
    var snippet = function (a) {
      if (!words.length) return esc(a.desc);
      var src = a.text, low = norm(src), at = low.indexOf(words[0]);
      if (at < 0) { src = a.key; low = norm(src); at = low.indexOf(words[0]); }
      if (at < 0) return esc(a.desc);
      var from = Math.max(0, at - 12), part = src.slice(from, at + 70);
      var html = (from ? '…' : '') + esc(part) + '…';
      words.forEach(function (w) { html = html.split(esc(w)).join('<mark>' + esc(w) + '</mark>'); });
      return html;
    };
    var card = function (h) {
      var a = h.a;
      return '<a href="' + a.slug + '.html" class="media-card is-visible">' +
        '<div class="thumb thumb--photo"><img src="../../images/photos/w/' + a.thumb + '-800.webp" alt="" loading="lazy" decoding="async" width="720" height="450">' +
        '<span class="thumb__cat">' + esc(a.cat) + '</span>' +
        '<span class="thumb__banner" aria-hidden="true"><span class="thumb__kicker">' + esc(a.cat) + '</span><span class="thumb__catch">' + esc(a.short || '').replace(/\n/g, '<br>') + '</span></span></div>' +
        '<div class="media-card__body"><span class="media-card__cat">' + esc(a.cat) + '</span>' +
        '<h3 class="media-card__title">' + tailKeep(a.title) + '</h3>' +
        (q ? '<p class="media-card__snippet">' + snippet(a) + '</p>' : '') +
        '<time class="media-card__date" datetime="' + a.date + '">' + a.date.replace(/-/g, '.') + '</time></div></a>';
    };
    var strong = hits.filter(function (h) { return h.strong; });
    var weak = hits.filter(function (h) { return !h.strong; });
    results.innerHTML = strong.map(card).join('');
    var weakBox = document.querySelector('.msearch-weak');
    if (weakBox) {
      weakBox.hidden = !weak.length;
      weakBox.querySelector('.msearch-weak__title').textContent = strong.length
        ? '本文で「' + q + '」に触れている記事'
        : '「' + q + '」を主に扱う記事はまだありませんが、本文で触れている記事があります';
      weakBox.querySelector('.msearch-weak__list').innerHTML = weak.map(function (h) {
        return '<li><a href="' + h.a.slug + '.html" class="msearch-weak__item"><span class="msearch-weak__name">' + esc(h.a.title) + '</span>' +
          '<span class="media-card__snippet">' + snippet(h.a) + '</span></a></li>';
      }).join('');
    }
    var status = document.querySelector('.msearch-status');
    if (status) status.textContent = q ? '「' + q + '」の検索結果：' + strong.length + '件' : 'すべての記事：' + hits.length + '件';
    var none = document.querySelector('.msearch-empty');
    if (none) none.hidden = strong.length > 0;
    if (q) document.title = '「' + q + '」の検索結果｜アキヤド';
    if (q) track('search', { search_term: q, results: hits.length });
  }

  /**
   * Media: カテゴリの絞り込みと「もっと記事を見てみる」
   * 例) media.html?cat=akiya
   */
  var mediaList = document.getElementById('media-list');
  if (mediaList) {
    var cards = Array.prototype.slice.call(mediaList.querySelectorAll('.media-card:not([data-future])'));
    var filters = document.querySelectorAll('.media-filter');
    var moreBtn = document.querySelector('.media-more__btn');
    var empty = document.querySelector('.media-empty');
    var pageSize = parseInt(mediaList.getAttribute('data-page-size'), 10) || 6;
    var shown = pageSize;
    var current = 'all';

    var renderMedia = function () {
      var matched = cards.filter(function (c) {
        return current === 'all' || c.getAttribute('data-category') === current;
      });
      cards.forEach(function (c) { c.hidden = true; });
      matched.slice(0, shown).forEach(function (c) { c.hidden = false; c.classList.add('is-visible'); });
      if (moreBtn) moreBtn.hidden = matched.length <= shown;
      if (empty) empty.hidden = matched.length > 0;
      filters.forEach(function (f) {
        var on = f.getAttribute('data-filter') === current;
        f.classList.toggle('is-active', on);
        f.setAttribute('aria-pressed', String(on));
      });
    };

    filters.forEach(function (f) {
      f.addEventListener('click', function () {
        current = f.getAttribute('data-filter');
        shown = pageSize;
        renderMedia();
      });
    });
    if (moreBtn) {
      moreBtn.addEventListener('click', function () {
        shown += pageSize;
        renderMedia();
      });
    }
    if (window.URLSearchParams) {
      var cat = new URLSearchParams(window.location.search).get('cat');
      if (cat && document.querySelector('.media-filter[data-filter="' + cat + '"]')) current = cat;
    }
    renderMedia();
  }

  /**
   * ファイル添付（採用・お問い合わせ）: 選択したファイル名を表示
   */
  document.querySelectorAll('.file input[type="file"]').forEach(function (input) {
    input.addEventListener('change', function () {
      var box = input.closest('.file');
      var name = box.querySelector('.file__name');
      var files = input.files || [];
      box.classList.toggle('has-file', files.length > 0);
      name.textContent = files.length === 0 ? name.getAttribute('data-default')
        : files.length === 1 ? files[0].name
        : files[0].name + (EN ? ' and ' + (files.length - 1) + ' more' : ' ほか' + (files.length - 1) + '件');
    });
  });

  /**
   * アキヤドのサービスページのフォーム：最初に「無料で相談する／資料をもらう」を選ぶ
   * 資料を選ぶと、ご相談カテゴリを「サービス資料の請求」にする
   * （tools/forms/Code.gs と下のフォーム送信が、この文言で資料の請求と判定する）
   */
  document.querySelectorAll('.mform2').forEach(function (box) {
    var form = box.querySelector('form');
    var cat = form.querySelector('input[name="ご相談カテゴリ"]');
    var subject = form.querySelector('input[name="_subject"]');
    var subjectBase = subject ? subject.value : '';
    var submitT = form.querySelector('.mform2__submit-t');
    var setMode = function (mode) {
      box.querySelectorAll('.mform2__mode').forEach(function (m) { m.setAttribute('aria-checked', String(m.getAttribute('data-mode') === mode)); });
      var doc = mode === 'doc';
      cat.value = cat.getAttribute(doc ? 'data-doc' : 'data-consult');
      if (subject) subject.value = doc ? subjectBase.replace('のご相談', 'の資料請求') : subjectBase;
      if (submitT) submitT.textContent = doc ? '資料をもらう（無料）' : '無料で相談する';
      form.querySelectorAll('.mform2__consult-only').forEach(function (el) { el.hidden = doc; });
    };
    box.querySelectorAll('.mform2__mode').forEach(function (m) {
      m.addEventListener('click', function () { setMode(m.getAttribute('data-mode')); });
    });
    // ページ内のボタン：#diag は相談、#diag-doc は資料を選んだ状態でフォームへ
    document.querySelectorAll('a[href="#diag"], a[href="#diag-doc"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        setMode(a.getAttribute('href') === '#diag-doc' ? 'doc' : 'consult');
        box.scrollIntoView({ behavior: 'smooth', block: 'start' });
        var first = form.querySelector('input[name="name"]');
        if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 500);
      });
    });
  });

  /**
   * フォーム送信：画面を移動せずに送信し、成功したら送信完了ページ（thanks.html）へ移動する
   * （JS が使えない環境では、通常の送信にそのまま切り替わる）
   */
  document.querySelectorAll('form[data-thanks]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!window.fetch || !window.FormData) return;
      e.preventDefault();
      var btn = form.querySelector('[type="submit"]');
      var err = form.querySelector('.form__error');
      if (!err) {
        err = document.createElement('p');
        err.className = 'form__error';
        err.setAttribute('role', 'alert');
        form.appendChild(err);
      }
      err.textContent = '';
      if (btn) { btn.disabled = true; btn.classList.add('is-sending'); }
      var fail = function (msg) {
        err.textContent = msg || (EN ? 'Your message could not be sent. Please try again later or check your entries.' : '送信できませんでした。時間をおいて再度お試しいただくか、入力内容をご確認ください。');
        if (btn) { btn.disabled = false; btn.classList.remove('is-sending'); }
      };
      // 送信先（Google Apps Script）が受け取れる形にする：項目は文字、添付ファイルは base64
      var thanks = form.getAttribute('data-thanks') || '';
      var fields = { _form: /form=careers/.test(thanks) ? 'careers' : (/\/media\//.test(location.pathname) ? 'akiyado' : 'contact'), _page: location.pathname };
      var fileList = [];
      new FormData(form).forEach(function (v, k) {
        if (typeof v === 'string') { fields[k] = fields[k] ? fields[k] + '、' + v : v; }
        else if (v && v.size) { fileList.push(v); }
      });
      // GA4 の generate_lead に付ける lead_type（document 資料請求／consult 相談／careers 採用）。thanks ページへ ?lead= で渡す
      // 資料請求の判定は tools/forms/Code.gs の DOC_REQUEST_VALUES・DOC_REQUEST_KEYS と同じ文言にそろえる（片方を変えたらもう片方も）
      var DOC_REQUEST_VALUES = ['サービス資料の請求', 'サービス資料がほしい'];
      var DOC_REQUEST_KEYS = ['category', 'ご相談の内容', 'ご相談カテゴリ'];
      var isDoc = DOC_REQUEST_KEYS.some(function (k) {
        return String(fields[k] || '').split('、').some(function (v) { return DOC_REQUEST_VALUES.indexOf(v.trim()) >= 0; });
      });
      var leadType = fields._form === 'careers' ? 'careers' : (isDoc ? 'document' : 'consult');
      var total = fileList.reduce(function (n, f) { return n + f.size; }, 0);
      if (total > 10 * 1024 * 1024) { fail('添付ファイルの合計が10MBを超えています。ファイルを減らすか、小さくしてから送信してください。'); return; }
      if (fileList.length > 5) { fail('添付ファイルは5つまでです。'); return; }
      Promise.all(fileList.map(function (f) {
        return new Promise(function (resolve, reject) {
          var r = new FileReader();
          r.onload = function () { resolve({ name: f.name, type: f.type, data: String(r.result).split(',')[1] || '' }); };
          r.onerror = reject;
          r.readAsDataURL(f);
        });
      }))
        .then(function (files) {
          // text/plain で送る（ブラウザの事前確認が不要な形式。Apps Script 側で JSON として読む）
          return fetch(form.action, { method: 'POST', body: JSON.stringify({ fields: fields, files: files }) });
        })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (!data || !data.ok) {
            if (data && data.error === 'rate_limit') throw new Error('rate');
            throw new Error('send failed');
          }
          window.location.href = thanks + (thanks.indexOf('?') >= 0 ? '&' : '?') + 'lead=' + leadType;
        })
        .catch(function (e) {
          fail(e && e.message === 'rate' ? '短い時間に続けて送信されたため、受け付けを一時停止しています。10分ほどおいてから、もう一度お試しください。' : null);
        });
    });
  });
})();

// スマホでは補足（.spfold）を閉じた状態で表示する
(function () {
  if (!window.matchMedia('(max-width: 899px)').matches) return;
  document.querySelectorAll('details.spfold[open]').forEach(function (d) { d.removeAttribute('open'); });
})();

// コーポレート：スクロールの進み具合・TOPの写真の切り替え・数字のカウントアップ
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 画面上端の細い線で、ページのどこまで読んだかを示す
  var bar = document.querySelector('.progress');
  if (bar) {
    var tick = false;
    var update = function () {
      tick = false;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.setProperty('--p', max > 0 ? Math.min(1, window.scrollY / max).toFixed(4) : 0);
    };
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  // 改行の仕方を、表示されている揃え方で決める（人の指摘 2026-11-06。docs/design-guide.md 3章）
  // ・中央揃えの文：言葉の切れ目（build で入れた <wbr>）でだけ改行する（n-w.c。見出しの n-w.h はもともと同じ）
  // ・左揃えの文：まず言葉の切れ目・まとまり（build で入れた <wbr>・<n-b>）を守って折る。ただし、そのせいで行末に3文字分を超える
  //   空き（22px以上の大きな見出しは5文字分を超える空き）ができる行があれば、そのまとまり（段落・項目・見出し）を .wrap-fill にして、
  //   言葉の途中でも折れるようにし、6文字以上の長い塊（日付・出典のかっこ・「・」のつながり）も解く（右の余白を少なくすることを優先。
  //   人の方針 2026-11-06：「右に余白が大きく残るなら、単語で折り返してよい。右側の見栄えが大事」）。5文字以下の塊（「5万円」「ます。」「物・立」）は解かない。
  //   数字の途中やかっこだけが残る折り方は、ブラウザの禁則処理で起きない
  // 部品によってはスマホとPCで揃え方が変わるので、画面の幅が変わったら付け直す
  var phraseTexts = document.querySelectorAll('n-w');
  var blockOf = function (el) { // 文字が並ぶまとまり（display: inline でない一番近い祖先）
    while (el.parentElement && getComputedStyle(el).display === 'inline') el = el.parentElement;
    return el;
  };
  var maxGap = function (blk) { // まとまりの中で、最後の行以外の行末の空き（文字数）の最大
    var cs = getComputedStyle(blk), fs = parseFloat(cs.fontSize);
    var right = blk.getBoundingClientRect().right - parseFloat(cs.paddingRight) - parseFloat(cs.borderRightWidth);
    var range = document.createRange(), lines = [], tw = document.createTreeWalker(blk, NodeFilter.SHOW_TEXT), t;
    while ((t = tw.nextNode())) { // 文字の部分だけで測る（要素の箱の幅は数えない）
      if (!t.data.trim()) continue;
      range.selectNodeContents(t);
      Array.prototype.forEach.call(range.getClientRects(), function (r) {
        if (!r.width || !r.height) return;
        var line = null;
        for (var k = 0; k < lines.length; k++) if (Math.abs(lines[k].top - r.top) < fs * 0.6) { line = lines[k]; break; }
        if (!line) { line = { top: r.top, right: r.right }; lines.push(line); }
        line.right = Math.max(line.right, r.right);
      });
    }
    blk.querySelectorAll('br').forEach(function (br) { // 手で入れた改行（<br>）の直前の行は、空いていて当然なので数えない
      var t = br.getBoundingClientRect().top;
      lines.forEach(function (l) { if (Math.abs(l.top - t) < fs * 0.6) l.hard = true; });
    });
    lines.sort(function (x, y) { return x.top - y.top; });
    return lines.slice(0, -1).reduce(function (m, l) { return l.hard ? m : Math.max(m, (right - l.right) / fs); }, 0);
  };
  var NUM = /約?\d[\d,.]*(?:万|億|兆)?(?:人泊|営業日|時間|か月|円|人|泊|年|月|日|倍|件|戸|棟|回|歳|㎡|室|%|％)?/g;
  var keepNums = function (b) { // b の中の数字と単位を、改行しないまとまり（n-b）で包む
    var tw = document.createTreeWalker(b, NodeFilter.SHOW_TEXT), t, nodes = [];
    while ((t = tw.nextNode())) if (!(t.parentNode.closest && t.parentNode.closest('n-b.num'))) nodes.push(t); // 前に包んだ数字（n-b.num）は包み直さない
    nodes.forEach(function (node) {
      var m, hits = [];
      NUM.lastIndex = 0;
      while ((m = NUM.exec(node.data))) if (m[0].length >= 2) hits.push([m.index, m[0].length]);
      for (var i = hits.length - 1; i >= 0; i--) {
        var mid = node.splitText(hits[i][0]); mid.splitText(hits[i][1]);
        var nb = document.createElement('n-b'); nb.className = 'num'; mid.parentNode.insertBefore(nb, mid); nb.appendChild(mid);
      }
    });
  };
  // まとまりの最後の4文字は、改行しないまとまりにしておく（最後の行が「す。」のように2〜3文字だけにならないように。
  // 「…<strong>約67%</strong>でした。」のように、build でまとめきれなかった語尾も含む）
  var keepTail = function (blk) {
    var tw = document.createTreeWalker(blk, NodeFilter.SHOW_TEXT), t, last = null;
    while ((t = tw.nextNode())) if (t.data.trim()) last = t;
    if (!last) return;
    var txt = last.data.replace(/\s+$/, ''), pe = last.parentNode, kept = false, a;
    for (a = pe; a && a !== blk; a = a.parentNode) if (a.tagName === 'N-B' && (a.classList.contains('tail') || !a.classList.contains('loose') && a.textContent.trim().length >= 4)) kept = true; // tail：前に包んだ最後の4文字
    if (kept) return;
    if (txt.length >= 4) {
      var cut = txt.length - 4; // 切れ目が数字と単位の途中（「80万／円の事例」）なら、数字の頭まで戻す
      while (cut > 0 && /[\d,.万億兆]/.test(txt[cut - 1]) && /[\d,.万億兆円人泊年月日倍件戸棟回歳㎡室%％]/.test(txt[cut])) cut--;
      if (cut > 0 && txt[cut - 1] === '約' && /\d/.test(txt[cut])) cut--;
      var tail = last.splitText(cut), nb = document.createElement('n-b'); nb.className = 'tail';
      pe.insertBefore(nb, tail); nb.appendChild(tail);
    } else if (pe.tagName === 'N-B' && pe.textContent.length < 4 && pe.previousSibling && pe.previousSibling.nodeType === 3 &&
               pe.previousSibling.data.length >= 4 - pe.textContent.length) {
      // 最後のまとまりが「ます。」のように4文字に足りないときは、直前の文字を足して守る（「あり／ます。」を防ぐ）
      var tn = pe.previousSibling, moved = tn.splitText(tn.data.length - (4 - pe.textContent.length)), nb3 = document.createElement('n-b');
      nb3.className = 'tail'; pe.parentNode.insertBefore(nb3, moved); nb3.appendChild(moved); nb3.appendChild(pe);
    } else if (last.previousSibling && (last.previousSibling.textContent + txt).length >= 4 && (last.previousSibling.textContent + txt).length <= 8) {
      // 最後の文字が短く分かれている（「…<n-b>10月</n-b>閲覧）」）ときは、直前のまとまりと合わせて守る
      var prev = last.previousSibling, nb2 = document.createElement('n-b'); nb2.className = 'tail';
      pe.insertBefore(nb2, prev); nb2.appendChild(prev); nb2.appendChild(last);
    } else { // それもできないときは、外側の塊を解かずに残す
      for (a = pe; a && a !== blk; a = a.parentNode) if (a.tagName === 'N-B') { a.classList.remove('loose'); a.querySelectorAll('n-b.loose').forEach(function (x) { x.classList.remove('loose'); }); }
    }
  };
  // 組んだ形の見栄えの悪さ：途中の行の右の空き（文字数の2乗÷4。3文字分まではなし）＋言葉の途中で切れた所×4＋最後の行が3文字以下なら6
  var JA_END = /[、。，．・：；！？!?）」』】〉》\s]/, JA_OPEN = /[「『（(【〈《]/;
  var cost = function (blk, fs) {
    var cs = getComputedStyle(blk);
    var right = blk.getBoundingClientRect().right - parseFloat(cs.paddingRight) - parseFloat(cs.borderRightWidth);
    var tw = document.createTreeWalker(blk, NodeFilter.SHOW_TEXT), t, r = document.createRange(), lines = [];
    while ((t = tw.nextNode())) {
      for (var j = 0; j < t.length; j++) {
        if (/\s/.test(t.data[j])) continue;
        r.setStart(t, j); r.setEnd(t, j + 1);
        var rc = r.getClientRects()[0]; if (!rc || !rc.width) continue;
        var l = lines[lines.length - 1], c = { node: t, i: j, ch: t.data[j] };
        if (!l || rc.top > l.top + rc.height * 0.6) lines.push({ top: rc.top, right: rc.right, first: c, last: c, n: 1 });
        else { l.right = Math.max(l.right, rc.right); l.last = c; l.n++; }
      }
    }
    if (lines.length < 2) return 0;
    var hard = blk.querySelectorAll('br');
    var total = 0;
    for (var k = 0; k < lines.length - 1; k++) {
      var L = lines[k], N = lines[k + 1], isHard = false;
      hard.forEach(function (br) { if (Math.abs(br.getBoundingClientRect().top - L.top) < fs * 0.6) isHard = true; });
      if (isHard) continue;
      var gap = (right - L.right) / fs;
      if (gap > 3) total += gap * gap / 4; // 空きは大きいほど目立つので、2乗で重くする
      var p = N.first.i === 0 ? N.first.node.previousSibling || (N.first.node.parentNode !== blk ? N.first.node.parentNode.previousSibling : null) : null;
      var nx = N.first.node.data.slice(N.first.i, N.first.i + 3);
      var atWord = (p && p.nodeName === 'WBR') || JA_END.test(L.last.ch) || JA_OPEN.test(N.first.ch) || (/[A-Za-z0-9]/.test(L.last.ch) !== /[A-Za-z0-9]/.test(N.first.ch)) ||
        // 漢字のあとの「します」「できます」、助詞（「要件／を」）は言葉の切れ目。送りがなの途中（「満／たせる」）は切れ目ではない
        (/[一-龯々]/.test(L.last.ch) && /^(?:し[てたまなょゃ]|する|され|させ|でき|[をがはへでのにとも])/.test(nx));
      if (!atWord) total += 4;
    }
    if (lines[lines.length - 1].n <= 3) total += 6;
    return total;
  };
  var lineCount = function (blk) { // まとまりの中の文字の行数
    var tops = [], r = document.createRange(), tw = document.createTreeWalker(blk, NodeFilter.SHOW_TEXT), t;
    var fs = parseFloat(getComputedStyle(blk).fontSize);
    while ((t = tw.nextNode())) {
      if (!t.data.trim()) continue;
      r.selectNodeContents(t);
      Array.prototype.forEach.call(r.getClientRects(), function (q) {
        if (q.width && !tops.some(function (y) { return Math.abs(y - q.top) < fs * 0.6; })) tops.push(q.top);
      });
    }
    return tops.length;
  };
  var fitLines = function () {
    // 文ごとの改行（br.sb。build が短い文に入れる）は、どの文も1行に収まるときだけ残す。そうでなければ文をつなげて流す
    // （PC の狭いカードで「受け付けて／います。」のように行が増え、ページが無駄に縦に長くなるため。人の指摘 2026-11-07）
    var sbBlocks = [];
    document.querySelectorAll('main br.sb').forEach(function (br) { var b = blockOf(br.parentElement); if (sbBlocks.indexOf(b) < 0) sbBlocks.push(b); });
    sbBlocks.forEach(function (b) {
      b.classList.remove('nosb');
      if (b.offsetParent === null) return;
      // どの文も1行に収まり、つなげても行数が減らないときだけ、文ごとに改行する（お手本のコンセプト文のように1文1行で並ぶ形）。
      // 1文が2行になる・PC の広い枠でつなげれば1行に収まる（右が大きく空く）ときは、文をつなげて流す
      var n = b.querySelectorAll('br.sb').length + 1, withSb = lineCount(b);
      b.classList.add('nosb');
      if (withSb <= n && lineCount(b) >= n) b.classList.remove('nosb');
      // 文をつなげたときは、文の終わりのまとまり（改行の直前の n-b）も段落の途中になるので、右詰めのときに解けるようにする
      b.querySelectorAll('br.sb').forEach(function (br) {
        var t = br.previousElementSibling;
        if (t && t.tagName === 'N-B') t.classList.toggle('sbl', b.classList.contains('nosb'));
      });
    });
    document.querySelectorAll('.wrap-fill').forEach(function (b) { b.classList.remove('wrap-fill'); });
    document.querySelectorAll('.jfy').forEach(function (b) { b.classList.remove('jfy'); });
    var jfy = [];
    document.querySelectorAll('n-b.loose').forEach(function (b) { b.classList.remove('loose'); });
    Array.prototype.forEach.call(phraseTexts, function (n) {
      var p = n.parentElement;
      if (!p || !n.querySelector('wbr')) return;
      var centered = getComputedStyle(p).textAlign === 'center';
      if (!n.classList.contains('h')) n.classList.toggle('c', centered);
    });
    var blocks = [];
    document.querySelectorAll('main n-w, main n-b').forEach(function (n) {
      var b = blockOf(n);
      if (blocks.indexOf(b) < 0) blocks.push(b);
    });
    blocks.forEach(function (blk) {
      if (blk.offsetParent === null || blk.querySelector('p, li, dd, div, ul, ol, table')) return;
      var inTable = !!blk.closest("table"); // 表のマスも右詰めの対象（右の最大の空きが小さくなるなら右詰め。人の指摘 2026-11-07）
      var cs = getComputedStyle(blk);
      if (cs.textAlign === 'center' || cs.textAlign === 'right' || cs.whiteSpace === 'nowrap' || cs.writingMode.indexOf('vertical') === 0) return;
      var fsz = parseFloat(cs.fontSize);
      // 左揃えの本文・項目・表のマスは、両端揃えにして右端をそろえる（半角〜1文字分の小さな空きは、折り方では消せないため。
      // 見出し・大きな文字・中央揃えは対象外。最後の行と手で入れた改行の前は左揃えのまま。人の指摘 2026-11-07）
      if (fsz < 20 && !/^H[1-6]$/.test(blk.tagName) && !blk.querySelector('.ml-s')) jfy.push(blk);
      keepTail(blk);
      var gapA = maxGap(blk);
      var narrow = !inTable && (blk.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight)) / fsz < 16; // 1行に16文字未満の狭い枠（スマホのカード・2列の図など）。表のマスは右の空きを優先
      if (gapA <= (fsz >= 22 ? 5 : narrow ? 3 : 1.5)) return; // 右の空きが小さければ、言葉の切れ目で折った形のまま（ふつうの幅は1.5文字分まで。基本は右詰め）
      var a = narrow ? cost(blk, fsz) : 0;
      // 言葉の切れ目で折った形（A）で右が空く・最後の行が短いときは、言葉の途中でも折る形（B）も組んで、見栄えの良いほうを使う
      blk.classList.add('wrap-fill');
      keepNums(blk); // 言葉の途中でも折れるので、先に数字と単位（「2営業日」「80万円」）をまとめておく
      var loosened = [];
      blk.querySelectorAll('n-b').forEach(function (b) {
        // 6文字以上の塊と、英単語の端を巻き込んだ塊（「価・R」＋「evPAR」、「Rとは？」）を解く（英単語の前後では折れる。英単語の中は折れない）。
        // 数字と単位（n-b.num）・最後の語尾（n-b.tail）・読点や句点で終わる区切りの終わり（「79件から、」）は解かない
        if (b.classList.contains('num') || b.classList.contains('tail') || /[、。，．！？]$/.test(b.textContent) || !(b.textContent.length >= 6 || /・[A-Za-z]$|[A-Za-z][^A-Za-z.\-]/.test(b.textContent))) return;
        keepNums(b); // 解く前に、中の数字と単位（「80万円」「2027年」）をまとめておく（「80万／円」を防ぐ）
        b.classList.add('loose'); loosened.push(b);
      });
      keepTail(blk);
      // ふつうの幅の枠は、右の最大の空きが小さくなるなら B（基本は右詰め。人の方針 2026-11-06）。
      // 狭い枠（カード・2列の図など）は、言葉の途中で切れる所も数えて、見栄えの良いほう（「ごみ袋の／予備」「要件を／満たせるか」）
      if (narrow ? cost(blk, fsz) >= a : maxGap(blk) > gapA - 1) {
        blk.classList.remove('wrap-fill');
        loosened.forEach(function (b) { b.classList.remove('loose'); });
      }
    });
    // 判定がすべて済んでから両端揃えにする。右の空きが1.5文字分を超える行があるまとまりは、字間が大きく開くので左揃えのまま
    jfy.filter(function (b) { return maxGap(b) <= 1.5; }).forEach(function (b) { b.classList.add('jfy'); });
  };
  if (phraseTexts.length) {
    var fitTimer, fitW = window.innerWidth;
    fitLines();
    window.addEventListener('load', fitLines);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitLines);
    // 幅が変わったときだけ組み直す（スマホはスクロールでアドレスバーが出入りし、高さだけが変わる resize が続くため。組み直しは重く、スクロールがカクつく）
    window.addEventListener('resize', function () { if (window.innerWidth === fitW) return; fitW = window.innerWidth; clearTimeout(fitTimer); fitTimer = setTimeout(fitLines, 150); });
  }

  // 横にスライドする表の案内（「表は左右にスライドできます →」）は、表が枠からはみ出すときだけ出す
  var hints = document.querySelectorAll('.table-hint');
  if (hints.length) {
    var checkHints = function () {
      Array.prototype.forEach.call(hints, function (h) {
        var sc = h.nextElementSibling;
        h.hidden = !(sc && sc.scrollWidth > sc.clientWidth + 2);
      });
    };
    checkHints();
    window.addEventListener('load', checkHints);
    window.addEventListener('resize', checkHints);
  }

  // TOPのファーストビュー：写真をゆっくり寄りながら切り替える（動きを減らす設定のときは1枚目のまま）
  var slides = document.querySelectorAll('.hero--x .hero__bg');
  var count = document.querySelector('.hero__count');
  if (slides.length) {
    var cur = 0, ms = 6000;
    slides[0].classList.add('is-active');
    if (!reduce && slides.length > 1) {
      var num = count && count.querySelector('.hero__count-n');
      var run = function () {
        if (!count) return;
        count.classList.remove('is-running');
        void count.offsetWidth;  // アニメーションを最初からやり直す
        count.style.setProperty('--slide-ms', ms + 'ms');
        count.classList.add('is-running');
      };
      run();
      setInterval(function () {
        if (document.hidden) return;
        var next = (cur + 1) % slides.length;
        var img = slides[next];
        if (!img.complete) return;  // 次の写真が読み込めるまで待つ
        slides[cur].classList.remove('is-active');
        img.classList.add('is-active');
        cur = next;
        if (num) num.textContent = ('0' + (cur + 1)).slice(-2);
        run();
      }, ms);
    }
  }

  // 数字のカウントアップ（data-count。画面に入ったら0から数える）
  // （動きを減らす設定でも数える。小さな数字の変化だけで、画面は動かないため）
  var nums = document.querySelectorAll('[data-count]');
  if (nums.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        var el = en.target.matches('[data-count]') ? en.target : en.target.querySelector('[data-count]'), to = parseFloat(el.getAttribute('data-count'));
        var dec = (el.getAttribute('data-count').split('.')[1] || '').length;
        var t0 = performance.now(), dur = 1400;
        var step = function (t) {
          var k = Math.min(1, (t - t0) / dur);
          el.textContent = (to * (1 - Math.pow(1 - k, 3))).toFixed(dec);
          if (k < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      });
    }, { threshold: 0.3 });
    nums.forEach(function (el) {
      // まだ画面の下にあるときだけ 0 にしておく（見えている数字は書き換えない）
      if (el.getBoundingClientRect().top > window.innerHeight) el.textContent = (0).toFixed((el.getAttribute('data-count').split('.')[1] || '').length);
      io.observe(el.closest('.project__rating') || el);
    });
  }
})();

// TOPの事業紹介（スマホ）：カルーセルで画面の中央に来たカードに色を付ける（ホバーの代わり）
(function () {
  'use strict';
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!window.matchMedia('(hover: none)').matches) return;
  document.querySelectorAll('.vrow__list').forEach(function (list) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { en.target.classList.toggle('is-current', en.intersectionRatio >= 0.75); });
    }, { root: list.scrollWidth > list.clientWidth ? list : null, threshold: [0, 0.75, 1], rootMargin: '0px 0px -25% 0px' });
    list.querySelectorAll('.vsvc').forEach(function (c) { io.observe(c); });
  });
})();

// コーポレート：図やカードが画面に入ったら .is-in を付けて動かす
(function () {
  'use strict';
  if (!document.body.classList.contains('is-corp')) return;
  var targets = document.querySelectorAll('.timeline, .issue, .flow, .sflow, .faq__list, .overview');
  if (!('IntersectionObserver' in window)) { targets.forEach(function (t) { t.classList.add('is-in'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
  }, { threshold: 0.25 });
  targets.forEach(function (t) { io.observe(t); });
})();


// スマホのプラン比較：3本の帯の右側の斜めの線を、帯の高さにかかわらず1本のまっすぐな線につなげる
(function () {
  'use strict';
  var pds = document.querySelectorAll('.pd');
  if (!pds.length) return;
  var mq = window.matchMedia('(max-width: 899px)');
  var TOP = 0.7; // 一番上の帯の上端の幅（帯の列幅に対する割合）。下端で 100% になる
  function shape() {
    pds.forEach(function (pd) {
      var segs = Array.prototype.slice.call(pd.querySelectorAll('.pd__seg'));
      if (!mq.matches) { segs.forEach(function (s) { s.style.clipPath = ''; }); return; }
      var top = segs[0].getBoundingClientRect().top;
      var h = segs[segs.length - 1].getBoundingClientRect().bottom - top;
      if (h <= 0) return;
      segs.forEach(function (s) {
        var r = s.getBoundingClientRect();
        var ft = TOP + (1 - TOP) * (r.top - top) / h;
        var fb = TOP + (1 - TOP) * (r.bottom - top) / h;
        s.style.clipPath = 'polygon(0 0, ' + (ft * 100).toFixed(2) + '% 0, ' + (fb * 100).toFixed(2) + '% 100%, 0 100%)';
      });
    });
  }
  var t;
  function later() { clearTimeout(t); t = setTimeout(shape, 100); }
  shape();
  window.addEventListener('load', shape);
  window.addEventListener('resize', later);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(shape);
})();

