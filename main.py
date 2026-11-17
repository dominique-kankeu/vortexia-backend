# Route 3 : Le Studio d'Intelligence Artificielle (Génération & Consommation de crédits)
@app.get("/ai", response_class=HTMLResponse)
def serve_ai_studio():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vortexia AI - Neural Studio</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }
            body {
                background-color: #050814;
                background-image: radial-gradient(circle at 50% 10%, #111e38 0%, #050814 80%);
                color: #ffffff;
                min-height: 100vh;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .studio-container {
                width: 100%;
                max-width: 500px;
                background: rgba(13, 22, 45, 0.8);
                backdrop-filter: blur(25px);
                border: 1px solid rgba(0, 242, 254, 0.2);
                border-radius: 24px;
                padding: 25px;
                box-shadow: 0 0 50px rgba(0, 242, 254, 0.15);
                display: flex;
                flex-direction: column;
                height: 85vh;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                padding-bottom: 15px;
            }
            .brand {
                font-size: 18px;
                font-weight: 800;
                letter-spacing: 1.5px;
                background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-transform: uppercase;
            }
            .credits-badge {
                font-size: 12px;
                color: #00f2fe;
                background: rgba(0, 242, 254, 0.1);
                padding: 6px 12px;
                border-radius: 20px;
                border: 1px solid rgba(0, 242, 254, 0.3);
                font-weight: 700;
            }
            .chat-box {
                flex: 1;
                background: rgba(5, 8, 20, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 15px;
                overflow-y: auto;
                margin-bottom: 15px;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            .message {
                padding: 12px 16px;
                border-radius: 12px;
                font-size: 14px;
                line-height: 1.4;
                max-width: 85%;
            }
            .message.user {
                background: rgba(0, 242, 254, 0.15);
                border: 1px solid rgba(0, 242, 254, 0.3);
                color: #ffffff;
                align-self: flex-end;
                border-bottom-right-radius: 2px;
            }
            .message.ai {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: #8fa3bf;
                align-self: flex-start;
                border-bottom-left-radius: 2px;
            }
            .input-area {
                display: flex;
                gap: 10px;
            }
            .prompt-input {
                flex: 1;
                padding: 14px 16px;
                background: rgba(5, 8, 20, 0.9);
                border: 1px solid rgba(0, 242, 254, 0.2);
                border-radius: 14px;
                color: #ffffff;
                font-size: 14px;
            }
            .prompt-input:focus {
                outline: none;
                border-color: #00f2fe;
                box-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
            }
            .btn-send {
                padding: 0 20px;
                background: linear-gradient(135deg, #00f2fe 0%, #00c6ff 100%);
                border: none;
                border-radius: 14px;
                color: #050814;
                font-weight: 700;
                cursor: pointer;
                text-transform: uppercase;
                box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
                transition: all 0.3s ease;
            }
            .btn-send:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
            }
            .cost-notice {
                font-size: 10px;
                color: #8fa3bf;
                text-align: center;
                margin-top: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        </style>
    </head>
    <body>
        <div class="studio-container">
            <div class="header">
                <div class="brand">Vortexia Studio</div>
                <div class="credits-badge">⚡ <span id="user-credits">50.0</span> Crédits</div>
            </div>

            <!-- Zone d'échange avec l'IA -->
            <div id="chat-container" class="chat-box">
                <div class="message ai">Système Vortexia initialisé. Comment puis-je propulser ton projet aujourd'hui ? (-5 crédits/génération)</div>
            </div>

            <!-- Formulaire de saisie -->
            <div class="input-area">
                <input type="text" id="user-prompt" class="prompt-input" placeholder="Écris ton prompt ici...">
                <button class="btn-send" onclick="sendPrompt()">Envoyer</button>
            </div>
            <div class="cost-notice">Coût par requête : 5.0 Crédits</div>
        </div>

        <script>
            let currentCredits = 50.0;

            function sendPrompt() {
                const inputField = document.getElementById('user-prompt');
                const promptText = inputField.value.trim();
                const chatContainer = document.getElementById('chat-container');

                if (!promptText) return;

                if (currentCredits < 5.0) {
                    alert("Crédits insuffisants ! Regarde une publicité ou parraine des amis pour recharger.");
                    return;
                }

                // Déduire les crédits (simulation front + appel API futur)
                currentCredits -= 5.0;
                document.getElementById('user-credits').innerText = currentCredits.toFixed(1);

                // Afficher le message de l'utilisateur
                const userMsg = document.createElement('div');
                userMsg.className = 'message user';
                userMsg.innerText = promptText;
                chatContainer.appendChild(userMsg);

                inputField.value = '';
                chatContainer.scrollTop = chatContainer.scrollHeight;

                // Simuler la réponse de l'IA après 1 seconde
                setTimeout(() => {
                    const aiMsg = document.createElement('div');
                    aiMsg.className = 'message ai';
                    aiMsg.innerText = "Analyse neurale en cours... Voici les résultats optimisés pour ta requête : \"" + promptText + "\" [Génération réussie]";
                    chatContainer.appendChild(aiMsg);
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }, 1000);
            }
        </script>
    </body>
    </html>
    """
