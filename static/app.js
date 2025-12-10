let ws;
let localStream;
let peerConnection;
let recognition;
let isListening = false;
let speechSynthesis = window.speechSynthesis;

// WebSocket connection
function connectWebSocket() {
    ws = new WebSocket('ws://localhost:8080/ws');
    
    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        if (data.type === 'ai_response') {
            addMessage('AI', data.content, 'ai');
            if (data.speak) {
                speakText(data.content);
            }
        } else if (data.type === 'webrtc_answer') {
            handleWebRTCAnswer(data.sdp);
        }
    };
    
    ws.onclose = function(event) {
        addMessage('System', 'Backend disconnected. Session ended.', 'ai');
        endSession();
    };
    
    ws.onerror = function(error) {
        addMessage('System', 'Connection error. Please restart the backend.', 'ai');
        endSession();
    };
}

// Speech synthesis with auto-restart listening
function speakText(text) {
    // Stop any ongoing speech
    speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 0.8;
    
    utterance.onstart = function() {
        updateVoiceStatus('🔊 AI Speaking...');
    };
    
    utterance.onend = function() {
        updateVoiceStatus('🔇 AI Finished');
        // Restart listening after AI finishes speaking
        setTimeout(() => {
            startListening();
        }, 800);
    };
    
    utterance.onerror = function(event) {
        console.log('Speech synthesis error:', event.error);
        updateVoiceStatus('❌ Speech error');
        setTimeout(() => startListening(), 1000);
    };
    
    speechSynthesis.speak(utterance);
}

// ChatGPT-like voice recognition with better reliability
function initSpeechRecognition() {
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        recognition.maxAlternatives = 1;
        
        recognition.onstart = function() {
            updateVoiceStatus('🎤 Listening...');
        };
        
        recognition.onresult = function(event) {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    transcript += event.results[i][0].transcript;
                }
            }
            
            transcript = transcript.trim();
            if (transcript.length > 0) {
                updateVoiceStatus('Processing...');
                addMessage('You', transcript, 'user');
                
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'voice_message',
                        content: transcript
                    }));
                } else {
                    addMessage('System', 'Connection lost. Please restart session.', 'ai');
                }
            }
        };
        
        recognition.onerror = function(event) {
            console.log('Speech recognition error:', event.error);
            updateVoiceStatus('❌ Error: ' + event.error);
            
            // Auto-retry on certain errors
            if (event.error === 'no-speech' || event.error === 'audio-capture') {
                setTimeout(() => {
                    if (!speechSynthesis.speaking) {
                        startListening();
                    }
                }, 2000);
            }
        };
        
        recognition.onend = function() {
            isListening = false;
            updateVoiceStatus('🔇 Stopped');
            
            // Auto-restart after AI finishes speaking
            setTimeout(() => {
                if (!speechSynthesis.speaking && document.getElementById('sessionActive').style.display !== 'none') {
                    startListening();
                }
            }, 1500);
        };
    } else {
        addMessage('System', 'Voice recognition not supported. Use Chrome/Edge browser.', 'ai');
    }
}

// Update voice status display
function updateVoiceStatus(status) {
    const statusDiv = document.getElementById('voiceStatus');
    if (statusDiv) {
        statusDiv.textContent = status;
    }
}

// Start listening function with better error handling
function startListening() {
    if (!recognition) {
        updateVoiceStatus('❌ Voice not supported');
        return;
    }
    
    if (isListening) {
        return; // Already listening
    }
    
    if (speechSynthesis.speaking) {
        // Wait for AI to finish speaking
        setTimeout(() => startListening(), 1000);
        return;
    }
    
    try {
        recognition.start();
        isListening = true;
    } catch (error) {
        console.log('Recognition start error:', error);
        updateVoiceStatus('❌ Failed to start');
        
        // Retry after delay
        setTimeout(() => {
            if (!isListening && !speechSynthesis.speaking) {
                startListening();
            }
        }, 2000);
    }
}

// Start AI Session
function startAISession() {
    const title = document.getElementById('sessionTitle').value.trim();
    const description = document.getElementById('sessionDescription').value.trim();
    
    if (!title || !description) {
        alert('Please provide both title and description for the session.');
        return;
    }
    
    // Hide setup, show session
    document.getElementById('sessionSetup').style.display = 'none';
    document.getElementById('sessionActive').style.display = 'block';
    
    // Initialize components
    connectWebSocket();
    initSpeechRecognition();
    setupCamera();
    
    // Auto-start voice recognition after WebSocket connects
    if (ws) {
        ws.onopen = function() {
            ws.send(JSON.stringify({
                type: 'start_session',
                title: title,
                description: description
            }));
        };
    }
    
    // Start listening after AI gives initial response
    setTimeout(() => {
        addMessage('System', '🎤 Voice conversation active. Start speaking after AI finishes.', 'ai');
        setTimeout(() => {
            startListening();
        }, 3000);
    }, 1000);
    

}



// Stop voice recognition
function stopVoiceRecognition() {
    if (recognition && isListening) {
        recognition.stop();
        isListening = false;
    }
}

// End session
function endSession() {
    // Stop voice recognition
    stopVoiceRecognition();
    
    // Stop speech synthesis
    if (speechSynthesis.speaking) {
        speechSynthesis.cancel();
    }
    
    // Close WebSocket
    if (ws) {
        ws.close();
        ws = null;
    }
    
    // Stop camera
    if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
        localStream = null;
    }
    
    // Reset UI
    document.getElementById('sessionSetup').style.display = 'block';
    document.getElementById('sessionActive').style.display = 'none';
    document.getElementById('chatContainer').innerHTML = '';
    document.getElementById('sessionTitle').value = '';
    document.getElementById('sessionDescription').value = '';
}

// Chat functionality
function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (message && ws) {
        addMessage('You', message, 'user');
        ws.send(JSON.stringify({
            type: 'user_message',
            content: message
        }));
        input.value = '';
    }
}

function addMessage(sender, content, className) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${content}`;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Setup camera
async function setupCamera() {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true
        });
        
        document.getElementById('localVideo').srcObject = localStream;
        
    } catch (error) {
        console.error('Error accessing camera:', error);
        addMessage('System', 'Camera access denied. Voice chat will still work.', 'ai');
    }
}

async function handleWebRTCAnswer(sdp) {
    if (peerConnection) {
        await peerConnection.setRemoteDescription({
            type: 'answer',
            sdp: sdp
        });
    }
}

// Enter key support
document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Initialize
window.onload = function() {
    // Show setup form on load
};