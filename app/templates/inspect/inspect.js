var table_length;
var check_table = $("#check-table tbody");

$(document).ready(function() {
    var date_element = $("#date");
    date_element.datepicker(datepicker_options);
    var now = new Date();
    date_element.val(now.getDate() + "-" + (now.getMonth() + 1) + "-" + now.getFullYear());


    // if(view_only) {$(".disable").attr("disabled", true);}

    // when the save-button is clicked, convert the purchases table to a json table
    $("#submit").click(function(){
        var check_table_json = $("#check-table").tableToJSON({
            extractor: {
                0: function(cell_index, $cell) { return $cell.html()},
                1: function(cell_index, $cell) { return $cell.html()},
                3: function(cell_index, $cell) {
                    var row_id = $cell.parent()[0].id;
                    var selected = $("[name=check-" + row_id + "]:checked").val();
                    return selected},
                6: function(cell_index, $cell) { return $cell.children()[0].value},

            }
        });
        $("input[name='check-data']").val(JSON.stringify(check_table_json));
    });

    // populate the purchase table
    $.each(check_template_data, function (i, v){
        // $("#choice-" + i).val(v.device_id);
        // $("#remark-" + i).val(v.commissioning);
        var row = "<tr id='" + i + "'>" +
            "<td>" + v.index+ "</td>" +
            "<td>" + v.is_check + "</td>"
        if (v.is_check) {
            row += "<td id='name-" + i + "'></td>"
            if (view_only) {
                row += "<td id='check-" + i + "'></td>"
            } else {
                row += "<td><input type='radio' id='yes-" + i + "' name='check-" + i + "' value='yes'></td>" +
                "<td><input type='radio' id='no-" + i + "' name='check-" + i + "' value='no'></td>" +
                "<td><input type='radio' id='na-" + i + "' name='check-" + i + "' value='na' checked></td>"
            }
                row += "<td><input type='text' id='remark-" + i + "'></td>"
        } else {
            row += "<td id='name-" + i + "' style='font-size:20px;color:#ff4500;'></td>"
        }
        row += "</td></tr>"
        check_table.append(row);
        $("#check-index-" + i).val(v.index);
        $("#is-check-" + i).val(v.is_check);
        $("#name-" + i).html(v.name);
        $("#remark-" + i).val(v.remark);
        if (v.is_check) {
            if (view_only) {
                var color = v.result == 'na' ? "gray" : v.result == "yes" ? "green" : "red";
                $("#check-" + i).css("background", color);
            } else {
                $("#" + v.result + "-" + i).prop("checked", true);
            }
        }
    });

    if(view_only) {$("#check-table :input").attr("disabled", true);}
    // add_floating_menu($("#invoice_floating_menu"), purchase_table, "contextmenu", floating_menu_cb, null);
});
