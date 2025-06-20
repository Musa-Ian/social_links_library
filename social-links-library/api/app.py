from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import JSONResponse
import json
import re
from pathlib import Path
import os
from typing import Optional

app = FastAPI()

DATA_PATH = Path(__file__).parent.parent / 'data' / 'social_links.json'
API_KEY = os.getenv('API_KEY', 'changeme')  # Set your API key in environment

# --- Utility functions ---
def load_data():
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, 'w') as f:
        json.dump(data, f, indent=2)

# --- API Key Auth ---
def check_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")

# --- Endpoints ---
@app.get("/platforms")
def list_platforms():
    data = load_data()
    return [p["platform"] for p in data]

@app.get("/platforms/{platform}")
def get_platform(platform: str):
    data = load_data()
    for p in data:
        if p["platform"] == platform:
            return p
    raise HTTPException(status_code=404, detail="Platform not found")

@app.get("/platforms/{platform}/validate/{username}")
def validate_username(platform: str, username: str):
    data = load_data()
    for p in data:
        if p["platform"] == platform:
            regex = p["validation_regex"]
            if re.match(regex, username):
                return {"valid": True}
            else:
                return {"valid": False}
    raise HTTPException(status_code=404, detail="Platform not found")

@app.get("/platforms/{platform}/link/{username}")
def generate_link(platform: str, username: str):
    data = load_data()
    for p in data:
        if p["platform"] == platform:
            url = p["url_pattern"].replace("{username}", username)
            return {"url": url}
    raise HTTPException(status_code=404, detail="Platform not found")

@app.post("/platforms")
def add_platform(request: Request, x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    new_platform = request.json()
    data = load_data()
    if any(p["platform"] == new_platform["platform"] for p in data):
        raise HTTPException(status_code=400, detail="Platform already exists.")
    data.append(new_platform)
    save_data(data)
    return {"message": "Platform added."}

@app.put("/platforms/{platform}")
def update_platform(platform: str, request: Request, x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    update_data = request.json()
    data = load_data()
    for i, p in enumerate(data):
        if p["platform"] == platform:
            data[i] = update_data
            save_data(data)
            return {"message": "Platform updated."}
    raise HTTPException(status_code=404, detail="Platform not found") 