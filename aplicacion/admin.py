from django.contrib import admin
from .models import Producto, StockAlmacen, Entrada, Venta, Caja

class productoAdmin(admin.ModelAdmin):
    list_display = ('get_producto', 'cAgrupacion', 'nPrecioDia', 'nPrecioNoche', 'nConversion', 'lVigente')

    def __str__(self):
        return self.producto
    
    def get_producto(self, obj):
        return obj
    
class stockAlmacenAdmin(admin.ModelAdmin):
    list_display = ('producto', 'nCantidad', 'cCantidad', 'dFechaMod', 'usuario')

    def __str__(self):
        return self.producto

class EntradaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'nCantidad', 'dFecha', 'usuario')

    def __str__(self):
        return self.producto
    
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'nCantidad', 'nPrecio', 'dFecha', 'usuario')

    def __str__(self):
        return self.producto
    
class CajaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nMontoApertura', 'dFechaApertura', 'cComentarioApertura', 'nMontoCierre', 'dFechaCierre', 'cComentarioCierre')

    def __str__(self):
        return self.usuario
    
admin.site.register(Producto, productoAdmin)
admin.site.register(StockAlmacen, stockAlmacenAdmin)
admin.site.register(Entrada, EntradaAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(Caja, CajaAdmin)
