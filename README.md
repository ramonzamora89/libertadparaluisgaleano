# #LibertadParaLuisGaleano

Sitio de campaña por la liberación de Luis Galeano, periodista nicaragüense en el exilio y director de *Café con Voz*. ICE lo detuvo el 14 de septiembre de 2026 en Orlando, Florida.

Dominio: **https://libertadparaluisgaleano.com**

Sigue el formato de [zamoralibre.com](https://github.com/ramonzamora89/zamoralibre): HTML, CSS y un JavaScript pequeño, **sin dependencias ni proceso de compilación**. Se publica con GitHub Pages. La estructura de contenidos es la de [freedomformario.com](https://freedomformario.com/) y la línea gráfica es la del CPJ.

## Estructura

```
index.html                      Inicio (español)
historia/                       La historia de Luis
por-que-importa/                Por qué importa
actua/                          Actúa: mensajes para compartir
noticias/                       En las noticias
cpj-y-aliados/                  CPJ y aliados
english/                        Las mismas seis páginas en inglés
  story/ why-this-matters/ take-action/ in-the-news/ cpj-and-partners/
404.html                        Página de error (rutas absolutas desde la raíz)
assets/css/style.css            Hoja de estilos única; colores y medidas en :root
assets/css/fonts.css            Tipografías autoalojadas
assets/js/site.js               Contador, menú, franja de alertas, botones de copiar
assets/fonts/                   Source Sans 3 y Source Serif 4 (woff2, licencia OFL)
assets/img/                     favicon.svg, compartir-es.png, compartir-en.png
data/noticias.json              Respaldo de la cobertura de prensa
scripts/actualizar_noticias.py  Genera las tarjetas de prensa desde un Google Sheet
scripts/noticias-semilla.csv    Las 7 notas iniciales; plantilla del Sheet
.github/workflows/              Corre el script todos los días
CNAME  .nojekyll  robots.txt  sitemap.xml
```

Todo el texto está directamente en los archivos `.html`. No hay plantillas ni base de datos: el encabezado, la franja de alertas y el pie se repiten en cada página. Las tipografías están autoalojadas, así que el sitio no hace peticiones a servidores externos.

La única excepción son las tarjetas de prensa, que salen de un Google Sheet. No cambia nada para quien visita el sitio: un script escribe el HTML antes de publicarlo y las páginas siguen siendo estáticas y legibles sin JavaScript. Ver [PROJECT.md](PROJECT.md#agregar-una-noticia).

## Ver el sitio en local

```sh
python3 -m http.server 8000
```

Luego abre http://localhost:8000. La página 404 solo se ve bien publicada, porque usa rutas absolutas.

## Publicar

```sh
git add -A
git commit -m "Describe el cambio"
git push
```

GitHub Pages republica en un par de minutos. Las tareas frecuentes (agregar una noticia, actualizar la franja de alertas, congelar el contador) están en [PROJECT.md](PROJECT.md).
