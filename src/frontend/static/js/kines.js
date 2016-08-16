/*
* Método útiles de la app.
* */

function addFileInputIntoDiv(count, div){
    // Function that add a input file into a div.
    // count is a input hidden with a index and attr 'field-name' with the name of field of form.
    // div is a div element
    var fieldname = $(count).attr('field_name');
    var idx = parseInt($(count).val()) + 1;
    var name = "form-"+idx+"-"+fieldname;
    $(div).append("<div class='inline_formset'>" +
        "<div class='input-group'>" +
            "<span class='input-group-btn'>" +
                "<span class='btn btn-primary btn-file'>" +
                    "Seleccionar archivo…" +
                    "<input id='id_"+name+"' name='"+name+"' type='file' />" +
                "</span>" +
            "</span>" +
            "<input type='text' class='form-control' id='id_"+name+"-name' readonly=''>" +
            "<span class='input-group-addon btn remove-input-file' rel='#id_"+name+"'>" +
                "<span class='glyphicon glyphicon-trash'></span>" +
            "</span>" +
        "</div>" +
    "</div>");
    $(count).val(idx);
    // update the TOTAL forms
    $("#id_form-TOTAL_FORMS").val(idx+1);
    // remove the input file value
    $(div).find("span.remove-input-file").each(function(){
        $(this).click(function() {
            $(""+$(this).attr('rel')).val('');
            $(""+$(this).attr('rel')+'-name').val('');
        });
    });
}

function scroll2Up(){
    $('html,body').animate({'scrollTop' : 0},700, 'swing');
    return false;
}

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
var showConfirm = function(title, message, callback_yes, callback_no, btnClass) {
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