$(function () {
    $('.producto').click(function () {
        //.addClass('active')
        $('#idProducto').val(0);
        $('#idEntrada').val(0);
        $('#idProducto').val($(this).data('id'));
        $('#nombreProducto').val($(this).data('nombre')).next().addClass('active');
        $('#cantidadGral').val('').next().removeClass('active').html('Cantidad en ' + $(this).data('und') + '<b>(' + $(this).data('conversion') + ')</b>');
        $('#cantidadUnd').val('').next().removeClass('active');

        $(this).data('conversion') == '1' ? $('#cantidadGral').parent().hide() : $('#cantidadGral').parent().show();

        $("#modalContactForm").modal("show");
    });

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
            nUnidad: $('#cantidadUnd').val() == '' ? 0 : $('#cantidadUnd').val(),
            CSRF: $('#cantidadUnd').val(),
        };

        $.ajax({
            url: base_url + '/guardarstock/',
            type: "POST",
            data: data,
            dataType: 'json',
            contentType: "application/json",
            success: function (res) {
                console.log(res);
                toastr.success('Se ha registrado exitosamente.');
            },
            error: function (res) {
                console.log(res);
                console.log('ocurrio errro');
                toastr.error('ocurrió un error, intente de nuevo.');
            }
        });
    });


});