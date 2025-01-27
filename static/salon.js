document.addEventListener('DOMContentLoaded', function () {
    const messagesContainer = document.getElementById('messages-container');
    const messagesList = document.getElementById('messages');
    const form = document.getElementById('message-form');
    const input = document.getElementById('contenu');
    const salonId = "{{ salon.id }}";

    // Fonction pour faire défiler automatiquement vers le bas
    const scrollToBottom = () => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    // Scroll initial vers le bas
    scrollToBottom();

    // WebSocket pour recevoir les nouveaux messages
    const socket = new WebSocket(`ws://${window.location.host}/ws/salon/${salonId}/`);

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const newMessage = document.createElement('li');
        newMessage.innerHTML = `<strong>${data.user}</strong>: ${data.message}`;
        messagesList.appendChild(newMessage);

        // Scroll automatiquement vers le bas
        scrollToBottom();
    };

    socket.onopen = function () {
        console.log("WebSocket connecté !");
    };

    socket.onerror = function (error) {
        console.error("Erreur WebSocket :", error);
    };

    socket.onclose = function () {
        console.warn("WebSocket fermé !");
    };

    // Gérer l'envoi des messages
    form.onsubmit = function (e) {
        e.preventDefault(); // Empêche l'envoi par défaut du formulaire

        const message = input.value;

        if (message.trim()) {
            // Envoyer le message via WebSocket
            socket.send(JSON.stringify({ 'message': message }));
            input.value = ''; // Vider le champ après l'envoi
        }
    };
});
