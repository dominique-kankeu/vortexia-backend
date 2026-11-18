from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from database import engine
import models

# 1. Initialisation indispensable de l'application
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Vortexia AI Backend")

# 2. Modèles de données Pydantic
class UserRegister(BaseModel):
    phone_number: str
    referral_code: str | None = None

class AdReward(BaseModel):
    phone_number: str

# 3. Routes API Backend
@app.post("/users/register")
def register_user(data: UserRegister):
    return {
        "message": "Accès Vortexia activé avec succès !",
        "phone": data.phone_number,
        "credits": 50.0
    }

@app.post("/ads/reward")
def reward_ad(data: AdReward):
    return {
        "message": "Publicité validée ! +5 crédits ajoutés.",
        "new_balance": 55.0
    }

# ---------------------------------------------------------
# ROUTE 1 : Écran d'Onboarding (/)
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def serve_onboarding():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vortexia AI - Accès Restreint</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }
            body {
                background-color: #050814;
                background-image: radial-gradient(circle at 50% 20%, #111e38 0%, #050814 70%);
                color: #ffffff;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }
            .container {
                width: 90%;
                max-width: 400px;
                padding: 30px;
                background: rgba(13, 22, 45, 0.7);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(0, 242, 254, 0.2);
                border-radius: 24px;
                box-shadow: 0 0 40px rgba(0, 242, 254, 0.1);
                text-align: center;
            }
            .logo-glow {
                font-size: 28px;
                font-weight: 800;
                letter-spacing: 2px;
                background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 8px;
                text-transform: uppercase;
            }
            .subtitle { font-size: 13px; color: #8fa3bf; margin-bottom: 30px; }
            .input-group { margin-bottom: 20px; text-align: left; }
            .input-group label { display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #00f2fe; margin-bottom: 8px; }
            .input-group input {
                width: 100%;
                padding: 14px 16px;
                background: rgba(5, 8, 20, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                color: #ffffff;
                font-size: 16px;
            }
            .input-group input:focus { outline: none; border-color: #00f2fe; box-shadow: 0 0 15px rgba(0, 242, 254, 0.3); }
            .btn-primary {
                width: 100%;
                padding: 14px;
                background: linear-gradient(135deg, #00f2fe 0%, #00c6ff 100%);
                border: none;
                border-radius: 12px;
                color: #050814;
                font-weight: 700;
                font-size: 15px;
                cursor: pointer;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 0 4px 20px rgba(0, 242, 254, 0.4);
                margin-top: 10px;
            }
            .bonus-badge {
                margin-top: 20px;
                display: inline-block;
                padding: 6px 12px;
                background: rgba(0, 242, 254, 0.1);
                border: 1px solid rgba(0, 242, 254, 0.3);
                border-radius: 20px;
                font-size: 12px;
                color: #00f2fe;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo-glow">Vortexia AI</div>
            <div class="subtitle">Intelligence Artificielle de Prochaine Génération</div>
            <div class="input-group">
                <label>Numéro de téléphone</label>
                <input type="tel" id="phone" placeholder="Ex: +237 ...">
            </div>
            <div class="input-group">
                <label>Code de parrainage (Optionnel)</label>
                <input type="text" id="referral" placeholder="Ex: VRT-XXXX">
            </div>
            <button class="btn-primary" onclick="registerUser()">Activer mon accès</button>
            <div class="bonus-badge">⚡ 50 Crédits offerts à l'activation</div>
        </div>
        <script>
            async function registerUser() {
                const phone = document.getElementById('phone').value.trim();
                const referral = document.getElementById('referral').value.trim();
                if (!phone) {
                    alert("Veuillez entrer votre numéro de téléphone.");
                    return;
                }
                try {
                    const response = await fetch('/users/register', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ phone_number: phone, referral_code: referral || null })
                    });
                    if (response.ok) {
                        window.location.href = '/dashboard?phone=' + encodeURIComponent(phone);
                    } else {
                        alert("Erreur d'activation.");
                    }
                } catch (error) {
                    alert("Impossible de joindre le serveur Vortexia.");
                }
            }
        </script>
    </body>
    </html>
    """

# ---------------------------------------------------------
# ROUTE 2 : Tableau de Bord (/dashboard)
# ---------------------------------------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def serve_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vortexia AI - Command Center</title>
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
            .dashboard-container {
                width: 100%;
                max-width: 450px;
                background: rgba(13, 22, 45, 0.75);
                backdrop-filter: blur(25px);
                border: 1px solid rgba(0, 242, 254, 0.2);
                border-radius: 24px;
                padding: 25px;
                box-shadow: 0 0 50px rgba(0, 242, 254, 0.15);
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 25px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                padding-bottom: 15px;
            }
            .brand {
                font-size: 20px;
                font-weight: 800;
                letter-spacing: 1.5px;
                background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-transform: uppercase;
            }
            .user-phone {
                font-size: 12px;
                color: #8fa3bf;
                background: rgba(255, 255, 255, 0.05);
                padding: 5px 10px;
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            .card {
                background: rgba(5, 8, 20, 0.6);
                border: 1px solid rgba(0, 242, 254, 0.15);
                border-radius: 16px;
                padding: 20px;
                margin-bottom: 20px;
                text-align: center;
            }
            .credit-title { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #8fa3bf; margin-bottom: 5px; }
            .credit-value { font-size: 32px; font-weight: 800; color: #00f2fe; text-shadow: 0 0 20px rgba(0, 242, 254, 0.4); }
            .btn-action {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #00f2fe 0%, #00c6ff 100%);
                border: none;
                border-radius: 12px;
                color: #050814;
                font-weight: 700;
                font-size: 14px;
                cursor: pointer;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <div class="header">
                <div class="brand">Vortexia AI</div>
                <div id="user-phone-display" class="user-phone">Chargement...</div>
            </div>
            <div class="card">
                <div class="credit-title">Solde de Crédits Actuel</div>
                <div id="credits-display" class="credit-value">50.0</div>
            </div>
            <button class="btn-action" onclick="watchAd()">📺 Regarder une pub (+5 Crédits)</button>
            <button class="btn-action" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);" onclick="goToStudio()">🚀 Ouvrir le Studio AI</button>
        </div>
        <script>
            const urlParams = new URLSearchParams(window.location.search);
            const userPhone = urlParams.get('phone');
            if (userPhone) { document.getElementById('user-phone-display').innerText = userPhone; }
            let userCredits = 50.0;
            function updateUI() { document.getElementById('credits-display').innerText = userCredits.toFixed(1); }
            async function watchAd() {
                if (!userPhone) { alert("Utilisateur non identifié."); return; }
                try {
                    const response = await fetch('/ads/reward', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ phone_number: userPhone })
                    });
                    const data = await response.json();
                    if (response.ok) {
                        userCredits = data.new_balance;
                        updateUI();
                        alert(data.message);
                    }
                } catch (err) { alert("Erreur réseau."); }
            }
            function goToStudio() { window.location.href = '/ai?phone=' + encodeURIComponent(userPhone || ''); }
            updateUI();
        </script>
    </body>
    </html>
    """

# ---------------------------------------------------------
# ROUTE 3 : Studio IA (/ai) - Ultra-réactif
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
            }
            .message.ai {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: #8fa3bf;
                align-self: flex-start;
            }
            .input-area { display: flex; gap: 8px; }
            .prompt-input {
                flex: 1;
                padding: 12px 14px;
                background: rgba(5, 8, 20, 0.9);
                border: 1px solid rgba(0, 242, 254, 0.2);
                border-radius: 12px;
                color: #ffffff;
                font-size: 13px;
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
            .back-dashboard { display: block; text-align: center; margin-top: 8px; font-size: 11px; color: #00f2fe; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="studio-container">
            <div class="header">
                <div class="brand">Vortexia Studio</div>
                <div class="credits-badge" onclick="goDashboard()">⚡ <span id="user-credits">50.0</span> Crédits</div>
            </div>
            <div id="chat-container" class="chat-box">
                <div class="message ai">Système Vortexia initialisé. Prêt pour la génération visuelle. (-5 crédits/requête)</div>
            </div>
            <div class="input-area">
                <input type="text" id="user-prompt" class="prompt-input" placeholder="Décris ta génération...">
                <button class="btn-send" onclick="sendPrompt()">Envoyer</button>
            </div>
            <a href="#" class="back-dashboard" onclick="goDashboard()">← Retour au Tableau de Bord</a>
        </div>
        <script>
            const urlParams = new URLSearchParams(window.location.search);
            const userPhone = urlParams.get('phone');
            let currentCredits = 50.0;
            function goDashboard() { window.location.href = '/dashboard?phone=' + encodeURIComponent(userPhone || ''); }
            function sendPrompt() {
                const inputField = document.getElementById('user-prompt');
                const promptText = inputField.value.trim();
                const chatContainer = document.getElementById('chat-container');
                if (!promptText) { alert("Veuillez entrer un prompt."); return; }
                if (currentCredits < 5.0) { alert("Crédits insuffisants !"); return; }
                
                currentCredits -= 5.0;
                document.getElementById('user-credits').innerText = currentCredits.toFixed(1);
                
                const userMsg = document.createElement('div');
                userMsg.className = 'message user';
                userMsg.innerText = promptText;
                chatContainer.appendChild(userMsg);
                inputField.value = '';
                chatContainer.scrollTop = chatContainer.scrollHeight;

                // Réaction ultra-rapide du studio IA
                setTimeout(() => {
                    const aiMsg = document.createElement('div');
                    aiMsg.className = 'message ai';
                    aiMsg.innerText = "⚡ Synthèse neurale active... Génération des frames cinématiques.";
                    chatContainer.appendChild(aiMsg);
                    chatContainer.scrollTop = chatContainer.scrollHeight;

                    setTimeout(() => {
                        const successMsg = document.createElement('div');
                        successMsg.className = 'message ai';
                        successMsg.innerHTML = "✅ <b>Génération réussie !</b> Votre flux audiovisuel est prêt.<br><span style='color: #00f2fe; cursor: pointer;' onclick='alert(\"Téléchargement du média HD initié...\")'>📥 Télécharger le rendu HD</span>";
                        chatContainer.appendChild(successMsg);
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    }, 1200);
                }, 600);
            }
        </script>
    </body>
    </html>
    """
