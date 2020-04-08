$(document).ready(function() {

    var $loading = $('.loader').hide();
    $(document)
        .ajaxStart(function () {
            $loading.show();
            $('.main-panel').css('opacity', 0.7);
        })
        .ajaxStop(function () {
            $loading.hide();
            $('.main-panel').css('opacity', 1);
        });
});








