var table_length;
var check_table = $("#check-table tbody");

$(document).ready(function() {
    var date_element = $("#date");
    date_element.datepicker(datepicker_options);
    if (add_only) {
        var now = new Date();
        date_element.val(now.getDate() + "-" + (now.getMonth() + 1) + "-" + now.getFullYear());
    }

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
        var row = "<tr id='" + i + "'>" +
            "<td>" + v.index+ "</td>" +
            "<td>" + v.is_check + "</td>"
        if (v.is_check) {
            row += "<td id='name-" + i + "'></td>"
            if (view_only) {
                row += "<td id='check-" + i + "'></td>"
            } else {
                var checked = "checked";
                for(var l=check_nbr_levels; l > 0; l--) {
                    var id = ["level", l, i].join("-");
                    var check = ["check", i].join("-");
                    row += "<td><input type='radio' id=" + id + " name=" + check + " value='" + l + "' " + checked + "></td>"
                    checked = "";
                }
            }
                row += "<td><input type='text' id='remark-" + i + "' size='100'></td>"
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
                $("#check-" + i).css("background", v.color);
            } else {
                var id = ["level", v.result, i].join("-");
                $("#" + id).prop("checked", true);
            }
        }
    });

    if(view_only) {$("#check-table :input").attr("disabled", true);}
});
