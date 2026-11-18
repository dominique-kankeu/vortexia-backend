# ---------------------------------------------------------
# ROUTE 3 : Le Studio d'Intelligence Artificielle (/ai)
# ---------------------------------------------------------
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
                padding: 15px;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .studio-container {
                width: 100%;
                max-width: 480px;
                background: rgba(13, 22, 45, 0.85);
                backdrop-filter: blur(25px);
                border: 1px solid rgba(0, 242, 254, 0.2);
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 0 40px rgba(0, 242, 254, 0.15);
                display: flex;
                flex-direction: column;
                height: 88vh;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                padding-bottom: 12px;
            }
            .brand {
                font-size: 16px;
                font-weight: 800;
                letter-spacing: 1.5px;
                background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-transform: uppercase;
            }
            .credits-badge {
                font-size: 11px;
                color: #00f2fe;
                background: rgba(0, 242, 254, 0.1);
                padding: 5px 10px;
                border-radius: 20px;
                border: 1px solid rgba(0, 242, 254, 0.3);
                font-weight: 700;
                cursor: pointer;
            }
            .chat-box {
                flex: 1;
                background: rgba(5, 8, 20, 0.75);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 12px;
                overflow-y: auto;
                margin-bottom: 12px;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .message {
                padding: 10px 14px;
                border-radius: 10px;
                font-size: 13px;
                line-height: 1.4;
                max-width: 85%;
                word-break: break-word;
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
                gap: 8px;
            }
            .prompt-input {
                flex: 1;
                padding: 12px 14px;
                background: rgba(5, 8, 20, 0.9);
                border: 1px solid rgba(0, 242, 254, 0.2);
                border-radius: 12px;
                color: #ffffff;
                font-size: 13px;
            }
            .prompt-input:focus {
                outline: none;
                border-color: #00f2fe;
                box-shadow: 0 0 12px rgba(0, 242, 254, 0.3);
            }
            .btn-send {
                padding: 0 16px;
                background: linear-gradient(135deg, #00f2fe 0%, #00c6ff 100%);
                border: none;
                border-radius: 12px;
                color: #050814;
                font-weight: 700;
                cursor: pointer;
                text-transform: uppercase;
                font-size: 12px;
                box-shadow: 0 4px 12px rgba(0, 242, 254, 0.3);
            }
            .cost-notice {
                font-size: 9px;
                color: #8fa3bf;
                text-align: center;
                margin-top: 6px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .back-dashboard {
                display: block;
                text-align: center;
                margin-top: 8px;
                font-size: 11px;
                color: #00f2fe;
                text-decoration: none;
            }
            .back-dashboard:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="studio-container">
            <div class="header">
                <div class="brand">Vortexia Studio</div>
                <div class="credits-badge" onclick="goDashboard()">⚡ <span id="user-credits">50.0</span> Crédits</div>
            </div>

            <!-- Zone d'échange avec l'IA -->
            <div id="chat-container" class="chat-box">
                <div class="message ai">Système Vortexia initialisé. Prêt pour la génération visuelle. (-5 crédits/requête)</div>
            </div>

            <!-- Formulaire de saisie -->
            <div class="input-area">
                <input type="text" id="user-prompt" class="prompt-input" placeholder="Décris ta génération...">
                <button class="btn-send" onclick="sendPrompt()">Envoyer</button>
            </div>
            <div class="cost-notice">Coût par requête : 5.0 Crédits</div>
            <a href="#" class="back-dashboard" onclick="goDashboard()">← Retour au Tableau de Bord</a>
        </div>

        <script>
            const urlParams = new URLSearchParams(window.location.search);
            const userPhone = urlParams.get('phone');
            let currentCredits = 50.0;

            function goDashboard() {
                window.location.href = '/dashboard?phone=' + encodeURIComponent(userPhone || '');
            }

            function sendPrompt() {
                const inputField = document.getElementById('user-prompt');
                const promptText = inputField.value.trim();
                const chatContainer = document.getElementById('chat-container');

                if (!promptText) {
                    alert("Veuillez entrer un prompt.");
                    return;
                }

                if (currentCredits < 5.0) {
                    alert("Crédits insuffisants !");
                    return;
                }

                // Déduction des crédits
                currentCredits -= 5.0;
                document.getElementById('user-credits').innerText = currentCredits.toFixed(1);

                // Affichage du message utilisateur
                const userMsg = document.createElement('div');
                userMsg.className = 'message user';
                userMsg.innerText = promptText;
                chatContainer.appendChild(userMsg);

                inputField.value = '';
                chatContainer.scrollTop = chatContainer.scrollHeight;

                // Simulation de la réponse de l'IA neuronale
                setTimeout(() => {
                    const aiMsg = document.createElement('div');
                    aiMsg.className = 'message ai';
                    aiMsg.innerText = "Synthèse neurale en cours pour : \"" + promptText + "\"\\n[Modèle cinématique activé - Rendu en file d'attente]";
                    chatContainer.appendChild(aiMsg);
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }, 800);
            }
        </script>
    </body>
    </html>
    """
