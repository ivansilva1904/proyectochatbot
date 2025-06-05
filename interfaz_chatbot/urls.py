from django.urls import path
from . import views # Importa las vistas de la app actual

app_name = 'interfaz_chatbot' # Opcional, pero buena práctica para namespacing

urlpatterns = [
    path('', views.vista_chatbot, name='chat'), # URL raíz de la app mostrará el chatbot
    path('process/', views.process_message_view, name='process_message'), # <--- NUEVA URL
]
