import json
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =============================================================================
#  Modelo de Prosperidad Sostenible (MPS) — Panel divulgativo
#  Objetivo: hacer los datos entendibles para cualquier persona, no solo para
#  quien sepa de estadística. Banderas + nombres, índice 0-100 comparable,
#  fichas en lenguaje llano, comparador con media ponderada, mapa y ranking.
# =============================================================================

st.set_page_config(
    page_title="MPS — Prosperidad Sostenible",
    page_icon="🌍",
    layout="wide",
)

# --- Identidad de países: ISO3 -> nombre en español -------------------------
ISO3_NOMBRE = {
    "AGO": "Angola", "ALB": "Albania", "ARE": "Emiratos Árabes", "ARG": "Argentina",
    "ARM": "Armenia", "AUS": "Australia", "AUT": "Austria", "AZE": "Azerbaiyán",
    "BDI": "Burundi", "BEL": "Bélgica", "BEN": "Benín", "BFA": "Burkina Faso",
    "BGD": "Bangladés", "BGR": "Bulgaria", "BHR": "Baréin", "BHS": "Bahamas",
    "BIH": "Bosnia", "BLZ": "Belice", "BOL": "Bolivia", "BRA": "Brasil",
    "BRB": "Barbados", "BRN": "Brunéi", "BTN": "Bután", "BWA": "Botsuana",
    "CAF": "Rep. Centroafricana", "CAN": "Canadá", "CHE": "Suiza", "CHL": "Chile",
    "CHN": "China", "CIV": "Costa de Marfil", "CMR": "Camerún", "COD": "R.D. Congo",
    "COG": "Congo", "COL": "Colombia", "COM": "Comoras", "CPV": "Cabo Verde",
    "CRI": "Costa Rica", "CYP": "Chipre", "CZE": "Rep. Checa", "DEU": "Alemania",
    "DJI": "Yibuti", "DNK": "Dinamarca", "DOM": "Rep. Dominicana", "DZA": "Argelia",
    "ECU": "Ecuador", "EGY": "Egipto", "ESP": "España", "EST": "Estonia",
    "ETH": "Etiopía", "FIN": "Finlandia", "FJI": "Fiyi", "FRA": "Francia",
    "GAB": "Gabón", "GBR": "Reino Unido", "GEO": "Georgia", "GHA": "Ghana",
    "GIN": "Guinea", "GMB": "Gambia", "GNB": "Guinea-Bisáu", "GRC": "Grecia",
    "GTM": "Guatemala", "GUY": "Guyana", "HKG": "Hong Kong", "HND": "Honduras",
    "HRV": "Croacia", "HUN": "Hungría", "IDN": "Indonesia", "IND": "India",
    "IRL": "Irlanda", "IRN": "Irán", "IRQ": "Irak", "ISL": "Islandia",
    "ISR": "Israel", "ITA": "Italia", "JAM": "Jamaica", "JOR": "Jordania",
    "JPN": "Japón", "KAZ": "Kazajistán", "KEN": "Kenia", "KGZ": "Kirguistán",
    "KHM": "Camboya", "KOR": "Corea del Sur", "KWT": "Kuwait", "LAO": "Laos",
    "LBN": "Líbano", "LBR": "Liberia", "LBY": "Libia", "LKA": "Sri Lanka",
    "LSO": "Lesoto", "LTU": "Lituania", "LUX": "Luxemburgo", "LVA": "Letonia",
    "MAR": "Marruecos", "MDA": "Moldavia", "MDG": "Madagascar", "MEX": "México",
    "MKD": "Macedonia del Norte", "MLI": "Mali", "MLT": "Malta", "MMR": "Myanmar",
    "MNE": "Montenegro", "MNG": "Mongolia", "MOZ": "Mozambique", "MRT": "Mauritania",
    "MUS": "Mauricio", "MWI": "Malaui", "MYS": "Malasia", "NAM": "Namibia",
    "NER": "Níger", "NGA": "Nigeria", "NIC": "Nicaragua", "NLD": "Países Bajos",
    "NOR": "Noruega", "NPL": "Nepal", "NZL": "Nueva Zelanda", "OMN": "Omán",
    "PAK": "Pakistán", "PAN": "Panamá", "PER": "Perú", "PHL": "Filipinas",
    "PNG": "Papúa Nueva Guinea", "POL": "Polonia", "PRT": "Portugal", "PRY": "Paraguay",
    "QAT": "Catar", "ROU": "Rumania", "RUS": "Rusia", "RWA": "Ruanda",
    "SAU": "Arabia Saudí", "SDN": "Sudán", "SEN": "Senegal", "SGP": "Singapur",
    "SLE": "Sierra Leona", "SLV": "El Salvador", "SOM": "Somalia", "SRB": "Serbia",
    "SUR": "Surinam", "SVK": "Eslovaquia", "SVN": "Eslovenia", "SWE": "Suecia",
    "SWZ": "Suazilandia", "SYC": "Seychelles", "SYR": "Siria", "TCD": "Chad",
    "TGO": "Togo", "THA": "Tailandia", "TJK": "Tayikistán", "TLS": "Timor Oriental",
    "TTO": "Trinidad y Tobago", "TUN": "Túnez", "TUR": "Turquía", "TWN": "Taiwán",
    "TZA": "Tanzania", "UGA": "Uganda", "UKR": "Ucrania", "URY": "Uruguay",
    "USA": "Estados Unidos", "VEN": "Venezuela", "VNM": "Vietnam", "YEM": "Yemen",
    "ZAF": "Sudáfrica", "ZMB": "Zambia", "ZWE": "Zimbabue",
}

