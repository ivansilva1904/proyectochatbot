from django.shortcuts import render
from django.http import JsonResponse # Para enviar respuestas en formato JSON
from django.views.decorators.http import require_POST # Para asegurar que la vista solo acepte POST
import json # Para trabajar con datos JSON

# Create your views here.

def vista_chatbot(request):
    return render(request, 'interfaz_chatbot/chatbot.html')


@require_POST # Esta vista solo aceptará peticiones POST
def process_message_view(request):
    try:
        # Decodificar el cuerpo de la petición (que esperamos sea JSON)
        data = json.loads(request.body.decode('utf-8'))
        user_message = data.get('message')

        if user_message is None:
            return JsonResponse({'error': 'No se proporcionó ningún mensaje.'}, status=400)

        # Aquí es donde manipulas el string con Python
        # Ejemplo: convertir a mayúsculas
        processed_message = user_message.upper()

        # Simular un pequeño "pensamiento" del bot (opcional)
        #import time
        #time.sleep(0.5) 

        return JsonResponse({'response': processed_message})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido.'}, status=400)
    except Exception as e:
        # Loguear el error real en un entorno de producción
        print(f"Error en process_message_view: {e}")
        return JsonResponse({'error': 'Ocurrió un error en el servidor.'}, status=500)
