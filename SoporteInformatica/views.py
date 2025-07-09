from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket
from .forms import FormularioSolicitud
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, "SoporteInformatica/index.html")


@login_required
def lista_solicitud(request):
    tickets = Ticket.objects.filter(usuario=request.user, tarea_completada__isnull = True)
    context = {"tickets": tickets}
    return render(request, "SoporteInformatica/lista_solicitud.html", context)
 
 
@login_required  
def solicitudes_completadas(request):
    tickets = Ticket.objects.filter(usuario=request.user, tarea_completada__isnull = False).order_by("-tarea_completada")
    context = {"tickets": tickets}
    return render(request, "SoporteInformatica/lista_solicitud.html", context)


@login_required
def crear_solicitud(request):
    if request.method == "GET":
        context = {"form": FormularioSolicitud}
        return render(request, "SoporteInformatica/crear_solicitud.html", context)
    
    else: 
        try: 
            form = FormularioSolicitud(request.POST)
            nueva_solicitud = form.save(commit=False)
            nueva_solicitud.usuario = request.user
            nueva_solicitud.save()
            return redirect("lista_solicitud")
        
        except ValueError:
            context = {"form": FormularioSolicitud,
                       "error": 'Ingrese datos correctos'}
            return render(request, "SoporteInformatica/crear_solicitud.html", context)
        

@login_required
def detalle_solicitud(request, solicitud_id):
    # Actualizar datos de la solicitud
    if request.method == "GET":
        solicitud = get_object_or_404(Ticket, id=solicitud_id, usuario=request.user)
        form = FormularioSolicitud(instance=solicitud)
        context = {"solicitud": solicitud, 
                   "form": form}
        return render(request, "SoporteInformatica/detalle_solicitud.html", context)
    
    else:
        try:
            solicitud = get_object_or_404(Ticket, id=solicitud_id, usuario=request.user)
            form = FormularioSolicitud(request.POST, instance=solicitud)
            form.save()
            context = {"solicitud": solicitud, 
                       "form": form}
            return render(request, "SoporteInformatica/detalle_solicitud.html", context)

        except ValueError:
            context = {"solicitud": solicitud, 
                       "form": form,
                       "error": "Error al actualizar la solicitud"}
            return render(request, "SoporteInformatica/detalle_solicitud.html", context)
        

@login_required
def solicitud_completada(request, solicitud_id):
    solicitud = get_object_or_404(Ticket, pk=solicitud_id, usuario=request.user)
    if request.method == "POST":
        solicitud.tarea_completada = timezone.now()
        solicitud.save()
        return redirect("lista_solicitud")


@login_required
def solicitud_eliminada(request, solicitud_id):
    solicitud = get_object_or_404(Ticket, pk=solicitud_id, usuario=request.user)
    if request.method == "POST":
        solicitud.delete()
        return redirect("lista_solicitud")


def registrar_usuario(request):
    if request.method == "GET":
        context = {"form": UserCreationForm}
        return render(request, "SoporteInformatica/registrar_usuario.html", context)
    
    else:
        if request.POST["password1"] == request.POST["password2"]:
            #registrar usuario
            try:
                username = request.POST["username"]
                password = request.POST["password1"]
                nuevo_usuario = User.objects.create_user(username=username, password=password)
                nuevo_usuario.save()
                login(request, nuevo_usuario)
                return redirect("index")
            except:
                context = {"form": UserCreationForm, "error": "El usuario ya existe"}
                return render(request, "SoporteInformatica/registrar_usuario.html", context)
        else:
            context = {"form": UserCreationForm, "error": "Las contraseñas no coinciden"}
            return render(request, "SoporteInformatica/registrar_usuario.html", context)
        
      
@login_required  
def cerrar_sesion(request):
    logout(request)
    return redirect("index")


def iniciar_sesion(request):
    print(request.POST) 
    if request.method == "GET":
        context = {"form": AuthenticationForm}
        return render(request, "SoporteInformatica/iniciar_sesion.html", context)
    
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {"form": AuthenticationForm, "error": "El usuario o la contraseña son incorrectos"}
            return render(request, "SoporteInformatica/iniciar_sesion.html", context)
        
        else:
            login(request, user)
            return redirect("index")
