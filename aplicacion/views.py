from django.shortcuts import render
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
def mostrador(request):
  user = Usuario.objects.get(username=request.user.username)
  productos = Producto.objects.all().filter(lVigente=True)
  stocks = StockAlmacen.objects.all()

  context = {'usuario':user, 'productos':productos, 'stocks':stocks, 'menu_mostrador':"active"}
  return render(request, 'mostrador.html', context)

@login_required
def almacen(request):
  user = Usuario.objects.get(username=request.user.username)
  stocks = StockAlmacen.objects.all()

  context = {'usuario':user, 'stocks':stocks, 'menu_almacen':"active"}
  return render(request, 'almacen.html', context)

@login_required
def perfil(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'usuario':user, 'menu_perfil':"active"}
  return render(request, 'perfil.html', context)

