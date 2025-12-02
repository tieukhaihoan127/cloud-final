import json
from flask import Flask, jsonify, request
import time, requests, os
from jose import jwt

# External issuer (cho token validation)
ISSUER = os.getenv("OIDC_ISSUER", "http://localhost:8081/realms/realm_sv001")
AUDIENCE = os.getenv("OIDC_AUDIENCE", "account")

# Internal JWKS URL (để lấy public keys từ Keycloak)
JWKS_URL = os.getenv("JWKS_URL", "http://authentication-identity-server:8080/realms/realm_sv001/protocol/openid-connect/certs")

_JWKS = None
_TS = 0

def get_jwks():
    global _JWKS, _TS
    now = time.time()
    if not _JWKS or now - _TS > 600:
        try:
            print(f"Fetching JWKS from: {JWKS_URL}")
            response = requests.get(JWKS_URL, timeout=5)
            print(f"JWKS Response Status: {response.status_code}")
            _JWKS = response.json()
            _TS = now
            print("JWKS fetched successfully")
        except Exception as e:
            print(f"Error fetching JWKS: {e}")
            raise
    return _JWKS

app = Flask(__name__)

@app.get("/hello")
def hello():
    return jsonify(message="Hello from App Server!")

@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401
    token = auth.split(" ",1)[1]
    try:
        payload = jwt.decode(token, get_jwks(), algorithms=["RS256"], 
                           audience=AUDIENCE, issuer=ISSUER)
        return jsonify(message="Secure resource OK",
                       preferred_username=payload.get("preferred_username"))
    except Exception as e:
        print(f"Token validation error: {e}")
        return jsonify(error=str(e)), 401
    
@app.get("/student")
def student():
    with open("students.json") as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)