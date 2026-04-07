/*! gfkspiel router — replaces jQuery Mobile page system */
(function ($) {
    'use strict';

    var created = {};

    function pageId(hash) {
        var id = (hash || '').replace(/^#/, '');
        return id || 'page-main_menu';
    }

    function showPage(id) {
        var $target = $('#' + id);
        if (!$target.length) { return; }

        var $current = $('.page:visible').not($target);
        if ($current.length) {
            $current.trigger('pagebeforehide');
            $current.hide();
            $current.trigger('pagehide');
        }

        if (!created[id]) {
            created[id] = true;
            $target.trigger('pagecreate');
        }

        $target.show();
        $target.trigger('pageshow');
        window.scrollTo(0, 0);
    }

    $(document).on('click', 'a[href^="#"]', function (e) {
        var $a = $(this);
        var href = $a.attr('href');
        if (!href || href === '#') { return; }

        if ($a.attr('data-rel') === 'back') {
            e.preventDefault();
            history.back();
            return;
        }

        // Only intercept links that target a .page element
        var $target = $(href);
        if (!$target.hasClass('page')) { return; }

        e.preventDefault();
        var id = pageId(href);
        history.pushState({ page: id }, '', '#' + id);
        showPage(id);
    });

    window.addEventListener('popstate', function () {
        showPage(pageId(window.location.hash));
    });

    // Compatibility stub so app.js $.mobile.changePage calls still work
    if (!$.mobile) { $.mobile = {}; }
    $.mobile.changePage = function (url) { window.location.replace(url); };

    // Boot: hide all pages, show initial
    $(function () {
        $('.page').hide();
        showPage(pageId(window.location.hash));
    });

}(jQuery));
