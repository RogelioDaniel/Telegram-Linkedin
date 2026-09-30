# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [Unreleased]
### Added
- Modo webhook para desplegar en Render (plan gratuito) con secreto de validación.
- `render.yaml`, `README.md` con runbook y variables de entorno.

- Envío de correo por Gmail API (HTTPS), con SMTP como alternativa local, y `get_gmail_token.py` para obtener el refresh token.

- Extracción de la captura con varios proveedores de visión (Gemini, Groq, OpenRouter) y respaldo automático si uno falla.

- Proveedores de visión adicionales (GitHub Models, Mistral, NVIDIA NIM) y reintento de la cadena completa con aviso en el chat y botón «Reintentar».

- Correo en HTML con firma profesional y versión de texto plano; `preview_email.py` para previsualizarlo.

### Fixed
- Reintentos con espera ante 429/5xx en proveedores de visión, varios modelos por proveedor y log con el motivo real del error.
- `WEBHOOK_SECRET` en base64 (generado por Render) ya no se rechaza.

### Changed
- `python-telegram-bot` ahora con el extra `[webhooks]`.
