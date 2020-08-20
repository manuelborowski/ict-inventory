$(document).ready(function() {
    append_download_upload_button('risk_analysis');
    append_download_upload_button('manual');
    append_download_upload_button('safety_information');
    append_download_upload_button('photo');

    if (!view_only) {
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
       $("#" + document).append("<option value='" + file_name + "' selected>" + file_name + "</\option>");
    }
}

