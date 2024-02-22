from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from usuario.models import Usuario
from aplicacion.models import Producto, StockAlmacen, Entrada, Caja, Venta

@login_required
def producto(request):
  if request.method=="POST":
    nombre = request.POST.get('producto', '')
    try:
      caja = Caja.objects.get(nMontoCierre=0)
    except Caja.DoesNotExist:
      return JsonResponse({'estado':'error', 'msg':"Caja no encontrado."})

    try:
      producto = Producto.objects.get(cProducto=nombre)
      pruducto_ = [
        {
          'producto':producto.cProducto, 
          'precio': producto.nPrecioDia if caja.cTurno=='Turno Dia' else producto.nPrecioNoche,
          'stock': producto.stockalmacen_set.first().nCantidad if producto.stockalmacen_set.count() > 0 else 0
        }]
      return JsonResponse({'estado':'success', 'msg':"", 'producto':pruducto_})
    except Producto.DoesNotExist:
      return JsonResponse({'estado':'error', 'msg':"Producto no encontrado."})
  else:
    return JsonResponse({'estado':'error', 'msg':"Método no válido."})

@login_required
def venta(request):
  user = Usuario.objects.get(username=request.user.username)
  productos = Producto.objects.filter(lVigente=1)
  try:
     caja = Caja.objects.get(nMontoCierre=0)
     iniciado = 1
     ventas = Venta.objects.filter(caja=caja).order_by('-dFecha')
     #sumar total venta
     total = obtener_total(ventas)
     context = {'usuario':user, 'menu_caja':"active", 'productos':productos,
                'iniciado':iniciado, 'caja':caja, 'ventas':ventas, 'total':total}
  except Caja.DoesNotExist:
     iniciado = 0
     context = {'usuario':user, 'menu_caja':"active", 'iniciado':iniciado, 'productos':productos,
                'ventas':[], 'total':0}
  return render(request, 'venta.html', context)

@login_required
def almacen(request, fecha=''):
  if not request.user.is_superuser:
    return JsonResponse({"estado":"error","msg":'No tiene privilegios de administrador para esta acción.'})
  fecha2=datetime.now()
  if fecha != '':
    fecha2 = datetime.strptime(fecha, "%d-%m-%Y").date()
  user = Usuario.objects.get(username=request.user.username)
  stocks = StockAlmacen.objects.all()
  productos = Producto.objects.filter(lVigente=True)
  # entradas = Entrada.objects.filter(dFecha__year=fecha2.year, dFecha__month=fecha2.month, 
                                    # dFecha__day=fecha2.day).order_by('-dFecha')

  # context = {'usuario':user, 'stocks':stocks, 'productos':productos, 
  #            'menu_almacen':"active", 'entradas':entradas, 'fecha':fecha}
  context = {'usuario':user, 'stocks':stocks,'productos':productos,}
  return render(request, 'almacen.html', context)

@login_required
def perfil(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'usuario':user, 'menu_perfil':"active"}
  return render(request, 'perfil.html', context)

# ------------------------------------------------------------------------
# Guardar Stock
@login_required
def guardar_stock(request):
  if not request.user.is_superuser:
    return JsonResponse({"estado":"error","msg":'No tiene privilegios de administrador para esta acción.'})
    
  if request.method=="POST":
    idProducto = request.POST.get('idProducto', 0)
    idEntrada = request.POST.get('idEntrada', 0)
    nCantidad = int(request.POST.get('nCantidad', 0))
    nUnidad = int(request.POST.get('nUnidad', 0))
    try:      
      producto = Producto.objects.get(id=idProducto)
      nStockAgregar = int(nCantidad)*int(producto.nConversion) + int(nUnidad)
    except Producto.DoesNotExist:
          return JsonResponse({"estado":"error","msg":'No se ha encontrado el producto a actualizar.'})

    agregar_stock(producto, nStockAgregar, request.user)
    
    #Guardado de Entrada Historico Detalle
    entrada = Entrada()
    entrada.producto = producto
    entrada.nCantidad = nStockAgregar
    entrada.nPrecio = 0
    entrada.dFecha = datetime.now()
    entrada.usuario = request.user
    entrada.save()

    context = {'estado':'success', 'msg':"Se actualizó exitosamente."}
    return JsonResponse(context)
  else:
    context = {'estado':'error', 'msg':"Método no válido."}
    return JsonResponse(context)

# Guardar Stock
@login_required
def guardar_caja(request):
  if request.method=="POST":
    try:
       caja = Caja.objects.get(nMontoCierre=0)
       caja.nMontoCierre = request.POST.get('montoCaja', 0)
       caja.cComentarioCierre = request.POST.get('comentarioCaja', '')
       caja.dFechaCierre = datetime.now()
       caja.save()
    except Caja.DoesNotExist:
       caja = Caja()
       caja.usuario = request.user
       caja.cTurno = request.POST.get('turnoCaja', 'Turno Dia')
       caja.nMontoApertura = request.POST.get('montoCaja', 0)
       caja.cComentarioApertura = request.POST.get('comentarioCaja', '')
       caja.dFechaApertura = datetime.now()
       caja.save()

    context = {'estado':'success', 'msg':"Se registró exitosamente."}
    return JsonResponse(context)
  else:
    context = {'estado':'error', 'msg':"Método no válido."}
    return JsonResponse(context)

