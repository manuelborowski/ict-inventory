$(document).ready(function(){
    //log out automatically after 10 minutes
    var idleTime = 0;
    setInterval(function(){
        idleTime = idleTime + 1;
        if (idleTime > 9) { // 10 minutes
            window.location.href=Flask.url_for('auth.logout');
        }
    }, 60000); // 1 minute
    $(this).mousemove(function (e) {idleTime = 0;});
    $(this).keypress(function (e) {idleTime = 0;});

    //when the file selection popup closes, upload the files via an ajax call
    var file_picker = $("#file-picker");
    file_picker.on("change", function() {
        upload_files_ajax();
    });
});

function flash_messages(list) {
    for (var i=0; i<list.length; i++){
        var message = list[i];
        bootbox.alert(message);
    }
}

function busy_indication_on() {
  document.getElementsByClassName("loader")[0].style.display = "block";
}

function busy_indication_off() {
  document.getElementsByClassName("loader")[0].style.display = "none";
}

var container = $('.bootstrap-iso form').length > 0 ? $('.bootstrap-iso form').parent() : "body";
var datepicker_options = {
    language: 'nl',
    container: container,
    todayHighlight: true,
    autoclose: true,
    orientation: "auto",
    format: 'dd-mm-yyyy',
};

function download_single_file(document_type, file_name) {
    var download_form = $("#download-form")
    var href = Flask.url_for("base.download", {document: document_type, file: file_name});
    download_form.prop("action", href);
    $("#download-submit").click();
}

// uploading files is asynchronously via an ajax call.  It is possible to install a callback function that is
// invoked when the ajax call is finished
// the callback must implement 2 parameters: an opaque parameter and the list of files
var upload_files_cb = {
    cb: null,
    opaque: null,
}

function upload_files(document_type, single_file=false, cb=null, opaque=null) {
    var upload_form = $("#upload-form");
    var file_picker = $("#file-picker");
    $("#document-type").val(document_type);
    var href = Flask.url_for("base.upload", {document: document_type, url: encodeURIComponent(encodeURIComponent(window.location.href))});
    upload_form.prop("action", href);
    if(cb) {
        upload_files_cb.cb = cb;
        upload_files_cb.opaque = opaque;
    }
    file_picker.prop("multiple", !single_file);
    file_picker.click();
}

// called when the file selection popup is closed
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
                    upload_files_cb.cb(upload_files_cb.opaque, $("#file-picker")[0].files);
                    upload_files_cb.cb = null;
                }
            } else {
                alert(data.details);
            }
        },
      })
    });
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

var floating_menu_cb = {
    cb: null,
    opaque: null
}
var floating_menu_style;
function add_floating_menu($menu_element, $trigger_element, trigger_type, callback, opaque) {
    if (callback) {
        floating_menu_cb.cb = callback;
        floating_menu_cb.opaque = opaque;
    }
    floating_menu_style = $menu_element[0].style;
    $trigger_element.on(trigger_type, function (e) {
        floating_menu_style.top = e.clientY + "px";
        floating_menu_style.left = e.clientX + "px";
        floating_menu_style.visibility = "visible";
        floating_menu_style.opacity = "1";
        e.preventDefault();
        e.stopPropagation();
        if (floating_menu_cb.cb) {floating_menu_cb.cb(e, floating_menu_cb.opaque)}
    });

    document.addEventListener('click', function (e) {
        floating_menu_style.opacity = "0";
        setTimeout(function () {floating_menu_style.visibility = "hidden";}, 1);
    }, false);
}