# --- ISO3 -> ISO2 (para construir el emoji de bandera) ----------------------
ISO3_ISO2 = {
    "AGO": "AO", "ALB": "AL", "ARE": "AE", "ARG": "AR", "ARM": "AM", "AUS": "AU",
    "AUT": "AT", "AZE": "AZ", "BDI": "BI", "BEL": "BE", "BEN": "BJ", "BFA": "BF",
    "BGD": "BD", "BGR": "BG", "BHR": "BH", "BHS": "BS", "BIH": "BA", "BLZ": "BZ",
    "BOL": "BO", "BRA": "BR", "BRB": "BB", "BRN": "BN", "BTN": "BT", "BWA": "BW",
    "CAF": "CF", "CAN": "CA", "CHE": "CH", "CHL": "CL", "CHN": "CN", "CIV": "CI",
    "CMR": "CM", "COD": "CD", "COG": "CG", "COL": "CO", "COM": "KM", "CPV": "CV",
    "CRI": "CR", "CYP": "CY", "CZE": "CZ", "DEU": "DE", "DJI": "DJ", "DNK": "DK",
    "DOM": "DO", "DZA": "DZ", "ECU": "EC", "EGY": "EG", "ESP": "ES", "EST": "EE",
    "ETH": "ET", "FIN": "FI", "FJI": "FJ", "FRA": "FR", "GAB": "GA", "GBR": "GB",
    "GEO": "GE", "GHA": "GH", "GIN": "GN", "GMB": "GM", "GNB": "GW", "GRC": "GR",
    "GTM": "GT", "GUY": "GY", "HKG": "HK", "HND": "HN", "HRV": "HR", "HUN": "HU",
    "IDN": "ID", "IND": "IN", "IRL": "IE", "IRN": "IR", "IRQ": "IQ", "ISL": "IS",
    "ISR": "IL", "ITA": "IT", "JAM": "JM", "JOR": "JO", "JPN": "JP", "KAZ": "KZ",
    "KEN": "KE", "KGZ": "KG", "KHM": "KH", "KOR": "KR", "KWT": "KW", "LAO": "LA",
    "LBN": "LB", "LBR": "LR", "LBY": "LY", "LKA": "LK", "LSO": "LS", "LTU": "LT",
    "LUX": "LU", "LVA": "LV", "MAR": "MA", "MDA": "MD", "MDG": "MG", "MEX": "MX",
    "MKD": "MK", "MLI": "ML", "MLT": "MT", "MMR": "MM", "MNE": "ME", "MNG": "MN",
    "MOZ": "MZ", "MRT": "MR", "MUS": "MU", "MWI": "MW", "MYS": "MY", "NAM": "NA",
    "NER": "NE", "NGA": "NG", "NIC": "NI", "NLD": "NL", "NOR": "NO", "NPL": "NP",
    "NZL": "NZ", "OMN": "OM", "PAK": "PK", "PAN": "PA", "PER": "PE", "PHL": "PH",
    "PNG": "PG", "POL": "PL", "PRT": "PT", "PRY": "PY", "QAT": "QA", "ROU": "RO",
    "RUS": "RU", "RWA": "RW", "SAU": "SA", "SDN": "SD", "SEN": "SN", "SGP": "SG",
    "SLE": "SL", "SLV": "SV", "SOM": "SO", "SRB": "RS", "SUR": "SR", "SVK": "SK",
    "SVN": "SI", "SWE": "SE", "SWZ": "SZ", "SYC": "SC", "SYR": "SY", "TCD": "TD",
    "TGO": "TG", "THA": "TH", "TJK": "TJ", "TLS": "TL", "TTO": "TT", "TUN": "TN",
    "TUR": "TR", "TWN": "TW", "TZA": "TZ", "UGA": "UG", "UKR": "UA", "URY": "UY",
    "USA": "US", "VEN": "VE", "VNM": "VN", "YEM": "YE", "ZAF": "ZA", "ZMB": "ZM",
    "ZWE": "ZW",
}


