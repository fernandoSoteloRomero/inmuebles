from django.urls import path
from inmuebleslist_app.api.views import InmuebleListAV, InmuebleDetalleAV


urlpatterns = [
  path('list/', InmuebleListAV.as_view(), name = "inmueble_list"),
  path('<int:pk>', InmuebleDetalleAV.as_view(), name="inmueble_detalle"),
]
