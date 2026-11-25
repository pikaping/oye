"""Publica en LinkedIn el post de hoy (posts/AAAA-MM-DD.md) si está en estado `ready`.

Variables de entorno:
  LINKEDIN_TOKEN    token OAuth con los scopes openid, profile y w_member_social
  LINKEDIN_VERSION  opcional, versión YYYYMM de la API (por defecto, la de hace dos meses)
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

API = "https://api.linkedin.com"


def api_version() -> str:
    if os.environ.get("LINKEDIN_VERSION"):
        return os.environ["LINKEDIN_VERSION"]
    today = dt.date.today()
    month = today.month - 2
    year = today.year
    if month < 1:
        month += 12
        year -= 1
    return f"{year}{month:02d}"


def request(method: str, path: str, token: str, body: dict | None = None):
    req = urllib.request.Request(API + path, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("LinkedIn-Version", api_version())
    req.add_header("X-Restli-Protocol-Version", "2.0.0")
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, data=data) as resp:
        return resp.status, resp.headers, resp.read().decode() or "{}"


def escape_little_text(text: str) -> str:
    # LinkedIn interpreta estos caracteres en `commentary`; sin escapar, el post se corta.
    return re.sub(r"([\\|{}@\[\]()<>#*_~])", r"\\\1", text)


def parse(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not match:
        sys.exit(f"{path} no tiene cabecera --- válida")
    meta = dict(line.split(":", 1) for line in match.group(1).splitlines() if ":" in line)
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    return meta, match.group(2).strip()


def main() -> None:
    token = os.environ["LINKEDIN_TOKEN"]
    path = Path("posts") / f"{dt.date.today().isoformat()}.md"
    if not path.exists():
        print(f"No hay post para hoy ({path}). Nada que publicar.")
        return
    meta, text = parse(path)
    if meta.get("status") != "ready":
        print(f"El post está en estado '{meta.get('status')}'. No se publica.")
        return

    _, _, body = request("GET", "/v2/userinfo", token)
    author = f"urn:li:person:{json.loads(body)['sub']}"

    status, headers, _ = request("POST", "/rest/posts", token, {
        "author": author,
        "commentary": escape_little_text(text),
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    })
    post_id = headers.get("x-restli-id", "")
    print(f"Publicado ({status}): {post_id}")

    raw = path.read_text(encoding="utf-8").replace("status: ready", f"status: published\nlinkedin_id: {post_id}", 1)
    path.write_text(raw, encoding="utf-8")


if __name__ == "__main__":
    main()
