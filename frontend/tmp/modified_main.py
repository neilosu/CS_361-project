
# main.py
from datetime import date
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import httpx

app = FastAPI()

# Example vocabulary data
VOCABULARIES = {
    "2024-02-13": [
        {"word": "Ephemeral", "definition": "Lasting for a very short time.", "example": "Fashions are ephemeral."},
        {"word": "Pernicious", "definition": "Having a harmful effect, especially in a gradual or subtle way.", "example": "The pernicious influences of the mass media."},
        {"word": "Ameliorate", "definition": "Make (something bad or unsatisfactory) better.", "example": "The reform did much to ameliorate living standards."},
        {"word": "Obfuscate", "definition": "Render obscure, unclear, or unintelligible.", "example": "The spelling changes will deform some familiar words and obfuscate their etymological origins."},
        {"word": "Plethora", "definition": "A large or excessive amount of (something).", "example": "A plethora of committees and subcommittees."},
    ]
}

VOCABULARIES_DICT = {
    "Ephemeral": "Lasting for a very short time.",
    "Pernicious": "Having a harmful effect, especially in a gradual or subtle way.",
    "Ameliorate": "Make (something bad or unsatisfactory) better.",
    "Obfuscate": "Render obscure, unclear, or unintelligible.",
    "Plethora": "A large or excessive amount of (something)."
}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/today")
async def get_todays_vocabulary():
    today_str = date.today().isoformat()
    return {
        "date": today_str,
        "vocabularies": VOCABULARIES.get(today_str, [])
    }

@app.get("/search/{word}")
async def search_vocabulary(word: str):
    return {
        "word": word,
        "definition": VOCABULARIES_DICT.get(word, "Not found")
    }
