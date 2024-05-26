from inmuebleslist_app.models import Edificacion, Empresa, Comentario
from inmuebleslist_app.api.serializers import EdificacionSerializer, EmpresaSerializer, ComentarioSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from inmuebleslist_app.api.permissions import IsAdminOrReadOnly, IsComentarioUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from inmuebleslist_app.api.throttling import ComentarioCreateThrottle, ComentarioListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.

class UsuarioComentario(generics.ListAPIView):
  serializer_class = ComentarioSerializer
  
  # def get_queryset(self):
  #   username = self.kwargs['username']
  #   return Comentario.objects.filter(comentario_user__username = username)
  
  def get_queryset(self):
    username = self.request.query_params.get('username', None)
    return Comentario.objects.filter(comentario_user__username = username)


class ComentarioCreate(generics.CreateAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = ComentarioSerializer
  throttle_classes = [ComentarioCreateThrottle]
  
  def get_queryset(self):
    return Comentario.objects.all()
  
  def perform_create(self, serializer):
    pk = self.kwargs.get('pk')
    inmueble = Edificacion.objects.get(pk = pk)
    
    user = self.request.user
    comentario_queryset = Comentario.objects.filter(edificacion = inmueble, comentario_user = user)    
    if comentario_queryset.exists():
      raise ValidationError('El usuario ya escribio un comentario para este inmueble')
    
    if inmueble.number_calificacion == 0:
      inmueble.avg_calificacion = serializer.validated_data['calificacion']
    else:
      inmueble.avg_calificacion = (serializer.validated_data['calificacion'] + inmueble.avg_calificacion)
      
    inmueble.number_calificacion = inmueble.number_calificacion + 1
    inmueble.save()
    serializer.save(edificacion = inmueble, comentario_user = user)

class ComentarioList(generics.ListCreateAPIView):
  # queryset = Comentario.objects.all()
  # permission_classes = [IsAuthenticated]
  throttle_classes = [ComentarioListThrottle, AnonRateThrottle]
  filter_backends = [DjangoFilterBackend]
  serializer_class = ComentarioSerializer
  filterset_fields = ['comentario_user__username', 'active']
  
  def get_queryset(self):
    pk = self.kwargs['pk']
    print(self.kwargs['pk'])
    return Comentario.objects.filter(edificacion = pk)

class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [IsComentarioUserOrReadOnly]
  throttle_classes = [UserRateThrottle, AnonRateThrottle]
  queryset = Comentario.objects.all()
  serializer_class = ComentarioSerializer

class EdificacionList(generics.ListAPIView)  :
  queryset = Edificacion.objects.all()
  serializer_class = EdificacionSerializer
  filter_backends = [filters.SearchFilter, filters.OrderingFilter]
  search_fields = ['direccion', 'empresa__nombre']

class EmpresaVS(viewsets.ModelViewSet):
  permission_classes = [IsAdminOrReadOnly]
  queryset = Empresa.objects.all()
  serializer_class = EmpresaSerializer
  
  
  
  # def list(self, request):
  #   queryset = Empresa.objects.all()
  #   serializer = EmpresaSerializer(queryset, many=True)
  #   return Response(serializer.data)
  
  # def retrieve(self, request, pk = None):
  #   queryset = Empresa.objects.all()
  #   edificacionlist = get_object_or_404(queryset, pk=pk)
  #   serializer = EmpresaSerializer(edificacionlist)
  #   return Response(serializer.data)
  
  


class EmpresaAV(APIView):
  def get(self, request):
    print(f'{request} aqui')
    empresas = Empresa.objects.all()
    serializer = EmpresaSerializer(empresas, many=True, context={'request': request})
    return Response(serializer.data)

  def post(self, request):
    de_serializer = EmpresaSerializer(data = request.data)
    if de_serializer.is_valid():
      de_serializer.save()
      return Response(de_serializer.data)
    else:
      return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmpresaDetalleAV(APIView):
  def get(self, request, pk):
    try:
      empresa = Empresa.objects.get(pk = pk)
    except Empresa.DoesNotExist:
      return Response({'error':'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = EmpresaSerializer(empresa, context={'request': request})
    return Response(serializer.data)
  
  def put(self, request, pk):
    try:
      empresa = Empresa.objects.get(pk = pk)
    except Empresa.DoesNotExist:
      return Response({'error':'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = EmpresaSerializer(empresa, data=request.data, context={'request': request})
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, pk):
    try:
      empresa = Empresa.objects.get(pk = pk)
    except Empresa.DoesNotExist:
      return Response({'error':'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    empresa.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    

class EdificacionAV(APIView):
  permission_classes = [IsAdminOrReadOnly]
  
  
  def get(self, request):
    inmuebles = Edificacion.objects.all()  
    serializer = EdificacionSerializer(inmuebles, many = True)
    return Response(serializer.data)
  
  def post(self, request):
    serializer = EdificacionSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
class EdificacionDetalleAV(APIView):
  permission_classes = [IsAdminOrReadOnly]
  def get(self, request, pk):
    try:
      edificacion = Edificacion.objects.get(pk = pk)
    except Edificacion.DoesNotExist:
      return Response({'error':'edificacion no encontrado'}, status=status.HTTP_404_NOT_FOUND) 
    serializer = EdificacionSerializer(edificacion)
    return Response(serializer.data)
  
  def put(self, request, pk):
    try:
      edificacion = Edificacion.objects.get(pk = pk)
    except Edificacion.DoesNotExist:
      return Response({'error':'edificacion no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = EdificacionSerializer(edificacion, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  def delete(self, request, pk):
    try:
      edificacion = Edificacion.objects.get(pk = pk)
    except Edificacion.DoesNotExist:
      return Response({'error':'edificacion no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    edificacion.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)







    
  # PQY39VR7UAHRDZWD9BJT4YUR
    

