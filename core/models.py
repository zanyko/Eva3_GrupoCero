from distutils.command.upload import upload
from django.db import models
import datetime
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    pic = models.ImageField(upload_to='profile_pics', null=True, blank=True, default='profile_pics/default.png')
    is_staff=models.BooleanField(default=False)

class Categoria(models.Model):
    idCategoria = models.IntegerField(primary_key=True, verbose_name='idCategoria')
    nombreCategoria= models.CharField(max_length=40, verbose_name='nombreCategoria')

    def __str__(self):
        return self.nombreCategoria

class Obra(models.Model):
    idObra=models.CharField(max_length=5, primary_key=True, verbose_name='id Arbeit')
    nombre=models.CharField(max_length=30, verbose_name='Name der Arbeit')
    descripcion=models.CharField(max_length=255, verbose_name='Description')
    autor=models.CharField(max_length=99, verbose_name='Name des Autors')
    anio=models.CharField(max_length=4, verbose_name='Jahr der Arbeit')
    stock=models.IntegerField(verbose_name='Stock')
    categoria=models.ForeignKey('Categoria', on_delete=models.CASCADE, verbose_name='Kategorie')
    imagen=models.ImageField(upload_to="imagenes", null=True, verbose_name='Fotografie')
    precio=models.IntegerField(blank=True,null=True,verbose_name='Precio')

    def __str__(self):
        return f"{self.idObra} - {self.nombre}"
    
class Boleta(models.Model):
    usuario=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, editable=False)
    total=models.IntegerField(default=0, null=True, blank=True, editable=False)
    complete=models.BooleanField(default=False, null=True, blank=False)
    fecha=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class BoletaItem(models.Model):
    product = models.ForeignKey(Obra, on_delete=models.SET_NULL, blank=True, null=True, editable=False)
    boleta = models.ForeignKey(Boleta, on_delete=models.SET_NULL, blank=True, null=True, editable=False)
    cantidad = models.IntegerField(default=0, null=True, blank=True, editable=False)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.boleta} - {self.id} - {self.product} - {self.cantidad} - {self.fecha}"



    
# para guardar los modelos hay que parar el server y hacer migraciones en la raiz del proyecto: 
# agregar "admin.site.register('modelo');" en admin.py
# py manage.py makemigrations
# py manage.py migrate