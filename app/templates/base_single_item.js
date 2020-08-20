function add_button(label, href) {
        $("#single-item-buttons").append("<a class=\"btn btn-default\" href=\"" + href + "\">" + label + "</a>");
}

function append_download_upload_button(document) {
    $("#" + document).parent().append(
        "<input type='button' onclick='download_file(\"" + document + "\")' value='Download'>" +
        "<input type='button' onclick='upload_file(\"" + document + "\")' value='Upload' hidden>"
    )
}
