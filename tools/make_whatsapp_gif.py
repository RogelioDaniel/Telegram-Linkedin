#!/usr/bin/env python3
"""Genera assets/whatsapp_button.gif: botón de WhatsApp con un pulso suave.

Gmail elimina el CSS animado, pero sí reproduce GIFs animados, por eso el botón es una
imagen. El primer y el último fotograma son el botón completo y estático (Outlook solo
muestra el primero) y el pulso se repite unas pocas veces para no distraer.

Uso (solo al rediseñar el botón; el resultado se versiona en el repo):
    pip install pillow
    python tools/make_whatsapp_gif.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCALE = 2  # se dibuja al doble y el correo lo muestra a 240x48 (nítido en pantallas retina)
W, H = 240 * SCALE, 48 * SCALE
NAVY = (0x1F, 0x3A, 0x5F)
GREEN = (0x25, 0xD3, 0x66)
WHITE = (255, 255, 255)
LABEL = "Escríbeme por WhatsApp"
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\segoeui.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]
OUT = Path(__file__).resolve().parent.parent / "assets" / "whatsapp_button.gif"


def _font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    raise SystemExit("No encontré una fuente TrueType; añade una ruta a FONT_CANDIDATES.")


def _mix(color: tuple, alpha: float) -> tuple:
    """Mezcla el color con blanco (los GIF no tienen transparencia parcial)."""
    return tuple(round(255 - (255 - c) * alpha) for c in color)


def frame(pulse: float) -> Image.Image:
    """Dibuja un fotograma; ``pulse`` va de 0 (sin anillo) a 1 (anillo más grande y tenue)."""
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((2, 2, W - 3, H - 3), radius=H // 2 - 2, fill=WHITE, outline=NAVY, width=2)

    cx, cy, r = 27 * SCALE, H // 2, 11 * SCALE
    if 0 < pulse < 1:  # anillo que se expande y se desvanece
        rr = r + pulse * 7 * SCALE
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=_mix(GREEN, 0.75 * (1 - pulse)), width=2 * SCALE)

    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GREEN)
    # globo de chat blanco con tres puntos
    d.ellipse((cx - 7 * SCALE, cy - 7 * SCALE, cx + 7 * SCALE, cy + 5 * SCALE), fill=WHITE)
    d.polygon([(cx - 6 * SCALE, cy + 3 * SCALE), (cx - 8 * SCALE, cy + 8 * SCALE), (cx - 1 * SCALE, cy + 5 * SCALE)], fill=WHITE)
    for dx in (-3, 0, 3):
        x = cx + dx * SCALE
        d.ellipse((x - 1 * SCALE, cy - 2 * SCALE, x + 1 * SCALE, cy), fill=GREEN)

    font = _font(15 * SCALE)
    box = d.textbbox((0, 0), LABEL, font=font)
    d.text((48 * SCALE, (H - (box[3] - box[1])) / 2 - box[1]), LABEL, font=font, fill=NAVY)
    return img


def main() -> None:
    steps = 12
    frames = [frame(0)] + [frame((i + 1) / (steps + 1)) for i in range(steps)] + [frame(0)]
    durations = [1500] + [80] * steps + [1500]
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=64) for f in frames]
    OUT.parent.mkdir(exist_ok=True)
    # loop=4: pulsa cuatro veces y se queda quieto (no distrae ni molesta a quien lee).
    pal[0].save(OUT, save_all=True, append_images=pal[1:], duration=durations, loop=4, optimize=False, disposal=2)
    print(f"{OUT} ({OUT.stat().st_size / 1024:.1f} KB, {len(frames)} fotogramas)")


if __name__ == "__main__":
    main()
