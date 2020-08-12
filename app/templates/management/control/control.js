var check_table = $("#check-table");
var check_table_length;
var standard_table_length;

$(document).ready(function() {
    var location_select = $("#floating_menu");
    var div_string = "<table><tr>"
    check_table_length = check_data.length > 0 ? check_data.length : 10;

    // build check table
    for(r = 0; r < check_table_length; r++) {check_table_add_row(r);}
    if(view_only) {$(".disable").attr("disabled", true);}

    // populate the check table when in edit mode
    $.each(check_data, function (i, v){
        $("#index-" + i).val(v.index);
        $("#active-" + i).prop("checked", v.active);
        $("#is-check-" + i).prop("checked", v.is_check);
        $("#name-" + i).val(v.name);
    });

    // when the save-button is clicked, convert the check and standard table to a json table
    $("#submit").click(function(){
        var check_table_json = check_table.tableToJSON({
            extractor: {
                0: function (cell_index, $cell) { return $cell.children()[0].value },
                1: function (cell_index, $cell) { return null },
                2: function (cell_index, $cell) { return null },
                3: function (cell_index, $cell) { return $cell.children()[0].checked },
                4: function (cell_index, $cell) { return $cell.children()[0].checked },
                5: function (cell_index, $cell) { return $cell.children()[0].value },
            }
        });
        $("input[name='check-data']").val(JSON.stringify(check_table_json));
    });

    //move row up or down
    if (!view_only) {
        $("#check-table td.move").click(function () {
            var row = $(this).closest('tr');
            if ($(this).hasClass("up")) {
                row.prev().before(row);
                var current_row_index = row.children()[0].children[0].value;
                row.children()[0].children[0].value = row.next().children()[0].children[0].value;
                row.next().children()[0].children[0].value = current_row_index;
            } else {
                row.next().after(row);
                var current_row_index = row.children()[0].children[0].value;
                row.children()[0].children[0].value = row.prev().children()[0].children[0].value;
                row.prev().children()[0].children[0].value = current_row_index;
            }
        });
    }

});

function check_table_add_row(row_id) {
    var row = "<tr id='" + row_id + "'>" +
        "<td style=\"padding:0px;\"><input type='text' id='index-" + row_id + "' size='2' value='-1' disabled></td>" +
        "<td style=\"padding:0px;\" class='move up'>&#8657;</td>" +
        "<td style=\"padding:0px;\" class='move down'>&#8659;</td>" +
        "<td><input type='checkbox' class='disable' id='active-" + row_id + "'></td>" +
        "<td><input type='checkbox' class='disable' id='is-check-" + row_id + "'></td>" +
        "<td><input type='text' class='disable' size='100%' id='name-" + row_id + "'></td>"
    row += "</td></tr>"
    check_table.append(row);
}
