#!/usr/bin/env python3
"""Push Google cookies to the Railway token."""
import urllib.request
import json
import ssl

BASE = "https://flow2api-production-a990.up.railway.app"

GOOGLE_COOKIES = (
    "__Secure-1PAPISID=hdcA6aEO6UqaWKhs/AvKARk8wZCHjg0Vdt"
    ";__Secure-1PSID=g.a0008Qgkh3dfOT4_JZY6u1kP66-ICUdtNVA0aksTmChooff3rrBOgf_kbU0Y9fG5Ha0CAYes6QACgYKAb4SARESFQHGX2MipcfDTu2xcVQYh-pJQDdrYhoVAUF8yKojx-hbKUF3_DC2I19i-ihF0076"
    ";__Secure-1PSIDCC=AKEyXzUP9dWPzfhfnUh1Y3p2Ai-3DQdHZyu7bSYvpJzfd02a8Q9pFtOZPzWAEOo4ZUTXexfwAQ"
    ";__Secure-1PSIDTS=sidts-CjIBWhotCVarXXVr1zALv1OQ1HfR3PnblODevU4IerGy_czk0cxJ8OYczbhnXZz5CsyZ2RAA"
    ";__Secure-3PAPISID=hdcA6aEO6UqaWKhs/AvKARk8wZCHjg0Vdt"
    ";__Secure-3PSID=g.a0008Qgkh3dfOT4_JZY6u1kP66-ICUdtNVA0aksTmChooff3rrBO_3dKRnaT2mUICsOy8H5RtAACgYKARYSARESFQHGX2MirjS2297xvLXcTgvToy_MbRoVAUF8yKr0Ht0NxJB9uN4xdpPRqo1_0076"
    ";__Secure-3PSIDCC=AKEyXzVWOO4cRgMIg1-Nnky4nOe4rdVADdGc8MXn8zlbY4LfKqD5qhMgCWczl10moUO0bupkl8I"
    ";__Secure-3PSIDTS=sidts-CjIBWhotCVarXXVr1zALv1OQ1HfR3PnblODevU4IerGy_czk0cxJ8OYczbhnXZz5CsyZ2RAA"
    ";APISID=YqglpK5_JoT9alHZ/ATNe3PVcP7bm5FxWZ"
    ";HSID=Anuije3SxovDDubub"
    ";SAPISID=hdcA6aEO6UqaWKhs/AvKARk8wZCHjg0Vdt"
    ";SID=g.a0008Qgkh3dfOT4_JZY6u1kP66-ICUdtNVA0aksTmChooff3rrBOgBeVbomm-Llx4bjzXvPfywACgYKAX0SARESFQHGX2MiAehtqYjb7jUuWXqc08ZdYhoVAUF8yKq3LrXnyDSKQHpJNhW-4DD10076"
    ";SIDCC=AKEyXzVPOZEKHFPLeNfHuQclY7m72Ga9RLSe0T-kiMroXwrgq6QRXGoG5RpCrcQVSRcG9-qdCPo"
    ";SSID=AhqN5kcHF5HR0vOHq"
)


def req(method, path, data=None, session=None):
    ctx = ssl.create_default_context()
    ctx.load_verify_locations(ssl.get_default_verify_paths().cafile or
                              "/etc/ssl/cert.pem")
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    headers = {"Content-Type": "application/json"}
    if session:
        headers["Authorization"] = f"Bearer {session}"
    payload = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(BASE + path, data=payload, headers=headers, method=method)
    with urllib.request.urlopen(r, timeout=60, context=ctx) as resp:
        return json.loads(resp.read().decode())


# 1. Login
print("Logging in...")
login = req("POST", "/api/admin/login", {"username": "admin", "password": "admin"})
session = login["token"]
print(f"  session={session[:20]}...")

# 2. Get token list
print("Getting token list...")
tokens = req("GET", "/api/tokens", session=session)
token_id = tokens[0]["id"]
print(f"  token_id={token_id}, email={tokens[0].get('email','?')}")

# 3. Push cookies
print(f"Uploading Google cookies to token {token_id}...")
result = req("PATCH", f"/api/tokens/{token_id}/google-cookies",
             {"google_cookies": GOOGLE_COOKIES}, session=session)
print(f"  result={result}")

# 4. Score test
print("\nRunning score test (personal mode)... this takes ~25-45s")
score = req("POST", "/api/captcha/score-test", {"captcha_method": "personal"}, session=session)
print(json.dumps(score, indent=2, ensure_ascii=False))
