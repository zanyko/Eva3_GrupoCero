from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from .forms import *
from core.compras import Carrito


# Create your views here

#::::::::::::::::::::::::::::::::::::::::::::::


def crear(request):
    if request.method=='POST':
        obraform = obraForm(request.POST, request.FILES)
        if obraform.is_valid():
            obraform.save()     # similar to"insert into" from sql
            messages.add_message(reques=request,level=messages.SUCCESS,message="Producto creado con éxito")
            return redirect('buscar')
    else:
        obraform=obraForm()   # asign an empty form
    return render(request,'crear.html',{'obraform':obraform}) # keys symbols are obligatory


def buscar(request):
    obras = Obra.objects.all()     #similar a select * from Vehiculo
    return render(request, 'buscar.html', {'obras':obras})

def editar(request):
    obras = Obra.objects.all()      #similar a select * from Vehiculo
    return render(request, 'editar.html', {'obras':obras})

def admire(request, id):
    obra = get_object_or_404(Obra, idObra = id) # cuando un objeto no ha sido encontrado se envia el error 404
    return render(request, 'admire.html', {'obra':obra}) # aqui se guarda lo encontrado en la linea anterior

def usuarios(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'usuarios.html', {'usuarios':usuarios})


#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::

def base(request):
    return render(request,'base.html')

def index(request):
    return render(request,'index.html')

def obras(request):
    obras = Obra.objects.all()     #similar a select * from Vehiculo
    return render(request, 'obras.html', {'obras':obras})

def nosotros(request):
    return render(request,'nosotros.html')


def modificar(request, id):
    obra = Obra.objects.get(idObra=id) # buscara el objeto con la id enviada
    daten={'fillMe': obraForm(instance=obra), 'obra':obra} 
        # rellenamos 'datos' con un formulario de tipo 'obraForm' con los datos "obra" de la linea anterior, en el otro parametro creamos otro objeto 'obra'
    if request.method=='POST':
        formulario = obraForm(request.POST, request.FILES, instance=obra)
        if formulario.is_valid():
            formulario.save()   #actualiza la info del objeto
            messages.add_message(reques=request,level=messages.SUCCESS,message="Producto creado con éxito")
            return redirect('editar')
    return render(request, 'modificar.html', daten)

#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::

def profile(request):
    return render(request,'profile.html')

def profileMod(request):
    if request.method == 'POST':
        fill= EditarPerfil(request.POST, request.FILES, instance=request.user)
        if fill.is_valid():
            fill.save()
            messages.add_message(request=request,level=messages.SUCCESS, message="Perfil actualizado correctamente.")
            return redirect('profile')
        else:
            messages.add_message(request=request,level=messages.SUCCESS, message="Error al actualizar el perfil.")
    else:
        fill = EditarPerfil(instance=request.user)
    
    return render(request, 'profileMod.html', {'form': fill})

def profileWatch(request, id):
    usuario = get_object_or_404(CustomUser, username = id)
    return render(request,'profileWatch.html', {'usuario':usuario})


#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::

def eliminar(request, id):
    obra = get_object_or_404(Obra,idObra=id)
    if request.method=='POST':
        if 'elimina' in request.POST:   # boton que elimnina
            obra.delete() # elimina el objeto despues de confirmar
            return redirect('editar')
        else:
            return redirect ('editar')
    return render (request, 'eliminar.html',{'obra':obra})

def cerrar(request):
    logout(request)
    return redirect('index')

def signup(request):
    data={'form':RegistroUserForm()}
    if request.method=="POST":
        formulario = RegistroUserForm(data=request.POST,files=request.FILES)
        if formulario.is_valid():
            user = formulario.save()
            user.refresh_from_db()  # Esto asegura que el perfil de usuario sea actualizado con los datos adicionales
            user.pic = formulario.cleaned_data.get('pic')
            user.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            if user is not None:
                login(request, user)
                messages.success(request, "Sesión iniciada con éxito")
                return redirect('index')
        data['form']=formulario
    return render(request, "registration/signup.html", data)

#::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::CARRITO::::::::::::::::::::

def carrito(request):
    return render(request,'carrito.html')

def carrito2(request):
    print(request.session.get('carrito', {}))   
    return render(request,'carrito2.html')

def agregar_obra(request,id):
    obra=Obra.objects.get(idObra=id)
    vy = int(obra.stock)
    carrito = request.session.get('carrito', {})
    vz = int(request.POST.get('cantidad', 1))
    if vy>0:
        if(vy-vz)<0:
            messages.add_message(request=request,level=messages.SUCCESS, message="No hay stock disponible")
        else:
            carrito_compra=Carrito(request)
            carrito_compra.agregar(obra)
            messages.add_message(request=request,level=messages.SUCCESS, message="Obra agregada")
    else:
        messages.add_message(request=request,level=messages.SUCCESS, message="No hay stock disponible")
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('obras')

def eliminar_obra(request, id):
    carrito_compra=Carrito(request)
    obra=Obra.objects.get(idObra=id)
    carrito_compra.eliminar(obra)
    messages.add_message(request=request,level=messages.SUCCESS, message="Obra eliminada")
    return redirect('carrito2')

def restar_obra(request, id):
    carrito_compra=Carrito(request)
    obra=Obra.objects.get(idObra=id)
    carrito_compra.restar(obra)
    messages.add_message(request=request,level=messages.SUCCESS, message="Obra restada")
    return redirect('carrito2')

def limpiar_obra(request):
    carrito_compra=Carrito(request)
    carrito_compra.limpiar()
    messages.add_message(request=request,level=messages.SUCCESS, message="El carrito ha sido vaciado")
    return redirect('obras')

#__________________________
def generarBoleta(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            carrito = request.session.get('carrito',{})
            total = sum(int(value['precio']) * int(value['cantidad']) for value in carrito.values())

            boleta = Boleta.objects.create(
                usuario=request.user,
                total=total,
                complete=False,
            )
            return redirect('detallecarrito', id=boleta.id) #gracias a que puse 'id' y no 'boleta_id', funciono
        else:
            print('------USER IS NOT AUTHENTICATED------')
    return redirect('carrito')
    
def detallecarrito(request,id):
    print("------ ",id," ------")
    boleta = get_object_or_404(Boleta, id=id)
    return render(request,'detallecarrito.html', {'boleta': boleta})

def comprar(request,id):
    boleta = get_object_or_404(Boleta, id=id)
    if request.method=='POST':
        carrito = request.session.get('carrito',{})
        for key, value in carrito.items():
            producto_id = str(key)
            quantity = value['cantidad']
            obra = get_object_or_404(Obra, idObra=producto_id)
            obra.stock -= quantity
            obra.save()
            boletaitem = BoletaItem.objects.create(
                product = obra,
                boleta = boleta,
                cantidad = quantity,
            )
            boletaitem.save();
        boleta.complete = True
        boleta.save()
        request.session['carrito'] = {} # Limpiar el carrito después de la compra
        request.session.modified = True
        return redirect('miscompras')
    return render(request,'carrito.html')

def miscompras(request):
    compras = None
    if request.user.is_authenticated:
        customer = request.user
        compras = Boleta.objects.filter(usuario=customer)
    return render(request,'miscompras.html', {'compras':compras})

#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::