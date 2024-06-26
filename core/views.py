from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Categoria, Obra, Boleta, DetalleBoleta
from .forms import obraForm, RegistroUserForm, EditarPerfil
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
    return render(request,'carrito2.html')

def detallecarrito(request):
    return render(request,'detallecarrito.html')

def agregar_obra(request,id):
    carrito_compra=Carrito(request)
    obra=Obra.objects.get(idObra=id)
    carrito_compra.agregar(obra)
    messages.add_message(request=request,level=messages.SUCCESS, message="Obra agregada :)")
    return redirect('obras')

def eliminar_obra(request, id):
    carrito_compra=Carrito(request)
    obra=Obra.objects.get(idObra=id)
    carrito_compra.eliminar(obra)
    return redirect('obras')

def restar_obra(request, id):
    carrito_compra=Carrito(request)
    obra=Obra.objects.get(idObra=id)
    carrito_compra.restar(obra)
    return redirect('obras')

def limpiar_obra(request):
    carrito_compra=Carrito(request)
    carrito_compra.limpiar()
    return redirect('obras')

#__________________________
def generarBoleta(request):
    precio_total=0
    for key, value in request.session['carrito'].items():
        precio_total = precio_total+int(value['precio'])*int(value['cantidad'])
    boleta=Boleta(total=precio_total)
    boleta.save()
    obras=[]
    for key, value in request.session['carrito'].items():
        obra=Obra.objects.get(patente=value['obra_id'])
        cant=value['cantidad']
        subtotal=cant*int(value['precio'])
        detalle=DetalleBoleta(
            id_boleta=boleta, 
            id_obra=obra, 
            cantidad=cant, 
            subtotal=subtotal
        )
        detalle.save()
        obras.append(detalle)
    datos={
        'obras':obras,
        'fecha':boleta.fechaCompra,
        'total':boleta.total
    }
    request.session['boleta']=boleta.id_boleta
    carrito=Carrito(request)
    carrito.limpiar()
    return render(request,'detallecarrito.html', datos)
    

#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::