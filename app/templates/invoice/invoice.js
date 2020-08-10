var category_options;
var device_options;
var commissioning_options;
var table_length;
var purchase_table = $("#purchase_table tbody");

$(document).ready(function() {
    // Create default options
    category_options = create_option_list(select_list.category);
    commissioning_options = create_option_list(select_list.commissioning);
    table_length = purchase_data.length > 0 ? purchase_data.length : 10;

    var since_element = $("#since");
    since_element.datepicker(datepicker_options);
    var now = new Date();
    since_element.val(now.getDate() + "-" + (now.getMonth() + 1) + "-" + now.getFullYear());

    // build purchase table
    for(r = 0; r < table_length; r++) {
        table_add_row(r);
    }

    if(view_only) {$(".disable").attr("disabled", true);}

    // when the save-button is clicked, convert the purchases table to a json table
    $("#submit").click(function(){
        var purchase_table_json = $("#purchase_table").tableToJSON({
            extractor:  function(cell_index, $cell) {
                        return $cell.children()[0].value
                    }
        });
        $("input[name='purchase-data']").val(JSON.stringify(purchase_table_json));
    });

    // populate the purchase table when in edit mode
    $.each(purchase_data, function (i, v){
        $("#purchase-" + i).html(v.id);
        $("#value-" + i).val(v.value);
        $("#category-" + i).val(v.category_id).change();
        $("#device-" + i).val(v.device_id);
        $("#commissioning-" + i).val(v.commissioning);
    });

    add_floating_menu($("#invoice_floating_menu"), purchase_table, "contextmenu", floating_menu_cb, null);
});

//download the current commissioning file
function download_commissioning_file(row_id) {
    var commissioning_file = $("#commissioning-" + row_id).val();
    download_single_file("commissioning", commissioning_file);
}

//upload a new commissioning file
function upload_commissioning_file(row_id) {
    upload_files("commissioning", true, update_commissioning_select, row_id);
}

//when a new commissioning is uploaded, renew the commissioning-option-list and select the new commissioning file
function update_commissioning_select(opaque, file_list) {
    console.log(opaque, file_list);
    if (file_list.length > 0) {
        var file_name = file_list[0].name;
    }
    var row_id = opaque;
    var jd = {
        "opaque": {row_id: row_id, file_name: file_name},
        "action": "get-commissioning-list"
    }
    $.getJSON(Flask.url_for("base.ajax_request", {'jds' : JSON.stringify(jd)}),
        function(jd) {
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

function table_add_row(row_id) {
    var row = "<tr id='" + row_id + "'>" +
        "<td id='purchase-" + row_id + "'>-1</td>" +
        "<td><input type='text' class='disable' size='10' id='value-" + row_id + "'></td>" +
        "<td><select class='on-change-category disable' id='category-" + row_id + "'>" + category_options + "</select></td>" +
        "<td><select class='disable' id='device-" + row_id + "'>" + device_options + "</select></td>" +
        "<td><select class='disable' id='commissioning-" + row_id + "'>" + commissioning_options + "</select>" +
        "<input type='button' onclick='download_commissioning_file(" + row_id + ");' value=\"Download\">"
    if (!view_only) {
        row += "<input type='button' onclick='upload_commissioning_file(" + row_id + ");' value=\"Upload\">"
    }
    row += "</td></tr>"
    purchase_table.append(row);
    $("#category-" + row_id).change(category_changed_event);
}

// when the category is changed, get a new device-list, filtered on the category.  This
// should make it easier to select a device
function category_changed_event(event){
    var element_id = this.id.split("-")[1];
    var category_id = this.value;
    var jd = {
        "category-id": category_id,
        "opaque": element_id,
        "action": "get-device-list"
    }
    $.getJSON(Flask.url_for("device.ajax_request", {'jds' : JSON.stringify(jd)}),
        function(jd) {
            if (jd.status) {
                var options = jd.data.device_options;
                var select_options = create_option_list(options);
                var element_id = jd.data.opaque;
                var device_element = $("#device-" + element_id);
                device_element.html(select_options);
                if (element_id < purchase_data.length && $("#category-" + element_id).val() == purchase_data[element_id].category_id) {
                    $("#device-" + element_id).val(purchase_data[element_id].device_id);
                }
            } else {
                alert(jd.details);
            }
    });
}

var row_id;
function floating_menu_cb(e, opaque) {
        row_id = $(e.target).closest('tr').prop('id');
}

function add_asset_with_purchase_id() {
    var purchase_id = $("#purchase-" + row_id).html();
    window.location.href = Flask.url_for("invoice.add_asset", {purchase_id: purchase_id});
}

function view_assets_with_purchase_id() {
    var purchase_id = $("#purchase-" + row_id).html();
    window.location.href = Flask.url_for("asset.assets", {purchase_id: purchase_id});
}