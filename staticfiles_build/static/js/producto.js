$(function () {
    $('.producto').click(function () {
        openModalStock($(this).parent());
    });

    $('.agregar').click(function () {
        openModalStock($(this).parent().parent().parent());
    });

    function openModalStock(element) {
        $('#idProducto').val(0);
        $('#idEntrada').val(0);
        $('#idProducto').val(element.data('id'));
        $('#nombreProducto').val(element.data('nombre')).next().addClass('active');
        $('#cantidadGral').val('').next().removeClass('active').html('Cantidad en ' + element.data('und') + '<b>(' + element.data('conversion') + ')</b>');
        $('#cantidadUnd').val('').next().removeClass('active');

        element.data('conversion') == '1' ? $('#cantidadGral').parent().hide() : $('#cantidadGral').parent().show();
        $("#modalContactForm").modal("show");
    };

    $('#formGuardarStock').submit(function (e) {
        e.preventDefault();
        if (($('#cantidadGral').val() == '0' || $('#cantidadGral').val() == '') && ($('#cantidadUnd').val() == '0' || $('#cantidadUnd').val() == '')) {
            toastr.error('Debe ingresar al menos una de las cantidades.');
            return;
        }

        var data = {
            idEntrada: $('#idEntrada').val(),
            idProducto: $('#idProducto').val(),
            nCantidad: $('#cantidadGral').val() == '' ? 0 : $('#cantidadGral').val(),
            nUnidad: $('#cantidadUnd').val() == '' ? 0 : $('#cantidadUnd').val()
        };
        $.ajax({
            url: base_url + '/guardar_stock/',
            type: "POST",
            data: data,
            headers: {
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            },
            dataType: 'Json',
            // contentType: "application/json",
            success: function (res) {
                if (res.estado == 'success') {
                    toastr.success(res.msg);
                    setTimeout(function () {
                        location.reload();
                    }, 1000);

                }
                else {
                    toastr.error(res.msg);
                }
                console.log(res);
            },
            error: function (res) {
                toastr.error('ocurrió un error, intente de nuevo.');
            }
        });
    });

    // Historico de entradas
    $('#dFechaStock').pickadate({
        format: 'dd-mm-yyyy',
    });

    $('#dFechaStock').change(function () {
        window.location.href = base_url + '/almacen/' + $('#dFechaStock').val() + '/';
        console.log($('#dFechaStock').val());
    });
});