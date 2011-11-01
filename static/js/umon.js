var uMon = uMon || {};

(function (uMon, $) {


     uMon.iFrameRefresh = function (event) {
        var sender = $(this);
        var newUrl = sender.closest('form').find('#url').val();
        var cssSelector = sender.closest('form').find('#css_selector').val();
        var iFrame = sender.closest('form').find('iframe');
        if (iFrame.length == 0 || !newUrl) {
            return false;
        }

        var param = {
            url: newUrl
        };

        if (cssSelector) {
            param.selector = cssSelector;
        }
   
        var cachedUrl = uMon.action('cached_url', 'tracker', param);
        iFrame.attr('src', cachedUrl);
        return false;
    };

    uMon.iFrameLoaded = function() {
        var iFrame = $('#select-frame');
        var iFrameChildren = iFrame.contents().find('.selectable-element');
        var iFrameHead = iFrame.contents().find('head');
        var input = $('input#css_selector');
        iFrameHead.append('<link rel="stylesheet" href="../static/css/frame.css" type="text/css" />');

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

    $(document).ready(function() {
        var iFrameButton = $('#refresh-iframe-button'); 
        iFrameButton.click(uMon.iFrameRefresh); 
        iFrameButton.trigger('click');
    });

})(uMon, jQuery);
