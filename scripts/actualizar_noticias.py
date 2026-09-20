#!/usr/bin/env python3
"""Genera las tarjetas de prensa del sitio a partir de un Google Sheet.

El Sheet se publica como CSV (Archivo › Compartir › Publicar en la web ›
CSV) y su dirección se pasa en la variable de entorno NOTICIAS_SHEET_URL.
Para probar sin red: --csv scripts/noticias-semilla.csv

Columnas del Sheet (el orden no importa; solo Publicar y Autor son opcionales):

    Fecha     2026-09-17  ·  también acepta 17/09/2026 y 9/17/2026
    Medio     The Guardian
    Titular   el titular tal como lo publicó el medio, en su idioma
    Enlace    https://…
    Autor     Timothy Pratt  ·  vacío si la nota no lleva firma
    Idioma    ES o EN  ·  el idioma de la nota, no el de la página
    Publicar  no / false / 0 esconde la fila; vacío o sí la publica

El script escribe data/noticias.json (archivo de respaldo) y reemplaza el
bloque entre <!-- noticias:inicio --> y <!-- noticias:fin --> en las cuatro
listas del sitio. No toca nada fuera de esos marcadores. Si algo cambió,
refresca además «Última actualización» en el pie de las 12 páginas y los
<lastmod> del sitemap.

Si el Sheet no responde o no deja ninguna fila válida, el script aborta sin
escribir: más vale dejar las noticias viejas que vaciar el sitio.
"""

import argparse, csv, html, json, os, pathlib, re, sys, unicodedata, urllib.request
from datetime import date

RAIZ = pathlib.Path(__file__).resolve().parent.parent

MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
            "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
MESES_EN = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]

# archivo, idioma de la página, etiqueta de la marca de idioma, nivel del
# titular (la portada va bajo un <h2> de sección, así que sus tarjetas usan
# <h3>), y cuántas tarjetas entran.
DESTINOS = [
    ("noticias/index.html",             "es", "Idioma",   "h2", None),
    ("english/in-the-news/index.html",  "en", "Language", "h2", None),
    ("index.html",                      "es", "Idioma",   "h3", 3),
    ("english/index.html",              "en", "Language", "h3", 3),
]

PIE_ES = re.compile(r"(Última actualización: )[^.<]+")
PIE_EN = re.compile(r"(Last updated: )[^.<]+")


def clave(nombre):
    """«Última fecha» y «ultima_fecha» deben leerse como la misma columna."""
    sin_tildes = unicodedata.normalize("NFKD", nombre or "")
    sin_tildes = "".join(c for c in sin_tildes if not unicodedata.combining(c))
    return re.sub(r"[^a-z]", "", sin_tildes.lower())


def campo(fila, *nombres):
    for n in nombres:
        v = fila.get(clave(n))
        if v and v.strip():
            return v.strip()
    return ""


def leer_fecha(texto):
    """Devuelve un date, o None si la celda no trae una fecha reconocible."""
    t = (texto or "").strip()
    if m := re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", t):
        a, b, c = (int(x) for x in m.groups())
        return fecha_segura(a, b, c)
    if m := re.match(r"^(\d{1,2})[/.](\d{1,2})[/.](\d{4})$", t):
        p, s, anio = (int(x) for x in m.groups())
        # Sheets exporta M/D/YYYY en inglés y D/M/YYYY en español. Un primer
        # número mayor que 12 solo puede ser un día; si no, gana el orden de
        # Sheets en inglés, que es como sale el CSV publicado.
        mes, dia = (s, p) if p > 12 else (p, s)
        return fecha_segura(anio, mes, dia)
    return None


def fecha_segura(anio, mes, dia):
    try:
        return date(anio, mes, dia)
    except ValueError:
        return None


def fecha_legible(f, idioma):
    if idioma == "en":
        return f"{MESES_EN[f.month - 1]} {f.day}, {f.year}"
    return f"{f.day} de {MESES_ES[f.month - 1]} de {f.year}"


def tarjeta(noticia, idioma_pagina, etiqueta_idioma, nivel):
    """Una tarjeta, con el mismo marcado que las que había escritas a mano."""
    f = date.fromisoformat(noticia["fecha"])
    idioma_nota = noticia["idioma"].lower()
    # En texto visible no hace falta escapar comillas; en el href sí.
    e = lambda s: html.escape(s, quote=False)

    firma = f' · {e(noticia["autor"])}' if noticia["autor"] else ""

    return (
        f'      <li class="tarjeta">\n'
        f'        <p class="tarjeta__medio">{e(noticia["medio"])}</p>\n'
        f'        <{nivel} class="tarjeta__titulo">'
        f'<a href="{html.escape(noticia["enlace"], quote=True)}" hreflang="{idioma_nota}"'
        f' target="_blank" rel="noopener">{e(noticia["titular"])}</a></{nivel}>\n'
        f'        <p class="tarjeta__meta">'
        f'<time datetime="{noticia["fecha"]}">{fecha_legible(f, idioma_pagina)}</time>'
        f'{firma}'
        f'<span class="tarjeta__idioma" title="{etiqueta_idioma}">{idioma_nota.upper()}</span></p>\n'
        f'      </li>\n'
    )


def bajar_csv(origen, es_archivo):
    if es_archivo:
        return pathlib.Path(origen).read_text(encoding="utf-8")
    with urllib.request.urlopen(origen, timeout=30) as r:
        return r.read().decode("utf-8")


