from django.db import models
from usuario.models import Usuario

AGRUPACION = (
  ('Cj', 'Cj'),
  ('Pqte', 'Pqte'),
  ('Und', 'Und'),
)

TURNO = (
  ('Turno Dia', 'Turno Dia'),
  ('Turno Noche', 'Turno Noche'),
)

class Producto(models.Model):
  cProducto = models.CharField('Producto', max_length=120, default='')
  cAgrupacion = models.CharField('Agrupación', choices=AGRUPACION, default="Unidad", max_length=120)
  nPrecioDia = models.DecimalField('Precio Día', max_digits=6, decimal_places=2, default=0)
  nPrecioNoche = models.DecimalField('Precio Noche', max_digits=6, decimal_places=2, default=0)
  nConversion = models.IntegerField('Conversión', default=1)
  lVigente = models.BooleanField('Vigente',default=True)

  def __str__(self):
    return self.cProducto

class StockAlmacen(models.Model):
  producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True)
  nCantidad = models.IntegerField('Cantidad', default=0)
  dFechaMod = models.DateTimeField('Última Actualización', blank=True, null=True)
  usuario = models.ForeignKey(Usuario, related_name='Usuario_Almacen', on_delete=models.CASCADE, blank=True, null=True)
  cCantidad = models.CharField('Cantidad', max_length=120, default='', blank=True)
  
  def save(self, *args, **kwargs):
    cCantidad = ''
    if self.producto.nConversion > 0:
      nEntero = int(self.nCantidad/self.producto.nConversion)
      nUnidad = self.nCantidad - nEntero*self.producto.nConversion

      cUnidad = ' y '+str(nUnidad)+' Und' if nUnidad > 0 else ''
      cCantidad = ''+str(nEntero)+' '+self.producto.cAgrupacion+cUnidad
      
    self.cCantidad = cCantidad
    super(StockAlmacen, self).save(*args, **kwargs)

class Entrada(models.Model):    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True)
    nCantidad = models.IntegerField('Cantidad', default=0)
    nPrecio = models.DecimalField('Precio', max_digits=6, decimal_places=2, default=0)
    dFecha = models.DateTimeField('Fecha', blank=True, null=True)
    usuario = models.ForeignKey(Usuario, related_name='Usuario_Entrada', on_delete=models.CASCADE, blank=True, null=True)

class Caja(models.Model):    
  usuario = models.ForeignKey(Usuario, related_name='Usuario_Caja', on_delete=models.CASCADE, blank=True, null=True)
  cTurno = models.CharField('Turno', choices=TURNO, default="Turno Dia", max_length=120)
  nMontoApertura = models.DecimalField('Monto Apertura', max_digits=6, decimal_places=2, default=0)
  dFechaApertura = models.DateTimeField('Fecha Apertura', blank=True, null=True)
  cComentarioApertura = models.CharField('Comentario Apertura', max_length=120, default='')
  nMontoCierre = models.DecimalField('Monto Cierre', max_digits=6, decimal_places=2, default=0)
  dFechaCierre = models.DateTimeField('Fecha Cierre', blank=True, null=True)
  cComentarioCierre = models.CharField('Comentario Cierre', max_length=120, default='')

class Venta(models.Model):    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True)
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, blank=True, null=True)
    nCantidad = models.IntegerField('Cantidad', default=0)
    nPrecio = models.DecimalField('Precio', max_digits=6, decimal_places=2, default=0)
    dFecha = models.DateTimeField('Fecha', blank=True, null=True)
    usuario = models.ForeignKey(Usuario, related_name='Usuario_Venta', on_delete=models.CASCADE, blank=True, null=True)
    nSubTotal = models.DecimalField('Sub Total', max_digits=6, decimal_places=2, default=0)
  
    def save(self, *args, **kwargs):
      self.nSubTotal = self.nCantidad*self.nPrecio
      super(Venta, self).save(*args, **kwargs)
  # def __str__(self):
  #   return self.usuario
