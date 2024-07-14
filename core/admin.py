from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Categoria)
admin.site.register(Obra)
admin.site.register(Boleta)
admin.site.register(BoletaItem)