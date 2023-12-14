const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const localStream = document.getElementById('localStream');
const remoteStream = document.getElementById('remoteStream');
const roomNameInput = document.getElementById('roomName');
const roomPasswordInput = document.getElementById('roomPassword');
let peerConnection;

startButton.addEventListener('click', startVoiceChat);
stopButton.addEventListener('click', stopVoiceChat);

async function startVoiceChat() {
    const roomName = roomNameInput.value;
    const roomPassword = roomPasswordInput.value;

    // Check if roomName and roomPassword are not empty and handle errors as needed

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    localStream.srcObject = stream;

    // Connect to the server and pass roomName and roomPassword as query parameters
    const socket = io.connect(`/?join=${roomName},${roomPassword}`);

    socket.on('room-error', (error) => {
        alert('Error: ' + error);
    });

    // Rest of your WebRTC code for creating offers, handling answers, and ICE candidates
}

function stopVoiceChat() {
    peerConnection.close();
    localStream.srcObject = null;
    remoteStream.srcObject = null;

    // Rest of your code for stopping the voice chat
}
