# Probar la web en tu ordenador antes de publicarla

> Para: Pedro
> Objetivo: ver los cambios **en tu propio ordenador**, exactamente como
> quedarán online, **sin que nadie más los vea todavía**. Solo cuando te
> convenzan, se publican.

La idea: trabajamos los cambios en una *rama* aparte de Git. Mientras estén en
esa rama, **no se publican**. Tú los revisas en local y, cuando das el visto
bueno, se llevan a la rama `main` (eso es lo que dispara la publicación en
GitHub Pages).

---

## Lo que necesitas (una sola vez)

- **Git** y **Python 3** instalados (en Mac suelen venir; comprueba con
  `git --version` y `python3 --version`).
- Una copia del repositorio en tu ordenador. Si aún no la tienes:
  ```bash
  git clone git@github.com:colegatron/MODELO-PROSPERIDAD-SOSTENIBLE.git
  cd MODELO-PROSPERIDAD-SOSTENIBLE
  ```

---

## Paso 1 — Sitúate en la rama que quieres revisar

Mira qué ramas hay y cámbiate a la que tiene los cambios nuevos:

```bash
git fetch                # trae las novedades del repositorio
git branch -a            # lista las ramas (las nuevas empiezan por "mps-")
git checkout NOMBRE-DE-LA-RAMA   # p. ej. mps-03-vista-autor-atribuciones
```

> ¿Qué es una rama? Una línea de trabajo separada. Lo que está aquí **no afecta**
> a la web publicada hasta que se fusione con `main`.

---

## Paso 2 — Arranca la web en local

Desde la carpeta del proyecto:

```bash
python3 -m http.server 8731
```

Verás algo como *"Serving HTTP on :: port 8731"*. **Deja esa ventana abierta**
(es el servidor; mientras esté abierta, la web funciona en tu ordenador).

---

## Paso 3 — Ábrela en el navegador

Ve a:

```
http://localhost:8731/index.html
```

- La primera carga tarda **unos segundos** (la web monta su motor dentro del
  navegador). Es normal.
- Lo que ves aquí es **idéntico** a lo que se publicaría. Nada de esto es
  público todavía.

Revisa con calma las vistas de la barra lateral: **Mapa**, **Ficha de país**,
**Comparador**, **Clasificación** y **El autor**.

> Si cambias algún archivo, refresca el navegador con **Cmd + Shift + R** para
> ver la versión nueva.

---

## Paso 4 — Para el servidor cuando termines

En la ventana donde arrancaste el servidor, pulsa **Ctrl + C**.

---

## Paso 5 — Publicar (solo cuando te convenza)

Cuando los cambios te gusten, se llevan a `main`, que es lo que publica la web:

```bash
git checkout main
git merge NOMBRE-DE-LA-RAMA
git push origin main
```

En 1-2 minutos, GitHub Actions regenera la web. Quedará en:

```
https://colegatron.github.io/MODELO-PROSPERIDAD-SOSTENIBLE/
```

> Si algo no te cuadra en local, **no hagas el paso 5**: los cambios se quedan
> en la rama, sin publicarse, y se pueden corregir.

---

## Resumen de un vistazo

| Quiero… | Hago… |
|---|---|
| Ver los cambios sin publicarlos | `git checkout <rama>` + `python3 -m http.server 8731` + abrir `http://localhost:8731/index.html` |
| Dejar de ver la web local | `Ctrl + C` en la ventana del servidor |
| Publicar lo que ya he aprobado | `git checkout main` + `git merge <rama>` + `git push origin main` |