def bandera(iso3):
    """Emoji de bandera a partir del código ISO3 (vía ISO2)."""
    iso2 = ISO3_ISO2.get(iso3)
    if not iso2:
        return "🏳️"
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in iso2)


def nombre(iso3):
    return ISO3_NOMBRE.get(iso3, iso3)


def etiqueta(iso3):
    return f"{bandera(iso3)} {nombre(iso3)}"


# Diccionarios auxiliares para los selectores (nombre -> iso3)
NOMBRE_ISO3 = {nombre(c): c for c in ISO3_NOMBRE}

# Categorías del Índice de Prosperidad (0-100, percentil dentro del año)
CATEGORIAS = [
    (80, "Excelente", "#16a34a"),
    (60, "Bueno", "#65a30d"),
    (40, "Regular", "#ca8a04"),
    (20, "Débil", "#ea580c"),
    (0, "Crítico", "#dc2626"),
]


def categoria(indice):
    for umbral, nombre_cat, color in CATEGORIAS:
        if indice >= umbral:
            return nombre_cat, color
    return "Crítico", "#dc2626"


# -----------------------------------------------------------------------------
#  Carga y preparación de datos
# -----------------------------------------------------------------------------
@st.cache_data
def cargar_datos():
    ruta = os.path.join("BaseDeDatos", "Pizarra_MPS_Master.json")
    if not os.path.exists(ruta):
        return pd.DataFrame(), {}
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    filas = []
    for iso3, anios in data.items():
        for anio, vars_ in anios.items():
            fila = dict(vars_)
            fila["iso3"] = iso3
            fila["pais"] = nombre(iso3)
            fila["bandera"] = bandera(iso3)
            fila["anio"] = int(anio)
            filas.append(fila)
    df = pd.DataFrame(filas)

    # Índice de Prosperidad 0-100: percentil de la PN dentro de cada año.
    # Esto "doma" la escala (la PN bruta llega a millones negativos por unos
    # pocos petroestados) y hace los países comparables de un vistazo.
    df["indice"] = df.groupby("anio")["PN"].rank(pct=True) * 100
    # Puesto (1 = más prosperidad neta) y total de países con dato ese año.
    df["puesto"] = df.groupby("anio")["PN"].rank(ascending=False, method="min").astype(int)
    df["total_anio"] = df.groupby("anio")["PN"].transform("count")

    # PIB PPA per cápita (para la media ponderada del comparador)
    pib = {}
    ruta_pib = os.path.join("BaseDeDatos", "pib_ppa_2008_2023.json")
    if os.path.exists(ruta_pib):
        with open(ruta_pib, "r", encoding="utf-8") as f:
            pib = json.load(f)
    return df, pib


df, PIB = cargar_datos()

GLOSARIO = {
    "PN": "Prosperidad Neta — la riqueza real que queda disponible tras descontar el lastre institucional. Más alto = mejor.",
    "TPL": "Tasa de Parasitismo Total — cuánto pesa la ineficiencia del aparato estatal. Más alto = peor.",
    "estructura": "Coste de mantener el aparato estatal (cargos, burocracia), en % del PIB. Más bajo = más ligero.",
    "transferencias": "Redistribución (pensiones, subvenciones, planes sociales), en % del PIB.",
    "carga_oculta": "Daño institucional por ineficiencias sistémicas, estimado por regresión. Más bajo = mejor.",
    "indice": "Índice de Prosperidad (0-100): posición del país frente al resto ese año. 100 = el mejor.",
}

if df.empty:
    st.error("No se han podido cargar los datos (BaseDeDatos/Pizarra_MPS_Master.json).")
    st.stop()

ANIOS = sorted(df["anio"].unique())
ANIO_MAX = max(ANIOS)


def fmt(x, dec=1):
    """Formatea números, abreviando los extremos para que sean legibles."""
    if pd.isna(x):
        return "—"
    ax = abs(x)
    if ax >= 1_000_000:
        return f"{x/1_000_000:.1f} M"
    if ax >= 10_000:
        return f"{x/1_000:.1f} k"
    return f"{x:,.{dec}f}".replace(",", " ")


