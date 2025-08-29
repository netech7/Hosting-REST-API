# FastAPI implementation for VIT BFHL assignment
# Run locally: uvicorn main:app --reload --port 8000
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, List, Dict
import os
import re

app = FastAPI(title="VIT BFHL API", version="1.0.0")

# Allow all origins (adjust for production if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration via env vars (fill these with your details)
FULL_NAME = os.getenv("FULL_NAME", "john doe")  # will be normalized to lowercase snake_case
DOB_DDMMYYYY = os.getenv("DOB_DDMMYYYY", "17091999")
EMAIL = os.getenv("EMAIL", "john@xyz.com")
ROLL_NUMBER = os.getenv("ROLL_NUMBER", "ABCD123")

def snake_lower(name: str) -> str:
    # Lowercase, replace non-alnum with underscores, collapse multiple underscores
    s = re.sub(r'[^a-z0-9]+', '_', name.strip().lower())
    s = re.sub(r'_+', '_', s).strip('_')
    return s

def is_alpha(s: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z]+", s))

def is_int_string(s: str) -> bool:
    return bool(re.fullmatch(r"[+-]?\d+", s))

def is_special_only(s: str) -> bool:
    return bool(re.fullmatch(r"[^A-Za-z0-9]+", s))

def alternating_caps_reverse(chars: List[str]) -> str:
    # reverse the list and apply alternating case starting with UPPER, then lower, etc.
    rev = list(reversed(chars))
    out_chars = []
    for i, ch in enumerate(rev):
        out_chars.append(ch.upper() if i % 2 == 0 else ch.lower())
    return "".join(out_chars)

class InputModel(BaseModel):
    data: List[Any]

@app.get("/")
async def root():
    return {"message": "BFHL API is up. POST your payload to /bfhl"}

@app.post("/bfhl")
async def bfhl(payload: InputModel):
    try:
        items = payload.data

        even_numbers: List[str] = []
        odd_numbers: List[str] = []
        alphabets: List[str] = []
        special_characters: List[str] = []
        letter_chars_in_input: List[str] = []
        total_sum = 0

        for item in items:
            s = str(item)

            # collect all alphabetical characters from the raw input items (for concat_string)
            letter_chars_in_input.extend(re.findall(r"[A-Za-z]", s))

            if is_alpha(s):
                alphabets.append(s.upper())
            elif is_int_string(s):
                # keep original string form in outputs
                n = int(s)
                (even_numbers if n % 2 == 0 else odd_numbers).append(s)
                total_sum += n
            elif is_special_only(s):
                special_characters.append(s)
            else:
                # mixed (alphanumeric or contains specials + others) -> treat as special bucket per spec interpretation
                special_characters.append(s)

        concat_string = alternating_caps_reverse(letter_chars_in_input)

        user_id = f"{snake_lower(FULL_NAME)}_{DOB_DDMMYYYY}"
        response: Dict[str, Any] = {
            "is_success": True,
            "user_id": user_id,
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_characters,
            "sum": str(total_sum),
            "concat_string": concat_string,
        }
        return response
    except Exception as e:
        # Return graceful error with is_success false, 200 status (per assignment's emphasis on 200 for success paths)
        return {
            "is_success": False,
            "user_id": f"{snake_lower(FULL_NAME)}_{DOB_DDMMYYYY}",
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "error": str(e),
            "odd_numbers": [],
            "even_numbers": [],
            "alphabets": [],
            "special_characters": [],
            "sum": "0",
            "concat_string": "",
        }
