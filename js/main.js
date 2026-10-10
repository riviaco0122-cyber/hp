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
  var category = document.getElementById('category');
  if (category && window.URLSearchParams) {
    var param = new URLSearchParams(window.location.search).get('category');
    if (param) {
      var option = category.querySelector('option[data-key="' + param + '"]');
      if (option) option.selected = true;
    }
  }

  /**
   * Media: 公開日を迎えていない記事は表示しない（予約公開）
   * 各カードの data-date（YYYY-MM-DD）と今日の日付を比べる
   */
  var now = new Date();
  var today = now.getFullYear() + '-' + ('0' + (now.getMonth() + 1)).slice(-2) + '-' + ('0' + now.getDate()).slice(-2);
  // 公開日前の記事ページを直接開いた場合は、記事一覧へ戻す
  var scheduled = document.querySelector('.article[data-publish]');
  if (scheduled && scheduled.getAttribute('data-publish') > today) {
    document.documentElement.style.visibility = 'hidden';
    location.replace(new URL('../media.html', location.href).href);
  }
  document.querySelectorAll('.media-card[data-date]').forEach(function (c) {
    if (c.getAttribute('data-date') > today) {
      c.setAttribute('data-future', '');
      c.hidden = true;
    }
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
  document.querySelectorAll('.mq li[data-date]').forEach(function (li) {
    if (li.getAttribute('data-date') > today) li.hidden = true;
  });
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
  // 記事ページのガイド欄：公開前の記事は出さない
  // 前後の記事は、公開済みの記事の中で決める
  document.querySelectorAll('.guide-box').forEach(function (box) {
    var items = Array.prototype.slice.call(box.querySelectorAll('.guide-box__list li'));
    items.forEach(function (li) { if (li.getAttribute('data-date') > today) li.hidden = true; });
    var shown = items.filter(function (li) { return !li.hidden; });
    var i = shown.findIndex(function (li) { return li.hasAttribute('aria-current'); });
    var pager = box.querySelector('.guide-box__pager');
    [[shown[i - 1], 'guide-box__prev', '前の記事'], [shown[i + 1], 'guide-box__next', '次の記事']].forEach(function (x) {
      var link = x[0] && x[0].querySelector('a');
      if (!link) return;
      var a = document.createElement('a');
      a.href = link.getAttribute('href');
      a.className = x[1];
      a.innerHTML = '<span>' + x[2] + '</span>';
      a.appendChild(document.createTextNode(link.textContent));
      pager.appendChild(a);
    });
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
  // アキヤドのトップ：FVを見ている間は、下部の相談ボタンを隠す（FVの入口・検索と重ならないように）
  var mfv = document.querySelector('.mfv');
  var fixedMedia = document.querySelector('.fixed-cta--media');
  if (mfv && fixedMedia && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (en) { fixedMedia.classList.toggle('is-hidden', en[0].isIntersecting); }, { threshold: 0.15 }).observe(mfv);
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
    var q = (new URLSearchParams(location.search).get('q') || '').trim();
    var words = norm(q).split(/\s+/).filter(Boolean);
    var input = document.querySelector('.msearch__input');
    if (input) input.value = q;
    var hits = window.MEDIA_INDEX.filter(function (a) { return a.date <= today; }).map(function (a) {
      var title = norm(a.title), text = norm(a.text), score = 0;
      for (var i = 0; i < words.length; i++) {
        if (text.indexOf(words[i]) < 0 && title.indexOf(words[i]) < 0) return null;
        score += (title.indexOf(words[i]) >= 0 ? 10 : 0) + Math.min(text.split(words[i]).length - 1, 10);
      }
      return { a: a, score: score };
    }).filter(Boolean).sort(function (x, y) { return y.score - x.score || (x.a.date < y.a.date ? 1 : -1); });
    results.innerHTML = hits.map(function (h) {
      var a = h.a;
      return '<a href="' + a.slug + '.html" class="media-card is-visible">' +
        '<div class="thumb thumb--photo"><img src="../../images/photos/w/' + a.thumb + '-800.webp" alt="" loading="lazy" decoding="async" width="720" height="450">' +
        '<span class="thumb__cat">' + esc(a.cat) + '</span></div>' +
        '<div class="media-card__body"><span class="media-card__cat">' + esc(a.cat) + '</span>' +
        '<h3 class="media-card__title">' + esc(a.title) + '</h3>' +
        '<time class="media-card__date" datetime="' + a.date + '">' + a.date.replace(/-/g, '.') + '</time></div></a>';
    }).join('');
    var status = document.querySelector('.msearch-status');
    if (status) status.textContent = q ? '「' + q + '」の検索結果：' + hits.length + '件' : 'すべての記事：' + hits.length + '件';
    var none = document.querySelector('.msearch-empty');
    if (none) none.hidden = hits.length > 0;
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
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (res) {
          if (!res.ok) throw new Error('send failed');
          window.location.href = form.getAttribute('data-thanks');
        })
        .catch(function () {
          err.textContent = EN ? 'Your message could not be sent. Please try again later or check your entries.' : '送信できませんでした。時間をおいて再度お試しいただくか、入力内容をご確認ください。';
          if (btn) { btn.disabled = false; btn.classList.remove('is-sending'); }
        });
    });
  });
  /**
   * 本文の段落末（改行の直前を含む）が「す。」「ます。」のような短い行になったら、
   * その段落の字間をわずかに（最大 0.05em）詰めて、短い行が残らないように整える
   * （字間を広げると段落ごとに見た目が変わるため、詰める方向だけにする）
   * 詰めても直らない左揃えの文は、文末の言葉をまとめて次の行へ送る
   */
  function shortLines(block, fs) {
    // 文字（テキスト）だけを行ごとに集計し、短い行の数を返す
    var lines = [];
    var walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
    var range = document.createRange();
    for (var node = walker.nextNode(); node; node = walker.nextNode()) {
      if (!node.nodeValue.trim()) continue;
      range.selectNodeContents(node);
      Array.prototype.forEach.call(range.getClientRects(), function (r) {
        if (!r.width) return;
        var line = null;
        for (var k = 0; k < lines.length; k++) if (Math.abs(lines[k].top - r.top) < fs * 0.6) { line = lines[k]; break; }
        if (!line) { line = { top: r.top, width: 0 }; lines.push(line); }
        line.width += r.width;
      });
    }
    if (lines.length < 2) return 0;
    return lines.filter(function (l) { return l.width / fs < 5; }).length;
  }
  function fixBlock(b) {
    b.style.letterSpacing = '';
    if (!b.offsetParent) return;
    var cs = getComputedStyle(b);
    var fs = parseFloat(cs.fontSize);
    var base = parseFloat(cs.letterSpacing) || 0;
    var best = shortLines(b, fs), bestStep = 0;
    if (!best) return;
    var steps = [-0.01, -0.02, -0.03, -0.04, -0.05];
    for (var i = 0; i < steps.length && best; i++) {
      b.style.letterSpacing = (base + steps[i] * fs) + 'px';
      var n = shortLines(b, fs);
      if (n < best) { best = n; bestStep = steps[i]; }
    }
    b.style.letterSpacing = bestStep ? (base + bestStep * fs) + 'px' : '';
    // 左揃えの短い文で、まだ最後の行が短い場合は、文末の言葉（5〜9字）をまとめて改行させない
    if (best && !b.querySelector('n-w.j')) guardTail(b, fs);
  }
  // 表示の負担を減らすため、画面に近づいた段落から順に整える
  var lineObserver = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      lineObserver.unobserve(en.target);
      fixBlock(en.target);
    });
  }, { rootMargin: '400px 0px' }) : null;
  function fixShortLines() {
    var blocks = [];
    document.querySelectorAll('n-w').forEach(function (el) {
      var b = el.parentElement;
      if (b && blocks.indexOf(b) < 0) blocks.push(b);
    });
    unguard(document);
    blocks.forEach(function (b) {
      if (lineObserver) { lineObserver.unobserve(b); lineObserver.observe(b); } else fixBlock(b);
    });
  }
  function guardTail(b, fs) {
    var nws = b.querySelectorAll('n-w');
    var nw = nws[nws.length - 1];
    var text = nw && nw.lastChild;
    if (!text || text.nodeType !== 3) return;
    var str = text.nodeValue.replace(/\s+$/, '');
    if (str.length < 12) return;
    var words = [];
    if (window.Intl && Intl.Segmenter) {
      var seg = new Intl.Segmenter('ja', { granularity: 'word' });
      words = Array.from(seg.segment(str), function (x) { return x.segment; });
    } else {
      words = str.split('');
    }
    var tail = '';
    while (words.length && tail.length < 5 && (tail + words[words.length - 1]).length <= 9) tail = words.pop() + tail;
    if (tail.length < 5) tail = str.slice(-5);
    var guard = document.createElement('n-b');
    guard.setAttribute('data-auto', '');
    guard.textContent = tail;
    text.nodeValue = str.slice(0, str.length - tail.length);
    nw.appendChild(guard);
    if (shortLines(b, fs)) unguard(b);  // 改善しなければ元に戻す
  }
  function unguard(root) {
    root.querySelectorAll('n-b[data-auto]').forEach(function (g) {
      var parent = g.parentNode;
      parent.replaceChild(document.createTextNode(g.textContent), g);
      parent.normalize();
    });
  }
  var fixTimer;
  function scheduleFix() { clearTimeout(fixTimer); fixTimer = setTimeout(fixShortLines, 150); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fixShortLines);
  else window.addEventListener('load', fixShortLines);
  var lastWidth = window.innerWidth;
  window.addEventListener('resize', function () {
    if (window.innerWidth === lastWidth) return;  // スマホのスクロールでの高さ変化は無視
    lastWidth = window.innerWidth;
    scheduleFix();
  });
})();
