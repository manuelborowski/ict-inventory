$(document).ready(function() {
    var location_select = $("#floating_menu");
    var div_string = "<table><tr>"

    if (location_select_list.length > 0) {
        $.each(location_select_list, function (index) {
            var id = location_select_list[index][0].toString();
            var name = location_select_list[index][1];
            div_string += '<td style="padding: 5px">' +
                '<input type="radio" id="' + name + '" name="location-select-btn" value="' + id + '">\n' +
                '<label for="' + name + '">' + name + '</label><br>' +
                '</td>'
            if (((index + 1) % 20) === 0) { //table is 20 buttons wide
                div_string += '</tr><tr>';
            }
        });
        div_string += "</tr></table>";
        location_select.append(div_string);

        var location_select_style = document.getElementById("floating_menu").style;
        document.getElementById("location").addEventListener('click', function (e) {
            location_select_style.top = "100px";
            location_select_style.left = "100px";
            location_select_style.visibility = "visible";
            location_select_style.opacity = "1";
            e.preventDefault();
            e.stopPropagation();
        }, false);

        document.addEventListener('click', function(e){
            location_select_style.opacity = "0";
            setTimeout(function () {location_select_style.visibility = "hidden";}, 1);
        }, false);

        $("input[name=location-select-btn]").click(function () {
            var location_btn = $("input[name=location-select-btn]:checked");
            var location_id = location_btn.val();
            var location_name = location_btn.prop("id");
            $("#location-id").val(location_id);
            $("#location").val(location_name);
        });
    }
});

function download_file(document) {
    var file = $("#" + document).val();
    download_single_file(document, file);
}

