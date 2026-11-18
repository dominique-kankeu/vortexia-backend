from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class VideoRequest(BaseModel):
    prompt: str

@app.post("/api/generate-video")
async def generate_video(request: VideoRequest):
    try:
        # Ici, on traite le prompt envoyé par l'utilisateur (ex: "Une jeune fille blonde à la plage")
        user_prompt = request.prompt
        
        # Si tu utilises une API externe de génération ou une simulation pour le moment :
        # On s'assure de renvoyer un objet JSON propre avec le statut et l'URL/ID du média
        return {
            "status": "success",
            "message": "Vidéo générée avec succès",
            "prompt": user_prompt,
            "video_url": "https://example.com/generated-video.mp4" # Remplace par le lien ou le résultat réel
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
