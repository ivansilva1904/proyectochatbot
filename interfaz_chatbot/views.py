from django.shortcuts import render
from django.http import JsonResponse # Para enviar respuestas en formato JSON
from django.views.decorators.http import require_POST # Para asegurar que la vista solo acepte POST
import json # Para trabajar con datos JSON
from .chatbot_parser import procesar_mensaje

from django.views.decorators.csrf import ensure_csrf_cookie # Para asegurarse de que funcione en otros dispositivos

# Create your views here.

@ensure_csrf_cookie
def vista_chatbot(request):
    return render(request, 'interfaz_chatbot/chatbot.html')


@require_POST
def process_message_view(request):
    try:
        # Decodificar el cuerpo de la peticion
        data = json.loads(request.body.decode('utf-8'))
        user_message = data.get('message')

        if user_message is None:
            return JsonResponse({'error': 'No se proporcionó ningún mensaje.'}, status=400)

        processed_message = procesar_mensaje(user_message)

        return JsonResponse({'response': processed_message})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido.'}, status=400)
    except Exception as e:
        print(f"Error en process_message_view: {e}")
        return JsonResponse({'error': 'Ocurrió un error en el servidor.'}, status=500)
