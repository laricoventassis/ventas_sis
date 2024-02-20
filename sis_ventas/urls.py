from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (LoginView, LogoutView,PasswordChangeView, PasswordResetDoneView)
from aplicacion.views import inicio, venta, almacen, perfil, guardar_stock, guardar_caja, guardar_venta, eliminar, rptventas, listaventas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='login.html'), name='logout'),
    # path('', inicio, name='inicio'),
    # path('venta/', venta, name='venta'),
    path('', venta, name='venta'),
    path('almacen/', almacen, name='almacen'),
    path('almacen/<str:fecha>/', almacen, name='almacen'),
    path('perfil/', perfil, name='perfil'),
    path('guardar_stock/', guardar_stock, name='guardar_stock'),
    path('guardar_caja/', guardar_caja, name='guardar_caja'),
    path('guardar_venta/', guardar_venta, name='guardar_venta'),
    path('eliminar/', eliminar, name='eliminar'),
    path('rptventas/', rptventas, name='rptventas'),
    path('rptventas/<str:fecha>/', rptventas, name='rptventas'),
    path('listaventas/', listaventas, name='listaventas'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)