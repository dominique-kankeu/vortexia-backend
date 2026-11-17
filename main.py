from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database import engine
import models
import routers.system
import routers.users
import routers.ads

# Crée les tables dans la base de données au démarrage
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vortexia AI Backend")

app.include_router(routers.system.router)
app.include_router(routers.users.router)
app.include_router(routers.ads.router)

# Route pour afficher l'écran d'Onboarding futuriste directement sur ton URL principale
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
                    // Utilise l'URL relative (fonctionne directement sur ton domaine Render)
                    const response = await window.location.origin + '/users/register';
                    const apiResponse = await fetch('/users/register', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            phone_number: phone,
                            referral_code: referral || null
                        })
                    });

                    const data = await apiResponse.json();

                    if (apiResponse.ok) {
                        alert(data.message + "\\nVos crédits actuels : " + data.credits + "\\nVotre code : " + (data.referral_code || 'N/A'));
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