# Guardar Venta
@login_required
def guardar_venta(request):
  if request.method=="POST":
    nCantidad = int(request.POST.get('cantidadVenta', 0))
    try:
       caja = Caja.objects.get(nMontoCierre=0)
    except Caja.DoesNotExist:
      return JsonResponse({'estado':'error', 'msg':"No se ha iniciado caja."})
    
    try:
       producto = Producto.objects.get(cProducto=request.POST.get('productoVenta',''))
       if producto.stockalmacen_set.count() == 0:
          return JsonResponse({'estado':'error', 'msg':"Stock insuficiente para atender."})
       if producto.stockalmacen_set.first().nCantidad < nCantidad:
          return JsonResponse({'estado':'error', 'msg':"Stock insuficiente para atender."})
    except Caja.DoesNotExist:
      return JsonResponse({'estado':'error', 'msg':"No se ha encontrado el producto."})
    
    venta = Venta()
    venta.producto = producto
    venta.caja = caja
    venta.nCantidad = nCantidad
    venta.nPrecio = producto.nPrecioDia if caja.cTurno=='Turno Dia' else producto.nPrecioNoche
    venta.dFecha = datetime.now()
    venta.usuario = request.user
    venta.save()

    agregar_stock(producto, nCantidad*-1, request.user)

    context = {'estado':'success', 'msg':"Se registró exitosamente."}
    return JsonResponse(context)
  else:
    context = {'estado':'error', 'msg':"Método no válido."}
    return JsonResponse(context)

# Guardar Venta
@login_required
def eliminar(request):
  if request.method=="POST":
    tipoOpe = request.POST.get('idTipoOperacion', '')
    idOperacion = int(request.POST.get('idOperacion', 0))

    if tipoOpe == 'stock' and not request.user.is_superuser:
      return JsonResponse({"estado":"error","msg":'No tiene privilegios de administrador para esta acción.'})

    if tipoOpe == 'stock':
      try:
        operacion = Entrada.objects.get(id=idOperacion)
        nCantidad = operacion.nCantidad*-1
      except StockAlmacen.DoesNotExist:
        return JsonResponse({'estado':'error', 'msg':"No se encontró la operación."})

    if tipoOpe == 'venta':
      try:
        operacion = Venta.objects.get(id=idOperacion)
        nCantidad = operacion.nCantidad
      except Venta.DoesNotExist:
        return JsonResponse({'estado':'error', 'msg':"No se encontró la operación."})

    operacion.delete()
    agregar_stock(operacion.producto, nCantidad, request.user)

    context = {'estado':'success', 'msg':"Se registró exitosamente."}
    return JsonResponse(context)
  else:
    context = {'estado':'error', 'msg':"Método no válido."}
    return JsonResponse(context)

# Reporte de cajas y ventas
@login_required
def rptventas(request, fecha=''):
  if not request.user.is_superuser:
      return JsonResponse({"estado":"error","msg":'No tiene privilegios de administrador para esta acción.'})
  fecha2=datetime.now()
  if fecha != '':
    fecha2 = datetime.strptime(fecha, "%d-%m-%Y").date()
  try:
      cajas = Caja.objects.filter(
        dFechaApertura__year=fecha2.year, dFechaApertura__month=fecha2.month, dFechaApertura__day=fecha2.day
      ).order_by('-dFechaApertura')
  except Caja.DoesNotExist:
    cajas = []
  
  context = {'usuario':request.user, 'cajas':cajas, 'fecha':fecha}
  return render(request, 'rptventas.html', context)

# Lista de Ventas por Caja
@login_required
def listaventas(request):
  if not request.user.is_superuser:
      return JsonResponse({"estado":"error","msg":'No tiene privilegios de administrador para esta acción.'})
  if request.method=="POST":
    idCaja = int(request.POST.get('idCaja', 0))
    try:
      caja = Caja.objects.get(id=idCaja)
    except Caja.DoesNotExist:
      return JsonResponse({'estado':'error', 'msg':"No se encontró la caja."})
    
    total = 0
    ventas_all = []
    ventas = Venta.objects.filter(caja=caja)
    if ventas.count()>0:
      for venta in ventas:
        v = {
              'cProducto': venta.producto.cProducto,
              'nCantidad': venta.nCantidad,
              'nPrecio': venta.nPrecio,
              'nSubTotal': venta.nSubTotal
            }
        ventas_all.append(v)
        total += venta.nSubTotal

    return JsonResponse({'ventas':ventas_all, 'total':total})
  else:
    context = {'estado':'error', 'msg':"Método no válido."}
    return JsonResponse(context)

# funciones
def agregar_stock(producto, nStockAgregar, usuario):
  try:
      stock = StockAlmacen.objects.get(producto=producto)
      #Actualizar Stock
      stock.nCantidad += nStockAgregar
      stock.save()
  except StockAlmacen.DoesNotExist:
        stock = StockAlmacen()
        stock.producto = producto
        stock.nCantidad = nStockAgregar
        stock.dFechaMod = datetime.now()
        stock.usuario = usuario
        stock.save()

def obtener_total(ventas):
  total = 0
  for venta in ventas:
    total += venta.nSubTotal
  return total
