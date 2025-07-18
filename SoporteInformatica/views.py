from django.contrib.auth.models import Group
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

# Admin
@login_required
def lista_solicitud_admin(request):
    tickets = Ticket.objects.all().order_by("fecha_creacion")
    context = {"tickets": tickets}
    return render(request, "SoporteInformatica/lista_solicitud_admin.html", context)
 

def detalle_solicitud_admin(request, solicitud_id):
    # Actualizar datos de la solicitud desde admin
    if request.method == "GET":
        solicitud = get_object_or_404(Ticket, id=solicitud_id, usuario=request.user)
        form = FormularioSolicitud(instance=solicitud)
        context = {"solicitud": solicitud, 
                   "form": form}
        return render(request, "SoporteInformatica/detalle_solicitud_admin.html", context)
    
    else:
        try:
            solicitud = get_object_or_404(Ticket, id=solicitud_id, usuario=request.user)
            form = FormularioSolicitud(request.POST, instance=solicitud)
            form.save()
            context = {"solicitud": solicitud, 
                       "form": form}
            return render(request, "SoporteInformatica/detalle_solicitud_admin.html", context)

        except ValueError:
            context = {"solicitud": solicitud, 
                       "form": form,
                       "error": "Error al actualizar la solicitud"}
            return render(request, "SoporteInformatica/detalle_solicitud_admin.html", context)


# usuarios 
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
        username = request.POST["username"].capitalize()
        lastname = request.POST["last_name"].capitalize()
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        
        if User.objects.filter(email=email).exists():
                return render(request, "SoporteInformatica/registrar_usuario.html", {
                "error": "Ya existe una cuenta con este correo electrónico"})
                
        if password1 != password2:
            return render(request, "SoporteInformatica/registrar_usuario.html", {
            "error": "Las contraseñas no coinciden"})
        
        # Crear usuario nuevo
        try: 
            nuevo_usuario = User.objects.create_user(username=username, last_name=lastname, password=password1, email=email)
            nuevo_usuario.save()
            
            #Añadir al grupo de usuarios
            grupo = Group.objects.get(name="usuario")
            nuevo_usuario.groups.add(grupo)
            return redirect("iniciar_sesion")
        
        except:
            context = {"form": UserCreationForm, "error": "El usuario ya existe"}
            return render(request, "SoporteInformatica/registrar_usuario.html", context)          
          
      
@login_required  
def cerrar_sesion(request):
    logout(request)
    return redirect("index")


def iniciar_sesion(request):
    if request.method == "GET":
        context = {"form": AuthenticationForm()}
        return render(request, "SoporteInformatica/iniciar_sesion.html", context)
    
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            usuario = User.objects.get(email=email)
        except User.DoesNotExist:
            context = {"form": AuthenticationForm(), "error": "Usuario no existe"}
            return render(request, "SoporteInformatica/iniciar_sesion.html", context)

        user = authenticate(request, username=usuario.username, password=password)

        if user is None:
            context = {"form": AuthenticationForm(), "error": "El usuario o la contraseña son incorrectos"}
            return render(request, "SoporteInformatica/iniciar_sesion.html", context)
        
        login(request, user)

        if user.is_staff or user.groups.filter(name="admin").exists():
            # si es admin lo manda aqui
            return redirect("lista_solicitud_admin")
        else:
            return redirect("index")
