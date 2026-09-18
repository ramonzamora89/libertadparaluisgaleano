# PROJECT — #LibertadParaLuisGaleano

Guía de trabajo para mantener el sitio. Para la estructura general, ver [README.md](README.md).

## Reglas

1. **Los dos idiomas dicen lo mismo.** Todo cambio de contenido se hace en la página en español y en su par en inglés, en el mismo commit. Si no, el sitio se contradice a sí mismo.
2. **El contador, la cronología y la franja de alertas no se contradicen.** Si cambia la situación de Luis (traslado, audiencia, liberación, deportación), se actualizan los tres.
3. **Solo hechos verificables, con fuente.** Cada entrada de la cronología y cada dato del caso cita al menos una fuente. Se prefieren el CPJ, otras organizaciones y la prensa reconocida, no las redes sociales. Frases cortas, con fecha.
4. **Privacidad y seguridad.** No se nombra a familiares de Luis ni se publican datos de ubicación que no sean ya públicos y necesarios.
5. **Colores y medidas solo como variables** en `:root` (`assets/css/style.css`). Para texto rojo chico se usa `--rojo-texto` sobre fondo claro y `--rojo-claro` sobre fondo negro, porque el rojo del CPJ (`--rojo`) no alcanza el contraste AA para texto chico.
6. **Git:** commits en español que explican el porqué. Solo se hace commit o push cuando Moncho lo confirma.

## Páginas

| Español | Inglés | Contenido |
|---|---|---|
| `/` | `/english/` | Portada, contador, resumen del caso, cita del CPJ, últimas 3 noticias, boletín The Torch |
| `/historia/` | `/english/story/` | Trayectoria y cronología |
| `/por-que-importa/` | `/english/why-this-matters/` | Riesgo, patrón y quiénes piden su liberación |
| `/actua/` | `/english/take-action/` | Pasos, botones para compartir, mensajes para copiar (ES y EN en ambas páginas) |
| `/noticias/` | `/english/in-the-news/` | Tarjetas de prensa, de la más reciente a la más antigua |
| `/cpj-y-aliados/` | `/english/cpj-and-partners/` | Comunicados del CPJ y la SIP, carrusel con los logos de las 15 organizaciones aliadas, contacto de prensa |

## Tareas frecuentes

### Agregar una noticia

La cobertura está en **tres lugares por idioma**: `noticias/` (todas), la portada (solo las 3 más recientes) y sus pares en inglés.

1. Copia una tarjeta `<li class="tarjeta">` al **inicio** de la lista en `noticias/index.html`:
   ```html
   <li class="tarjeta">
     <p class="tarjeta__medio">Medio</p>
     <h2 class="tarjeta__titulo"><a href="URL" hreflang="es" target="_blank" rel="noopener">Titular exacto</a></h2>
     <p class="tarjeta__meta"><time datetime="2026-09-18">18 de septiembre de 2026</time> · Autor<span class="tarjeta__idioma" title="Idioma">ES</span></p>
   </li>
   ```
2. Haz lo mismo en `english/in-the-news/index.html`, con la fecha en inglés (`September 18, 2026`) y `title="Language"`. El titular y el medio van en su idioma original.
3. En `index.html` y `english/index.html` (sección «En las noticias»), la lista usa `<h3>` en vez de `<h2>`: agrega la tarjeta nueva arriba y borra la última para que queden 3.
4. Revisa que el enlace abra **la nota correcta**. freedomformario.com tenía tarjetas que apuntaban a notas de otros medios.

### Agregar un hecho a la cronología

En `historia/index.html` y `english/story/index.html`, dentro de `<ol class="cronologia">`, en orden cronológico (el más antiguo arriba):

```html
<li class="cronologia__item">
  <p class="cronologia__fecha"><time datetime="2026-10-02">2 de octubre de 2026</time></p>
  <p class="cronologia__texto">Qué pasó, en una o dos frases.</p>
  <p class="cronologia__fuentes">Fuente: <a href="URL" target="_blank" rel="noopener">Medio</a></p>
</li>
```

