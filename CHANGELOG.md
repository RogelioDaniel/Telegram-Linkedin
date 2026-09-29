# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [Unreleased]
### Added
- Modo webhook para desplegar en Render (plan gratuito) con secreto de validación.
- `render.yaml`, `README.md` con runbook y variables de entorno.

- Envío de correo por la API HTTP de Brevo (`BREVO_API_KEY`), con SMTP como alternativa local.

### Fixed
- `WEBHOOK_SECRET` en base64 (generado por Render) ya no se rechaza.

### Changed
- `python-telegram-bot` ahora con el extra `[webhooks]`.
