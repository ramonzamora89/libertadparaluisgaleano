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
| `/cpj-y-aliados/` | `/english/cpj-and-partners/` | Comunicados del CPJ y la SIP, contacto de prensa |

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
2. Guarda el archivo en `assets/img/logos/` con nombre en minúsculas (`nombre-organizacion.svg`, o `.png` con fondo transparente). Los logos se muestran sobre fondo blanco, así que deben ser oscuros o a color.
3. Agrega un `<li>` al final de la pista, en las dos páginas:
   ```html
   <li>
     <a class="carrusel__logo" href="URL de la organización" target="_blank" rel="noopener">
       <img src="../assets/img/logos/archivo.svg" alt="Nombre de la organización" width="200" height="80" loading="lazy">
     </a>
   </li>
   ```
   En la página en inglés la ruta es `../../assets/img/logos/`.
4. El `alt` lleva el nombre de la organización, sin la palabra «logo».
5. Las flechas del carrusel aparecen solas cuando hay más logos de los que caben; con pocos quedan ocultas.

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

| Organización | Archivo | Origen | Permiso |
|---|---|---|---|
| CPJ | `assets/img/logos/cpj.webp` (255×300) | Lo entregó Moncho | **Por registrar:** quién lo autorizó y cuándo |
| Free Press | `assets/img/logos/free-press.webp` (300×300) | Lo entregó Moncho | **Por registrar** |
| SIP | `assets/img/logos/sip.svg` | Lo entregó Moncho | **Por registrar** |

Ninguna de las tres publica condiciones de uso de su logo. Free Press sí ofrece un kit de marca descargable (freepress.net/media-kit); el CPJ excluye las imágenes de su licencia Creative Commons y la SIP no publica nada. Si hace falta pedir permiso: press@cpj.org, tkarr@freepress.net y sipiapa.org/contacto.

Versiones oficiales de mejor calidad, por si se quieren reemplazar:
- CPJ horizontal en SVG: `cpj.org/wp-content/themes/cpj/client/src/images/cpj-logo-black-small.svg`.
- Free Press horizontal en PNG con transparencia (1999×567), dentro del kit de marca. El archivo que se usa hoy viene de seeklogo y tiene fondo blanco, no transparente.
- SIP en SVG, con versión en inglés: `en.sipiapa.org/css-custom/xpress/images/header-logo-en.svg`.

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
- [ ] **Logo del CPJ:** confirmar si se puede usar. Hoy el CPJ aparece solo como texto con enlace.
- [ ] **Crédito del pie** («Con el respaldo del CPJ» / «Supported by CPJ»): confirmar la redacción con el CPJ.
- [ ] **Petición o carta:** si existe, agregarla como llamado principal en Actúa y en la portada.
- [ ] Confirmar la cuenta de X de *Café con Voz* (`@CafeconVozNi`, tomada de un tuit citado por Artículo 66).
- [ ] Imágenes para compartir (`assets/img/compartir-*.png`): hoy son provisionales, generadas con Georgia y Arial. Reemplazarlas por una pieza diseñada, de 1200×630.

## Publicación (GitHub Pages)

1. Repo `ramonzamora89/libertadparaluisgaleano`, rama `main`, carpeta raíz.
2. En **Settings → Pages**: Source = Deploy from a branch → `main` / `(root)`. En *Custom domain* escribe `libertadparaluisgaleano.com`. El archivo `CNAME` ya está en el repo.
3. **DNS** en el registrador del dominio:
   - `@` → cuatro registros A: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
   - `www` → CNAME a `ramonzamora89.github.io`.
   - El dominio canónico es el que **no lleva www** (así están escritos `canonical`, `og:url` y `hreflang`). GitHub redirige www a la versión sin www.
4. Verifica con `dig +short libertadparaluisgaleano.com A` y `dig +short www.libertadparaluisgaleano.com CNAME`.
5. Cuando el certificado cubra ambos nombres, activa **Enforce HTTPS**.
