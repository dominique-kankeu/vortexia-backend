from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from database import engine
import models

# 1. INITIALISATION OBLIGATOIRE (DOIT ETRE EN HAUT)
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
    return {"message": "Publicité validée", "new_balance": 55.0}

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
        <title>Vortexia AI - Accès</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
            body { background: #050814; color: #fff; height: 100vh; display: flex; justify-content: center; align-items: center; }
            .container { width: 90%; max-width: 400px; padding: 30px; background: rgba(13, 22, 45, 0.8); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 20px; text-align: center; }
            .logo { font-size: 26px; font-weight: 800; color: #00f2fe; margin-bottom: 20px; text-transform: uppercase; }
            input { width: 100%; padding: 12px; background: #050814; border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; color: #fff; margin-bottom: 15px; font-size: 15px; }
            button { width: 100%; padding: 12px; background: #00f2fe; border: none; border-radius: 10px; color: #050814; font-weight: bold; cursor: pointer; text-transform: uppercase; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">Vortexia AI</div>
            <input type="tel" id="phone" placeholder="Numéro de téléphone...">
            <button onclick="reg()">Activer mon accès</button>
        </div>
        <script>
            async function reg() {
                const phone = document.getElementById('phone').value.trim();
                if (!phone) { alert("Entrez un numéro."); return; }
                const res = await fetch('/users/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ phone_number: phone })
                });
                if (res.ok) window.location.href = '/dashboard?phone=' + encodeURIComponent(phone);
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
        <title>Vortexia AI - Dashboard</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
            body { background: #050814; color: #fff; min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 15px; }
            .box { width: 100%; max-width: 400px; background: #0d162d; border: 1px solid #00f2fe; border-radius: 20px; padding: 20px; text-align: center; }
            .credits { font-size: 32px; font-weight: bold; color: #00f2fe; margin: 15px 0; }
            .btn { width: 100%; padding: 12px; background: #00f2fe; border: none; border-radius: 10px; color: #050814; font-weight: bold; cursor: pointer; margin-top: 10px; text-transform: uppercase; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2 style="color: #00f2fe;">Command Center</h2>
            <div class="credits" id="cred">50.0</div>
            <button class="btn" onclick="openStudio()">🚀 Ouvrir le Studio AI</button>
        </div>
        <script>
            const p = new URLSearchParams(window.location.search).get('phone') || '';
            function openStudio() { window.location.href = '/ai?phone=' + encodeURIComponent(p); }
        </script>
    </body>
    </html>
    """

# ---------------------------------------------------------
# ROUTE 3 : Studio IA (/ai) - Ultra-réactif avec Popup Modal
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
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
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
            
            /* Fenêtre Modale de Rendu */
            #modal { display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(5, 8, 20, 0.95); backdrop-filter: blur(10px); border-radius: 20px; z-index: 100; flex-direction: column; justify-content: center; align-items: center; padding: 20px; text-align: center; }
            .modal-content { background: #0d162d; border: 2px solid #00f2fe; border-radius: 15px; padding: 20px; width: 100%; }
            .preview { width: 100%; height: 160px; background: #050814; border: 1px dashed #00f2fe; border-radius: 10px; margin: 15px 0; display: flex; justify-content: center; align-items: center; color: #00f2fe; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="studio">
            <div class="header">
                <span style="color:#00f2fe; font-weight:bold;">VORTEXIA STUDIO</span>
                <span style="color:#00f2fe; font-size:12px;">⚡ <span id="cred">45.0</span> Crédits</span>
            </div>
            <div id="chat" class="chat">
                <div class="msg ai">Système prêt. Entrez votre description. (-5 crédits)</div>
            </div>
            <div class="input-area">
                <input type="text" id="prompt" placeholder="Décrivez votre visuel...">
                <button onclick="send()">Envoyer</button>
            </div>
            <a href="/dashboard" style="text-align:center; font-size:11px; color:#00f2fe; margin-top:5px; text-decoration:none;">← Tableau de bord</a>

            <!-- Pop-up Modal -->
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
            let credits = 45.0;
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
