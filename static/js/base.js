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

    $('#print-qrcode-form-all').submit(function(event) {
        event.preventDefault();
    
        let formData = new FormData(this);
        $('#preloaderModal').modal('show');
    
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            xhrFields: {
                responseType: 'blob'
            },
            success: function(data, status, xhr) {
                $('#preloaderModal').modal('hide');
                let disposition = xhr.getResponseHeader('Content-Disposition');
                let filename = "stop_point_report.pdf";
                if (disposition && disposition.indexOf('attachment') !== -1) {
                    let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    let matches = filenameRegex.exec(disposition);
                    if (matches != null && matches[1]) { 
                        filename = matches[1].replace(/['"]/g, '');
                    }
                }
    
                let blob = new Blob([data], { type: 'application/pdf' });
                let link = document.createElement('a');
                let url = window.URL.createObjectURL(blob);
                link.href = url;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
    
                window.URL.revokeObjectURL(url);
            },
            error: function() {
                $('#preloaderModal').modal('hide');
                alert("發生錯誤！");
            }
        });
    });
});

