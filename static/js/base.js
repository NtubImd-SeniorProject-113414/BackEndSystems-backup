$(document).ready(function () {
    $('#preloaderModal').modal('show');
    $('#preloaderModal').modal('hide');
    
    $('.hamburger-menu').click(function () {
        $('.sidebar').toggleClass('show');
        $('.overlay').toggle();
    });

    $('.overlay').click(function () {
        $('.sidebar').removeClass('show');
        $('.overlay').hide();
    });

    $('.main-option').click(function () {
        var $submenu = $(this).next('.collapse');
        var $icon = $(this).find('i.fa-chevron-down');

        if (!$submenu.hasClass('show')) {
            $('.collapse.show').collapse('hide').prev('.main-option').find('i.fa-chevron-down').removeClass('open');
            $submenu.collapse('show');
            $icon.addClass('open');
        } else {
            $submenu.collapse('hide');
            $icon.removeClass('open');
        }
    });

    $('.collapse').on('shown.bs.collapse', function () {
        $(this).prev('.main-option').find('i.fa-chevron-down').addClass('open');
    });

    $('.collapse').on('hidden.bs.collapse', function () {
        $(this).prev('.main-option').find('i.fa-chevron-down').removeClass('open');
    });

    $(window).on('beforeunload', function () {
        $('#preloaderModal').modal('show');
    });
    
    $(window).on('pageshow', function (event) {
        if (event.originalEvent.persisted) {
            $('.modal').modal('hide');
            location.reload();
        }
    });
    
    $('#preloaderModal').on('show.bs.modal', function () {
        $(this).css('z-index', 9999);
        $('.modal-backdrop').last().css('z-index', 9998);
    });
});
