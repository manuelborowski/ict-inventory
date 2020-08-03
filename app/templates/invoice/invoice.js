$(document).ready(function() {
    var purchase_table = $("#purchase_table tbody");

    var category_options = create_option_list(select_list.category);
    var device_options = create_option_list(select_list.device);
    var commissioning_options = create_option_list(select_list.commissioning);

    for(r = 0; r < 10; r++) {
        var row = "<tr id='tr-'" + r + ">" +
            "<td style=\"display: none\"><input type='text' value='-1' id='purchase-id-" + r + "'></td>" +
            "<td><input type='text' size='10' id='value-" + r + "'></td>" +
            "<td><select class='on-change' id='category-" + r + "'>" + category_options + "</select></td>" +
            "<td><select id='device-" + r + "'>" + device_options + "</select></td>" +
            "<td><select id='commissioning-" + r + "'>" + commissioning_options + "</select></td>" +
            "</tr>"
        purchase_table.append(row);
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
        console.log(event);
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
