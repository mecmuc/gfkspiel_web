/*! gfkspiel router — vanilla JS, no jQuery */
(function () {
    'use strict';

    var created = {};

    function pageId(hash) {
        var id = (hash || '').replace(/^#/, '');
        return id || 'page-main_menu';
    }

    function fire(el, eventName) {
        el.dispatchEvent(new CustomEvent(eventName, { bubbles: false }));
    }

    function showPage(id) {
        var target = document.getElementById(id);
        if (!target) { return; }

        var current = document.querySelector('.page[style*="block"]') ||
                      document.querySelector('.page:not([style])');
        // find the currently visible page more reliably
        var pages = document.querySelectorAll('.page');
        var currentPage = null;
        pages.forEach(function (p) {
            if (p !== target && p.style.display === 'block') {
                currentPage = p;
            }
        });

        if (currentPage) {
            fire(currentPage, 'pagebeforehide');
            currentPage.style.display = 'none';
            fire(currentPage, 'pagehide');
        }

        if (!created[id]) {
            created[id] = true;
            fire(target, 'pagecreate');
        }

        target.style.display = 'block';
        fire(target, 'pageshow');
        window.scrollTo(0, 0);
    }

    document.addEventListener('click', function (e) {
        var a = e.target.closest('a[href^="#"]');
        if (!a) { return; }
        var href = a.getAttribute('href');
        if (!href || href === '#') { return; }

        if (a.getAttribute('data-rel') === 'back') {
            e.preventDefault();
            history.back();
            return;
        }

        var targetEl = document.querySelector(href);
        if (!targetEl || !targetEl.classList.contains('page')) { return; }

        e.preventDefault();
        var id = pageId(href);
        history.pushState({ page: id }, '', '#' + id);
        showPage(id);
    });

    window.addEventListener('popstate', function () {
        showPage(pageId(window.location.hash));
    });

    // Stub for app.js compatibility
    window.mobileChangePage = function (url) { window.location.replace(url); };

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.page').forEach(function (p) {
            p.style.display = 'none';
        });
        showPage(pageId(window.location.hash));
    });

}());
