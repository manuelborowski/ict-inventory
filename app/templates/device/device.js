$(document).ready(function() {
    $("#risk_analysis").parent().append(
        "<input type='button' onclick='download_file(\"risk_analysis\")' value='Download'>" +
        "<input type='button' onclick='upload_file(\"risk_analysis\")' value='Upload' hidden>"
    )
    if (!view_only) {
        // var risk_analysis_options = create_option_list(risk_analysis.choices, risk_analysis.data);
        // $("#risk_analysis").html(risk_analysis_options);

        $("input[value=Upload]").show();
        $("select").prop("disabled", false);
    }
});

    function download_file(document) {
    var file = $("#" + document).val();
    download_single_file(document, file);
}

function upload_file(document) {
    upload_files(document, true, update_document_select, document);
}

function update_document_select(opaque, file_list) {
    if (file_list.length > 0) {
        var file_name = file_list[0].name;
        var document = opaque;
        var jd = {
            opaque: document,
            action: "get-document-options",
            document: document
       }
        $.getJSON(Flask.url_for("base.ajax_request", {'jds': JSON.stringify(jd)}),
            function (jd) {
                if (jd.status) {



                    commissioning_options = create_option_list(jd.data.commissioning_options);
                    var row_id = jd.data.opaque.row_id;
                    var file_name = jd.data.opaque.file_name;
                    var commissioning_element = $("#commissioning-" + row_id);
                    commissioning_element.html(commissioning_options);
                    commissioning_element.val(file_name);
                } else {
                    alert(jd.details);
                }
            });
    }
}


