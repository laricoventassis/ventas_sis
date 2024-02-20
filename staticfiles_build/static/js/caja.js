$(function () {
    $("#montoCaja").blur(function () {
        if (this.value == '')
            this.value = 0;
        this.value = parseFloat(this.value).toFixed(2);
    });

    $('#formCaja').submit(function (e) {
        e.preventDefault();
        if ($('#montoCaja').val() <= 0 || $('#montoCaja').val() == '') {
            toastr.error('El monto a registrar debe ser mayor a cero.');
            return;
        }

        var data = {
            turnoCaja: $('#trunoCaja').is(':checked') ? 'Turno Noche' : 'Turno Dia',
            montoCaja: $('#montoCaja').val(),
            comentarioCaja: $('#comentarioCaja').val(),
        };
        $.ajax({
            url: base_url + '/guardar_caja/',
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
                    }, 1000);

                }
                else {
                    toastr.error(res.msg);
                }
            },
            error: function (res) {
                toastr.error('ocurrió un error, intente de nuevo.');
            }
        });
    });
});