Clases opcionales:
- `cronologia__item--hito` resalta un hecho clave con un punto rojo.
- `cronologia__item--proximo` marca un hecho programado con un punto punteado. Cuando ocurra, quita la clase y reescribe el texto en pasado.

### Agregar el logo de una organización aliada

Los logos viven en un carrusel en `cpj-y-aliados/index.html` y `english/cpj-and-partners/index.html`.

1. **Primero el permiso.** No se agrega un logo sin autorización de la organización. Anota abajo, en «Permisos de logos», quién lo autorizó y cuándo.
2. Guarda el archivo en `assets/img/logos/` con nombre en minúsculas y guiones (`nombre-organizacion.svg`). Formato: **SVG** cuando la organización lo publique, si no **WebP con transparencia**, de hasta 600×240 px.
3. **Cuidado con las versiones en blanco.** Muchas organizaciones publican en su encabezado el logo en blanco, porque su sitio tiene fondo oscuro. El carrusel es de fondo blanco, así que ese archivo se ve vacío. Comprueba siempre el logo sobre blanco antes de darlo por bueno. Si solo existe en blanco, busca la versión oscura en su kit de marca o en Wikimedia Commons.
4. **Que el logo se lea al tamaño real.** El carrusel muestra los logos a 130 px de alto con 20 px de padding, o sea unos 90 px útiles. Un logo cuadrado con el nombre en letra chica queda ilegible: prefiere el lockup horizontal.
5. Agrega un `<li>` a la pista, en las dos páginas:
   ```html
   <li>
     <a class="carrusel__logo" href="URL de la organización" target="_blank" rel="noopener">
       <img src="../assets/img/logos/archivo.svg" alt="Nombre de la organización" width="200" height="80" loading="lazy">
     </a>
   </li>
   ```
   En la página en inglés la ruta es `../../assets/img/logos/`.
6. `width` y `height` llevan las **dimensiones reales** del archivo, para que el navegador reserve el espacio y no haya salto de layout. Para un SVG, míralas con `rsvg-convert -h 200 archivo.svg -o /tmp/r.png && identify /tmp/r.png`, porque el `viewBox` no siempre coincide con los atributos.
7. El `alt` lleva el nombre de la organización, sin la palabra «logo», traducido en cada idioma cuando la organización tiene nombre en español.
8. Si la organización tiene sitio en español y en inglés (CPJ, SIP, RSF), cada página enlaza a la versión en su idioma.
9. Las flechas del carrusel aparecen solas cuando hay más logos de los que caben.

### Actualizar la franja de alertas

Está copiada en las 12 páginas, dentro de `<ul class="alerta__pista">`. El JS la duplica para el bucle, así que se escribe una sola vez por página. Para cambiarla en todas a la vez, usa un script de reemplazo y verifica después:

```sh
grep -c "texto nuevo" index.html */index.html english/*/index.html english/index.html
```

### Congelar o cambiar el contador

El contador está en `index.html` y `english/index.html`:

```html
<div class="contador" data-contador data-desde="2026-09-14">
  ...
  <span class="dias-numero">3</span>
```

- `site.js` cuenta los días de calendario desde `data-desde`. El número escrito en el HTML es el respaldo si el JavaScript no carga; conviene actualizarlo de vez en cuando.
- **Si Luis es liberado:** escribe la cifra final en `.dias-numero`, quita el atributo `data-contador` y cambia el rótulo («Pasó N días detenido» / «Spent N days in detention») y la nota. Actualiza también la franja, la cronología y el resumen del caso.

### Actualizar la fecha de «Última actualización»

Está en el pie de las 12 páginas (`.pie__legal`) y en `sitemap.xml` (`<lastmod>`).

## Permisos de logos

Moncho confirmó el 18/09/2026 que la campaña tiene la aprobación de las organizaciones para usar sus logos. **Falta registrar el detalle por organización** (quién lo autorizó, en qué fecha y por qué vía), por si alguna lo pide más adelante.