# -----------------------------------------------------------------------------
#  Cabecera + navegación
# -----------------------------------------------------------------------------
st.title("🌍 Modelo de Prosperidad Sostenible")
st.caption(
    "¿Cuánta de la riqueza que genera tu país llega de verdad a la gente, y "
    "cuánta se diluye en el lastre institucional? Explóralo de forma sencilla."
)

VISTAS = {
    "🗺️ Mapa mundial": "mapa",
    "🪪 Ficha de país": "ficha",
    "⚖️ Comparador": "comparador",
    "🏆 Clasificación": "ranking",
    "🏛️ El autor": "autor",
}
eleccion = st.sidebar.radio("Vista", list(VISTAS.keys()))
vista = VISTAS[eleccion]

st.sidebar.markdown("---")
st.sidebar.markdown("#### ¿Qué significan los términos?")
for clave in ["indice", "PN", "TPL", "estructura", "transferencias", "carga_oculta"]:
    st.sidebar.caption(f"**{clave}** — {GLOSARIO[clave]}")


def selector_anio(key):
    return st.select_slider(
        "Año", options=ANIOS, value=ANIO_MAX, key=key
    )


# =============================================================================
#  VISTA 1 — MAPA MUNDIAL
# =============================================================================
if vista == "mapa":
    st.header("🗺️ El mundo de un vistazo")
    col1, col2 = st.columns([1, 2])
    with col1:
        metrica = st.selectbox(
            "¿Qué quieres ver en el mapa?",
            ["Índice de Prosperidad (0-100)", "Prosperidad Neta (PN)", "Parasitismo (TPL)"],
        )
    with col2:
        anio = selector_anio("anio_mapa")

    dfa = df[df["anio"] == anio].copy()

    if metrica.startswith("Índice"):
        color_col, escala, titulo_color = "indice", "RdYlGn", "Índice 0-100"
    elif metrica.startswith("Prosperidad"):
        # El índice colorea (legible); la PN bruta se enseña al pasar el ratón.
        color_col, escala, titulo_color = "indice", "RdYlGn", "Índice 0-100"
    else:
        # Parasitismo: invertimos el índice para que rojo = más parásito.
        dfa["indice_inv"] = 100 - dfa["indice"]
        color_col, escala, titulo_color = "indice_inv", "RdYlGn_r", "Parasitismo (rel.)"

    dfa["PN_txt"] = dfa["PN"].map(lambda v: fmt(v))
    dfa["TPL_txt"] = dfa["TPL"].map(lambda v: fmt(v))
    fig = px.choropleth(
        dfa,
        locations="iso3",
        color=color_col,
        hover_name="pais",
        color_continuous_scale=escala,
        range_color=(0, 100),
        custom_data=["PN_txt", "TPL_txt", "puesto", "total_anio"],
        labels={color_col: titulo_color},
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>"
        "Prosperidad Neta: %{customdata[0]}<br>"
        "Parasitismo (TPL): %{customdata[1]}<br>"
        "Puesto: %{customdata[2]} de %{customdata[3]}<extra></extra>"
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=520,
        geo=dict(showframe=False, projection_type="natural earth"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "El color refleja la posición relativa de cada país ese año (verde = mejor). "
        "Los valores brutos aparecen al pasar el ratón."
    )


# =============================================================================
#  VISTA 2 — FICHA DE PAÍS
# =============================================================================
elif vista == "ficha":
    st.header("🪪 Ficha de país")
    c1, c2 = st.columns([2, 1])
    with c1:
        nombres = sorted(df["pais"].unique())
        idx_def = nombres.index("España") if "España" in nombres else 0
        pais_sel = st.selectbox("País", nombres, index=idx_def)
    with c2:
        anio = selector_anio("anio_ficha")

    iso3 = NOMBRE_ISO3.get(pais_sel)
    fila = df[(df["pais"] == pais_sel) & (df["anio"] == anio)]
    hist = df[df["pais"] == pais_sel].sort_values("anio")
    if fila.empty:
        st.warning("No hay datos para ese país y año.")
        st.stop()
    r = fila.iloc[0]
    prev = hist[hist["anio"] == anio - 1]

    cat_nombre, cat_color = categoria(r["indice"])
    st.markdown(
        f"## {bandera(iso3)} {pais_sel} "
        f"<span style='background:{cat_color};color:white;padding:2px 12px;"
        f"border-radius:999px;font-size:0.5em;vertical-align:middle;'>{cat_nombre}</span>",
        unsafe_allow_html=True,
    )

    # KPIs con variación respecto al año anterior
    def delta(col, inverso=False):
        if prev.empty:
            return None
        d = r[col] - prev.iloc[0][col]
        return round(d, 2)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Índice de Prosperidad", f"{r['indice']:.0f}/100", delta("indice"))
    k2.metric("Puesto mundial", f"{int(r['puesto'])}º de {int(r['total_anio'])}")
    k3.metric("Prosperidad Neta (PN)", fmt(r["PN"]), delta("PN"))
    k4.metric("Parasitismo (TPL)", fmt(r["TPL"]), delta("TPL"), delta_color="inverse")

    # Veredicto en lenguaje llano
    pct_mejor = 100 - r["indice"]
    if r["PN"] >= 0:
        frase_pn = (
            f"De cada 100 € de riqueza, alrededor de **{max(0, min(100, r['PN'])):.0f} €** "
            "quedan como prosperidad neta tras el lastre institucional."
        )
    else:
        frase_pn = (
            "El modelo estima que el lastre institucional **se come toda la riqueza "
            "generada** (prosperidad neta negativa): un caso extremo."
        )
    st.info(
        f"**{pais_sel}** está en el puesto **{int(r['puesto'])} de {int(r['total_anio'])}** "
        f"en {anio}. Lo hace mejor que el **{r['indice']:.0f}%** de los países y peor que "
        f"el **{pct_mejor:.0f}%**. {frase_pn}"
    )

    # Evolución temporal
    cg1, cg2 = st.columns(2)
    with cg1:
        fig_idx = px.line(
            hist, x="anio", y="indice", markers=True,
            title="Índice de Prosperidad (0-100) en el tiempo",
        )
        fig_idx.update_yaxes(range=[0, 100])
        fig_idx.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig_idx, use_container_width=True)
    with cg2:
        fig_p = px.line(
            hist, x="anio", y="puesto", markers=True,
            title="Puesto mundial (1 = mejor)",
        )
        fig_p.update_yaxes(autorange="reversed")
        fig_p.update_layout(height=320, margin=dict(t=40, b=0))
        st.plotly_chart(fig_p, use_container_width=True)

    # Componentes: país vs mediana mundial del año
    st.subheader("¿De dónde viene? Componentes frente a la mediana mundial")
    dfa = df[df["anio"] == anio]
    comp = []
    for col in ["estructura", "transferencias", "carga_oculta"]:
        comp.append({"Componente": col, "Este país": r[col], "Mediana mundial": dfa[col].median()})
    comp_df = pd.DataFrame(comp).melt(
        id_vars="Componente", var_name="Serie", value_name="Valor"
    )
    fig_comp = px.bar(
        comp_df, x="Componente", y="Valor", color="Serie", barmode="group",
    )
    fig_comp.update_layout(height=320, margin=dict(t=10, b=0))
    st.plotly_chart(fig_comp, use_container_width=True)


