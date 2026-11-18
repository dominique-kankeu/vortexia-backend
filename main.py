# ---------------------------------------------------------
# ROUTE 3 : Studio IA (/ai) - Ultra-réactif et direct
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
                background: #0d162d;
                border: 1px solid #00f2fe;
                border-radius: 20px;
                padding: 20px;
                display: flex;
                flex-direction: column;
                height: 85vh;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
                padding-bottom: 10px;
            }
            .brand { color: #00f2fe; font-weight: bold; font-size: 16px; }
            .credits { color: #00f2fe; font-size: 12px; }
            .chat-box {
                flex: 1;
                background: #050814;
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 10px;
                overflow-y: auto;
                margin-bottom: 10px;
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .msg {
                padding: 8px 12px;
                border-radius: 8px;
                font-size: 13px;
                max-width: 85%;
                word-break: break-word;
            }
            .msg.user { background: rgba(0,242,254,0.2); color: #fff; align-self: flex-end; }
            .msg.ai { background: rgba(255,255,255,0.05); color: #8fa3bf; align-self: flex-start; }
            .input-area { display: flex; gap: 8px; }
            .prompt-input {
                flex: 1;
                padding: 10px;
                background: #050814;
                border: 1px solid #00f2fe;
                border-radius: 8px;
                color: #fff;
                font-size: 13px;
            }
            .btn-send {
                padding: 0 15px;
                background: #00f2fe;
                border: none;
                border-radius: 8px;
                color: #050814;
                font-weight: bold;
                cursor: pointer;
            }
            .back { text-align: center; margin-top: 5px; font-size: 11px; color: #00f2fe; text-decoration: none; display: block; }
        </style>
    </head>
    <body>
        <div class="studio-container">
            <div class="header">
                <div class="brand">VORTEXIA STUDIO</div>
                <div class="credits">⚡ <span id="cred">50.0</span> Crédits</div>
            </div>
            <div id="chat" class="chat-box">
                <div class="msg ai">Système prêt. Entrez votre description ci-dessous. (-5 crédits)</div>
            </div>
            <div class="input-area">
                <input type="text" id="prompt" class="prompt-input" placeholder="Ex: Une cinématique futuriste...">
                <button class="btn-send" onclick="send()">Envoyer</button>
            </div>
            <a href="#" class="back" onclick="history.back()">← Retour</a>
        </div>
        <script>
            let credits = 50.0;
            function send() {
                const input = document.getElementById('prompt');
                const text = input.value.trim();
                const chat = document.getElementById('chat');
                
                if (!text) {
                    alert("Veuillez saisir un prompt.");
                    return;
                }
                if (credits < 5.0) {
                    alert("Crédits insuffisants !");
                    return;
                }
                
                credits -= 5.0;
                document.getElementById('cred').innerText = credits.toFixed(1);
                
                // Affichage immédiat du message utilisateur
                const uMsg = document.createElement('div');
                uMsg.className = 'msg user';
                uMsg.innerText = text;
                chat.appendChild(uMsg);
                input.value = '';
                chat.scrollTop = chat.scrollHeight;

                // Réponse instantanée de l'IA du tac au tic
                setTimeout(() => {
                    const aMsg = document.createElement('div');
                    aMsg.className = 'msg ai';
                    aMsg.innerHTML = "✅ <b>Génération validée !</b> Flux cinématique prêt pour export HD.";
                    chat.appendChild(aMsg);
                    chat.scrollTop = chat.scrollHeight;
                }, 500);
            }
        </script>
    </body>
    </html>
    """