Las 15 organizaciones del carrusel, en el orden en que aparecen:

| # | Organización | Archivo | Tamaño | Origen |
|---|---|---|---|---|
| 1 | CPJ | `cpj.webp` | 255×300 | Lo entregó Moncho |
| 2 | SIP / IAPA | `sip.svg` | 179×65 | Lo entregó Moncho |
| 3 | AFPC-USA | `afpc.webp` | 459×206 | Lo entregó Moncho (18/09/2026) |
| 4 | First Amendment Coalition | `first-amendment-coalition.svg` | 265×60 | firstamendmentcoalition.org |
| 5 | First Amendment Foundation | `first-amendment-foundation.webp` | 433×240 | floridafaf.org |
| 6 | Free Press | `free-press.webp` | 300×300 | Lo entregó Moncho |
| 7 | Freedom of the Press Foundation | `freedom-of-the-press-foundation.svg` | 564×85 | Wikimedia Commons |
| 8 | The Media and Democracy Project | `media-and-democracy-project.webp` | 192×240 | mediaanddemocracyproject.org |
| 9 | NAHJ | `nahj.webp` | 494×240 | nahj.org |
| 10 | NPPA | `nppa.svg` | 113×31 | nppa.org |
| 11 | PEN America | `pen-america.svg` | 149×55 | pen.org, recoloreado |
| 12 | RTDNA | `rtdna.webp` | 600×190 | rtdna.org |
| 13 | RSF | `rsf.svg` | 190×48 | rsf.org/en |
| 14 | Society of Environmental Journalists | `sej.webp` | 200×200 | sej.org |
| 15 | SPJ | `spj.webp` | 240×240 | spj.org |

Tres archivos necesitaron trabajo extra, porque sus organizaciones solo publican el logo en blanco:

- **Freedom of the Press Foundation:** su sitio solo ofrece la versión en blanco. Se usa la versión negra de Wikimedia Commons.
- **SEJ:** el logo del encabezado es blanco. Se usa `sej.org/sites/default/files/SEJ-logo-blue-2018-200_6.jpg`, la versión azul.
- **PEN America:** su SVG oficial es la variante en blanco (el grupo se llama literalmente `Pen_Box_white`). Se recoloreó a la variante para fondo claro: el globo queda rojo, «PEN AMERICA» en tinta oscura y el lema «The Freedom to Write» en rojo. **Si la organización prefiere su archivo original**, hay un JPG oficial sobre fondo blanco en Wikimedia Commons (`Pen_Box_tagline_lrg.jpg`).

Versiones oficiales de mejor calidad, por si se quieren reemplazar:
- CPJ horizontal en SVG: `cpj.org/wp-content/themes/cpj/client/src/images/cpj-logo-black-small.svg`. El que se usa hoy es vertical.
- Free Press horizontal en PNG con transparencia (1999×567), dentro del kit de marca (freepress.net/media-kit). El archivo actual viene de seeklogo y tiene fondo blanco, no transparente.
- SIP en SVG, con versión en inglés: `en.sipiapa.org/css-custom/xpress/images/header-logo-en.svg`.
- AFPC-USA: el archivo actual es un WebP de 459×206 y el nombre se lee bien, pero la línea de los dos dominios queda apretada. Si la organización tiene el vectorial (SVG, AI o EPS), conviene pedirlo.

`sip.svg` se optimizó el 18/09/2026 de 102 KB a 76 KB (40 KB a 27 KB ya comprimido) redondeando las coordenadas de sus 95 paths a dos decimales. Sigue siendo el logo más pesado del carrusel: casi todo su peso es el sello con el globo y el anillo de texto convertido a curvas.

## Datos del caso y discrepancias entre fuentes

Revisado el 17/09/2026:

