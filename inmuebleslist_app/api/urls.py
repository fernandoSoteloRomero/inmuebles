from django.urls import path
from inmuebleslist_app.api.views import EdificacionAV, EdificacionDetalleAV, EmpresaAV, EmpresaDetalleAV


urlpatterns = [
  path('list/', EdificacionAV.as_view(), name = "edificacion_list"),
  path('<int:pk>', EdificacionDetalleAV.as_view(), name="edificacion-detail"),
  path('empresa/', EmpresaAV.as_view(), name = "empresa_list"),
  path('empresa/<int:pk>', EmpresaDetalleAV.as_view(), name="empresa-detail")
]
