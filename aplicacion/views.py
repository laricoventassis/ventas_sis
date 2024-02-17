from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from usuario.models import Usuario
from aplicacion.models import Producto, StockAlmacen

@login_required
def inicio(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'usuario':user, 'menu_inicio':"active"}
  return render(request, 'inicio.html', context)

@login_required
def caja(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'usuario':user, 'menu_caja':"active"}
  return render(request, 'caja.html', context)

@login_required
def venta(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'usuario':user, 'menu_venta':"active"}
  return render(request, 'venta.html', context)

@login_required
def almacen(request):
  user = Usuario.objects.get(username=request.user.username)
  stocks = StockAlmacen.objects.all()
  productos = Producto.objects.filter(lVigente=True)

  context = {'usuario':user, 'stocks':stocks, 'productos':productos, 'menu_almacen':"active"}
  return render(request, 'almacen.html', context)

@login_required
def perfil(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'usuario':user, 'menu_perfil':"active"}
  return render(request, 'perfil.html', context)

# ------------------------------------------------------------------------
# Guardar Stock
@login_required
def guardarstock(request):
  if request.method=="POST":
    try:
      idProducto = request.POST['idProducto']
      idEntrada = request.POST['idEntrada']
      
      producto = Producto.objects.get(id=idProducto)

      context = {'state':'success', 'msg':"Desde view "+idProducto + " => "+idEntrada}
      return JsonResponse(context)
    except Producto.DoesNotExist:
          return JsonResponse({"state":"error","cMensaje":'No se ha encontrado evidencia cargada.'})