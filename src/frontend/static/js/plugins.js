// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeline', 'timelineEnd', 'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());

// Place any jQuery/helper plugins in here.
showConfirm = function(title, message, callback_yes, callback_no, btnClass) {
    if (btnClass == undefined){
        btnClass = 'btn-success';
    }
    BootstrapDialog.confirm({
        title: title,
        message: message,
        type: BootstrapDialog.TYPE_DEFAULT,
        closable: true, // <-- Default value is false
        draggable: true, // <-- Default value is false
        btnCancelLabel: 'Cancelar', // <-- Default value is 'Cancel',
        btnOKLabel: 'Continuar', // <-- Default value is 'OK',
        btnOKClass: btnClass,
        callback: function (result) {
            // result will be true if button was click, while it will be false if users close the dialog directly.
            if (result) {
                try {
                    callback_yes();
                } catch (e) {
                    console.log(e);
                }
            } else {
                try {
                    if (callback_no != undefined)
                        callback_no();
                } catch (e) {
                    console.log(e);
                }

            }
        }
    });
};


function get_today() {
  function pad(s) { return (s < 10) ? '0' + s : s; }
  var d = new Date();
  return [pad(d.getDate()), pad(d.getMonth()+1), d.getFullYear()].join('/');
}