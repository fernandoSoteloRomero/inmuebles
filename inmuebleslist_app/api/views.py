from inmuebleslist_app.models import Edificacion, Empresa
from inmuebleslist_app.api.serializers import EdificacionSerializer, EmpresaSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.

class EmpresaAV(APIView):
  def get(self, request):
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
    

