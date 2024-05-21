from inmuebleslist_app.models import Inmueble
from inmuebleslist_app.api.serializers import InmuebleSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.


class InmuebleListAV(APIView):
  
  def get(self, request):
    inmuebles = Inmueble.objects.all()  
    serializer = InmuebleSerializer(inmuebles, many = True)
    return Response(serializer.data)
  
  def post(self, request):
    serializer = InmuebleSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
class InmuebleDetalleAV(APIView):
  
  def get(self, request, pk):
    try:
      inmueble = Inmueble.objects.get(pk = pk)
    except Inmueble.DoesNotExist:
      return Response({'error':'Inmueble no encontrado'}, status=status.HTTP_404_NOT_FOUND) 
    serializer = InmuebleSerializer(inmueble)
    return Response(serializer.data)
  
  def put(self, request, pk):
    try:
      inmueble = Inmueble.objects.get(pk = pk)
    except Inmueble.DoesNotExist:
      return Response({'error':'Inmueble no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = InmuebleSerializer(inmueble, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  def delete(self, request, pk):
    try:
      inmueble = Inmueble.objects.get(pk = pk)
    except Inmueble.DoesNotExist:
      return Response({'error':'Inmueble no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    inmueble.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)







    
  # PQY39VR7UAHRDZWD9BJT4YUR
    

