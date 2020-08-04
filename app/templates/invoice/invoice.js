var category_options;
var device_options;
var commissioning_options;
var table_length;
var purchase_table = $("#purchase_table tbody");

$(document).ready(function() {
    category_options = create_option_list(select_list.category);
    device_options = create_option_list(select_list.device);
    commissioning_options = create_option_list(select_list.commissioning);
    table_length = purchase_data.length > 0 ? purchase_data.length : 10;

    for(r = 0; r < table_length; r++) {
        table_add_row(r);
        // var row = "<tr id='tr-" + r + "'>" +
        //     "<td style=\"display: none\"><input type='text' value='-1' id='purchase-id-" + r + "'></td>" +
        //     "<td><input type='text' class='disable' size='10' id='value-" + r + "'></td>" +
        //     "<td><select class='on-change disable' id='category-" + r + "'>" + category_options + "</select></td>" +
        //     "<td><select class='disable' id='device-" + r + "'>" + device_options + "</select></td>" +
        //     "<td><select class='disable' id='commissioning-" + r + "'>" + commissioning_options + "</select></td>" +
        //     "<td><input type='button' onclick='download_commissioning_file(" + r + ");' value=\"Download\"></td>" +
        //     "</tr>"
        // purchase_table.append(row);
    }

    if(view_only) {
        $(".disable").attr("disabled", true);
    }

    $("#submit").click(function(){
        var purchase_table_json = $("#purchase_table").tableToJSON({
            extractor:  function(cell_index, $cell) {
                        return $cell.children()[0].value
                    }
        });
        $("input[name='purchase-data']").val(JSON.stringify(purchase_table_json));
    });

    $(".on-change").change(function(event){
        var element_id = this.id.split("-")[1];
        var category_id = this.value;

        var jd = {
            "category-id": category_id,
            "opaque-element-id": element_id,
            "action": "category-changed"
        }
        $.getJSON(Flask.url_for("invoice.item_ajax", {'jds' : JSON.stringify(jd)}),
            function(jd) {
                if (jd.status) {
                    var options = jd.data.device_options;
                    var select_options = create_option_list(options);
                    var element_id = jd.data.opaque_element_id;
                    var device_element = $("#device-" + element_id);
                    device_element.html(select_options);
                    if (element_id < purchase_data.length && $("#category-" + element_id).val() == purchase_data[element_id].category_id) {
                        $("#device-" + element_id).val(purchase_data[element_id].device_id);
                    }
                } else {
                    alert(jd.details);
                }
        });
    });

    // Edit an invoice
    $.each(purchase_data, function (i, v){
        $("#purchase-id-" + i).val(v.id);
        $("#value-" + i).val(v.value);
        $("#category-" + i).val(v.category_id).change();
        $("#device-" + i).val(v.device_id);
        $("#commissioning-" + i).val(v.commissioning);
    });
});

function download_commissioning_file(row_id) {
    var commissioning_file = $("#commissioning-" + row_id).val();
    $("input[name='commissioning']").val(commissioning_file);
    $("#base-single-action").prop("action", "{{ url_for('asset.download') }}").submit();
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

function table_add_row(row_id) {
    var row = "<tr id='tr-" + row_id + "'>" +
        "<td style=\"display: none\"><input type='text' value='-1' id='purchase-id-" + row_id + "'></td>" +
        "<td><input type='text' class='disable' size='10' id='value-" + row_id + "'></td>" +
        "<td><select class='on-change disable' id='category-" + row_id + "'>" + category_options + "</select></td>" +
        "<td><select class='disable' id='device-" + row_id + "'>" + device_options + "</select></td>" +
        "<td><select class='disable' id='commissioning-" + row_id + "'>" + commissioning_options + "</select></td>" +
        "<td><input type='button' onclick='download_commissioning_file(" + row_id + ");' value=\"Download\"></td>" +
        "</tr>"
    purchase_table.append(row);
}