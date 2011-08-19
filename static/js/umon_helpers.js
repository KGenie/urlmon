var uMon = uMon || {};

(function (uMon, $) {

    uMon.action = function(name, controller, parameters) {
        var appDirectory = '';
        if (uMon.globals.appDirectory) {
            appDirectory = uMon.globals.appDirectory;
        }

        if (parameters) {
            parameters = '?' + $.param(parameters);
        }
        else {
            parameters = '';
        }

        return appDirectory + '/' + controller + '/' + name + parameters;
    };

})(uMon, jQuery);
