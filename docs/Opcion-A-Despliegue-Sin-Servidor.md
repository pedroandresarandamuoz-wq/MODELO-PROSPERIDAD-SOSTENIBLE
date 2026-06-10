# Opción A — Publicar el MPS sin hostear nada (stlite + GitHub Pages)

> Para: Pedro
> Resumen: cómo poner la aplicación del Modelo de Prosperidad Sostenible online **sin contratar ni mantener ningún servidor**. Solo usando ramas de Git y GitHub Actions, que generan automáticamente la web en GitHub Pages.

---

## El problema que resuelve

La aplicación está hecha en **Streamlit**. Streamlit, normalmente, necesita un **servidor Python encendido todo el tiempo**: alguien tiene que pagarlo, mantenerlo y vigilar que no se caiga (por ejemplo Streamlit Community Cloud, un VPS, etc.). Eso es justo lo que queremos evitar.

## La idea de la Opción A

Existe una versión de Streamlit llamada **stlite** que compila Streamlit a *WebAssembly*. En cristiano: **la aplicación entera se ejecuta dentro del navegador del visitante**, no en un servidor nuestro.

Eso cambia todo:

- No hay servidor que encender, pagar ni mantener.
- La web es solo un puñado de ficheros estáticos (un `index.html`, el código `MPS.py` y el JSON de datos).
- Esos ficheros se pueden publicar **gratis** en **GitHub Pages**, el hosting estático del propio GitHub.
- El **mismo código `MPS.py`** funciona sin reescribirlo.

El visitante entra a una URL tipo `https://<usuario>.github.io/MODELO-PROSPERIDAD-SOSTENIBLE/`, su navegador descarga el runtime la primera vez (tarda unos segundos), y a partir de ahí la app funciona igual que ahora.

## Cómo funciona el día a día: solo Git

Tu flujo de trabajo se reduce a **trabajar con ramas de Git**, exactamente como ya hacemos:

```
1. Haces cambios (en el código o en los datos) en una rama.
2. Haces push a la rama (o la fusionas a main).
3. GitHub Actions se dispara solo y regenera la web.
4. GitHub Pages publica la versión nueva en un par de minutos.
```

No hay ningún paso de "desplegar a un servidor". **Empujar a Git ES el despliegue.** Si más adelante quieres regenerar también los datos (volver a tirar de las APIs del Banco Mundial / FMI), se añade ese paso al mismo flujo automático y listo.

## Qué se ha añadido al repositorio

Tres piezas, nada más:

| Fichero | Para qué sirve |
|---|---|
| `index.html` | La página web. Carga stlite y le dice que ejecute `MPS.py` con los datos. |
| `.github/workflows/deploy-pages.yml` | La automatización de GitHub Actions: recoge los ficheros y los publica en Pages. |
| `docs/Opcion-A-Despliegue-Sin-Servidor.md` | Este documento. |

**No se ha tocado** ni `MPS.py` ni los datos: la lógica de la aplicación sigue intacta.

## Puesta en marcha (una sola vez)

Para activarlo, en el repositorio de GitHub:

1. Ve a **Settings → Pages**.
2. En **"Build and deployment" → "Source"**, elige **"GitHub Actions"**.
3. Haz push de esta rama (o fusiónala a `main`). El flujo se ejecutará y, al terminar, en la pestaña **Actions** verás la URL pública.

A partir de ahí, cada push a `main` (o a la rama de trabajo configurada) republica la web automáticamente.

## Ventajas e inconvenientes (con honestidad)

**Ventajas**
- Coste: **0 €**. Sin servidores, sin facturas, sin mantenimiento.
- Imposible que "se caiga el servidor": no hay servidor.
- Aguanta muchísimas visitas sin despeinarse (son ficheros estáticos).
- El despliegue es transparente: queda registrado en el historial de Git.

**Inconvenientes / límites**
- La **primera carga** para cada visitante tarda unos segundos (su navegador descarga el motor de Python). Después va fluido.
- Es para datos **publicados** (públicos): todo viaja al navegador del visitante. Para esta herramienta de transparencia, es exactamente lo que queremos.
- Funciona en cualquier navegador moderno de escritorio o móvil; en móviles muy antiguos puede ir más justo.

## En una frase

Convertimos la aplicación en una **web estática que se ejecuta sola en el navegador**, de modo que **nunca tengas que preocuparte de dónde hostearla**: tu único trabajo es usar Git, y GitHub se encarga del resto.
