//row_id is filled in with the database id of the item (asset, purchase,...) at the moment the user rightclicks on a row
var row_id
//The metadata of the floating menu.  See tables_config.py
var floating_menu = JSON.parse('{{config.floating_menu|tojson}}');
//menu_id indicates what entry is clicked in the floating menu (edit, add, ...)
function handle_floating_menu(menu_id) {
    console.log(menu_id + ' : ' + row_id);
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

    var filter_settings
    //Get content from localstorage and store in fields
    try {
        filter_settings = JSON.parse(localStorage.getItem("Filter"));
        $('#date_before').val(filter_settings['date_before']);
        $('#date_after').val(filter_settings['date_after']);
        $('#value_from').val(filter_settings['value_from']);
        $('#value_till').val(filter_settings['value_till']);
        $('#invoice').val(filter_settings['invoice']);
        $('#category').val(filter_settings['category']);
        $('#status').val(filter_settings['status']);
        $('#device').val(filter_settings['device']);
        $('#supplier').val(filter_settings['supplier']);
        $('#room').val(filter_settings['room']);
        $('#purchase_id').val(filter_settings['purchase_id']);
    } catch (err) {
    }

    //The filter button of the filter is pushed
    $('#filter').click(function() {
        //Store filter in localstorage
        filter_settings = {"date_before" : $('#date_before').val(),
                   "date_after" : $('#date_after').val(),
                   "value_from" : $('#value_from').val(),
                   "value_till" : $('#value_till').val(),
                   "invoice" : $('#invoice').val(),
                   "category" : $('#category').val(),
                   "status" : $('#status').val(),
                   "device" : $('#device').val(),
                   "supplier" : $('#supplier').val(),
                   "room" : $('#room').val(),
                   "purchase_id" : $('#purchase_id').val(),
        }
        //alert(JSON.stringify(filter_settings));
        localStorage.setItem("Filter", JSON.stringify(filter_settings));
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


    //right click on an item in the table.  A menu pops up to execute an action on the selected row/item
    var i = document.getElementById("menu").style;
    document.getElementById("datatable").addEventListener('contextmenu', function(e) {
        var posX = e.clientX;
        var posY = e.clientY;
        menu(posX, posY);
        e.preventDefault();
        row_id = $(e.target).closest('tr').prop('id');
    }, false);
    document.addEventListener('click', function(e) {
        i.opacity = "0";
        setTimeout(function() {i.visibility = "hidden";}, 1);
    }, false);

    // Get column index when right clicking on a cell
    //$('#datatable tbody').on( 'contextmenu', 'td', function () {
    //    column_id = table.cell( this ).index().column;
    //    console.log( 'Clicked on cell in visible column: '+column_id );
    //});


    function menu(x, y) {
      i.top = y + "px";
      i.left = x + "px";
      i.visibility = "visible";
      i.opacity = "1";
    }
});
