from django import forms
from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import Widget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Categoria, Obra, CustomUser

class RegistroUserForm(UserCreationForm):
    pic = forms.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2', 'pic')

class EditarPerfil(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'pic')
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
            'pic': 'Imagen de Perfil',
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese primer nombre',
                'id': 'first_name'
                }),
            'last_name': forms.TextInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese apellido',
                'id': 'last_name'
                }),
            'email': forms.EmailInput(
                attrs={
                'class': 'form-control', 
                'placeholder': 'Ingrese email',
                'id': 'email'
                }),
            'pic': forms.FileInput(
                attrs={
                'class': 'form-control', 
                'id': 'pic'
                }),
        }

class obraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['idObra','nombre','descripcion','autor','anio','stock','categoria','imagen','precio']
        # cada field se compone de un 'label' y un 'widget'
        labels={
            'idObra':'ID',
            'nombre':'Nombre',
            'descripcion':'Descripcion',
            'autor':'Autor',
            'anio':'Año',
            'stock':'Stock',
            'categoria':'Categoria',
            'imagen':'Imagen',
            'precio':'Precio'
        }
        # tipo de etiqueta para los atributos:
        widgets={
            'idObra':forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Ingrese id de Obra',
                    'id' : 'idObra'
                }
            ),
            'nombre' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Ingrese nombre de Obra',
                    'id' : 'nombre'
                }
            ),
            'descripcion':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese breve descripcion',
                    'id':'descripcion'
                }
            ),
            'autor':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese nombre de Autor',
                    'id':'autor'
                }
            ),
            'anio':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese año de la obra',
                    'id':'anio'
                }
            ),
            'stock':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'id':'precio'
                }
            ),
            # categoria es un select, es decir, una lista desplegable
            'categoria' : forms.Select(
                attrs={
                    'class' : 'form-control',
                    'id' : 'categoria'
                }
            ),
            'imagen' : forms.FileInput(
                attrs={
                    'class' : 'form-control',
                    'id' : 'imagen'
                }
            ),
            'precio':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'id':'precio'
                }
            ),
        } # end widgets
