document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // Estas variables userAvatarUrl y botAvatarUrl vienen del script inline en el HTML
    // const userAvatarUrl = window.userAvatarUrl; // No es necesario si se declaran globalmente sin window.
    // const botAvatarUrl = window.botAvatarUrl;

    if (!chatBox || !userInput || !sendButton) {
        console.error("Elementos del chat no encontrados. Verifica los IDs en el HTML.");
        return;
    }

    // Event listener para el botón de enviar
    sendButton.addEventListener('click', handleSendMessage);

    // Event listener para la tecla 'Enter' en el input
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Previene el comportamiento por defecto (ej. submit de formulario)
            handleSendMessage();
        }
    });

    function handleSendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') {
            return; // No enviar mensajes vacíos
        }

        appendMessage(messageText, 'user');
        userInput.value = ''; // Limpiar el input
        userInput.focus(); // Devolver el foco al input

        // Aquí es donde en el futuro podrías llamar a una función para obtener la respuesta del bot
        // Por ahora, lo dejamos así, solo se muestra el mensaje del usuario.
        // Ejemplo:
        // simulateBotResponse(messageText);

        setTimeout(() => {
            getBotResponseFromServer(messageText);
        }, 1000 + Math.random() * 5000);

    }

    function appendMessage(text, senderType) {
        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('message', senderType === 'user' ? 'user-message' : 'bot-message');
        if (senderType === 'bot-typing') { // Ejemplo si quieres un estilo "escribiendo..."
            messageWrapper.classList.add('bot-typing-message'); // Clase adicional
        }

        const avatar = document.createElement('img');
        avatar.classList.add('avatar');
        avatar.src = senderType === 'user' ? userAvatarUrl : botAvatarUrl;
        avatar.alt = senderType === 'user' ? 'User Avatar' : 'Bot Avatar';

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');

        const messageTextElement = document.createElement('p');
        messageTextElement.textContent = text;

        const messageTime = document.createElement('span');
        messageTime.classList.add('message-time');
        messageTime.textContent = getCurrentTime();

        messageContent.appendChild(messageTextElement);
        messageContent.appendChild(messageTime);

        if (senderType === 'user') {
            messageWrapper.appendChild(messageContent); // Contenido primero
            messageWrapper.appendChild(avatar);         // Avatar después
        } else { // bot
            messageWrapper.appendChild(avatar);         // Avatar primero
            messageWrapper.appendChild(messageContent); // Contenido después
        }

        chatBox.appendChild(messageWrapper);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll al último mensaje
    }

    function getCurrentTime() {
        const now = new Date();
        let hours = now.getHours();
        const minutes = now.getMinutes().toString().padStart(2, '0');
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // La hora '0' debería ser '12'
        return `${hours}:${minutes} ${ampm}`;
    }

    async function getBotResponseFromServer(userMessage) {
        // Mostrar un mensaje de "pensando" (opcional)
        //appendMessage("Bot está pensando...", 'bot-typing'); // Necesitarías CSS para 'bot-typing'

        const csrftoken = getCookie('csrftoken'); // Necesitamos esta función (ver abajo)

        try {
            const response = await fetch(processMessageUrl, { // Usar la URL pasada desde HTML
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken // Esencial para peticiones POST en Django
                },
                body: JSON.stringify({ message: userMessage }) // Enviar el mensaje como JSON
            });

            if (!response.ok) {
                // Si la respuesta HTTP no es exitosa (ej. 400, 403, 500)
                let errorData = { error: `Error del servidor: ${response.status}` };
                try {
                    errorData = await response.json(); // Intenta parsear el error JSON del backend
                } catch (e) {
                    // Si el cuerpo del error no es JSON, usa el statusText
                    errorData.error = errorData.error || response.statusText;
                }
                console.error('Error desde el servidor:', errorData);
                appendMessage(errorData.error || `Error ${response.status}`, 'bot');
                return;
            }

            const data = await response.json(); // Parsear la respuesta JSON del backend

            if (data.response) {
                appendMessage(data.response, 'bot');
            } else if (data.error) {
                console.error('Error en la respuesta del bot:', data.error);
                appendMessage(`Error: ${data.error}`, 'bot');
            }

        } catch (error) {
            console.error('Error en la petición fetch:', error);
            appendMessage('Lo siento, no pude conectarme al servidor para procesar el mensaje.', 'bot');
        }
    }

    // Función para obtener el CSRF token de las cookies (esencial para POST con Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // ¿El nombre de la cookie coincide con el que buscamos?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // --- Placeholder para futura funcionalidad del Bot ---
    // function simulateBotResponse(userMessage) {
    //     // Simular un pequeño retraso como si el bot estuviera "pensando"
    //     setTimeout(() => {
    //         let botTextResponse = "No he entendido tu mensaje. Todavía estoy aprendiendo.";
    //
    //         // Lógica simple de respuesta (puedes expandir esto enormemente)
    //         if (userMessage.toLowerCase().includes("hola")) {
    //             botTextResponse = "¡Hola! ¿Cómo puedo ayudarte?";
    //         } else if (userMessage.toLowerCase().includes("adiós") || userMessage.toLowerCase().includes("gracias")) {
    //             botTextResponse = "¡De nada! Que tengas un buen día.";
    //         } else if (userMessage.toLowerCase().includes("ayuda")) {
    //             botTextResponse = "Claro, dime qué necesitas.";
    //         }
    //
    //         appendMessage(botTextResponse, 'bot');
    //     }, 1000 + Math.random() * 1000); // Retraso entre 1 y 2 segundos
    // }
});