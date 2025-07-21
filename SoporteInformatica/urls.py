from django.urls import path
from . import views

urlpatterns = [
    #app principal
    path('', views.index, name='index'),  # ruta principal
    path('crear_solicitud/', views.crear_solicitud, name='crear_solicitud'),
    path('lista_solicitud/', views.lista_solicitud, name='lista_solicitud'),
    path('lista_solicitud/<int:solicitud_id>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('lista_solicitud/<int:solicitud_id>/eliminada', views.solicitud_eliminada, name='solicitud_eliminada'),
    path('solicitudes_completadas/', views.solicitudes_completadas, name='solicitudes_completadas'),
    
    # Sesion de usuarios
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    
    #admin
    path('lista_solicitud_admin', views.lista_solicitud_admin, name='lista_solicitud_admin'),
    path('lista_solicitud_admin/<int:solicitud_id>/', views.detalle_solicitud_admin, name='detalle_solicitud_admin'),
    path('lista_solicitud_admin/<int:solicitud_id>/completada', views.solicitud_completada_admin, name='solicitud_completada_admin'),
    path('solicitudes_completadas_admin/', views.solicitudes_completadas_admin, name='solicitudes_completadas_admin'),
    path('lista_solicitud_admin/<int:solicitud_id>/eliminada', views.solicitud_eliminada_admin, name='solicitud_eliminada_admin'),
    path('lista_solicitud_admin/<int:solicitud_id>/incompletar', views.solicitud_incompletar_admin, name='solicitud_incompletar_admin'),
]