jQuery(document).ready(function () {
    jQuery('a.submit-link').click(function() {
        jQuery(this).closest('form').submit();
        return false;
    });
});
