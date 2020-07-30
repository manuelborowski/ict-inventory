$(document).ready(function() {
    var location_select = $("#menu");
    var div_string = "<table><tr>"

    if (location_select_list.length > 0) {
        $.each(location_select_list, function (index) {
            var id = location_select_list[index][0].toString();
            var name = location_select_list[index][1];
            div_string += '<td style="padding: 5px">' +
                '<input type="radio" id="' + name + '" name="location-select-btn" value="' + id + '">\n' +
                '<label for="' + name + '">' + name + '</label><br>' +
                '</td>'
            if (((index + 1) % 20) == 0) { //table is 20 buttons wide
                div_string += '</tr><tr>';
            }
        });
        div_string += "</tr></table>";
        location_select.append(div_string);

        function disable_menu(e) {
            location_select_style.opacity = "0";
            setTimeout(function () {
                location_select_style.visibility = "hidden";
                document.removeEventListener('click', disable_menu, false);
            }, 1);
        }

        var location_select_style = document.getElementById("menu").style;
        location_select_style.opacity = "0";
        location_select_style.visibility = "hidden";
        // document.getElementById("location").addEventListener('contextmenu', function(e) {
        document.getElementById("location").addEventListener('click', function (e) {
            var posX = e.clientX;
            var posY = e.clientY;
            menu(posX, posY);
            e.preventDefault();
            e.stopPropagation();
            // row_id = $(e.target).closest('tr').prop('id');
            document.addEventListener('click', disable_menu, false);
        }, false);

        function menu(x, y) {
            location_select_style.top = "100px";
            location_select_style.left = "100px";
            location_select_style.visibility = "visible";
            location_select_style.opacity = "1";
        }

        $("input[name=location-select-btn]").click(function () {
            var location_btn = $("input[name=location-select-btn]:checked");
            var location_id = location_btn.val();
            var location_name = location_btn.prop("id");
            $("#location-id").val(location_id);
            $("#location").val(location_name);
        });
    }
});