# CLAUDE.md — #LibertadParaLuisGaleano

Sitio estático de campaña (HTML, CSS y JS sin build) publicado con GitHub Pages en https://libertadparaluisgaleano.com. Español en la raíz, inglés en `/english/`.

**Antes de tocar nada, lee [PROJECT.md](PROJECT.md):** tiene el estado del caso, las reglas, las tareas frecuentes paso a paso y los pendientes. La estructura de archivos está en [README.md](README.md).

## Lo que no se negocia

- **El repo es público.** Lo que la campaña sabe por la familia de Luis o por vías internas, y que no ha sido publicado, no se escribe en páginas, en PROJECT.md, en commits ni en este archivo. Si hace falta justificar una decisión que depende de ese dato, se anota la decisión, no el dato.
- **Solo hechos con fuente publicada** (CPJ, otras organizaciones, prensa reconocida). No se infiere ni se adelanta el resultado del caso migratorio.
- **Español e inglés en el mismo commit.** Las 12 páginas son 6 pares.
- **Si cambia la situación de Luis**, se actualizan juntos: contador, franja de alertas, cronología, resumen de la portada, pie de las 12 páginas, descripciones (`description`, `og:description`) e imágenes para compartir (con el `?v=` del `og:image`). Busca en todo el sitio con `grep -rn` antes de dar el cambio por terminado.
- **Commit y push solo cuando Moncho lo confirma.** Commits en español que explican el porqué.

## Cosas fáciles de romper

- Las tarjetas de noticias entre `<!-- noticias:inicio -->` y `<!-- noticias:fin -->` las escribe `scripts/actualizar_noticias.py`. No se editan a mano: se agrega la fila al Sheet (o, mientras no esté conectado, a `scripts/noticias-semilla.csv`) y se corre el script.
- `scripts/noticias-semilla.csv` usa finales de línea CRLF. Si lo reescribes con Python, abre el archivo con `newline=''` para no cambiarlos.
- La franja de alertas y el pie están copiados en las 12 páginas: cambia con un script y verifica con `grep -c`.
- Después de un push, GitHub Pages tarda uno o dos minutos. Verifica en el sitio publicado con `curl`, no solo en local.
