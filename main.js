/**
 * RIVIA&CO. Corporate Site
 * 全ページを index.html にまとめ、URL の # でページを切り替える
 */
(function () {
  'use strict';

  window.RIVIA_READY = true;
  document.documentElement.classList.add('js');

  var SITE_NAME = '合同会社RIVIA&CO.';
  var DEFAULT_TITLE = document.title;
  var pages = Array.prototype.slice.call(document.querySelectorAll('.page'));
  var header = document.querySelector('.header');
  var stickyCta = document.querySelector('.sticky-cta');
  var stickyLink = stickyCta && stickyCta.querySelector('a');
  var currentPage = null;
  var pendingCategory = null;

  /**
   * ページ切り替え
   * #about のようなページIDなら、そのページを表示してページ先頭へ。
   * #project のようなページ内の要素IDなら、そのページを表示してその位置へ。
   */
  function findPage(id) {
    var el = id && document.getElementById(id);
    if (!el) return { page: pages[0], target: null };
    if (el.classList.contains('page')) return { page: el, target: null };
    return { page: el.closest('.page') || pages[0], target: el };
  }

  function showPage(page) {
    if (page === currentPage) return;
    pages.forEach(function (p) { p.classList.toggle('is-active', p === page); });
    currentPage = page;

    var title = page.getAttribute('data-title');
    document.title = title ? title + ' | ' + SITE_NAME : DEFAULT_TITLE;

    // ナビの現在地表示
    document.querySelectorAll('[data-nav]').forEach(function (a) {
      if (a.getAttribute('data-nav') === page.id) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    var serviceBtn = document.querySelector('.gnav__item--has-sub > .gnav__link');
    if (serviceBtn) {
      if (page.id.indexOf('service-') === 0) serviceBtn.setAttribute('aria-current', 'page');
      else serviceBtn.removeAttribute('aria-current');
    }

    // スマホ用の固定相談バー（お問い合わせ・採用・ポリシーでは非表示）
    if (stickyCta) {
      stickyCta.hidden = page.getAttribute('data-sticky') === 'false';
      stickyLink.setAttribute('data-category', page.getAttribute('data-category') || '');
    }
  }

  function route() {
    var id = decodeURIComponent(window.location.hash.replace('#', ''));
    var found = findPage(id);
    var changed = found.page !== currentPage;
    showPage(found.page);
    closeSubnav();

    if (found.target) {
      found.target.scrollIntoView();
    } else if (changed) {
      window.scrollTo({ top: 0, behavior: 'instant' });
    }
    applyCategory();
    onScroll();
    requestReveal();
  }

  window.addEventListener('hashchange', route);

  /**
   * お問い合わせ: 相談ボタンに設定されたカテゴリを自動選択
   */
  function applyCategory() {
    if (!pendingCategory) return;
    var select = document.getElementById('category');
    var option = select && select.querySelector('option[data-key="' + pendingCategory + '"]');
    if (option) option.selected = true;
    pendingCategory = null;
  }

  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="#"]');
    if (!link) return;
    var category = link.getAttribute('data-category');
    if (category) pendingCategory = category;
    // 同じ # を再度クリックした場合も位置合わせ・カテゴリ反映を行う
    if (link.getAttribute('href') === window.location.hash) {
      e.preventDefault();
      route();
    }
  });

  /**
   * Header の下線と、スマホ用の固定相談バーの表示切り替え
   */
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('is-scrolled', y > 10);
    // ファーストビューを過ぎたら固定相談バーを表示
    if (stickyCta) stickyCta.classList.toggle('is-visible', y > window.innerHeight * 0.6);
  }
  window.addEventListener('scroll', onScroll, { passive: true });

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
   * （ページ切り替えや高速スクロールでも表示抜けが起きないようにする）
   */
  var ticking = false;
  function revealInView() {
    ticking = false;
    if (!currentPage) return;
    var limit = window.innerHeight * 0.92;
    currentPage.querySelectorAll('.reveal:not(.is-visible)').forEach(function (el) {
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

  /**
   * Careers: 選択したファイル名を表示
   */
  document.querySelectorAll('.file input[type="file"]').forEach(function (input) {
    input.addEventListener('change', function () {
      var box = input.closest('.file');
      var name = box.querySelector('.file__name');
      var file = input.files && input.files[0];
      box.classList.toggle('has-file', !!file);
      name.textContent = file ? file.name : name.getAttribute('data-default');
    });
  });

  route();
})();
