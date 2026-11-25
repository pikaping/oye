"""Obtiene un token de LinkedIn para el workflow. Ejecútalo en tu ordenador:

    python scripts/linkedin_auth.py <CLIENT_ID> <CLIENT_SECRET>

En tu app de LinkedIn, añade http://localhost:8765/callback como Authorized redirect URL.
El token dura unos 60 días: vuelve a ejecutarlo cuando caduque y actualiza el secreto LINKEDIN_TOKEN.
"""
import http.server
import json
import secrets
import sys
import urllib.parse
import urllib.request
import webbrowser

REDIRECT = "http://localhost:8765/callback"
SCOPES = "openid profile w_member_social"


def main() -> None:
    client_id, client_secret = sys.argv[1], sys.argv[2]
    state = secrets.token_urlsafe(16)
    url = "https://www.linkedin.com/oauth/v2/authorization?" + urllib.parse.urlencode({
        "response_type": "code", "client_id": client_id, "redirect_uri": REDIRECT,
        "state": state, "scope": SCOPES,
    })
    result = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            result.update({k: v[0] for k, v in query.items()})
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Listo. Puedes cerrar esta ventana.".encode())

        def log_message(self, *args):
            pass

    print("Abriendo LinkedIn para autorizar la app…")
    webbrowser.open(url)
    http.server.HTTPServer(("localhost", 8765), Handler).handle_request()

    if result.get("state") != state or "code" not in result:
        sys.exit(f"Autorización fallida: {result}")

    data = urllib.parse.urlencode({
        "grant_type": "authorization_code", "code": result["code"], "redirect_uri": REDIRECT,
        "client_id": client_id, "client_secret": client_secret,
    }).encode()
    with urllib.request.urlopen("https://www.linkedin.com/oauth/v2/accessToken", data=data) as resp:
        token = json.loads(resp.read())
    print("\nGuarda esto como secreto LINKEDIN_TOKEN en GitHub (no lo compartas):\n")
    print(token["access_token"])
    print(f"\nCaduca en {token['expires_in'] // 86400} días.")


if __name__ == "__main__":
    main()
