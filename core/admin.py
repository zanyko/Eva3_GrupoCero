from django.contrib import admin
from .models import Categoria, Obra, Boleta, DetalleBoleta,CustomUser

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Categoria)
admin.site.register(Obra)
admin.site.register(Boleta)
admin.site.register(DetalleBoleta)