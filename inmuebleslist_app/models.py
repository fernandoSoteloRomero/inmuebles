from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from user_app.models import Account
# Create your models here.





class Empresa(models.Model):
  nombre = models.CharField(max_length=250)
  website = models.URLField(max_length=250)
  active = models.BooleanField(default=True)
  
  
  
  def __str__(self):
    return self.nombre
  
  
  
class Edificacion(models.Model):
  direccion = models.CharField(max_length=250)
  pais = models.CharField(max_length=150)
  descripcion = models.CharField(max_length=500)
  imagen = models.CharField(max_length=500)
  active = models.BooleanField(default=True)
  avg_calificacion = models.FloatField(default=0)
  number_calificacion = models.IntegerField(default=0)
  empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="edificacionlist")
  created = models.DateTimeField(auto_now_add=True)
  
  
  
  def __str__(self):
    return self.descripcion
  
  
  
class Comentario(models.Model):
  comentario_user = models.ForeignKey(Account, on_delete=models.CASCADE)
  calificacion = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
  texto = models.CharField(max_length=200, null=True)
  edificacion = models.ForeignKey(Edificacion, on_delete=models.CASCADE, related_name='comentarios')
  active = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return str(self.calificacion) + " " + self.edificacion.direccion
  