# =============================================================================
#  VISTA 3 — COMPARADOR (incluye grupo con media ponderada)
# =============================================================================
elif vista == "comparador":
    st.header("⚖️ Comparador de países")
    anio = selector_anio("anio_comp")
    dfa = df[df["anio"] == anio].copy()
    nombres = sorted(dfa["pais"].unique())

    pre = [p for p in ["España", "Alemania", "Estados Unidos", "Suiza"] if p in nombres]
    seleccion = st.multiselect(
        "Elige uno o varios países", nombres, default=pre
    )

    if len(seleccion) < 1:
        st.info("Selecciona al menos un país.")
        st.stop()

    metrica = st.radio(
        "Métrica",
        ["Índice de Prosperidad (0-100)", "Prosperidad Neta (PN)", "Parasitismo (TPL)"],
        horizontal=True,
    )
    col_map = {
        "Índice de Prosperidad (0-100)": "indice",
        "Prosperidad Neta (PN)": "PN",
        "Parasitismo (TPL)": "TPL",
    }
    col = col_map[metrica]

    sub = dfa[dfa["pais"].isin(seleccion)].copy()
    sub["etiqueta"] = sub["bandera"] + " " + sub["pais"]
    sub = sub.sort_values(col, ascending=(col == "TPL"))
    fig = px.bar(
        sub, x=col, y="etiqueta", orientation="h", color=col,
        color_continuous_scale="RdYlGn" if col != "TPL" else "RdYlGn_r",
        text=sub[col].map(lambda v: fmt(v)),
    )
    fig.update_layout(
        height=80 + 45 * len(sub), margin=dict(t=10, b=0),
        yaxis_title="", coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)
    if col in ("PN", "TPL"):
        st.caption(
            "Aviso: la PN y la TPL brutas pueden tener valores extremos en unos "
            "pocos países (petroestados). El Índice 0-100 es más comparable."
        )

    # ---- Grupo con media ponderada vs país objetivo ----
    st.markdown("---")
    st.subheader("🧮 Grupo vs país: media ponderada")
    st.caption(
        "Agrupa los países seleccionados arriba en un solo bloque y compáralo "
        "con un país concreto."
    )
    cponder, cobj = st.columns(2)
    with cponder:
        modo = st.radio(
            "¿Cómo promediar el grupo?",
            ["Media simple", "Ponderada por PIB (PPA per cápita)"],
        )
    with cobj:
        objetivo = st.selectbox(
            "País a comparar contra el grupo",
            nombres,
            index=nombres.index("España") if "España" in nombres else 0,
        )

    def peso(iso3_code):
        if modo.startswith("Media simple"):
            return 1.0
        return float(PIB.get(iso3_code, {}).get(str(anio), 0.0)) or 0.0

    grupo = dfa[dfa["pais"].isin(seleccion)]
    resumen = {}
    for c in ["indice", "PN", "TPL"]:
        pesos = grupo["iso3"].map(peso)
        total = pesos.sum()
        if total > 0:
            resumen[c] = float((grupo[c] * pesos).sum() / total)
        else:
            resumen[c] = float(grupo[c].mean())

    obj_row = dfa[dfa["pais"] == objetivo].iloc[0]
    comp_df = pd.DataFrame(
        {
            "Métrica": ["Índice (0-100)", "Prosperidad Neta", "Parasitismo (TPL)"],
            f"Grupo ({len(seleccion)} países)": [resumen["indice"], resumen["PN"], resumen["TPL"]],
            objetivo: [obj_row["indice"], obj_row["PN"], obj_row["TPL"]],
        }
    )
    largo = comp_df.melt(id_vars="Métrica", var_name="Quién", value_name="Valor")
    # Comparación clara con el índice (comparable); PN/TPL en tabla aparte.
    idx_only = largo[largo["Métrica"] == "Índice (0-100)"]
    fig_g = px.bar(
        idx_only, x="Quién", y="Valor", color="Quién", text=idx_only["Valor"].map(lambda v: f"{v:.0f}"),
        title="Índice de Prosperidad (0-100): grupo vs país",
    )
    fig_g.update_yaxes(range=[0, 100])
    fig_g.update_layout(height=360, margin=dict(t=40, b=0), showlegend=False)
    st.plotly_chart(fig_g, use_container_width=True)

    tabla = comp_df.copy()
    for c in tabla.columns[1:]:
        tabla[c] = tabla[c].map(lambda v: fmt(v))
    st.table(tabla.set_index("Métrica"))


