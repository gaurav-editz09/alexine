/* =========================================================
   EMBER & SPICE — interactions
   Vanilla JS. No dependencies.
   ========================================================= */

(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var menuToggle = doc.querySelector('.menu-toggle');
  var mobileNav = doc.getElementById('mobile-nav');
  var reserveDialog = doc.getElementById('reserve-dialog');
  var lightbox = doc.getElementById('lightbox');
  var lightboxImg = doc.getElementById('lightbox-img');
  var lightboxCaption = doc.getElementById('lightbox-caption');
  var lightboxCount = doc.querySelector('.lightbox__count');
  var reserveOpener = null;
  var lightboxIndex = 0;

  /* ---------------------------------------------------------
     Header, scroll progress, parallax
     --------------------------------------------------------- */

  var header = doc.getElementById('site-header');
  var progress = doc.querySelector('.scroll-progress span');
  var parallaxEls = Array.prototype.slice.call(doc.querySelectorAll('[data-parallax]'));
  var ticking = false;

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;

    if (header) header.classList.toggle('is-scrolled', y > 42);

    if (progress) {
      var max = doc.documentElement.scrollHeight - window.innerHeight;
      var pct = max > 0 ? Math.min(100, Math.max(0, (y / max) * 100)) : 0;
      progress.style.width = pct + '%';
    }

    if (!reduceMotion && parallaxEls.length) {
      var vh = window.innerHeight;
      parallaxEls.forEach(function (el) {
        var rect = el.getBoundingClientRect();
        if (rect.bottom < -100 || rect.top > vh + 100) return;
        var speed = parseFloat(el.getAttribute('data-parallax')) || 0.08;
        var offset = (rect.top + rect.height / 2 - vh / 2) * -speed;
        el.style.transform = 'translate3d(0,' + offset.toFixed(2) + 'px,0)';
      });
    }

    ticking = false;
  }

  function requestScroll() {
    if (!ticking) {
      window.requestAnimationFrame(onScroll);
      ticking = true;
    }
  }

  window.addEventListener('scroll', requestScroll, { passive: true });
  window.addEventListener('resize', requestScroll, { passive: true });
  onScroll();

  /* ---------------------------------------------------------
     Reveal on scroll
     --------------------------------------------------------- */

  var revealEls = Array.prototype.slice.call(doc.querySelectorAll('.reveal'));

  if (!('IntersectionObserver' in window) || reduceMotion) {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -6% 0px' });

    revealEls.forEach(function (el) { revealObserver.observe(el); });
  }

  /* ---------------------------------------------------------
     Active navigation
     --------------------------------------------------------- */

  var navLinks = Array.prototype.slice.call(doc.querySelectorAll('[data-nav]'));
  var sections = ['story', 'dishes', 'menu', 'gallery', 'experience', 'contact']
    .map(function (id) { return doc.getElementById(id); })
    .filter(Boolean);

  if ('IntersectionObserver' in window) {
    var sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var id = entry.target.id;
        navLinks.forEach(function (link) {
          if (link.getAttribute('href') === '#' + id) {
            link.setAttribute('aria-current', 'true');
          } else {
            link.removeAttribute('aria-current');
          }
        });
      });
    }, { rootMargin: '-38% 0px -52% 0px', threshold: 0 });

    sections.forEach(function (section) { sectionObserver.observe(section); });
  }

  /* ---------------------------------------------------------
     Smooth same-page navigation
     --------------------------------------------------------- */

  function scrollToTarget(target) {
    var top = target.getBoundingClientRect().top + window.scrollY;
    var headerH = header ? header.offsetHeight : 0;
    var barH = doc.querySelector('.demo-bar') ? doc.querySelector('.demo-bar').offsetHeight : 0;
    var offset = headerH + 18;
    if (window.scrollY < 10) offset += barH;

    window.scrollTo({
      top: Math.max(0, top - offset),
      behavior: reduceMotion ? 'auto' : 'smooth'
    });
  }

  doc.addEventListener('click', function (event) {
    var link = event.target.closest('a[href^="#"]');
    if (!link) return;
    var href = link.getAttribute('href');
    if (!href || href === '#') return;
    var target = doc.querySelector(href);
    if (!target) return;

    event.preventDefault();

    if (mobileNav && mobileNav.open) {
      closeMobileNav(false);
    }

    if (href === '#home') {
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    } else {
      scrollToTarget(target);
    }

    if (history.pushState) {
      history.pushState(null, '', href);
    } else {
      window.location.hash = href;
    }
  });

  /* ---------------------------------------------------------
     Menu tabs
     --------------------------------------------------------- */

  var tabs = Array.prototype.slice.call(doc.querySelectorAll('.menu__tab'));
  var panels = Array.prototype.slice.call(doc.querySelectorAll('.menu__panel'));
  var figures = Array.prototype.slice.call(doc.querySelectorAll('.menu__figure'));

  function activateTab(tab, moveFocus) {
    var id = tab.id.replace('tab-', '');

    tabs.forEach(function (item) {
      var active = item === tab;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-selected', active ? 'true' : 'false');
      item.setAttribute('tabindex', active ? '0' : '-1');
    });

    panels.forEach(function (panel) {
      var active = panel.id === 'panel-' + id;
      panel.hidden = !active;
      panel.classList.toggle('is-active', active);
    });

    figures.forEach(function (figure) {
      figure.classList.toggle('is-active', figure.getAttribute('data-panel-img') === id);
    });

    if (moveFocus) tab.focus();

    if (window.matchMedia('(max-width: 720px)').matches) {
      tab.scrollIntoView({ inline: 'center', block: 'nearest', behavior: reduceMotion ? 'auto' : 'smooth' });
    }
  }

  tabs.forEach(function (tab, index) {
    tab.addEventListener('click', function () { activateTab(tab, false); });

    tab.addEventListener('keydown', function (event) {
      var next = null;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
        next = tabs[(index + 1) % tabs.length];
      } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
        next = tabs[(index - 1 + tabs.length) % tabs.length];
      } else if (event.key === 'Home') {
        next = tabs[0];
      } else if (event.key === 'End') {
        next = tabs[tabs.length - 1];
      }
      if (next) {
        event.preventDefault();
        activateTab(next, true);
      }
    });
  });

  /* ---------------------------------------------------------
     Dialogs
     --------------------------------------------------------- */

  function syncScrollLock() {
    var anyOpen = Array.prototype.slice.call(doc.querySelectorAll('dialog[open]')).length > 0;
    doc.body.classList.toggle('modal-open', anyOpen);
  }

  function showDialog(dialog) {
    if (!dialog) return;
    if (typeof dialog.showModal === 'function') {
      if (!dialog.open) dialog.showModal();
    } else {
      dialog.setAttribute('open', '');
    }
    syncScrollLock();
  }

  function closeDialog(dialog) {
    if (!dialog || !dialog.open) return;
    if (typeof dialog.close === 'function') dialog.close();
    else dialog.removeAttribute('open');
    syncScrollLock();
  }

  // Reserve panel
  doc.querySelectorAll('[data-open-reserve]').forEach(function (button) {
    button.addEventListener('click', function () {
      var fromMobileNav = !!(button.closest && button.closest('dialog'));
      if (mobileNav && mobileNav.open) closeMobileNav(false);
      reserveOpener = fromMobileNav ? menuToggle : button;
      showDialog(reserveDialog);
      var closeBtn = reserveDialog.querySelector('.modal__close');
      if (closeBtn) closeBtn.focus();
    });
  });

  doc.querySelectorAll('[data-close-reserve]').forEach(function (button) {
    button.addEventListener('click', function () {
      closeDialog(reserveDialog);
    });
  });

  if (reserveDialog) {
    reserveDialog.addEventListener('click', function (event) {
      if (event.target === reserveDialog) closeDialog(reserveDialog);
    });
    reserveDialog.addEventListener('close', function () {
      syncScrollLock();
      if (reserveOpener && doc.contains(reserveOpener) && reserveOpener.offsetParent !== null) {
        reserveOpener.focus();
      } else if (menuToggle) {
        menuToggle.focus();
      }
    });
  }

  // Mobile navigation
  function openMobileNav() {
    if (!mobileNav) return;
    showDialog(mobileNav);
    if (menuToggle) menuToggle.setAttribute('aria-expanded', 'true');
    var first = mobileNav.querySelector('.mobile-nav__close');
    if (first) first.focus();
  }

  function closeMobileNav(returnFocus) {
    if (!mobileNav || !mobileNav.open) return;
    closeDialog(mobileNav);
    if (menuToggle) {
      menuToggle.setAttribute('aria-expanded', 'false');
      if (returnFocus !== false) menuToggle.focus();
    }
  }

  if (menuToggle) {
    menuToggle.addEventListener('click', function () {
      if (mobileNav && mobileNav.open) closeMobileNav(true);
      else openMobileNav();
    });
  }

  doc.querySelectorAll('[data-close-nav]').forEach(function (button) {
    button.addEventListener('click', function (event) {
      // Anchor links are handled by the global smooth-scroll handler.
      if (button.tagName === 'A' && button.getAttribute('href') && button.getAttribute('href').charAt(0) === '#') {
        closeMobileNav(false);
        return;
      }
      event.preventDefault();
      closeMobileNav(true);
    });
  });

  if (mobileNav) {
    mobileNav.addEventListener('click', function (event) {
      if (event.target === mobileNav) closeMobileNav(true);
    });
    mobileNav.addEventListener('close', function () {
      syncScrollLock();
      if (menuToggle) menuToggle.setAttribute('aria-expanded', 'false');
    });
  }

  /* ---------------------------------------------------------
     Gallery lightbox
     --------------------------------------------------------- */

  var galleryItems = Array.prototype.slice.call(doc.querySelectorAll('[data-gallery]'));

  function renderLightbox(index) {
    if (!galleryItems.length || !lightboxImg) return;
    lightboxIndex = (index + galleryItems.length) % galleryItems.length;
    var item = galleryItems[lightboxIndex];
    var sourceImg = item.querySelector('img');
    var full = item.getAttribute('data-full');
    var srcset = item.getAttribute('data-full-srcset');
    var caption = item.getAttribute('data-caption') || '';

    lightboxImg.src = full;
    if (srcset) lightboxImg.setAttribute('srcset', srcset);
    else lightboxImg.removeAttribute('srcset');
    lightboxImg.sizes = '100vw';
    lightboxImg.alt = sourceImg ? sourceImg.alt : caption;
    if (lightboxCaption) lightboxCaption.textContent = caption;
    if (lightboxCount) {
      lightboxCount.textContent =
        String(lightboxIndex + 1).padStart(2, '0') + ' / ' + String(galleryItems.length).padStart(2, '0');
    }
  }

  function openLightbox(index) {
    if (!lightbox) return;
    renderLightbox(index);
    showDialog(lightbox);
    var closeBtn = lightbox.querySelector('[data-close-lightbox]');
    if (closeBtn) closeBtn.focus();
  }

  galleryItems.forEach(function (item, index) {
    item.addEventListener('click', function () { openLightbox(index); });
  });

  doc.querySelectorAll('[data-close-lightbox]').forEach(function (button) {
    button.addEventListener('click', function () { closeDialog(lightbox); });
  });

  var prevBtn = doc.querySelector('[data-lightbox-prev]');
  var nextBtn = doc.querySelector('[data-lightbox-next]');
  if (prevBtn) prevBtn.addEventListener('click', function () { renderLightbox(lightboxIndex - 1); });
  if (nextBtn) nextBtn.addEventListener('click', function () { renderLightbox(lightboxIndex + 1); });

  if (lightbox) {
    lightbox.addEventListener('click', function (event) {
      if (event.target === lightbox) closeDialog(lightbox);
    });
    lightbox.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowLeft') {
        event.preventDefault();
        renderLightbox(lightboxIndex - 1);
      } else if (event.key === 'ArrowRight') {
        event.preventDefault();
        renderLightbox(lightboxIndex + 1);
      }
    });
    lightbox.addEventListener('close', function () {
      syncScrollLock();
      if (galleryItems[lightboxIndex]) galleryItems[lightboxIndex].focus();
    });
  }

  /* ---------------------------------------------------------
     Hero pointer parallax
     --------------------------------------------------------- */

  var hero = doc.querySelector('.hero');
  var heroMedia = doc.querySelector('.hero__media');

  if (hero && heroMedia && !reduceMotion && window.matchMedia('(pointer: fine)').matches) {
    var heroTicking = false;
    var mx = 0;
    var my = 0;

    hero.addEventListener('pointermove', function (event) {
      var rect = hero.getBoundingClientRect();
      mx = ((event.clientX - rect.left) / rect.width - 0.5) * 2;
      my = ((event.clientY - rect.top) / rect.height - 0.5) * 2;

      if (!heroTicking) {
        heroTicking = true;
        window.requestAnimationFrame(function () {
          hero.style.setProperty('--mx', mx.toFixed(3));
          hero.style.setProperty('--my', my.toFixed(3));
          heroTicking = false;
        });
      }
    }, { passive: true });

    hero.addEventListener('pointerleave', function () {
      hero.style.setProperty('--mx', '0');
      hero.style.setProperty('--my', '0');
    });
  }

  /* ---------------------------------------------------------
     Pointer tilt on image cards
     --------------------------------------------------------- */

  if (!reduceMotion && window.matchMedia('(pointer: fine)').matches) {
    doc.querySelectorAll('.dish__media, .gallery__item').forEach(function (el) {
      var queued = false;
      var tx = 0;
      var ty = 0;

      el.addEventListener('pointermove', function (event) {
        var rect = el.getBoundingClientRect();
        tx = (event.clientX - rect.left) / rect.width - 0.5;
        ty = (event.clientY - rect.top) / rect.height - 0.5;

        if (queued) return;
        queued = true;
        window.requestAnimationFrame(function () {
          queued = false;
          el.style.setProperty('--tilt-y', (tx * 4).toFixed(2) + 'deg');
          el.style.setProperty('--tilt-x', (-ty * 4).toFixed(2) + 'deg');
        });
      }, { passive: true });

      el.addEventListener('pointerleave', function () {
        el.style.setProperty('--tilt-x', '0deg');
        el.style.setProperty('--tilt-y', '0deg');
      });
    });
  }

  /* ---------------------------------------------------------
     Footer year
     --------------------------------------------------------- */

  var yearEl = doc.querySelector('[data-year]');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