def leer_noticias(texto_csv):
    filas = csv.DictReader(texto_csv.splitlines())
    noticias, descartadas = [], 0

    for n, cruda in enumerate(filas, start=2):  # la 1 es el encabezado
        fila = {clave(k): v for k, v in cruda.items() if k}
        if not any((v or "").strip() for v in fila.values()):
            continue

        publicar = campo(fila, "Publicar").lower()
        if publicar in ("no", "false", "0", "n", "oculto"):
            continue

        medio   = campo(fila, "Medio", "Outlet")
        titular = campo(fila, "Titular", "Título", "Headline", "Title")
        enlace  = campo(fila, "Enlace", "URL", "Link", "Artículo", "Article")
        fecha   = leer_fecha(campo(fila, "Fecha", "Date"))
        idioma  = campo(fila, "Idioma", "Language").lower()[:2] or "es"

        faltan = [n for n, v in (("Medio", medio), ("Titular", titular),
                                 ("Enlace", enlace), ("Fecha", fecha)) if not v]
        if faltan:
            print(f"  fila {n}: se omite, falta {', '.join(faltan)}", file=sys.stderr)
            descartadas += 1
            continue
        if not enlace.startswith(("http://", "https://")):
            print(f"  fila {n}: se omite, el enlace no es una dirección web", file=sys.stderr)
            descartadas += 1
            continue
        if idioma not in ("es", "en"):
            print(f"  fila {n}: idioma «{idioma}» desconocido, se asume ES", file=sys.stderr)
            idioma = "es"

        noticias.append({
            "fecha": fecha.isoformat(),
            "medio": medio,
            "titular": titular,
            "enlace": enlace,
            "autor": campo(fila, "Autor", "Author", "Firma"),
            "idioma": idioma,
        })

    # Orden estable: lo más reciente arriba y, dentro de un mismo día, el
    # orden en que están las filas del Sheet.
    noticias.sort(key=lambda x: x["fecha"], reverse=True)
    return noticias, descartadas


def escribir_bloque(ruta, bloque):
    """Reemplaza lo que hay entre los marcadores. Devuelve True si cambió."""
    t = ruta.read_text(encoding="utf-8")
    patron = re.compile(
        r"(?P<ini>[ \t]*<!-- noticias:inicio.*?-->\n).*?(?P<fin>[ \t]*<!-- noticias:fin -->\n)",
        re.DOTALL,
    )
    if not patron.search(t):
        raise SystemExit(f"ERROR: {ruta} no tiene los marcadores noticias:inicio/fin.")

    nuevo = patron.sub(lambda m: m.group("ini") + bloque + m.group("fin"), t, count=1)
    if nuevo == t:
        return False
    ruta.write_text(nuevo, encoding="utf-8")
    return True


def actualizar_fechas(hoy):
    """Pone la fecha de hoy en «Última actualización» y en el sitemap.

    El pie está copiado en las 12 páginas y el sitemap lleva un <lastmod> por
    página, así que los dos se mueven juntos: si no, el sitio se contradice.
    """
    cambiados = 0
    for ruta in sorted(RAIZ.rglob("*.html")):
        if ".git" in ruta.parts:
            continue
        t = ruta.read_text(encoding="utf-8")
        nuevo = PIE_ES.sub(lambda m: m.group(1) + fecha_legible(hoy, "es"), t)
        nuevo = PIE_EN.sub(lambda m: m.group(1) + fecha_legible(hoy, "en"), nuevo)
        if nuevo != t:
            ruta.write_text(nuevo, encoding="utf-8")
            cambiados += 1

    mapa = RAIZ / "sitemap.xml"
    if mapa.exists():
        t = mapa.read_text(encoding="utf-8")
        nuevo = re.sub(r"<lastmod>[\d-]+</lastmod>", f"<lastmod>{hoy.isoformat()}</lastmod>", t)
        if nuevo != t:
            mapa.write_text(nuevo, encoding="utf-8")
            cambiados += 1
    return cambiados


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", help="lee un CSV local en vez del Sheet (para probar)")
    ap.add_argument("--sin-pie", action="store_true",
                    help="no toca «Última actualización» ni el sitemap")
    args = ap.parse_args()

    origen = args.csv or os.environ.get("NOTICIAS_SHEET_URL")
    if not origen:
        raise SystemExit("ERROR: falta NOTICIAS_SHEET_URL (o usa --csv).")

    try:
        texto = bajar_csv(origen, bool(args.csv))
    except Exception as e:
        raise SystemExit(f"ERROR al leer el origen: {e}")

    noticias, descartadas = leer_noticias(texto)
    if not noticias:
        raise SystemExit("ERROR: el origen no dejó ninguna noticia válida. "
                         "No se tocó el sitio.")

    (RAIZ / "data").mkdir(exist_ok=True)
    (RAIZ / "data/noticias.json").write_text(
        json.dumps(noticias, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    tocados = []
    for nombre, idioma, etiqueta, nivel, tope in DESTINOS:
        seleccion = noticias[:tope] if tope else noticias
        bloque = "".join(tarjeta(n, idioma, etiqueta, nivel) for n in seleccion)
        if escribir_bloque(RAIZ / nombre, bloque):
            tocados.append(nombre)

    if tocados and not args.sin_pie:
        actualizar_fechas(date.today())

    print(f"{len(noticias)} noticias" + (f", {descartadas} filas descartadas" if descartadas else ""))
    print("Páginas actualizadas: " + (", ".join(tocados) if tocados else "ninguna, ya estaban al día"))


if __name__ == "__main__":
    main()
