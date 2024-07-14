from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"), # path del index, debe ser un path por cada def
    path('base/', views.base,name="base"),
    path('obras/', views.obras,name="obras"),
    path('buscar/', views.buscar,name="buscar"),
    path('editar/', views.editar,name="editar"),
    path('crear/', views.crear,name="crear"),
    path('nosotros/', views.nosotros,name="nosotros"),
    path('carrito/', views.carrito,name="carrito"),
    path('carrito2/', views.carrito2,name="carrito2"),
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    path('login/', views.login, name='login'),
    path('signup/', views.signup,name="signup"),
    path('logout/', views.cerrar,name="cerrar"),
    path('usuarios/', views.usuarios,name="usuarios"),
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    path('profile/', views.profile,name="profile"),
    path('profileMod/', views.profileMod,name="profileMod"),
    path('profileWatch/<id>', views.profileWatch,name="profileWatch"),
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    path('admire/<id>/', views.admire,name="admire"),
    path('modificar/<id>/',views.modificar,name="modificar"),
    path('eliminar/<id>/',views.eliminar,name="eliminar"),
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    path('generarBoleta/', views.generarBoleta,name="generarBoleta"),
    path('detallecarrito/<int:id>/', views.detallecarrito,name="detallecarrito"),
    path('comprar/<int:id>/', views.comprar,name="comprar"),
    path('miscompras', views.miscompras,name="miscompras"),
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    path('agregar/<id>',views.agregar_obra,name="Add"),
    path('eliminar/<id>',views.eliminar_obra,name="Del"),
    path('restar/<id>',views.restar_obra,name="Sub"),
    path('limpiar/',views.limpiar_obra,name="CLS"),
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
]
