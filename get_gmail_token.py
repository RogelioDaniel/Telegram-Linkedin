#!/usr/bin/env python3
"""Obtiene el refresh token de Gmail API (se ejecuta UNA vez, en tu PC).

Uso:
    pip install google-auth-oauthlib
    python get_gmail_token.py ruta/al/client_secret.json

Abre el navegador para que autorices el permiso ``gmail.send`` (solo enviar, no leer
correos) e imprime las tres variables que debes pegar en Render. No guarda nada en disco.
"""
import json
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    secret_file = sys.argv[1]
    flow = InstalledAppFlow.from_client_secrets_file(secret_file, SCOPES)
    # access_type=offline + prompt=consent garantizan que Google devuelva refresh_token.
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    if not creds.refresh_token:
        sys.exit("Google no devolvió refresh_token. Revoca el acceso previo y reintenta.")
    with open(secret_file, encoding="utf-8") as f:
        client = json.load(f)
    client = client.get("installed") or client.get("web")
    print("\nPega estas variables en Render (Environment):\n")
    print(f"GMAIL_CLIENT_ID={client['client_id']}")
    print(f"GMAIL_CLIENT_SECRET={client['client_secret']}")
    print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")


if __name__ == "__main__":
    main()
