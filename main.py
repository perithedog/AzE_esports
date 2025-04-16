from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from datetime import datetime

# 👉 Reemplaza por tus valores reales
SUPABASE_URL = "https://xapdpjzmdcuqnabhtrxf.supabase.co"
SUPABASE_KEY = "TU_ANON_KEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# CORS para frontend (Vercel, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada
class Player(BaseModel):
    puuid: str
    gameName: str
    tagLine: str

@app.get("/data")
def get_data():
    response = supabase.table("players").select("*").execute()
    return response.data

@app.post("/data")
def add_player(player: Player):
    nuevo_jugador = {
        "puuid": player.puuid,
        "gameName": player.gameName,
        "tagLine": player.tagLine,
        "created": datetime.utcnow().isoformat()
    }
    supabase.table("players").insert(nuevo_jugador).execute()
    return {"message": "Jugador guardado", "data": nuevo_jugador}

@app.delete("/data/{puuid}")
def delete_player(puuid: str):
    result = supabase.table("players").delete().eq("puuid", puuid).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"message": f"Jugador con puuid {puuid} eliminado."}