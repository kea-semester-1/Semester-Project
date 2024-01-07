<template>
    <div class="chat-container">
        <div id="chatBox" class="chat-box" v-html="chatBoxContent"></div>
        <input type="text" v-model="messageInput" placeholder="Type a message..." class="message-input">
        <button @click="sendMessage" class="send-button">Send</button>
    </div>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue';

const chatBoxContent = ref('');
const messageInput = ref('');
const ws = ref(null);

// Receiving the character prop
const props = defineProps({
    player: Object
});

const serverUrl = ref('');

const setupWebSocketConnection = () => {
    console.log("Connecting to WebSocket", serverUrl.value);
    // Check if a WebSocket connection already exists
    if (ws.value) {
        // If the WebSocket is connecting or open, close it first
        if (ws.value.readyState === WebSocket.CONNECTING || ws.value.readyState === WebSocket.OPEN) {
            ws.value.close();
        }
    }

    // Establish a new WebSocket connection
    ws.value = new WebSocket(serverUrl.value);

    // Setup event listeners for the new WebSocket connection
    ws.value.onmessage = (event) => {
        chatBoxContent.value += `<div>${event.data}</div>`; // Display the received message
    };

    ws.value.onerror = (error) => {
        console.error('WebSocket Error:', error);
    };

    ws.value.onclose = () => {
        console.log('WebSocket connection closed');
    };
};


watch(() => props.player.place.name, (newPlace) => {
    serverUrl.value = `ws://localhost:8080/ws/${newPlace}/${props.player.id}`;
    setupWebSocketConnection();
}, { deep: true });

const sendMessage = () => {
    if (messageInput.value.trim() !== '') {
        const messageToSend = `${props.player.character_name}: ${messageInput.value}`;
        ws.value.send(messageToSend); // Send the message
        messageInput.value = '';
    }
};

onMounted(() => {
    if (!ws.value && props.player && props.player.place && props.player.place.name) {
        serverUrl.value = `ws://localhost:8080/ws/${props.player.place.name}/${props.player.id}`;
        setupWebSocketConnection();
    }
});

</script>


<style scoped>
.chat-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 300px;
}

.chat-box {
    width: 100%;
    height: 200px;
    border: 1px solid #ddd;
    margin-bottom: 10px;
    overflow-y: auto;
}

.message-input {
    width: calc(100% - 60px);
    padding: 10px;
}

.send-button {
    width: 50px;
    height: 36px;
}
</style>
