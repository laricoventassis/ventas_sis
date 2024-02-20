$(function () {
    $('#input-datalist').autocomplete();

    $('#input-datalist').change(function () {
        console.log($(this).val());
        console.log($("#lista-productos option[value='" + $('#input-datalist').val() + "']").attr('id'));
    });

    $("#pagoVenta").blur(function () {
        if (this.value == '')
            this.value = 0;
        this.value = parseFloat(this.value).toFixed(2);
    });

    var enviando = 0;
    $('#formVenta').submit(function (e) {
        e.preventDefault();
        $('#btnGuardarVenta').attr('disabled', 'disabed');

        if ($('#productoVenta').val() == '') {
            toastr.error('Producto no seleccionado.');
            return;
        }

        if ($('#cantidadVenta').val() == '' || $('#cantidadVenta').val() == 0) {
            toastr.error('Cantidad no válida.');
            return;
        }

        var data = {
            productoVenta: $('#productoVenta').val(),
            cantidadVenta: $('#cantidadVenta').val(),
        };
        enviando++;
        if (enviando == 1)
            $.ajax({
                url: base_url + '/guardar_venta/',
                type: "POST",
                data: data,
                headers: {
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                },
                dataType: 'Json',
                success: function (res) {
                    if (res.estado == 'success') {
                        toastr.success(res.msg);
                        setTimeout(function () {
                            $('#btnGuardarVenta').removeAttr('disabled');
                            enviando = 0;
                            location.reload();
                        }, 1000);

                    }
                    else {
                        toastr.error(res.msg);
                    }
                },
                error: function (res) {
                    $('#btnGuardarVenta').removeAttr('disabled');
                    toastr.error('ocurrió un error, intente de nuevo.');
                    enviando = 0;
                }
            });
    });

    /* Confirmacion */
    $('.eliminar').click(function () {
        $('#idTipoOperacion').val($(this).data('tipo'));
        $('#idOperacion').val($(this).data('id'));
        $('#modalConfirm').modal("show");
    });

    $('#btnConfirmNo').click(function () {
        $('#modalConfirm').modal("hide");
    });

    $('#btnConfirmSi').click(function () {
        var element = $(this);
        element.attr('disabled', 'disabled');
        var data = {
            idTipoOperacion: $('#idTipoOperacion').val(),
            idOperacion: $('#idOperacion').val()
        }
        $.ajax({
            url: base_url + '/eliminar/',
            type: "POST",
            data: data,
            headers: {
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            },
            dataType: 'Json',
            success: function (res) {
                if (res.estado == 'success') {
                    toastr.success(res.msg);
                    setTimeout(function () {
                        location.reload();
                        element.removeAttr('disabled');
                    }, 1000);
                }
                else {
                    toastr.error(res.msg);
                    element.removeAttr('disabled');
                }
            },
            error: function (res) {
                element.removeAttr('disabled');
            }
        });
    });
});