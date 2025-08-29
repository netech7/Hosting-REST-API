# quick local test (run after starting uvicorn)
import requests, json

url = "http://127.0.0.1:8000/bfhl"
payloads = {
    "A": {"data": ["a","1","334","4","R","$"]},
    "B": {"data": ["2","a","y","4","&","-","*","5","92","b"]},
    "C": {"data": ["A","ABcD","DOE"]},
}

for k, v in payloads.items():
    r = requests.post(url, json=v)
    print(f"\nCase {k}: {r.status_code}")
    print(json.dumps(r.json(), indent=2))
