from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket
from .forms import FormularioSolicitud, FormularioSeleccionUsuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

# Admin
@staff_member_required
def registrar_usuario(request):
    if request.method == "GET":
        context = {"form": UserCreationForm}
        return render(request, "SoporteInformatica/registrar_usuario.html", context)
    
    else:
        first_name = request.POST["first_name"].lower().capitalize()
        lastname = request.POST["last_name"].lower().capitalize()
        username = first_name + " " + lastname
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        
        if User.objects.filter(email=email).exists():
                return render(request, "SoporteInformatica/registrar_usuario.html", {
                "error": "Ya existe una cuenta con este correo electrónico, ingrese otra distinta."})
                
        if password1 != password2:
            return render(request, "SoporteInformatica/registrar_usuario.html", {
            "error": "Las contraseñas no coinciden, intente denuevo."})
        
        # Crear usuario nuevo
        try: 
            nuevo_usuario = User.objects.create_user(username=username, first_name=first_name, last_name=lastname, password=password1, email=email)
            nuevo_usuario.save()
            
            #Añadir al grupo de usuarios
            grupo = Group.objects.get(name="usuario")
            nuevo_usuario.groups.add(grupo)
            return redirect("iniciar_sesion")
        
        except:
            context = {"form": UserCreationForm, "error": "El usuario ya existe"}
            return render(request, "SoporteInformatica/registrar_usuario.html", context)          
          

@staff_member_required
def detalle_solicitud_admin(request, solicitud_id):
    # Actualizar datos de la solicitud desde admin
    if request.method == "GET":
        solicitud = get_object_or_404(Ticket, id=solicitud_id)
        form = FormularioSolicitud(instance=solicitud)
        context = {"solicitud": solicitud, 
                   "form": form}
        return render(request, "SoporteInformatica/detalle_solicitud_admin.html", context)
    
    else:
        try:
            solicitud = get_object_or_404(Ticket, id=solicitud_id)
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


@staff_member_required
def lista_solicitud_admin(request):
    form = FormularioSeleccionUsuario(request.GET or None)
    tickets = Ticket.objects.filter(tarea_completada__isnull=True).order_by("fecha_creacion")
    
    if form.is_valid() and form.cleaned_data["usuario"]:
        usuario = form.cleaned_data["usuario"]
        tickets = tickets.filter(usuario=usuario)
    
    context = {"tickets": tickets, 
               "peticion": "Peticiones Pendientes",
               "form": form}
    
    return render(request, "SoporteInformatica/lista_solicitud_admin.html", context)
 

@staff_member_required  
def solicitudes_completadas_admin(request):
    form = FormularioSeleccionUsuario(request.GET or None)
    tickets = Ticket.objects.filter(tarea_completada__isnull = False).order_by("-tarea_completada")
    
    if form.is_valid() and form.cleaned_data["usuario"]:
        usuario = form.cleaned_data["usuario"]
        tickets = tickets.filter(usuario=usuario)
    
    context = {"tickets": tickets,
               "peticion": "Peticiones Completadas",
               "form": form}
    
    return render(request, "SoporteInformatica/lista_solicitud_admin.html", context)


@staff_member_required
def solicitud_completada_admin(request, solicitud_id):
    solicitud = get_object_or_404(Ticket, pk=solicitud_id)
    if request.method == "POST":
        solicitud.tarea_completada = timezone.now()
        solicitud.save()
        return redirect("lista_solicitud_admin")


@staff_member_required
def solicitud_eliminada_admin(request, solicitud_id):
    solicitud = get_object_or_404(Ticket, pk=solicitud_id)
    if request.method == "POST":
        solicitud.delete()
        return redirect("lista_solicitud_admin")


@staff_member_required
def solicitud_incompletar_admin(request, solicitud_id):
    solicitud = get_object_or_404(Ticket, pk=solicitud_id)
    if request.method == "POST":
        solicitud.tarea_completada = None
        solicitud.save()
        return redirect("lista_solicitud_admin")


# usuarios 
def index(request):
    return render(request, "SoporteInformatica/index.html")


@login_required
def lista_solicitud(request):
    tickets = Ticket.objects.filter(usuario=request.user, tarea_completada__isnull = True)
    context = {"tickets": tickets, "peticion": "Sus Solicitudes Pendientes"}
    return render(request, "SoporteInformatica/lista_solicitud.html", context)


@login_required  
def solicitudes_completadas(request):
    tickets = Ticket.objects.filter(usuario = request.user, tarea_completada__isnull = False).order_by("-tarea_completada")
    context = {"tickets": tickets, "peticion": "Sus Peticiones Completadas"}
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
def solicitud_eliminada(request, solicitud_id):
    solicitud = get_object_or_404(Ticket, pk=solicitud_id, usuario=request.user)
    if request.method == "POST":
        solicitud.delete()
        return redirect("lista_solicitud")


      
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
            #si es normal lo manda aqui
            return redirect("index")
