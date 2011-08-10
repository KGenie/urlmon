(function ($) {
    // Force all link buttons to look exactly like anchors
    $(document).ready(function() {
        $('button.link[type="submit"]').each(function() {
            var current = $(this);
            var link = $('<a href="#" class="link-button" />');
            link.html(current.html());
            link.click(function() {
                $(this).closest('form').submit();
                return false;
            });
            current.replaceWith(link);
        });
    });
})(jQuery)
