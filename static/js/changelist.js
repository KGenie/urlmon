var uMon = uMon || {};

(function (uMon, $) {
    $(document).ready(function() {
        var form = $('#query');
        var tracker_combo = form.find('select');
        tracker_combo.change(function () {
            form.submit();
        });
    });

})(uMon, jQuery);
