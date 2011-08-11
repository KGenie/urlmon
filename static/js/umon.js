var uMon = {};

(function (uMon, $) {
    uMon.iFrameLoaded = function() {
        var iFrame = $('#select-frame');
        var iFrameChildren = iFrame.contents().find('.selectable-element');
        var iFrameHead = iFrame.contents().find('head');
        var input = $('input#css_selector');
        iFrameHead.append('<link rel="stylesheet" href="../css/frame.css" type="text/css" />');

        var clearSelection = function() {
            iFrameChildren.removeClass('selected-element');
        };

        iFrameChildren.click(function(event) {
            clearSelection();
            $(this).addClass('selected-element');
            $(this).parents().removeClass('selected-element');
            $(this).children().removeClass('selected-element');
            input.val('#' + this.id);
            return false;
        }).hover(function(event) {
            $(this).addClass('hovered-element');
            $(this).parents().removeClass('hovered-element');
            $(this).children().removeClass('hovered-element');
        }, function(event) {
            $(this).removeClass('hovered-element');
        });
    };
})(uMon, jQuery);