# =============================================================================
#  VISTA 4 — CLASIFICACIÓN (ranking tipo liga)
# =============================================================================
elif vista == "ranking":
    st.header("🏆 Clasificación mundial")
    c1, c2 = st.columns([1, 1])
    with c1:
        anio = selector_anio("anio_rank")
    with c2:
        orden = st.selectbox(
            "Ordenar por", ["Índice de Prosperidad", "Prosperidad Neta", "Menor parasitismo (TPL)"]
        )

    dfa = df[df["anio"] == anio].copy()
    prevdf = df[df["anio"] == anio - 1][["iso3", "puesto"]].rename(
        columns={"puesto": "puesto_prev"}
    )
    dfa = dfa.merge(prevdf, on="iso3", how="left")

    if orden == "Índice de Prosperidad":
        dfa = dfa.sort_values("indice", ascending=False)
    elif orden == "Prosperidad Neta":
        dfa = dfa.sort_values("PN", ascending=False)
    else:
        dfa = dfa.sort_values("TPL", ascending=True)
    dfa = dfa.reset_index(drop=True)
    dfa["#"] = dfa.index + 1

    def cambio(row):
        if pd.isna(row["puesto_prev"]):
            return "—"
        d = int(row["puesto_prev"] - row["puesto"])
        if d > 0:
            return f"▲ {d}"
        if d < 0:
            return f"▼ {abs(d)}"
        return "="

    dfa["Δ vs año anterior"] = dfa.apply(cambio, axis=1)
    dfa["País"] = dfa["bandera"] + " " + dfa["pais"]
    dfa["Prosperidad Neta"] = dfa["PN"].map(lambda v: fmt(v))
    dfa["Parasitismo (TPL)"] = dfa["TPL"].map(lambda v: fmt(v))

    tabla = dfa[["#", "País", "indice", "Prosperidad Neta", "Parasitismo (TPL)", "Δ vs año anterior"]]
    st.dataframe(
        tabla,
        hide_index=True,
        use_container_width=True,
        height=620,
        column_config={
            "#": st.column_config.NumberColumn("#", width="small"),
            "indice": st.column_config.ProgressColumn(
                "Índice de Prosperidad", min_value=0, max_value=100, format="%.0f"
            ),
        },
    )
    st.caption(
        "Δ compara el puesto (por Prosperidad Neta) con el del año anterior. "
        "▲ sube, ▼ baja."
    )

