from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from database import engine
import models

# 1. INITIALISATION OBLIGATOIRE
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Vortexia AI Backend")

# 2. MODÈLES DE DONNÉES
class UserRegister(BaseModel):
    phone_number: str
    referral_code: str | None = None

class AdReward(BaseModel):
    phone_number: str

# 3. ROUTES API BACKEND
@app.post("/users/register")
def register_user(data: UserRegister):
    return {"message": "Succès", "phone": data.phone_number, "credits": 50.0}

@app.post("/ads/reward")
def reward_ad(data: AdReward):
    return {"message": "Publicité validée ! +5 crédits ajoutés.", "new_balance": 55.0}

# ---------------------------------------------------------
# ROUTE 1 : Onboarding (/)
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
# ROUTE 2 : Tableau de Bord (/dashboard) - Complet et stylé
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
                padding: 14px;
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
                margin-top: 12px;
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
            function goToStudio() { 
                window.location.href = '/ai?phone=' + encodeURIComponent(userPhone || ''); 
            }
            updateUI();
        </script>
    </body>
    </html>
    """

# ---------------------------------------------------------
# ROUTE 3 : Studio IA (/ai) - Avec pop-up modal de rendu
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
            body { background: #050814; color: #fff; height: 100vh; display: flex; justify-content: center; align-items: center; padding: 10px; }
            .studio { width: 100%; max-width: 450px; background: #0d162d; border: 1px solid #00f2fe; border-radius: 20px; padding: 15px; display: flex; flex-direction: column; height: 90vh; position: relative; }
            .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 10px; }
            .chat { flex: 1; background: #050814; border-radius: 10px; padding: 10px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; margin-bottom: 10px; }
            .msg { padding: 8px 12px; border-radius: 8px; font-size: 13px; max-width: 85%; word-break: break-word; }
            .msg.user { background: rgba(0,242,254,0.2); align-self: flex-end; }
            .msg.ai { background: rgba(255,255,255,0.05); color: #8fa3bf; align-self: flex-start; }
            .input-area { display: flex; gap: 8px; }
            input { flex: 1; padding: 10px; background: #050814; border: 1px solid #00f2fe; border-radius: 8px; color: #fff; font-size: 13px; }
            button { padding: 0 15px; background: #00f2fe; border: none; border-radius: 8px; color: #050814; font-weight: bold; cursor: pointer; }
            
            #modal { display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(5, 8, 20, 0.95); backdrop-filter: blur(10px); border-radius: 20px; z-index: 100; flex-direction: column; justify-content: center; align-items: center; padding: 20px; text-align: center; }
            .modal-content { background: #0d162d; border: 2px solid #00f2fe; border-radius: 15px; padding: 20px; width: 100%; }
            .preview { width: 100%; height: 160px; background: #050814; border: 1px dashed #00f2fe; border-radius: 10px; margin: 15px 0; display: flex; justify-content: center; align-items: center; color: #00f2fe; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="studio">
            <div class="header">
                <span style="color:#00f2fe; font-weight:bold;">VORTEXIA STUDIO</span>
                <span style="color:#00f2fe; font-size:12px; cursor:pointer;" onclick="goDashboard()">⚡ <span id="cred">45.0</span> Crédits</span>
            </div>
            <div id="chat" class="chat">
                <div class="msg ai">Système prêt. Entrez votre description. (-5 crédits)</div>
            </div>
            <div class="input-area">
                <input type="text" id="prompt" placeholder="Décrivez votre visuel...">
                <button onclick="send()">Envoyer</button>
            </div>
            <a href="#" style="text-align:center; font-size:11px; color:#00f2fe; margin-top:5px; text-decoration:none;" onclick="goDashboard()">← Tableau de bord</a>

            <div id="modal">
                <div class="modal-content">
                    <h3 style="color: #00f2fe; margin-bottom: 5px;">Rendu Audiovisuel Prêt</h3>
                    <p style="font-size: 12px; color: #8fa3bf;" id="modal-txt">...</p>
                    <div class="preview">🎬 Aperçu Média HD</div>
                    <button onclick="closeModal()" style="width:100%; padding:10px; background:#00f2fe; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">Fermer</button>
                </div>
            </div>
        </div>

        <script>
            const urlParams = new URLSearchParams(window.location.search);
            const userPhone = urlParams.get('phone');
            let credits = 45.0;

            function goDashboard() { 
                window.location.href = '/dashboard?phone=' + encodeURIComponent(userPhone || ''); 
            }

            function send() {
                const input = document.getElementById('prompt');
                const text = input.value.trim();
                const chat = document.getElementById('chat');
                if (!text) { alert("Entrez un prompt."); return; }
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
                    aMsg.innerHTML = "✅ <b>Génération réussie !</b> Cliquez pour voir le rendu.";
                    aMsg.style.cursor = "pointer";
                    aMsg.onclick = () => openModal(text);
                    chat.appendChild(aMsg);
                    chat.scrollTop = chat.scrollHeight;
                    
                    openModal(text);
                }, 400);
            }

            function openModal(t) {
                document.getElementById('modal-txt').innerText = "Prompt : \\"" + t + "\\"";
                document.getElementById('modal').style.display = 'flex';
            }
            function closeModal() {
                document.getElementById('modal').style.display = 'none';
            }
        </script>
    </body>
    </html>
    """
