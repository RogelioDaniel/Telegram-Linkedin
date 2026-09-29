# Telegram → LinkedIn → Email

Bot de Telegram que recibe la captura de una oferta de LinkedIn, extrae los datos con un
modelo de visión (OpenRouter), arma un borrador de postulación con tu CV adjunto y lo envía
por SMTP **solo tras tu confirmación** con un botón.

## Ejecución local (polling)
```bash
pip install -r requirements.txt
python Bot.py
```
Crea un `.env` con las variables de la tabla. Sin `WEBHOOK_URL`/`RENDER_EXTERNAL_URL` el bot usa polling.

## Variables de entorno
| Variable | Obligatoria | Descripción |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | sí | Token de @BotFather |
| `TELEGRAM_ALLOWED_USER_ID` | sí | ID numérico del único usuario autorizado |
| `OPENROUTER_API_KEY` | sí | Clave de OpenRouter |
| `OPENROUTER_MODEL` | no | Modelo con visión (def. `openai/gpt-4o-mini`) |
| `MY_NAME`, `MY_EMAIL` | sí | Remitente |
| `MY_HEADLINE`, `MY_SKILLS` | no | Presentación y skills que se pueden afirmar en el correo |
| `CV_PATH` | sí | Ruta al PDF del CV |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` | no | Def. `smtp.office365.com`, `587`, `MY_EMAIL`. Hotmail/Outlook.com personal: `smtp-mail.outlook.com` |
| `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN` | las tres, o SMTP | Envío por Gmail API (HTTPS). **Obligatorio en Render free**, que bloquea SMTP saliente. Se generan con `get_gmail_token.py`. Tienen prioridad sobre SMTP |
| `SMTP_PASSWORD` | si no usas Gmail API | Contraseña de aplicación; solo para uso local |
| `WEBHOOK_URL` | no | URL pública; en Render se toma de `RENDER_EXTERNAL_URL` |
| `WEBHOOK_SECRET` | en webhook | Cualquier cadena de mínimo 16 caracteres (Render la genera sola) |

## Despliegue en Render (gratis)
1. El repo **debe ser privado** (el CV contiene datos personales). Añade el PDF con `git add -f cv.pdf`
   (`*.pdf` está en `.gitignore` para evitar subirlo por accidente) y llámalo igual que `CV_PATH`.
2. Render → **New → Blueprint** → elige el repo. Lee `render.yaml`.
3. Captura los secretos que Render pide (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USER_ID`,
   `OPENROUTER_API_KEY`, `SMTP_PASSWORD`). `WEBHOOK_SECRET` se genera solo.
4. Espera el deploy; en los logs debe aparecer `Bot en marcha (webhook en ...)`.

## Runbook
- **El bot tarda en responder:** plan free dormido; el primer mensaje tarda 30-60 s. Es normal.
- **No responde nada:** revisa logs en Render; confirma que `TELEGRAM_ALLOWED_USER_ID` es tu ID.
- **`Google OAuth 400 invalid_grant`:** el refresh token caducó o se revocó (app de Google Cloud en modo *Testing* caduca a los 7 días; publícala en *In production*). Repite `get_gmail_token.py` y actualiza `GMAIL_REFRESH_TOKEN`.
- **`Network is unreachable` al enviar:** SMTP bloqueado en Render free; usa Gmail API.
- **`535 Authentication unsuccessful`:** host SMTP incorrecto o contraseña de aplicación inválida.
- **Rotar credenciales:** BotFather `/revoke` (token), openrouter.ai/keys, contraseñas de aplicación
  de Microsoft; actualiza en Render → Environment (redeploy automático).
- **Volver a local:** ejecuta sin `RENDER_EXTERNAL_URL`; si el webhook sigue registrado en Telegram,
  el polling lo reemplaza al arrancar (`drop_pending_updates` en webhook; borra con `deleteWebhook` si falla).
