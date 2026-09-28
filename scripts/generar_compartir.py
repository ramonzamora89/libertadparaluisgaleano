"""Genera las imágenes para compartir (assets/img/compartir-es.png y -en.png).

Son las que muestran WhatsApp, X, Facebook, etc. al compartir el sitio
(og:image), de 1200×630. Si cambia la situación de Luis, se edita TEXTOS y
se corre:

    python3 scripts/generar_compartir.py

Después hay que subir el número de ?v= en el og:image de las 12 páginas:
las redes guardan la imagen en caché por URL y, sin eso, siguen mostrando
la vieja durante días.

Usa Georgia y Arial de macOS; es provisional hasta tener una pieza diseñada.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TEXTOS = {
    "es": {
        "hashtag": ("#LibertadPara", "LuisGaleano"),
        "titulo": ["Periodista nicaragüense", "en libertad"],
        "bajada": ["Libre desde el 26 de septiembre de 2026.",
                   "Enfrentará su proceso migratorio en libertad."],
    },
    "en": {
        "hashtag": ("#Free", "LuisGaleano"),
        "titulo": ["Nicaraguan journalist", "released from ICE"],
        "bajada": ["Free since September 26, 2026.",
                   "He will face his immigration case in freedom."],
    },
}

ANCHO, ALTO = 1200, 630
FONDO = (29, 29, 29)
ROJO = (218, 46, 44)
BLANCO = (255, 255, 255)
GRIS = (215, 215, 215)
FUENTES = Path("/System/Library/Fonts/Supplemental")
SALIDA = Path(__file__).resolve().parent.parent / "assets" / "img"


def fuente(nombre, tam):
    return ImageFont.truetype(str(FUENTES / nombre), tam)


def generar(idioma, t):
    im = Image.new("RGB", (ANCHO, ALTO), FONDO)
    d = ImageDraw.Draw(im)
    d.rectangle([0, ALTO - 24, ANCHO, ALTO], fill=ROJO)

    x, y = 110, 95
    f_hash = fuente("Arial Bold.ttf", 44)
    d.text((x, y), t["hashtag"][0], font=f_hash, fill=BLANCO)
    x2 = x + d.textlength(t["hashtag"][0], font=f_hash)
    d.text((x2, y), t["hashtag"][1], font=f_hash, fill=ROJO)

    y = 195
    f_tit = fuente("Georgia Bold.ttf", 78)
    for linea in t["titulo"]:
        d.text((x, y), linea, font=f_tit, fill=BLANCO)
        y += 94

    y += 25
    f_baj = fuente("Arial.ttf", 34)
    for linea in t["bajada"]:
        d.text((x, y), linea, font=f_baj, fill=GRIS)
        y += 46

    # Barra roja a la izquierda, del hashtag al final de la bajada.
    d.rectangle([70, 90, 81, y + 5], fill=ROJO)
    im.save(SALIDA / f"compartir-{idioma}.png", optimize=True)


if __name__ == "__main__":
    for idioma, t in TEXTOS.items():
        generar(idioma, t)
        print(f"assets/img/compartir-{idioma}.png")
