# ---------------------------------------------------------
# ROUTE 3 : Studio IA (/ai) avec ouverture visuelle instantanée
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
                position: relative;
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
            .msg.ai { background: rgba(255,255,255,0.05); color: #8fa3bf; align-self: flex-start; cursor: pointer; }
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
            
            /* Fenêtre Modale (Popup de rendu) */
            #modal {
                display: none;
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(5, 8, 20, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                z-index: 100;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 20px;
                text-align: center;
            }
            .modal-content {
                background: #0d162d;
                border: 2px solid #00f2fe;
                border-radius: 15px;
                padding: 20px;
                width: 100%;
                box-shadow: 0 0 30px rgba(0, 242, 254, 0.4);
            }
            .preview-box {
                width: 100%;
                height: 180px;
                background: #050814;
                border-radius: 10px;
                margin: 15px 0;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #00f2fe;
                font-weight: bold;
                border: 1px dashed rgba(0, 242, 254, 0.4);
            }
            .btn-close {
                padding: 10px 20px;
                background: #00f2fe;
                border: none;
                border-radius: 8px;
                color: #050814;
                font-weight: bold;
                cursor: pointer;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="studio-container">
            <div class="header">
                <div class="brand">VORTEXIA STUDIO</div>
                <div class="credits">⚡ <span id="cred">45.0</span> Crédits</div>
            </div>
            <div id="chat" class="chat-box">
                <div class="msg ai">Système prêt. Entrez votre description ci-dessous. (-5 crédits)</div>
            </div>
            <div class="input-area">
                <input type="text" id="prompt" class="prompt-input" placeholder="Ex: Une cinématique futuriste...">
                <button class="btn-send" onclick="send()">Envoyer</button>
            </div>
            <a href="#" class="back" onclick="history.back()">← Retour</a>

            <!-- Fenêtre Pop-up de Rendu -->
            <div id="modal">
                <div class="modal-content">
                    <h3 style="color: #00f2fe; margin-bottom: 5px;">Rendu Audiovisuel Prêt</h3>
                    <p style="font-size: 12px; color: #8fa3bf;" id="modal-prompt-text">...</p>
                    <div class="preview-box">🎬 [Aperçu Vidéo / Image HD]</div>
                    <button class="btn-close" onclick="closeModal()">Fermer & Continuer</button>
                </div>
            </div>
        </div>

        <script>
            let credits = 45.0;
            function send() {
                const input = document.getElementById('prompt');
                const text = input.value.trim();
                const chat = document.getElementById('chat');
                
                if (!text) { alert("Veuillez saisir un prompt."); return; }
                if (credits < 5.0) { alert("Crédits insuffisants !"); return; }
                
                credits -= 5.0;
                document.getElementById('cred').innerText = credits.toFixed(1);
                
                const uMsg = document.createElement('div');
                uMsg.className = 'msg user';
                uMsg.innerText = text;
                chat.appendChild(uMsg);
                input.value = '';
                chat.scrollTop = chat.scrollHeight;

                setTimeout(() => {
                    const aMsg = document.createElement('div');
                    aMsg.className = 'msg ai';
                    aMsg.innerHTML = "✅ <b>Génération validée !</b> <u style='color:#00f2fe;'>Cliquez ici pour ouvrir le rendu HD.</u>";
                    aMsg.onclick = () => openModal(text);
                    chat.appendChild(aMsg);
                    chat.scrollTop = chat.scrollHeight;
                    
                    openModal(text);
                }, 500);
            }

            function openModal(promptText) {
                document.getElementById('modal-prompt-text').innerText = "Prompt : \\"" + promptText + "\\"";
                document.getElementById('modal').style.display = 'flex';
            }

            function closeModal() {
                document.getElementById('modal').style.display = 'none';
            }
        </script>
    </body>
    </html>
    """