# =============================================================================
#  VISTA 5 — EL AUTOR (atribuciones a Pedro Andrés Aranda Muñoz)
# =============================================================================
elif vista == "autor":
    st.markdown(
        """
        <style>
        .tab-hero {
            background: radial-gradient(circle at 20% 20%, #3a0d0d 0%, #1a0808 70%);
            border: 1px solid #c9a227; border-radius: 18px;
            padding: 34px 30px; color: #f5ede0; margin-bottom: 22px;
            display: flex; gap: 26px; align-items: center; flex-wrap: wrap;
        }
        .tab-monograma {
            width: 110px; height: 110px; flex: 0 0 110px; border-radius: 50%;
            background: linear-gradient(145deg, #c9a227, #8b6f14);
            display: flex; align-items: center; justify-content: center;
            font-size: 58px; box-shadow: 0 0 0 4px rgba(201,162,39,.25);
        }
        .tab-hero h1 { color: #ffffff; margin: 0 0 4px 0; font-size: 1.9rem; }
        .tab-tagline { color: #c9a227; font-weight: 700; letter-spacing: .5px;
            text-transform: uppercase; font-size: .9rem; margin-bottom: 8px; }
        .tab-hero p { margin: 0; color: #e7dcc8; max-width: 640px; line-height: 1.5; }
        .tab-maximas { display: flex; gap: 14px; flex-wrap: wrap; margin: 6px 0 22px; }
        .tab-maxima {
            flex: 1 1 200px; background: #fbf7ee; border-left: 4px solid #c9a227;
            border-radius: 8px; padding: 16px 18px; font-style: italic;
            font-size: 1.05rem; color: #3a2e10;
        }
        .tab-cards { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 22px; }
        .tab-card {
            flex: 1 1 260px; border: 1px solid #e6e0d2; border-radius: 14px;
            padding: 20px 22px; background: #ffffff;
        }
        .tab-card h3 { margin: 0 0 8px 0; }
        .tab-card.quiosco { border-top: 5px solid #c0392b; }
        .tab-card.forjador { border-top: 5px solid #5b3a8c; }
        .tab-libro {
            display: flex; gap: 22px; flex-wrap: wrap; align-items: center;
            background: linear-gradient(135deg, #1a0808, #3a0d0d); color: #f5ede0;
            border: 1px solid #c9a227; border-radius: 16px; padding: 26px 28px;
            margin-bottom: 22px;
        }
        .tab-portada {
            flex: 0 0 120px; width: 120px; height: 170px; border-radius: 8px;
            background: linear-gradient(160deg, #c9a227, #6b5310); color: #1a0808;
            display: flex; align-items: center; justify-content: center;
            text-align: center; font-weight: 800; padding: 14px; font-size: .95rem;
            box-shadow: 0 8px 24px rgba(0,0,0,.4);
        }
        .tab-libro h2 { color: #fff; margin: 0 0 6px 0; }
        .tab-badge {
            display: inline-block; background: #c9a227; color: #1a0808;
            font-weight: 700; border-radius: 999px; padding: 3px 14px;
            font-size: .8rem; margin-bottom: 10px;
        }
        .tab-btn {
            display: inline-block; background: #c9a227; color: #1a0808 !important;
            text-decoration: none; font-weight: 700; padding: 10px 20px;
            border-radius: 8px; margin-top: 6px;
        }
        .tab-enlaces { display: flex; gap: 12px; flex-wrap: wrap; }
        .tab-enlace {
            text-decoration: none; border: 1px solid #e0dccf; border-radius: 10px;
            padding: 12px 18px; color: #2b2b2b !important; font-weight: 600;
            background: #fbf9f4; flex: 1 1 150px; text-align: center;
        }
        .tab-enlace:hover, .tab-card:hover { border-color: #c9a227; }
        </style>

        <div class="tab-hero">
            <div class="tab-monograma">🏛️</div>
            <div>
                <div class="tab-tagline">Bienvenido al Tablinum</div>
                <h1>Pedro Andrés Aranda Muñoz</h1>
                <p><b>Jurista, analista y creador.</b> Autor del <b>Modelo de
                Prosperidad Sostenible (MPS)</b> en el que se basa este panel.
                «El dato mata al relato»: aquí se auditan las cuentas del poder y
                se mide, con números, cuánto pesa de verdad la fricción estatal.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="tab-maximas">
            <div class="tab-maxima">«El dato mata al relato.»</div>
            <div class="tab-maxima">«El individuo prevalece sobre la masa.»</div>
            <div class="tab-maxima">«Nadie tiene derecho a pasar sobre ti.»</div>
        </div>

        <div class="tab-cards">
            <div class="tab-card quiosco">
                <h3>🔴 El Quiosco</h3>
                <p>Análisis diario de prensa y geopolítica sin filtros. Usa el
                Modelo de Prosperidad Sostenible para medir matemáticamente la
                <b>Carga Parasitaria Total</b> y mostrar la fricción del aparato
                estatal.</p>
            </div>
            <div class="tab-card forjador">
                <h3>🌌 El Forjador</h3>
                <p>Ciencia ficción y <i>lore</i>. Porque el hombre libre también
                necesita imaginación: el último refugio que no pueden regular.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="tab-libro">
            <div class="tab-portada">Genealogía del Conflicto Eterno</div>
            <div>
                <div class="tab-badge">📚 Disponible el 12 de octubre</div>
                <h2>Genealogía del Conflicto Eterno</h2>
                <p>La nueva obra de Pedro Andrés Aranda Muñoz.</p>
                <a class="tab-btn" href="https://www.amazon.es/dp/B0GMLH9NL2"
                   target="_blank" rel="noopener">Verlo en Amazon →</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("📺 Canal de YouTube")
    st.markdown(
        '<a class="tab-btn" href="https://www.youtube.com/@pedroandresaranda" '
        'target="_blank" rel="noopener">▶ El Tablinum — @pedroandresaranda</a>',
        unsafe_allow_html=True,
    )
    st.caption("717 vídeos · análisis, geopolítica y ciencia ficción.")

    st.subheader("📚 Más libros")
    st.markdown(
        """
        <div class="tab-enlaces">
            <a class="tab-enlace" href="https://amzn.eu/d/0gzMv98Y" target="_blank" rel="noopener">¿Cuánto cuesta tu político?</a>
            <a class="tab-enlace" href="https://amzn.eu/d/4Si0xvm" target="_blank" rel="noopener">Las Realidades de Eva</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("🔗 Síguelo")
    st.markdown(
        """
        <div class="tab-enlaces">
            <a class="tab-enlace" href="https://www.youtube.com/@pedroandresaranda" target="_blank" rel="noopener">▶ YouTube</a>
            <a class="tab-enlace" href="https://www.tiktok.com/@andrs.muoz646" target="_blank" rel="noopener">🎵 TikTok</a>
            <a class="tab-enlace" href="https://www.instagram.com/amopoemp" target="_blank" rel="noopener">📷 Instagram</a>
            <a class="tab-enlace" href="https://www.facebook.com/pedroandres.arandamunoz" target="_blank" rel="noopener">👍 Facebook</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "El **Modelo de Prosperidad Sostenible** y su metodología son obra de "
        "Pedro Andrés Aranda Muñoz. Este panel es una herramienta para divulgar "
        "y explorar su trabajo. *Pan, Patria y Justicia.*"
    )

# --- Pie -----------------------------------------------------------------------
st.markdown("---")
with st.expander("🆕 Novedades de esta versión (2.0)"):
    st.markdown(
        "Esta versión rediseña el panel para que se entienda sin saber de "
        "estadística:\n"
        "- **Países con nombre y bandera** en vez de códigos.\n"
        "- **Índice de Prosperidad 0-100** comparable (antes los valores brutos "
        "tenían extremos que hacían ilegibles las gráficas).\n"
        "- **Mapa mundial**, **ficha de país** en lenguaje llano, **comparador** "
        "con media ponderada y **clasificación** tipo liga.\n\n"
        "Versiones anteriores: tres vistas con tablas/gráficas de datos en crudo "
        "y códigos de país. Detalle completo en el `CHANGELOG.md` del repositorio."
    )
with st.expander("⚠️ Metodología y fuentes"):
    st.warning(
        "Datos armonizados de organismos internacionales (BM, FMI, BCE, OCDE). "
        "El **Índice de Prosperidad (0-100)** es la posición relativa (percentil) "
        "de la Prosperidad Neta dentro de cada año; se usa para hacer los países "
        "comparables, ya que los valores brutos de PN y TPL tienen extremos muy "
        "grandes. Pan, Patria y Justicia."
    )
