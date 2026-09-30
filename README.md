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
| `GEMINI_API_KEY` | al menos una de las 3 | Clave de Google AI Studio (tier gratuito) |
| `GROQ_API_KEY` | al menos una de las 3 | Clave de Groq (tier gratuito) |
| `OPENROUTER_API_KEY` | al menos una de las 3 | Clave de OpenRouter (los modelos sin sufijo `:free` son de pago) |
| `VISION_ORDER` | no | Orden de proveedores; si uno falla se usa el siguiente (def. `gemini,groq,openrouter`) |
| `GEMINI_MODEL`, `GROQ_MODEL` | no | Lista de modelos con visión separados por coma, probados en orden (def. `gemini-2.5-flash,gemini-2.5-flash-lite` y `meta-llama/llama-4-scout-17b-16e-instruct,meta-llama/llama-4-maverick-17b-128e-instruct`). Si un proveedor retira un modelo (404), sustitúyelo aquí |
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
   `GEMINI_API_KEY`/`GROQ_API_KEY`/`OPENROUTER_API_KEY` y las de Gmail). `WEBHOOK_SECRET` se genera solo.
4. Espera el deploy; en los logs debe aparecer `Bot en marcha (webhook en ...)`.

## Runbook
- **El bot tarda en responder:** plan free dormido; el primer mensaje tarda 30-60 s. Es normal.
- **No responde nada:** revisa logs en Render; confirma que `TELEGRAM_ALLOWED_USER_ID` es tu ID.
- **Visión `404` (modelo inexistente) / `503` (saturado):** los 5xx y 429 se reintentan solos; un 404 pasa al siguiente modelo. El log muestra el motivo devuelto por la API.
- **`402 Payment Required` (OpenRouter):** sin saldo; el bot pasa al siguiente proveedor de `VISION_ORDER`. Añade `GEMINI_API_KEY` o `GROQ_API_KEY`.
- **`Google OAuth 400 invalid_grant`:** el refresh token caducó o se revocó (app de Google Cloud en modo *Testing* caduca a los 7 días; publícala en *In production*). Repite `get_gmail_token.py` y actualiza `GMAIL_REFRESH_TOKEN`.
- **`Network is unreachable` al enviar:** SMTP bloqueado en Render free; usa Gmail API.
- **`535 Authentication unsuccessful`:** host SMTP incorrecto o contraseña de aplicación inválida.
- **Rotar credenciales:** BotFather `/revoke` (token), openrouter.ai/keys, contraseñas de aplicación
  de Microsoft; actualiza en Render → Environment (redeploy automático).
- **Volver a local:** ejecuta sin `RENDER_EXTERNAL_URL`; si el webhook sigue registrado en Telegram,
  el polling lo reemplaza al arrancar (`drop_pending_updates` en webhook; borra con `deleteWebhook` si falla).