| Dato | Lo que dice el sitio | Detalle |
|---|---|---|
| Fecha y lugar de detención | 14/09/2026, por la mañana, Orlando (FL) | CPJ, EL PAÍS, France 24, Confidencial, Infobae. Artículo 66 dice Miami. |
| Centro de detención | «bajo custodia de ICE en Florida» | CPJ (citando a La Prensa) y EL PAÍS dicen Baker (Sanderson). The Guardian dice que el miércoles 16 estaba en Krome (Miami). **Por confirmar.** |
| Plataforma | «aplicación de transporte» | La mayoría dice Uber; The Guardian dice Lyft. |
| Entrada a EE. UU. | 21/12/2018 | EL PAÍS (y el DHS). The Guardian dice que huyó «días después» del allanamiento. Confirmado por un mensaje recibido el 17/09/2026. |
| Orden de captura | Sin fecha | Las fuentes no coinciden en si fue antes o después de su salida. |
| Solicitud de asilo | Presentada el 17/06/2019 | La fecha exacta viene de un mensaje recibido el 17/09/2026; **sin fuente publicada que la respalde**. EL PAÍS e Infobae dicen solo «2019»; Artículo 66 dice «pendiente desde 2018». Cae tres días antes del 20/06/2019, fecha hasta la que el DHS dice que tenía autorización de estadía. |
| Audiencia | 2/10/2026 | CPJ, EL PAÍS, The Guardian, Infobae. |
| Nacionalidad española (abril de 2026) | **No se publica** | Solo lo dice Artículo 66; sin verificar. |
| Corresponsal de EFE (2004–2006) | **No se publica** | Solo lo dice France 24, que no se pudo abrir directamente para verificarlo. |
| Nombre de la esposa | **No se publica** | Aparece como Deykell, Deykel y Daykel Santamaría. |

## Pendientes (TODO)

- [ ] **Confirmar la fecha del asilo (17/06/2019)** con la familia o el abogado, o con un documento (recibo I-589 de USCIS). Hoy el sitio la publica atribuida a «información aportada a esta campaña».
- [ ] **Foto de Luis** con permiso de uso y crédito, para la portada y las imágenes para compartir. Hoy la portada es solo tipográfica.
- [ ] **Registrar el detalle de los permisos de logos:** quién autorizó cada uno, cuándo y por qué vía. La aprobación existe (Moncho la confirmó el 18/09/2026), pero no está documentada organización por organización.
- [ ] **Crédito del pie** («Con el respaldo del CPJ» / «Supported by CPJ»): confirmar la redacción con el CPJ.
- [ ] **Petición o carta:** si existe, agregarla como llamado principal en Actúa y en la portada.
- [ ] Confirmar la cuenta de X de *Café con Voz* (`@CafeconVozNi`, tomada de un tuit citado por Artículo 66).
- [ ] Imágenes para compartir (`assets/img/compartir-*.png`): hoy son provisionales, generadas con Georgia y Arial. Reemplazarlas por una pieza diseñada, de 1200×630.
- [ ] Limpieza menor: la regla `.carrusel__pie` de `assets/css/style.css` quedó sin uso al quitarse la nota al pie del carrusel. Se conserva por si vuelve a hacer falta una nota bajo los logos.

## Publicación (GitHub Pages)

1. Repo `ramonzamora89/libertadparaluisgaleano`, rama `main`, carpeta raíz.
2. En **Settings → Pages**: Source = Deploy from a branch → `main` / `(root)`. En *Custom domain* escribe `libertadparaluisgaleano.com`. El archivo `CNAME` ya está en el repo.
3. **DNS** en el registrador del dominio:
   - `@` → cuatro registros A: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
   - `www` → CNAME a `ramonzamora89.github.io`.
   - El dominio canónico es el que **no lleva www** (así están escritos `canonical`, `og:url` y `hreflang`). GitHub redirige www a la versión sin www.
4. Verifica con `dig +short libertadparaluisgaleano.com A` y `dig +short www.libertadparaluisgaleano.com CNAME`.
5. Cuando el certificado cubra ambos nombres, activa **Enforce HTTPS**.
