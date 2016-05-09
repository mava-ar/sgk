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
