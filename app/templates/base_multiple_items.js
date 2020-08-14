var filter_settings = {}
$(document).ready(function() {
    //The clear button of the filter is pushed
    $('#clear').click(function() {
        $('.filter').val('');
        $('#category').val('');
        $('#status').val('');
        $('#device').val('');
        $('#supplier').val('');
        //emulate click on trigger button
        $('#filter').trigger('click');
    });

    $.each(default_filter_values, function(k, v){
        try {
            localStorage.setItem(k, JSON.stringify(v));
        } catch (err) {
            //let is pass
        }
    });

    $.each(filter, function (i, v){
        try {
            var value = JSON.parse(localStorage.getItem(v));
            $("#" + v).val(value);
            filter_settings[v] = value;
        } catch (err) {
            //let is pass
        }
    });

    $("#filter").click(function() {
        $.each(filter, function (i, v) {
            try {
                var value = $("#" + v).val();
                localStorage.setItem(v, JSON.stringify(value));
                filter_settings[v] = value;
            } catch (err) {
                //let is pass
            }
        });
        table.ajax.reload();
    });

    //Configure datatable.
    var table = $('#datatable').DataTable({
       serverSide: true,
       stateSave: true,
       dom : 'lfiptp',
       ajax: {
           url: "{{ url_for(config.subject + '.source_data') }}",
           type: 'POST',
           data : function (d) {
               return $.extend( {}, d, filter_settings);
           }
       },
       pagingType: "full_numbers",
       lengthMenu: [50, 100, 200],
       "columns": datatables_columns,
       "language" : {
        /*"url" : "static/DataTables/nl_nl.lang"*/
        "url" : "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Dutch.json"
      }
    });

    add_floating_menu($("#floating_menu"), $('#datatable'), 'contextmenu', floating_menu_cb, null);

     //flash messages, if required
     table.on( 'draw', function () {
        var j = table.ajax.json();
        $("#flash-list").html('');
        if(j.flash && j.flash.length) {
            var flash_string="";
            for(let s of j.flash) {
                flash_string += "<div class=\"alert alert-info\" role=\"alert\">" + s +"</div>";
            }
                $("#flash-list").html(flash_string);
        }
     });

     // document.addEventListener("keyup", function(e){
     //     if (e.keyCode === 13) {
     //         $("#export").blur();
     //         $("#filter").focus().click();
     //     }
     // });
    if (filter.includes("date_after")) {
        var date_after_element = $("#date_after");
        date_after_element.datepicker(datepicker_options);
    }
    if (filter.includes("date_before")) {
        var date_before_element = $("#date_before");
        date_before_element.datepicker(datepicker_options);
    }

});

var row_id;
function floating_menu_cb(e, opaque) {
        row_id = $(e.target).closest('tr').prop('id');
}

var floating_menu = JSON.parse('{{config.floating_menu[current_user.get_level]|tojson}}');
function handle_floating_menu(menu_id) {
    for(var i=0; i < floating_menu.length; i++) {
        if(floating_menu[i].menu_id == menu_id) {
            if(floating_menu[i].flags.includes('confirm_before_delete')) {
                confirm_before_delete(row_id);
            } else if(floating_menu[i].flags.includes('id_required')) {
                window.location.href=Flask.url_for('{{config.subject}}.' + floating_menu[i].route, {'id':row_id});
            } else {
                window.location.href=Flask.url_for('{{config.subject}}.' + floating_menu[i].route);
            }
        }
    }
}

//Before removing an entry, a confirm-box is shown.
function confirm_before_delete(id) {
    var message = "Bent u zeker dat u dit item wil verwijderen?";
    if ('{{ config.delete_message }}') {message='{{ config.delete_message }}';}
    bootbox.confirm(message, function(result) {
        if (result) {
            window.location.href = Flask.url_for('{{config.subject}}' + ".delete", {'id' : id})
        }
    });
}


