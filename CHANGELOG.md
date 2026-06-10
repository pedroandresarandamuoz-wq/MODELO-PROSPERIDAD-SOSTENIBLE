# Registro de cambios

Cambios en las páginas de contenido (la web del MPS) respecto a versiones anteriores.

---

## Versión 2.0 — Panel divulgativo (2026-06-11)

Rediseño completo para que los datos los entienda **cualquier persona**, no solo
quien sepa de estadística. La lógica del modelo (PN, TPL, etc.) no cambia; cambia
cómo se presenta.

### Novedades
- **Países con nombre y bandera.** Se acabaron los códigos crípticos: ahora se ve
  🇨🇭 Suiza, 🇪🇸 España… en lugar de `CHE`, `ESP`.
- **Índice de Prosperidad (0-100).** Nuevo indicador comparable: la posición
  relativa de cada país dentro de su año. Resuelve que los valores brutos de PN y
  TPL tuvieran extremos enormes (de millones negativos) que hacían ilegibles las
  gráficas. Incluye categorías: Excelente / Bueno / Regular / Débil / Crítico.
- **🗺️ Mapa mundial** coroplético, con selector de métrica y deslizador de año.
- **🪪 Ficha de país** en lenguaje llano: un veredicto en una frase, indicadores
  grandes con su variación interanual, puesto mundial, evolución en el tiempo y
  comparación de componentes con la mediana mundial.
- **⚖️ Comparador** de países con barras, y **grupo con media ponderada** (simple
  o ponderada por PIB PPA per cápita) frente a un país objetivo. Admite desde un
  solo país.
- **🏆 Clasificación** tipo liga: ranking ordenable con barras y flechas ▲▼ de
  cambio respecto al año anterior.
- **Glosario** contextual en la barra lateral.

### Antes (versión 1.x)
La app tenía tres vistas centradas en datos en crudo:
- *Histórico Global*: tabla dinámica por año.
- *Análisis por País*: gráficas de líneas de un país.
- *Gráfica de Dispersión*: scatter de dos métricas.

Todo se mostraba con códigos ISO3 y con los valores brutos sin normalizar, lo que
dificultaba la lectura a un público no técnico.

---

## Versión 1.1 — Despliegue sin servidor (2026-06-11)

- La web pasa a ejecutarse **íntegramente en el navegador** mediante **stlite**
  (Streamlit compilado a WebAssembly). Ya no hace falta mantener ningún servidor.
- Publicación automática en **GitHub Pages** vía GitHub Actions: cada push a la
  rama publica la web sola.
- Ver [docs/Opcion-A-Despliegue-Sin-Servidor.md](docs/Opcion-A-Despliegue-Sin-Servidor.md).

---

## Versión 1.0 — Original

Aplicación Streamlit inicial con las tres vistas descritas arriba, pensada para
ejecutarse en un servidor (p. ej. Streamlit Community Cloud).
