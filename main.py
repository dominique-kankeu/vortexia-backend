from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from database import engine
import models

# Crée les tables dans la base de données au démarrage
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vortexia AI Backend")

# Modèles Pydantic pour les requêtes API
class UserRegister(BaseModel):
    phone_number: str
    referral_code: str | None = None

class AdReward(BaseModel):
    phone_number: str

# ---------------------------------------------------------
# ROUTES API (Utilisateurs et Publicités)
# ---------------------------------------------------------
@app.post("/users/register")
def register_user(data: UserRegister):
    # Logique d'inscription simplifiée avec 50 crédits offerts
    return {
        "message": "Accès Vortexia activé avec succès !",
        "phone": data.phone_number,
        "credits": 50.0
    }

@app.post("/ads/reward")
def reward_ad(data: AdReward):
    # Ajout de +5 crédits après pub
    return {
        "message": "Publicité validée ! +5 crédits ajoutés.",
        "new_balance": 55.0
    }

# ---------------------------------------------------------
# ROUTE 1 : L'écran d'Onboarding futuriste (Page d'accueil /)
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
                        body: JSON.stringify({
                            phone_number: phone,
                            referral_code: referral || null
                        })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        window.location.href = '/dashboard?phone=' + encodeURIComponent(phone);
                    } else {
                        alert("Erreur : " + (data.detail || "Une erreur est survenue"));
                    }
                } catch (error) {
                    console.error("Erreur :", error);
                    alert("Impossible de joindre le serveur Vortexia.");
                }
            }
        </script>
    </body>
    </html>
    """

# ---------------------------------------------------------
# ROUTE 2 : Le Tableau de Bord & Gamification (/dashboard)
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
                position: relative;
                overflow: hidden;
            }
            .card::before {
                content: '';
                position: absolute;
                top: 0; left: 0; width: 4px; height: 100%;
                background: linear-gradient(to bottom, #00f2fe, #4facfe);
            }
            .credit-title {
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 1px;
                color: #8fa3bf;
                margin-bottom: 5px;
            }
            .credit-value {
                font-size: 32px;
                font-weight: 800;
                color: #00f2fe;
                text-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
            }
            .section-title {
                font-size: 13px;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .progress-bar-bg {
                width: 100%;
                height: 10px;
                background: rgba(255, 255, 255, 0.08);
                border-radius: 5px;
                overflow: hidden;
                margin: 10px 0;
            }
            .progress-bar-fill {
                width: 0%;
                height: 100%;
                background: linear-gradient(90deg, #00f2fe, #00c6ff);
                box-shadow: 0 0 10px #00f2fe;
                transition: width 0.5s ease;
            }
            .referral-box {
                display: flex;
                gap: 10px;
                margin-top: 10px;
            }
            .referral-input {
                flex: 1;
                background: rgba(5, 8, 20, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                color: #00f2fe;
                padding: 10px;
                text-align: center;
                font-weight: 700;
                letter-spacing: 1px;
            }
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
                transition: all 0.3s ease;
                margin-top: 10px;
            }
            .btn-action:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
            }
            .info-text {
                font-size: 11px;
                color: #8fa3bf;
                text-align: center;
                margin-top: 8px;
            }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <div class="header">
                <div class="brand">Vortexia AI</div>
                <div id="user-phone-display" class="user-phone">Chargement...</div>
            </div>

            <!-- Solde de Crédits -->
            <div class="card">
                <div class="credit-title">Solde de Crédits Actuel</div>
                <div id="credits-display" class="credit-value">50.0</div>
            </div>

            <!-- Système de Parrainage & Gamification -->
            <div class="card" style="text-align: left;">
                <div class="section-title">
                    <span>Programme Viral</span>
                    <span id="referral-count-text" style="color: #00f2fe;">0 / 5 amis</span>
                </div>
                <p class="info-text" style="text-align: left; margin-bottom: 8px;">Parraine 5 amis pour débloquer <strong>100 crédits bonus</strong> !</p>
                
                <div class="progress-bar-bg">
                    <div id="progress-fill" class="progress-bar-fill" style="width: 0%;"></div>
                </div>

                <div class="referral-box">
                    <input type="text" id="my-referral-code" class="referral-input" readonly value="VRT-DOM">
                    <button class="btn-action" style="margin-top:0; width: auto; padding: 0 15px;" onclick="copyCode()">Copier</button>
                </div>
            </div>

            <!-- Bouton Publicité & Accès Studio AI -->
            <button class="btn-action" onclick="watchAd()">📺 Regarder une pub (+5 Crédits)</button>
            <button class="btn-action" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); margin-top: 10px;" onclick="goToStudio()">🚀 Ouvrir le Studio AI</button>
        </div>

        <script>
            const urlParams = new URLSearchParams(window.location.search);
            const userPhone = urlParams.get('phone');

            if (userPhone) {
                document.getElementById('user-phone-display').innerText = userPhone;
            }

            let userCredits = 50.0;
            let referralCount = 0;

            function updateUI() {
                document.getElementById('credits-display').innerText = userCredits.toFixed(1);
                document.getElementById('referral-count-text').innerText = referralCount + " / 5 amis";
                const percentage = (referralCount / 5) * 100;
                document.getElementById('progress-fill').style.width = percentage + "%";
            }

            async function watchAd() {
                if (!userPhone) {
                    alert("Utilisateur non identifié.");
                    return;
                }
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
                    } else {
                        alert("Erreur serveur publicité.");
                    }
                } catch (err) {
                    alert("Erreur de connexion.");
                }
            }

            function copyCode() {
                const codeInput = document.getElementById('my-referral-code');
                navigator.clipboard.writeText(codeInput.value);
                alert("Code de parrainage copié !");
            }

            function goToStudio() {
                window.location.href = '/ai?phone=' + encodeURIComponent(userPhone || '');
            }

            updateUI();
        </script>
    </body>
    </html>
    """

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
                cursor: pointer;
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
            .back-dashboard {
                display: block;
                text-align: center;
                margin-top: 10px;
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
                <div class="message ai">Système Vortexia initialisé. Comment puis-je propulser ton projet aujourd'hui ? (-5 crédits/génération)</div>
            </div>

            <!-- Formulaire de saisie -->
            <div class="input-area">
                <input type="text" id="user-prompt" class="prompt-input" placeholder="Écris ton prompt ici...">
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

                if (!promptText) return;

                if (currentCredits < 5.0) {
                    alert("Crédits insuffisants ! Regarde une publicité ou parraine des amis pour recharger.");
                    return;
                }

                currentCredits -= 5.0;
                document.getElementById('user-credits').innerText = currentCredits.toFixed(1);

                const userMsg = document.createElement('div');
                userMsg.className = 'message user';
                userMsg.innerText = promptText;
                chatContainer.appendChild(userMsg);

                inputField.value = '';
                chatContainer.scrollTop = chatContainer.scrollHeight;

                setTimeout(() => {
                    const aiMsg = document.createElement('div');
                    aiMsg.className = 'message ai';
                    aiMsg.innerText = "Analyse neurale en cours... Résultat optimisé pour : \"" + promptText + "\" [Génération réussie]";
                    chatContainer.appendChild(aiMsg);
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }, 1000);
            }
        </script>
    </body>
    </html>
    """
