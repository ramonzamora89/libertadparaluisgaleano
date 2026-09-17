/* #LibertadParaLuisGaleano — contador de días, menú, franja de alertas y
   botones de copiar. Sin dependencias. */
(function () {
  "use strict";

  /* ----- Contador de días de detención ---------------------------------- */
  /* Días completos desde la detención (2026-09-14), contados por fecha del
     calendario local, no por horas. El número escrito en el HTML es el
     respaldo si el JavaScript no corre. Para congelar el contador, escribe
     la cifra final en el HTML y quita el atributo data-contador. */
  function diasDesde(fechaISO) {
    var p = fechaISO.split("-");
    var inicio = new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
    var hoy = new Date();
    hoy = new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate());
    return Math.max(0, Math.round((hoy - inicio) / 86400000));
  }

  function pintarContador() {
    document.querySelectorAll("[data-contador]").forEach(function (el) {
      var dias = diasDesde(el.getAttribute("data-desde") || "2026-09-14");
      var numero = el.querySelector(".dias-numero");
      if (numero) numero.textContent = dias.toLocaleString("en-US");
      var unidad = el.querySelector("[data-unidad]");
      if (unidad) {
        var formas = unidad.getAttribute("data-unidad").split("|");
        unidad.textContent = dias === 1 ? formas[0] : formas[1];
      }
    });
  }

  /* ----- Menú (solo en pantallas angostas) ------------------------------ */
  function iniciarMenu() {
    var boton = document.querySelector("[data-menu-boton]");
    var panel = document.querySelector("[data-menu-panel]");
    if (!boton || !panel) return;

    function abrir(estado) {
      boton.setAttribute("aria-expanded", String(estado));
      boton.setAttribute("aria-label", estado ? boton.getAttribute("data-cerrar") : boton.getAttribute("data-abrir"));
      panel.setAttribute("data-abierto", String(estado));
      document.body.setAttribute("data-menu-abierto", String(estado));
      if (estado) {
        var primero = panel.querySelector("a");
        if (primero) primero.focus();
      }
    }

    boton.addEventListener("click", function () {
      abrir(boton.getAttribute("aria-expanded") !== "true");
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && boton.getAttribute("aria-expanded") === "true") {
        abrir(false);
        boton.focus();
      }
    });

    panel.addEventListener("click", function (e) {
      if (e.target.tagName === "A") abrir(false);
    });

    // Si la ventana crece y el menú pasa a verse en línea, se cierra el panel.
    window.matchMedia("(min-width: 960px)").addEventListener("change", function (m) {
      if (m.matches) abrir(false);
    });
  }

  /* ----- Franja de alertas: duplica el contenido para un bucle continuo -- */
  function iniciarAlerta() {
    document.querySelectorAll("[data-alerta]").forEach(function (ventana) {
      var pista = ventana.querySelector(".alerta__pista");
      if (!pista) return;
      var copia = pista.cloneNode(true);
      copia.setAttribute("aria-hidden", "true");
      copia.querySelectorAll("a").forEach(function (a) { a.setAttribute("tabindex", "-1"); });
      ventana.appendChild(copia);
    });
  }

  /* ----- Botones para copiar mensajes ----------------------------------- */
  function iniciarCopiar() {
    document.querySelectorAll("[data-copiar]").forEach(function (boton) {
      boton.hidden = false;
      boton.addEventListener("click", function () {
        var fuente = document.getElementById(boton.getAttribute("data-copiar"));
        var estado = boton.parentNode.querySelector(".mensaje__estado");
        if (!fuente) return;
        function avisar(clave) { if (estado) estado.textContent = boton.getAttribute(clave); }

        // Deja el texto seleccionado: si la copia falla, se puede copiar a mano.
        var rango = document.createRange();
        rango.selectNodeContents(fuente);
        var seleccion = window.getSelection();
        seleccion.removeAllRanges();
        seleccion.addRange(rango);

        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(fuente.textContent.trim()).then(
            function () { avisar("data-copiado"); },
            function () { avisar("data-error"); }
          );
        } else {
          var ok = false;
          try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
          avisar(ok ? "data-copiado" : "data-error");
        }
      });
    });
  }

  function iniciar() {
    pintarContador();
    iniciarMenu();
    iniciarAlerta();
    iniciarCopiar();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }
})();
