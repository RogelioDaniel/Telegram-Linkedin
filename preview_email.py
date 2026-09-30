#!/usr/bin/env python3
"""Genera preview.html con el correo de ejemplo, para ver el diseño sin enviar nada.

Uso:
    python preview_email.py            # usa los datos de tu .env
    python preview_email.py --open     # además lo abre en el navegador
"""
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
out.write_text(draft.html, encoding="utf-8")
print(f"Asunto: {draft.subject}\n\n{draft.body}\n\nVista previa HTML: {out}")
if "--open" in sys.argv:
    webbrowser.open(out.as_uri())
