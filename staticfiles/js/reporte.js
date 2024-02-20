$(function () {
    // Historico de Ventas
    $('#dFechaCaja').pickadate({
        format: 'dd-mm-yyyy',
    });

    $('#dFechaCaja').change(function () {
        window.location.href = base_url + '/rptventas/' + $('#dFechaCaja').val() + '/';
        console.log($('#dFechaCaja').val());
    });

    $('.vercaja').click(function () {
        var $this = $(this);
        $this.attr('disabled', 'disabed');
        $.ajax({
            url: base_url + '/listaventas/',
            type: "POST",
            data: { idCaja: $(this).data('id') },
            headers: {
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            },
            dataType: 'Json',
            success: function (res) {
                $('.num_ventas').html(res.ventas.length + ' ventas');
                $('.sum_ventas').html('s/ ' + res.total);
                var html = '';
                $.each(res.ventas, function (key, venta) {
                    html += '<tr>\n\
                    <td>'+ venta.cProducto + '</td>\n\
                    <td>'+ venta.nCantidad + '</td>\n\
                    <td>'+ venta.nPrecio + '</td>\n\
                    <td>'+ venta.nSubTotal + '</td>\n\
                    </tr>';
                });

                $('#tBodyVentas').html(html);
                $this.removeAttr('disabled');
            },
            error: function (res) {
                $this.removeAttr('disabled');
                toastr.error('ocurrió un error, intente de nuevo.');
                enviando = 0;
            }
        });
    });
});