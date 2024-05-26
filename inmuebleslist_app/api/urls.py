from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inmuebleslist_app.api.views import EdificacionAV, EdificacionDetalleAV, ComentarioList, ComentarioDetail, ComentarioCreate, EmpresaVS, UsuarioComentario, EdificacionList

router = DefaultRouter()
router.register('empresa', EmpresaVS, basename = "empresa")


urlpatterns = [
  path('list/', EdificacionAV.as_view(), name = "edificacion_list"),
  path('edificaciones/', EdificacionList.as_view(), name = "edificacion"),
  path('<int:pk>', EdificacionDetalleAV.as_view(), name="edificacion-detail"),
  
  path("", include(router.urls)),
  
  # path('empresa/', EmpresaAV.as_view(), name = "empresa_list"),
  # path('empresa/<int:pk>', EmpresaDetalleAV.as_view(), name="empresa-detail"),
  
  # Creamos un comentario dentro de una edificacion
  path('<int:pk>/comentario-create', ComentarioCreate.as_view(), name='comentario-create'),
  # Obtenemos todos los comentarios que hay dentro de una edificacion
  path('<int:pk>/comentario/', ComentarioList.as_view(), name = "comentario_list"),
  # Obtenemos un comentario en especifico y podremos aplicarle los metodos del CRUD
  path('comentario/<int:pk>', ComentarioDetail.as_view(), name="comentario-detail"),
  # path('comentarios/<str:username>/', UsuarioComentario.as_view(), name='usuario-comentario'),
  path('comentarios/', UsuarioComentario.as_view(), name='usuario-comentario'),
]
