from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Permitir llamadas desde el frontend en Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/data")
def get_data():
    df = pd.DataFrame({
        "Nombre": ["Ana", "Luis", "Sofía"],
        "Edad": [23, 34, 29]
    })
    return df.to_dict(orient="records")