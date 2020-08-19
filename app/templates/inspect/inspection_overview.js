var table_length;
var overview_table_header = $("#overview-table thead");
var overview_table = $("#overview-table tbody");

$(document).ready(function() {

    if(overview_data) {
        var header = "<tr><th>Inspectie item</th>";
        var rows = [];
        $.each(overview_data.template_items, function(i, v){
            var red_style = v.is_check ? "" : "font-size:20px;color:#ff4500;";
            rows[i] = "<tr><td style='" + red_style + "'>" + v.name + "</td>"
        });

        $.each(overview_data.all_checks, function(i_nu, all_check){
            var title = all_check.date.replace(/<br>/g, "-") + "\n" + all_check.inspector + "\n" + all_check.info;
            header += "<th style='text-align: center;' title='" + title + "'>" + all_check.date + "</th>"
            $.each(all_check.checks, function(i, check){
                if (check.is_check) {
                    var remark = check.remark != '' ? "O" : "";
                    rows[i] += "<td style='background:" + check.color + ";text-align:center' title='" + check.remark + "'>" + remark + "</td>"
                }
            });
        });
        header += "</tr>"
        var body = '';
        $.each(overview_data.template_items, function(i, v){
           body += rows[i] + "</tr>"
        });
    }
    overview_table_header.append(header);
    overview_table.append(body)

    // Show the legend
    var level = overview_data.levels_info.length;
    if (level > 0) {
        $.each(overview_data.levels_info, function(i, v) {
            $("#legend").append("<div style='display: flex;'>" +
                "<div style='width:100px;margin:5px;color: black;font-size:20px;text-align:center;background:" + v.color +  ";'>" + level +"</div>" +
                "<div style='margin:10px;color: black;font-size:15px;text-align:center'>" + v.info + "</div>" +
                "</div>")
            level--;
        });
    }

});
