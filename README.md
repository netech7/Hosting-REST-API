# VIT BFHL – FastAPI Solution (Python)

This repository contains a complete Python implementation of the **VIT BFHL** assignment using **FastAPI**.  
It satisfies the required POST `/bfhl` endpoint and response logic.

## ✅ What it does
- **POST** `/bfhl` receives a JSON body like:
  ```json
  { "data": ["a", "1", "334", "4", "R", "$"] }
  ```
- Returns:
  - `is_success` (boolean)
  - `user_id` in the format: `full_name_ddmmyyyy` (full name in lowercase, snake_case)
  - `email`, `roll_number`
  - `odd_numbers` (strings), `even_numbers` (strings)
  - `alphabets` (uppercase)
  - `special_characters`
  - `sum` (string)
  - `concat_string`: **all letter characters found in the input**, reversed, with **alternating caps** starting with **UPPER** (e.g., `"ByA"`)

### Classification rules
- **Alphabet** item: matches `^[A-Za-z]+$` → goes to `alphabets` **uppercased**.
- **Number** item: matches `^[+-]?\d+$` → goes to `odd_numbers` / `even_numbers` (kept as original string).
- **Special** item: if it is neither pure alpha nor pure number → goes to `special_characters` (this includes *mixed* alphanumeric like `"ab12"` and strings with special characters).  
- `sum` is the integer sum of all number items; returned as a **string**.

> This matches the examples in the paper and handles mixed strings gracefully.

## 🚀 Run locally

```bash
# 1) Create a virtualenv (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Set your identity (replace with your details)
export FULL_NAME="Nehal Jain"
export DOB_DDMMYYYY="01012000"
export EMAIL="nehal@example.com"
export ROLL_NUMBER="VITXXXX"

# 4) Start the server
uvicorn main:app --reload --port 8000
```

Send a request:
```bash
curl -X POST "http://127.0.0.1:8000/bfhl" \
  -H "Content-Type: application/json" \
  -d '{"data": ["a","1","334","4","R","$"]}'
```

## 🧪 Quick examples

**Example A**
```json
Request:
{ "data": ["a","1","334","4","R","$"] }

Response:
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": ["1"],
  "even_numbers": ["334","4"],
  "alphabets": ["A","R"],
  "special_characters": ["$"],
  "sum": "339",
  "concat_string": "Ra"
}
```

**Example B**
```json
Request:
{ "data": ["2","a","y","4","&","-","*","5","92","b"] }

Response:
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": ["5"],
  "even_numbers": ["2","4","92"],
  "alphabets": ["A","Y","B"],
  "special_characters": ["&","-","*"],
  "sum": "103",
  "concat_string": "ByA"
}
```

**Example C**
```json
Request:
{ "data": ["A","ABcD","DOE"] }

Response:
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": [],
  "even_numbers": [],
  "alphabets": ["A","ABCD","DOE"],
  "special_characters": [],
  "sum": "0",
  "concat_string": "EoDdCbAa"
}
```

> Tip: Set your own env vars (`FULL_NAME`, `DOB_DDMMYYYY`, `EMAIL`, `ROLL_NUMBER`) before running to personalize the response.

## 🌐 Deploy (Render — recommended)

1. Push this folder to a new **public GitHub repo**.
2. Create a **New Web Service** on [Render](https://render.com/), connect the repo.
3. Use:
   - **Runtime**: Python 3.x
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. Set environment variables in **Render → Settings → Environment**:
   - `FULL_NAME`, `DOB_DDMMYYYY`, `EMAIL`, `ROLL_NUMBER`
5. Once deployed, your endpoint will be:
   - `POST https://<your-service>.onrender.com/bfhl` (HTTP 200 on success)

## 🌐 Deploy (Railway)

1. Push to GitHub.
2. On [Railway](https://railway.app/), create a new project → **Deploy from GitHub**.
3. Set the **Start Command** to:  
   `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add the same environment variables.

## 🧾 Notes
- The service returns **HTTP 200** with `"is_success": true` on success. For unexpected errors, it returns a graceful JSON with `"is_success": false`.
- The `/` route just returns a health message.
- All number outputs (`even_numbers`, `odd_numbers`, `sum`) are **strings**, per the assignment.

---

Made with ❤️ using FastAPI.
