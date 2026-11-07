import os
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Get your secure API key from Render environment variables
GAMESDROP_API_KEY = os.getenv("GAMESDROP_API_KEY")
GAMESDROP_BASE_URL = "https://partner.gamesdrop.io"

@app.get("/")
def read_root():
    return {"status": "WildCore API is running live!"}

@app.post("/api/create-order")
def create_order(player_id: str, zone_id: str, product_code: str):
    headers = {
        "Authorization": f"Bearer {GAMESDROP_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "product_code": product_code,
        "player_id": player_id,
        "zone_id": zone_id
    }
    
    try:
        response = requests.post(f"{GAMESDROP_BASE_URL}/v1/orders", json=payload, headers=headers)
        
        if response.status_code not in [200, 201]:
            raise HTTPException(status_code=response.status_code, detail=response.json())
            
        return {
            "success": True,
            "message": "Order successfully processed by GamesDrop!",
            "supplier_response": response.json()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))