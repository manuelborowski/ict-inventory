$(document).ready(function() {
    var file_picker = $("#file-picker");
    file_picker.on("change", function() {
        console.log(file_picker.prop("multiple"));
        // $("#upload-submit").click();
        upload_files_ajax();
    });
});

function download_single_file(document_type, file_name) {
    var download_form = $("#download-form")
    var href = Flask.url_for("base.download", {document: document_type, file: file_name});
    download_form.prop("action", href);
    $("#download-submit").click();
}

var upload_files_cb = {
    cb: null,
    cb_opaque: null,
}

function upload_files(document_type, single_file=false, cb=null, cb_opaque=null) {
    var upload_form = $("#upload-form");
    var file_picker = $("#file-picker");
    $("#document-type").val(document_type);
    var href = Flask.url_for("base.upload", {document: document_type, url: encodeURIComponent(encodeURIComponent(window.location.href))});
    upload_form.prop("action", href);
    if(cb) {
        upload_files_cb.cb = cb;
        upload_files_cb.cb_opaque = cb_opaque;
    }
    file_picker.prop("multiple", !single_file);
    file_picker.click();
}


function create_option_list(list) {
    var out = []
    $.each(list, function (i, v){
        if (v[0] == 'disabled') {
            out += "<option value='" + v[0] + "' disabled>" + v[1] + "</option>";
        } else {
            out += "<option value='" + v[0] + "'>" + v[1] + "</option>";
        }
    });
    return out;
}

function upload_files_ajax() {
    var form_data = new FormData( $("#upload-form")[0]);
    $(function() {
    $.ajax({
        type: 'POST',
        url:  Flask.url_for("base.upload_ajax"),
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            if (data.status) {
                if (upload_files_cb.cb) {
                    upload_files_cb.cb(upload_files_cb.cb_opaque, $("#file-picker")[0].files);
                    upload_files_cb.cb = null;
                }
            }
            console.log('Success!');
        },
      })
    });
}

