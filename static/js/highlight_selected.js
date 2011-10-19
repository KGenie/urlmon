(function ($) {
    $(document).ready(function() {
        $('.selected-element').each(function() {
            var obj = $(this);
            var current_left = obj.offset().left;
            var current_top = obj.offset().top;
            var current_width = obj.width();
            var current_height = obj.height();
            obj.css('top', current_top);
            obj.css('left', current_left);
            obj.css('width', current_width);
            obj.css('height', current_height);
            obj.addClass('highlighted');
        });
    });
})(jQuery);
