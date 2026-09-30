#!/usr/bin/env python3
"""Genera preview.html con el correo de ejemplo, para ver el diseño sin enviar nada.

Uso:
    python preview_email.py            # usa los datos de tu .env
    python preview_email.py --open     # además lo abre en el navegador
"""
import base64
import os
import sys
import webbrowser
from pathlib import Path
from types import SimpleNamespace

from dotenv import load_dotenv

import Bot  # noqa: E402

load_dotenv()

cfg = SimpleNamespace(
    my_name=os.getenv("MY_NAME", "Rogelio Daniel"),
    my_email=os.getenv("MY_EMAIL", "tu_correo@gmail.com"),
    my_headline=os.getenv("MY_HEADLINE", "desarrollador de software"),
    my_skills=[s.strip() for s in os.getenv("MY_SKILLS", ".NET,React,SQL Server").split(",") if s.strip()],
    my_phone=os.getenv("MY_PHONE", ""),
    my_linkedin=os.getenv("MY_LINKEDIN", ""),
    my_github=os.getenv("MY_GITHUB", ""),
    my_whatsapp=os.getenv("MY_WHATSAPP", ""),
)
job = {
    "empresa": "VALTRE",
    "puesto": "Desarrollador Fullstack JR",
    "contacto": "Yareli Dariana Rodriguez Calderon",
    "modalidad": "Híbrido",
    "ubicacion": "Monterrey, N.L.",
    "requisitos": [".NET", "React", "Angular", "APIs REST", "Azure DevOps", "SQL Server"],
}
draft = Bot.build_draft(cfg, job, "reclutador@empresa.com")
out = Path(__file__).with_name("preview.html")
# En el correo real el GIF va incrustado (cid:); para verlo en el navegador se pasa a data URI.
page = draft.html
if Bot.WA_GIF.is_file():
    uri = "data:image/gif;base64," + base64.b64encode(Bot.WA_GIF.read_bytes()).decode()
    page = page.replace(f"cid:{Bot.WA_CID}", uri)
out.write_text(page, encoding="utf-8")
print(f"Asunto: {draft.subject}\n\n{draft.body}\n\nVista previa HTML: {out}")
if "--open" in sys.argv:
    webbrowser.open(out.as_uri())
