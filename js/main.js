/**
 * RIVIA&CO. Corporate Site
 */
(function () {
  'use strict';

  window.RIVIA_READY = true;
  document.documentElement.classList.add('js');

  /**
   * Header の下線と、スマホ用の固定相談バーの表示切り替え
   */
  var header = document.querySelector('.header');
  var stickyCta = document.querySelector('.sticky-cta');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('is-scrolled', y > 10);
    // ファーストビューを過ぎたら固定相談バーを表示
    // 同じボタンがあるページ末尾の相談セクションが見えている間は重複させない
    if (stickyCta) stickyCta.classList.toggle('is-visible', y > window.innerHeight * 0.6 && !ctaInView);
  }
  var ctaInView = false;
  var ctaSection = document.querySelector('.cta');
  if (stickyCta && ctaSection && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      ctaInView = entries[0].isIntersecting;
      onScroll();
    }, { threshold: 0.3 }).observe(ctaSection);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

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
        : files[0].name + ' ほか' + (files.length - 1) + '件';
    });
  });
})();
