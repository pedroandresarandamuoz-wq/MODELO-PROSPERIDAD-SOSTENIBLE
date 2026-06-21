import json
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =============================================================================
#  Modelo de Prosperidad Sostenible (MPS) — Panel divulgativo Completo
#  Mantiene: Vista Económica, ERI, Mapa, Ficha, Comparador, Ranking, Autor.
#  Integra: Subsidio Exterior (S_E) y Prosperidad Sostenible (PS) de la v3.0.
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
    iso2 = ISO3_ISO2.get(iso3)
    if not iso2:
        return "🏳️"
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in iso2)

def nombre(iso3):
    return ISO3_NOMBRE.get(iso3, iso3)

def etiqueta(iso3):
    return f"{bandera(iso3)} {nombre(iso3)}"

NOMBRE_ISO3 = {nombre(c): c for c in ISO3_NOMBRE}

# Categorías del Índice MPS
CATEGORIAS_MPS = [
    (80, "Excelente", "#16a34a"),
    (60, "Bueno", "#65a30d"),
    (40, "Regular", "#ca8a04"),
    (20, "Débil", "#ea580c"),
    (0,  "Crítico", "#dc2626"),
]

def categoria_mps(indice):
    for umbral, etiq, color in CATEGORIAS_MPS:
        if indice >= umbral:
            return etiq, color
    return "Crítico", "#dc2626"

def etiqueta_se(se_pct):
    if se_pct < -15:
        return "Gran exportador neto", "#16a34a"
    elif se_pct < -5:
        return "Exportador neto", "#65a30d"
    elif se_pct < 0:
        return "Ligero exportador neto", "#a3e635"
    elif se_pct < 5:
        return "Ligero importador neto", "#fbbf24"
    elif se_pct < 15:
        return "Importador neto", "#f97316"
    else:
        return "Gran importador neto", "#dc2626"

def fmt(x, dec=1):
    if pd.isna(x):
        return "—"
    ax = abs(x)
    if ax >= 1_000_000_000:
        return f"{x/1_000_000_000:.1f} B"
    if ax >= 1_000_000:
        return f"{x/1_000_000:.1f} M"
    if ax >= 10_000:
        return f"{x/1_000:.1f} k"
    return f"{x:,.{dec}f}".replace(",", " ")


# -----------------------------------------------------------------------------
#  Carga de datos
# -----------------------------------------------------------------------------
BASE = "BaseDeDatos"

def _json(filename):
    path = os.path.join(BASE, filename)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def cargar_datos_principales():
    # --- MPS principal (PN, TPL, estructura, transferencias, carga_oculta) ---
    data = _json("Pizarra_MPS_Master.json")
    filas = []
    if data:
        for iso3, anios in data.items():
            for anio, vars_ in anios.items():
                fila = dict(vars_)
                fila["iso3"] = iso3
                fila["pais"] = nombre(iso3)
                fila["bandera"] = bandera(iso3)
                fila["anio"] = int(anio)
                filas.append(fila)
    df = pd.DataFrame(filas)
    if not df.empty:
        df["indice"] = df.groupby("anio")["PN"].rank(pct=True) * 100
        df["puesto"] = df.groupby("anio")["PN"].rank(ascending=False, method="min").astype(int)
        df["total_anio"] = df.groupby("anio")["PN"].transform("count")

    # --- PIB PPA per cápita (comparador) ---
    pib = _json("pib_ppa_2008_2023.json")

    # --- Subsidio Exterior S_E ---
    se_raw = _json("S_E.json")
    se_filas = []
    if se_raw:
        for iso3, anios in se_raw.items():
            for anio, v in anios.items():
                se_filas.append({
                    "iso3": iso3,
                    "pais": nombre(iso3),
                    "anio": int(anio),
                    "s_e_raw_usd": v.get("s_e_raw_usd"),
                    "s_e_pct_pib": v.get("s_e_pct_pib"),
                    "pib_nominal": v.get("pib_nominal"),
                })
    df_se = pd.DataFrame(se_filas) if se_filas else pd.DataFrame()

    # --- Prosperidad Sostenible PS = PN + S_E_pct_pib ---
    ps_raw = _json("PS.json")
    ps_filas = []
    if ps_raw:
        for iso3, anios in ps_raw.items():
            for anio, v in anios.items():
                ps_filas.append({
                    "iso3": iso3,
                    "pais": nombre(iso3),
                    "anio": int(anio),
                    "ps_valor": v,
                })
    df_ps = pd.DataFrame(ps_filas) if ps_filas else pd.DataFrame()
    if not df_ps.empty:
        # Clave para el mapa: calcular el índice 0-100 para la PS (igual que la PN)
        df_ps["indice_ps"] = df_ps.groupby("anio")["ps_valor"].rank(pct=True) * 100

    # --- Interdependencia (desglose del S_E) ---
    inter_raw = _json("interdependencia.json")
    inter_filas = []
    if inter_raw:
        for iso3, anios in inter_raw.items():
            for anio, v in anios.items():
                fin = v.get("financiero", {}) or {}
                sec = v.get("sectorial", {}) or {}
                com = v.get("comercio", {}) or {}
                inter_filas.append({
                    "iso3": iso3,
                    "pais": nombre(iso3),
                    "anio": int(anio),
                    "pn_valor": v.get("pn_valor"),
                    "oda_recibida_usd": fin.get("oda_recibida_usd"),
                    "remesas_recibidas_usd": fin.get("remesas_recibidas_usd"),
                    "tech_exports_pct": sec.get("tech_exports_pct"),
                    "energy_imports_pct": sec.get("energy_imports_pct"),
                    "exportaciones": com.get("exportaciones"),
                    "importaciones": com.get("importaciones"),
                    "balance_comercial": com.get("balance"),
                })
    df_inter = pd.DataFrame(inter_filas) if inter_filas else pd.DataFrame()

    return df, pib, df_se, df_ps, df_inter

@st.cache_data
def cargar_eri():
    """Dataset ERI (Inversión / Capital Humano) de la V2"""
    data = _json("Base_Datos_MPS_Final_ERI.json")
    filas = []
    if data:
        for iso3, anios in data.items():
            for anio, v in anios.items():
                filas.append({
                    "iso3": iso3,
                    "pais": nombre(iso3),
                    "bandera": bandera(iso3),
                    "anio": int(anio),
                    "inversion": v.get("inversion"),
                    "ch": v.get("ch"),
                    "eri": v.get("eri"),
                })
    return pd.DataFrame(filas)

df, PIB, df_se, df_ps, df_inter = cargar_datos_principales()
df_eri = cargar_eri()

GLOSARIO = {
    "PN": "Prosperidad Neta — riqueza disponible tras descontar el lastre institucional.",
    "TPL": "Tasa de Parasitismo Total — cuánto pesa la ineficiencia del aparato estatal.",
    "estructura": "Coste de mantener el aparato estatal (cargos, burocracia), en % del PIB.",
    "transferencias": "Redistribución (pensiones, subvenciones), en % del PIB.",
    "carga_oculta": "Daño institucional por ineficiencias sistémicas, estimado por regresión.",
    "indice": "Índice de Prosperidad (0-100): posición del país frente al resto ese año.",
    "eri": "ERI = Inversión / Capital Humano (CH). Indicador propio del modelo.",
    "inversion": "Inversión — variable del modelo usada en el ERI.",
    "ch": "CH — Capital Humano, variable del modelo usada en el ERI.",
    "S_E": "Subsidio Exterior — flujo neto con el mercado global. NEGATIVO = exportador neto (aporta valor). POSITIVO = importador neto (dependiente).",
    "PS": "Prosperidad Sostenible = PN + S_E. Prosperidad real una vez incorporado el efecto exterior.",
}

if df.empty:
    st.error("No se han podido cargar los datos principales (BaseDeDatos/Pizarra_MPS_Master.json).")
    st.stop()

ANIOS = sorted(df["anio"].unique())
ANIO_MAX = max(ANIOS)
ANIOS_SE = sorted(df_se["anio"].unique()) if not df_se.empty else ANIOS
ANIO_MAX_SE = max(ANIOS_SE) if ANIOS_SE else ANIO_MAX
ANIOS_ERI = sorted(df_eri["anio"].unique()) if not df_eri.empty else ANIOS


# =============================================================================
#  Cabecera + navegación
# =============================================================================
st.title("🌍 Modelo de Prosperidad Sostenible")
st.caption(
    "¿Cuánta de la riqueza que genera tu país llega de verdad a la gente, "
    "y cuánta se diluye en el lastre institucional o en la dependencia exterior?"
)

VISTAS = {
    "🗺️ Mapa mundial": "mapa",
    "🪪 Ficha de país": "ficha",
    "⚖️ Comparador": "comparador",
    "🏆 Clasificación": "ranking",
    "🧮 Vista económica (datos crudos)": "economista",
    "📈 Inversión y eficiencia (ERI)": "eri",
    "🔄 Subsidio Exterior (S_E)": "se",
    "🌱 Prosperidad Sostenible (PS)": "ps",
    "🏛️ El autor": "autor",
}
eleccion = st.sidebar.radio("Vista", list(VISTAS.keys()))
vista = VISTAS[eleccion]

st.sidebar.markdown("---")
st.sidebar.markdown("#### Glosario")
for clave, texto in GLOSARIO.items():
    st.sidebar.caption(f"**{clave}** — {texto}")

def selector_anio(key, anios=None, anio_max=None):
    _anios = anios if anios is not None else ANIOS
    _max = anio_max if anio_max is not None else ANIO_MAX
    return st.select_slider("Año", options=_anios, value=_max, key=key)

# =============================================================================
#  VISTAS
# =============================================================================

if vista == "mapa":
    st.header("🗺️ El mundo de un vistazo")
    col1, col2 = st.columns([1, 2])
    with col1:
        metrica = st.selectbox(
            "¿Qué quieres ver?",
            ["Índice de Prosperidad (0-100)", "Prosperidad Neta (PN)", "Parasitismo (TPL)"],
        )
    with col2:
        anio = selector_anio("anio_mapa")

    dfa = df[df["anio"] == anio].copy()
    if metrica.startswith("Parasitismo"):
        dfa["indice_inv"] = 100 - dfa["indice"]
        color_col, escala, titulo_color = "indice_inv", "RdYlGn_r", "Parasitismo (rel.)"
    else:
        color_col, escala, titulo_color = "indice", "RdYlGn", "Índice 0-100"

    dfa["PN_txt"] = dfa["PN"].map(fmt)
    dfa["TPL_txt"] = dfa["TPL"].map(fmt)
    fig = px.choropleth(
        dfa, locations="iso3", color=color_col, hover_name="pais",
        color_continuous_scale=escala, range_color=(0, 100),
        custom_data=["PN_txt", "TPL_txt", "puesto", "total_anio"],
        labels={color_col: titulo_color},
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>PN: %{customdata[0]}<br>"
        "TPL: %{customdata[1]}<br>Puesto: %{customdata[2]} de %{customdata[3]}<extra></extra>"
    )
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=520,
                      geo=dict(showframe=False, projection_type="natural earth"))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Verde = mejor posición relativa. Los valores brutos aparecen al pasar el ratón.")


elif vista == "ficha":
    st.header("🪪 Ficha de país")
    c1, c2 = st.columns([2, 1])
    with c1:
        nombres = sorted(df["pais"].unique())
        idx_def = nombres.index("España") if "España" in nombres else 0
        pais_sel = st.selectbox("País", nombres, index=idx_def)
    with c2:
        anio = selector_anio("anio_ficha", anios=ANIOS_SE, anio_max=ANIO_MAX_SE)

    iso3 = NOMBRE_ISO3.get(pais_sel)
    fila = df[(df["pais"] == pais_sel) & (df["anio"] == anio)]
    hist = df[df["pais"] == pais_sel].sort_values("anio")
    fila_se = df_se[(df_se["iso3"] == iso3) & (df_se["anio"] == anio)]
    fila_ps = df_ps[(df_ps["iso3"] == iso3) & (df_ps["anio"] == anio)]

    if fila.empty:
        st.warning("No hay datos MPS para ese país y año.")
        st.stop()

    r = fila.iloc[0]
    prev = hist[hist["anio"] == anio - 1]
    cat_nombre, cat_color = categoria_mps(r["indice"])

    st.markdown(
        f"## {bandera(iso3)} {pais_sel} "
        f"<span style='background:{cat_color};color:white;padding:2px 12px;"
        f"border-radius:999px;font-size:0.5em;vertical-align:middle;'>{cat_nombre}</span>",
        unsafe_allow_html=True,
    )

    def delta(col):
        if prev.empty or col not in prev.columns:
            return None
        return round(float(r[col]) - float(prev.iloc[0][col]), 2)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Índice de Prosperidad", f"{r['indice']:.0f}/100", delta("indice"))
    k2.metric("Puesto mundial", f"{int(r['puesto'])}º de {int(r['total_anio'])}")
    k3.metric("Prosperidad Neta (PN)", fmt(r["PN"]), delta("PN"))
    k4.metric("Parasitismo (TPL)", fmt(r["TPL"]), delta("TPL"), delta_color="inverse")

    # --- Descomposición PS = PN + S_E ---
    se_val = float(fila_se.iloc[0]["s_e_pct_pib"]) if not fila_se.empty else None
    ps_val = float(fila_ps.iloc[0]["ps_valor"]) if not fila_ps.empty else None

    if se_val is not None and ps_val is not None:
        st.markdown("---")
        st.subheader("🌱 Prosperidad Sostenible = PN + Subsidio Exterior")
        se_etiq, se_color = etiqueta_se(se_val)
        kp1, kp2, kp3 = st.columns(3)
        kp1.metric("Prosperidad Neta (PN)", f"{r['PN']:.2f}",
                   help="Base del modelo: riqueza disponible tras descontar el lastre institucional.")
        kp2.metric("Subsidio Exterior (S_E)", f"{se_val:+.2f}% PIB",
                   help="Negativo = exportador neto (bueno). Positivo = importador neto (dependiente).")
        kp3.metric("Prosperidad Sostenible (PS)", f"{ps_val:.2f}",
                   help="PS = PN + S_E. Prosperidad real incorporando la posición exterior.")

        fig_decom = go.Figure()
        fig_decom.add_trace(go.Bar(
            x=[r["PN"]], y=[""], orientation="h", name="Prosperidad Neta (PN)",
            marker_color="#3b82f6", text=[f"PN = {r['PN']:.2f}"], textposition="inside"
        ))
        fig_decom.add_trace(go.Bar(
            x=[se_val], y=[""], orientation="h",
            name=f"Subsidio Exterior ({'exportador' if se_val < 0 else 'importador'} neto)",
            marker_color=se_color, text=[f"S_E = {se_val:+.2f}%"], textposition="inside"
        ))
        fig_decom.update_layout(
            barmode="relative", height=140, margin=dict(t=10, b=10, l=0, r=0),
            showlegend=True, legend=dict(orientation="h", y=-0.3),
            xaxis_title="Valor (unidades del modelo / % PIB para S_E)"
        )
        st.plotly_chart(fig_decom, use_container_width=True)

        if se_val < 0:
            st.info(f"**{pais_sel} es exportador neto** ({se_val:+.2f}% del PIB): aporta más valor al mercado global del que recibe. Esto *resta* al indicador de PS porque el país «presta» riqueza al sistema exterior.")
        else:
            st.info(f"**{pais_sel} es importador neto** ({se_val:+.2f}% del PIB): consume más valor del mercado global del que aporta. Esto *suma* a la PS pero revela dependencia del exterior.")

    st.markdown("---")
    cg1, cg2 = st.columns(2)
    with cg1:
        fig_idx = px.line(hist, x="anio", y="indice", markers=True, title="Índice de Prosperidad (0-100)")
        fig_idx.update_yaxes(range=[0, 100])
        fig_idx.update_layout(height=300, margin=dict(t=40, b=0))
        st.plotly_chart(fig_idx, use_container_width=True)
    with cg2:
        hist_ps_d = df_ps[df_ps["iso3"] == iso3].sort_values("anio")
        hist_pn_d = df_inter[df_inter["iso3"] == iso3].sort_values("anio")[["anio", "pn_valor"]]
        if not hist_ps_d.empty and not hist_pn_d.empty:
            merged = hist_ps_d.merge(hist_pn_d, on="anio", how="left")
            fig_ps_line = go.Figure()
            # PN en azul claro punteado, PS en azul oscuro sólido
            fig_ps_line.add_trace(go.Scatter(x=merged["anio"], y=merged["pn_valor"], name="PN", mode="lines+markers", line=dict(color="#3b82f6", dash="dot")))
            fig_ps_line.add_trace(go.Scatter(x=merged["anio"], y=merged["ps_valor"], name="PS", mode="lines+markers", line=dict(color="#1e40af")))
            fig_ps_line.add_hline(y=0, line_dash="dash", line_color="gray")
            fig_ps_line.update_layout(title="PS vs PN en el tiempo", height=300, margin=dict(t=40, b=0))
            st.plotly_chart(fig_ps_line, use_container_width=True)
        else:
            fig_p = px.line(hist, x="anio", y="puesto", markers=True, title="Puesto mundial (1 = mejor)")
            fig_p.update_yaxes(autorange="reversed")
            fig_p.update_layout(height=300, margin=dict(t=40, b=0))
            st.plotly_chart(fig_p, use_container_width=True)

    st.subheader("Componentes MPS vs mediana mundial")
    dfa = df[df["anio"] == anio]
    comp = [{"C": c, "Este país": r[c], "Mediana mundial": dfa[c].median()} for c in ["estructura", "transferencias", "carga_oculta"]]
    comp_df = pd.DataFrame(comp).melt(id_vars="C", var_name="Serie", value_name="Valor")
    fig_comp = px.bar(comp_df, x="C", y="Valor", color="Serie", barmode="group", labels={"C": "Componente"})
    fig_comp.update_layout(height=300, margin=dict(t=10, b=0))
    st.plotly_chart(fig_comp, use_container_width=True)


elif vista == "comparador":
    st.header("⚖️ Comparador de países")
    anio = selector_anio("anio_comp")
    dfa = df[df["anio"] == anio].copy()
    nombres = sorted(dfa["pais"].unique())
    pre = [p for p in ["España", "Alemania", "Estados Unidos", "Suiza"] if p in nombres]
    seleccion = st.multiselect("Elige uno o varios países", nombres, default=pre)
    if len(seleccion) < 1:
        st.info("Selecciona al menos un país.")
        st.stop()

    metrica = st.radio("Métrica", ["Índice de Prosperidad (0-100)", "Prosperidad Neta (PN)", "Parasitismo (TPL)"], horizontal=True)
    col_map = {"Índice de Prosperidad (0-100)": "indice", "Prosperidad Neta (PN)": "PN", "Parasitismo (TPL)": "TPL"}
    col = col_map[metrica]
    sub = dfa[dfa["pais"].isin(seleccion)].copy()
    sub["etiqueta"] = sub["bandera"] + " " + sub["pais"]
    sub = sub.sort_values(col, ascending=(col == "TPL"))
    fig = px.bar(sub, x=col, y="etiqueta", orientation="h", color=col,
                 color_continuous_scale="RdYlGn" if col != "TPL" else "RdYlGn_r", text=sub[col].map(fmt))
    fig.update_layout(height=80 + 45 * len(sub), margin=dict(t=10, b=0), yaxis_title="", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🧮 Grupo vs país: media ponderada")
    cponder, cobj = st.columns(2)
    with cponder:
        modo = st.radio("¿Cómo promediar el grupo?", ["Media simple", "Ponderada por PIB (PPA per cápita)"])
    with cobj:
        objetivo = st.selectbox("País a comparar contra el grupo", nombres, index=nombres.index("España") if "España" in nombres else 0)

    def peso(iso3_code):
        if modo.startswith("Media simple"): return 1.0
        return float(PIB.get(iso3_code, {}).get(str(anio), 0.0)) or 0.0

    grupo = dfa[dfa["pais"].isin(seleccion)]
    resumen = {}
    for c in ["indice", "PN", "TPL"]:
        pesos = grupo["iso3"].map(peso)
        total = pesos.sum()
        resumen[c] = float((grupo[c] * pesos).sum() / total) if total > 0 else float(grupo[c].mean())

    obj_row = dfa[dfa["pais"] == objetivo].iloc[0]
    comp_df = pd.DataFrame({
        "Métrica": ["Índice (0-100)", "Prosperidad Neta", "Parasitismo (TPL)"],
        f"Grupo ({len(seleccion)} países)": [resumen["indice"], resumen["PN"], resumen["TPL"]],
        objetivo: [obj_row["indice"], obj_row["PN"], obj_row["TPL"]],
    })
    largo = comp_df.melt(id_vars="Métrica", var_name="Quién", value_name="Valor")
    idx_only = largo[largo["Métrica"] == "Índice (0-100)"]
    fig_g = px.bar(idx_only, x="Quién", y="Valor", color="Quién", text=idx_only["Valor"].map(lambda v: f"{v:.0f}"),
                   title="Índice de Prosperidad (0-100): grupo vs país")
    fig_g.update_yaxes(range=[0, 100])
    fig_g.update_layout(height=360, margin=dict(t=40, b=0), showlegend=False)
    st.plotly_chart(fig_g, use_container_width=True)
    tabla = comp_df.copy()
    for c in tabla.columns[1:]: tabla[c] = tabla[c].map(fmt)
    st.table(tabla.set_index("Métrica"))


elif vista == "ranking":
    st.header("🏆 Clasificación mundial")
    c1, c2 = st.columns([1, 1])
    with c1:
        anio = selector_anio("anio_rank")
    with c2:
        orden = st.selectbox("Ordenar por", ["Prosperidad Sostenible (PS)", "Índice de Prosperidad (PN)", "Mayor exportador neto (S_E)", "Menor parasitismo (TPL)"])

    dfa = df[df["anio"] == anio].copy()
    if not df_ps.empty:
        dfa = dfa.merge(df_ps[df_ps["anio"] == anio][["iso3", "ps_valor"]], on="iso3", how="left")
    else: dfa["ps_valor"] = float("nan")
    if not df_se.empty:
        dfa = dfa.merge(df_se[df_se["anio"] == anio][["iso3", "s_e_pct_pib"]], on="iso3", how="left")
    else: dfa["s_e_pct_pib"] = float("nan")

    prevdf = df[df["anio"] == anio - 1][["iso3", "puesto"]].rename(columns={"puesto": "puesto_prev"})
    dfa = dfa.merge(prevdf, on="iso3", how="left")

    if orden.startswith("Prosperidad Sostenible"): dfa = dfa.sort_values("ps_valor", ascending=False)
    elif orden.startswith("Índice"): dfa = dfa.sort_values("indice", ascending=False)
    elif orden.startswith("Mayor exportador"): dfa = dfa.sort_values("s_e_pct_pib", ascending=True)
    else: dfa = dfa.sort_values("TPL", ascending=True)

    dfa = dfa.reset_index(drop=True)
    dfa["#"] = dfa.index + 1

    def cambio(row):
        if pd.isna(row.get("puesto_prev")): return "—"
        d = int(row["puesto_prev"] - row["puesto"])
        return f"▲ {d}" if d > 0 else (f"▼ {abs(d)}" if d < 0 else "=")

    dfa["Δ"] = dfa.apply(cambio, axis=1)
    dfa["País"] = dfa["bandera"] + " " + dfa["pais"]
    dfa["PN"] = dfa["PN"].map(fmt)
    dfa["TPL"] = dfa["TPL"].map(fmt)
    dfa["PS"] = dfa["ps_valor"].map(lambda v: f"{v:.1f}" if pd.notna(v) else "—")
    dfa["S_E (% PIB)"] = dfa["s_e_pct_pib"].map(lambda v: f"{v:+.1f}%" if pd.notna(v) else "—")

    tabla = dfa[["#", "País", "indice", "PN", "PS", "S_E (% PIB)", "TPL", "Δ"]]
    st.dataframe(
        tabla, hide_index=True, use_container_width=True, height=620,
        column_config={
            "#": st.column_config.NumberColumn("#", width="small"),
            "indice": st.column_config.ProgressColumn("Índice PN", min_value=0, max_value=100, format="%.0f"),
        },
    )
    st.caption("**PS** = Prosperidad Sostenible (PN + S_E). **S_E negativo** = exportador neto. Δ compara el puesto de PN con el año anterior.")


elif vista == "economista":
    st.header("🧮 Vista económica (datos crudos)")
    st.caption("Reproducción de las gráficas originales del modelo: valores en bruto, sin normalizar ni suavizar. Pensada para análisis técnico.")
    sub = st.radio("Gráfica", ["Histórico global (tabla)", "Análisis por país", "Gráfica de dispersión"], horizontal=True)
    cols_crudas = ["estructura", "transferencias", "carga_oculta", "TPL", "PN"]

    if sub.startswith("Histórico"):
        st.subheader("Tabla dinámica por año (ordenada por TPL)")
        anio_t = selector_anio("anio_eco_hist")
        df_t = df[df["anio"] == anio_t][["iso3", "pais"] + cols_crudas].sort_values("TPL").reset_index(drop=True)
        st.dataframe(df_t, use_container_width=True, hide_index=True)

    elif sub == "Análisis por país":
        st.subheader("Dossier de país")
        nombres = sorted(df["pais"].unique())
        idx = nombres.index("España") if "España" in nombres else 0
        pais_sel = st.selectbox("País", nombres, index=idx, key="eco_pais")
        dpais = df[df["pais"] == pais_sel].sort_values("anio")
        fig = px.line(dpais, x="anio", y=["TPL", "PN", "estructura", "carga_oculta"], markers=True, title=f"Evolución MPS: {pais_sel}")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(dpais.set_index("anio")[cols_crudas], use_container_width=True)

    else:
        st.subheader("Análisis de tendencias (dispersión)")
        anio_d = selector_anio("anio_eco_disp")
        c1, c2 = st.columns(2)
        with c1: mx = st.selectbox("Eje X", ["TPL", "estructura", "carga_oculta", "transferencias", "PN"], index=0)
        with c2: my = st.selectbox("Eje Y", ["PN", "transferencias", "TPL", "estructura", "carga_oculta"], index=0)
        d_an = df[df["anio"] == anio_d]
        fig = px.scatter(d_an, x=mx, y=my, color="pais", size="estructura", hover_name="pais", title=f"{mx} vs {my} ({anio_d})")
        fig.update_layout(showlegend=False, height=560)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Cada punto es un país. Tamaño = estructura. Sin leyenda por legibilidad.")


elif vista == "eri":
    st.header("📈 Inversión y eficiencia (ERI)")
    st.caption("ERI = Inversión / Capital Humano (CH). Indicador propio del modelo. Se muestra el valor **sin juicio de bueno/malo**: solo para comparar.")
    if df_eri.empty:
        st.warning("No está disponible el dataset ERI (BaseDeDatos/Base_Datos_MPS_Final_ERI.json).")
    else:
        sub = st.radio("Vista", ["Mapa", "Clasificación", "Evolución por país", "Inversión vs CH"], horizontal=True)
        if sub == "Mapa":
            anio = selector_anio("eri_mapa", anios=ANIOS_ERI)
            d = df_eri[df_eri["anio"] == anio]
            fig = px.choropleth(d, locations="iso3", color="eri", hover_name="pais", color_continuous_scale="Viridis",
                                custom_data=["inversion", "ch", "eri"], labels={"eri": "ERI"})
            fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>ERI: %{customdata[2]:.3f}<br>Inversión: %{customdata[0]:.2f}<br>CH: %{customdata[1]:.3f}<extra></extra>")
            fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=520, geo=dict(showframe=False, projection_type="natural earth"))
            st.plotly_chart(fig, use_container_width=True)
        elif sub == "Clasificación":
            anio = selector_anio("eri_rank", anios=ANIOS_ERI)
            d = df_eri[df_eri["anio"] == anio].sort_values("eri", ascending=False).reset_index(drop=True)
            d["#"] = d.index + 1
            d["País"] = d["bandera"] + " " + d["pais"]
            eri_max = float(df_eri["eri"].max())
            st.dataframe(d[["#", "País", "eri", "inversion", "ch"]], hide_index=True, use_container_width=True, height=620,
                         column_config={"#": st.column_config.NumberColumn("#", width="small"), "eri": st.column_config.ProgressColumn("ERI", min_value=0, max_value=eri_max, format="%.3f"), "inversion": st.column_config.NumberColumn("Inversión", format="%.2f"), "ch": st.column_config.NumberColumn("CH", format="%.3f")})
        elif sub == "Evolución por país":
            nombres = sorted(df_eri["pais"].unique())
            idx = nombres.index("España") if "España" in nombres else 0
            pais_sel = st.selectbox("País", nombres, index=idx, key="eri_pais")
            dp = df_eri[df_eri["pais"] == pais_sel].sort_values("anio")
            fig = px.line(dp, x="anio", y="eri", markers=True, title=f"ERI en el tiempo: {pais_sel}")
            fig.update_layout(height=320, margin=dict(t=40, b=0))
            st.plotly_chart(fig, use_container_width=True)
            fig2 = px.line(dp, x="anio", y=["inversion", "ch"], markers=True, title="Componentes: Inversión y Capital Humano")
            fig2.update_layout(height=320, margin=dict(t=40, b=0))
            st.plotly_chart(fig2, use_container_width=True)
        else:
            anio = selector_anio("eri_disp", anios=ANIOS_ERI)
            d = df_eri[df_eri["anio"] == anio]
            fig = px.scatter(d, x="ch", y="inversion", color="eri", hover_name="pais", color_continuous_scale="Viridis",
                             labels={"ch": "Capital Humano (CH)", "inversion": "Inversión", "eri": "ERI"}, title=f"Inversión frente a Capital Humano ({anio})")
            fig.update_layout(height=560, margin=dict(t=40, b=0))
            st.plotly_chart(fig, use_container_width=True)


elif vista == "se":
    st.header("🔄 Subsidio Exterior (S_E)")
    st.markdown("""
        El **Subsidio Exterior** mide la posición neta del país frente al mercado global:
        | Signo del S_E | Significado | Efecto sobre la PS |
        |---|---|---|
        | **Negativo** 🟢 | Exportador neto — aporta más valor de lo que recibe | Reduce la PS: «presta» riqueza al sistema |
        | **Positivo** 🔴 | Importador neto — consume más de lo que exporta | Aumenta la PS pero a costa de dependencia |
    """)
    st.markdown("---")
    if df_se.empty:
        st.warning("No se encontró S_E.json en BaseDeDatos/.")
        st.stop()

    c1, c2 = st.columns([2, 1])
    with c1:
        nombres_se = sorted(df_se["pais"].unique())
        idx_esp = nombres_se.index("España") if "España" in nombres_se else 0
        pais_se = st.selectbox("País", nombres_se, index=idx_esp, key="pais_se_sel")
    with c2:
        anio_se = selector_anio("anio_se", anios=ANIOS_SE, anio_max=ANIO_MAX_SE)

    iso3_se = NOMBRE_ISO3.get(pais_se)
    fila_se = df_se[(df_se["iso3"] == iso3_se) & (df_se["anio"] == anio_se)]
    fila_inter = df_inter[(df_inter["iso3"] == iso3_se) & (df_inter["anio"] == anio_se)]
    fila_ps_se = df_ps[(df_ps["iso3"] == iso3_se) & (df_ps["anio"] == anio_se)]
    fila_mps = df[(df["iso3"] == iso3_se) & (df["anio"] == anio_se)]
    hist_se = df_se[df_se["iso3"] == iso3_se].sort_values("anio")

    if fila_se.empty:
        st.warning("Sin datos de S_E para ese país y año.")
        st.stop()

    r_se = fila_se.iloc[0]
    se_pct = r_se["s_e_pct_pib"]
    se_etiq, se_color = etiqueta_se(se_pct)

    st.markdown(f"### {bandera(iso3_se)} {pais_se} · {anio_se} &nbsp; <span style='background:{se_color};color:white;padding:3px 14px;border-radius:999px;font-size:0.6em;vertical-align:middle;'>{se_etiq}</span>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("S_E (% del PIB)", f"{se_pct:+.2f}%")
    k2.metric("S_E (valor absoluto)", fmt(r_se["s_e_raw_usd"]))
    if not fila_mps.empty:
        k3.metric("Prosperidad Neta (PN)", f"{float(fila_mps.iloc[0]['PN']):.2f}")
    if not fila_ps_se.empty:
        k4.metric("PS = PN + S_E", f"{float(fila_ps_se.iloc[0]['ps_valor']):.2f}")

    if se_pct < 0:
        st.info(f"**{pais_se} es exportador neto** ({se_pct:+.2f}% del PIB en {anio_se}). El país genera más valor del que importa del sistema global.")
    else:
        st.info(f"**{pais_se} es importador neto** ({se_pct:+.2f}% del PIB en {anio_se}). El país consume más del mercado global de lo que le aporta.")

    st.markdown("---")
    st.subheader("🔍 Dimensiones del S_E")
    if not fila_inter.empty:
        r_inter = fila_inter.iloc[0]
        tab_fin, tab_sec, tab_com = st.tabs(["💰 Financiero", "🏭 Sectorial", "🚢 Comercio"])
        with tab_fin:
            c1f, c2f = st.columns(2)
            c1f.metric("ODA recibida", fmt(r_inter["oda_recibida_usd"]) if pd.notna(r_inter["oda_recibida_usd"]) else "Sin dato")
            c2f.metric("Remesas de emigrantes", fmt(r_inter["remesas_recibidas_usd"]) if pd.notna(r_inter["remesas_recibidas_usd"]) else "Sin dato")
            hist_fin = df_inter[df_inter["iso3"] == iso3_se].sort_values("anio")
            if hist_fin["remesas_recibidas_usd"].notna().any():
                fig_fin = px.bar(hist_fin, x="anio", y="remesas_recibidas_usd", title="Remesas recibidas — evolución")
                fig_fin.update_layout(height=260, margin=dict(t=40, b=0))
                st.plotly_chart(fig_fin, use_container_width=True)
        with tab_sec:
            c1s, c2s = st.columns(2)
            c1s.metric("Exportaciones tecnológicas", f"{r_inter['tech_exports_pct']:.1f}%" if pd.notna(r_inter['tech_exports_pct']) else "Sin dato")
            c2s.metric("Dependencia energética", f"{r_inter['energy_imports_pct']:.1f}%" if pd.notna(r_inter['energy_imports_pct']) else "Sin dato")
            hist_sec = df_inter[df_inter["iso3"] == iso3_se].sort_values("anio")
            fig_sec = go.Figure()
            if hist_sec["tech_exports_pct"].notna().any(): fig_sec.add_trace(go.Scatter(x=hist_sec["anio"], y=hist_sec["tech_exports_pct"], name="Tech exports %", line=dict(color="#16a34a")))
            if hist_sec["energy_imports_pct"].notna().any(): fig_sec.add_trace(go.Scatter(x=hist_sec["anio"], y=hist_sec["energy_imports_pct"], name="Dep. energética %", line=dict(color="#dc2626")))
            fig_sec.update_layout(title="Especialización sectorial — evolución", height=260, margin=dict(t=40, b=0))
            st.plotly_chart(fig_sec, use_container_width=True)
        with tab_com:
            c1c, c2c, c3c = st.columns(3)
            c1c.metric("Exportaciones", fmt(r_inter["exportaciones"]) if pd.notna(r_inter["exportaciones"]) else "Sin dato")
            c2c.metric("Importaciones", fmt(r_inter["importaciones"]) if pd.notna(r_inter["importaciones"]) else "Sin dato")
            c3c.metric("Saldo comercial", fmt(r_inter["balance_comercial"]) if pd.notna(r_inter["balance_comercial"]) else "Sin dato")
            hist_com = df_inter[df_inter["iso3"] == iso3_se].sort_values("anio")
            if hist_com["balance_comercial"].notna().any():
                hist_com_plot = hist_com.copy()
                hist_com_plot["color"] = hist_com_plot["balance_comercial"].apply(lambda v: "#16a34a" if (pd.notna(v) and v <= 0) else "#dc2626")
                fig_com = px.bar(hist_com_plot, x="anio", y="balance_comercial", color="color", color_discrete_map="identity", title="Saldo comercial (verde = exportador neto)")
                fig_com.update_layout(height=260, margin=dict(t=40, b=0), showlegend=False)
                st.plotly_chart(fig_com, use_container_width=True)

    st.markdown("---")
    cg1, cg2 = st.columns(2)
    with cg1:
        hist_se_plot = hist_se.copy()
        hist_se_plot["color"] = hist_se_plot["s_e_pct_pib"].apply(lambda v: "#16a34a" if v < 0 else "#dc2626")
        fig_se_pct = px.bar(hist_se_plot, x="anio", y="s_e_pct_pib", color="color", color_discrete_map="identity", title="S_E (% del PIB) — verde = exportador neto")
        fig_se_pct.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_se_pct.update_layout(height=300, margin=dict(t=40, b=0), showlegend=False)
        st.plotly_chart(fig_se_pct, use_container_width=True)
    with cg2:
        hist_ps_local = df_ps[df_ps["iso3"] == iso3_se].sort_values("anio")
        hist_pn_local = df_inter[df_inter["iso3"] == iso3_se].sort_values("anio")[["anio", "pn_valor"]]
        if not hist_ps_local.empty:
            merged_hist = hist_ps_local.merge(hist_pn_local, on="anio", how="left")
            fig_ps_pn = go.Figure()
            # PN en azul claro punteado, PS en azul oscuro sólido
            fig_ps_pn.add_trace(go.Scatter(x=merged_hist["anio"], y=merged_hist["pn_valor"], name="PN", line=dict(color="#3b82f6", dash="dot")))
            fig_ps_pn.add_trace(go.Scatter(x=merged_hist["anio"], y=merged_hist["ps_valor"], name="PS", line=dict(color="#1e40af")))
            fig_ps_pn.add_hline(y=0, line_dash="dash", line_color="gray")
            fig_ps_pn.update_layout(title="PS (azul oscuro) vs PN (azul claro) — la brecha es el S_E", height=300, margin=dict(t=40, b=0))
            st.plotly_chart(fig_ps_pn, use_container_width=True)

    st.subheader(f"🗺️ Mapa del Subsidio Exterior en {anio_se}")
    dfa_se_mapa = df_se[df_se["anio"] == anio_se].copy()
    dfa_se_mapa["se_inv"] = -dfa_se_mapa["s_e_pct_pib"]
    dfa_se_mapa["se_pct_txt"] = dfa_se_mapa["s_e_pct_pib"].map(lambda v: f"{v:+.1f}%")
    dfa_se_mapa["se_label"] = dfa_se_mapa["s_e_pct_pib"].map(lambda v: "Exportador neto" if v < 0 else "Importador neto")
    fig_mapa_se = px.choropleth(dfa_se_mapa, locations="iso3", color="se_inv", hover_name="pais", color_continuous_scale="RdYlGn", custom_data=["se_pct_txt", "se_label"])
    fig_mapa_se.update_traces(hovertemplate="<b>%{hovertext}</b><br>S_E: %{customdata[0]}<br>%{customdata[1]}<extra></extra>")
    fig_mapa_se.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=450, geo=dict(showframe=False, projection_type="natural earth"))
    st.plotly_chart(fig_mapa_se, use_container_width=True)


elif vista == "ps":
    st.header("🌱 Prosperidad Sostenible (PS)")
    st.markdown("""
        La **Prosperidad Sostenible** es el indicador final del modelo:
        > **PS = PN + S_E**
    """)
    st.markdown("---")
    if df_ps.empty:
        st.warning("No se encontró PS.json en BaseDeDatos/.")
        st.stop()

    ANIOS_PS = sorted(df_ps["anio"].unique())
    c1, c2 = st.columns([2, 1])
    with c1:
        nombres_ps = sorted(df_ps["pais"].unique())
        idx_esp_ps = nombres_ps.index("España") if "España" in nombres_ps else 0
        pais_ps = st.selectbox("País", nombres_ps, index=idx_esp_ps, key="pais_ps_sel")
    with c2:
        anio_ps = selector_anio("anio_ps", anios=ANIOS_PS, anio_max=max(ANIOS_PS))

    iso3_ps = NOMBRE_ISO3.get(pais_ps)
    fila_ps = df_ps[(df_ps["iso3"] == iso3_ps) & (df_ps["anio"] == anio_ps)]
    fila_se_ps = df_se[(df_se["iso3"] == iso3_ps) & (df_se["anio"] == anio_ps)]
    fila_inter_ps = df_inter[(df_inter["iso3"] == iso3_ps) & (df_inter["anio"] == anio_ps)]

    if fila_ps.empty:
        st.warning("Sin datos de PS para ese país y año.")
        st.stop()

    r_ps = fila_ps.iloc[0]
    ps_val = float(r_ps["ps_valor"])
    se_val_ps = float(fila_se_ps.iloc[0]["s_e_pct_pib"]) if not fila_se_ps.empty else None
    pn_val_ps = float(fila_inter_ps.iloc[0]["pn_valor"]) if not fila_inter_ps.empty else None

    ps_anio_vals = df_ps[df_ps["anio"] == anio_ps]["ps_valor"]
    percentil_ps = float((ps_anio_vals < ps_val).mean() * 100)

    st.markdown(f"### {bandera(iso3_ps)} {pais_ps} · {anio_ps}")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Prosperidad Neta (PN)", f"{pn_val_ps:.2f}" if pn_val_ps is not None else "—")
    k2.metric("Subsidio Exterior (S_E)", f"{se_val_ps:+.2f}% PIB" if se_val_ps is not None else "—")
    k3.metric("Prosperidad Sostenible (PS)", f"{ps_val:.2f}")
    k4.metric("Percentil mundial", f"{percentil_ps:.0f}/100")

    if pn_val_ps is not None and se_val_ps is not None:
        se_etiq_ps, se_color_ps = etiqueta_se(se_val_ps)
        fig_decom_ps = go.Figure()
        fig_decom_ps.add_trace(go.Bar(x=[pn_val_ps], y=["PS"], orientation="h", name="PN", marker_color="#3b82f6", text=[f"PN = {pn_val_ps:.2f}"], textposition="inside"))
        fig_decom_ps.add_trace(go.Bar(x=[se_val_ps], y=["PS"], orientation="h", name=f"S_E", marker_color=se_color_ps, text=[f"S_E = {se_val_ps:+.2f}%"], textposition="inside"))
        fig_decom_ps.add_vline(x=ps_val, line_dash="solid", line_color="#111", annotation_text=f"PS = {ps_val:.2f}", annotation_position="top right")
        fig_decom_ps.update_layout(barmode="relative", height=150, margin=dict(t=20, b=30, l=0, r=0), showlegend=True, legend=dict(orientation="h", y=-0.4))
        st.plotly_chart(fig_decom_ps, use_container_width=True)

    st.markdown("---")
    st.subheader("📈 Evolución histórica: PS = PN + S_E")
    hist_ps_gen = df_ps[df_ps["iso3"] == iso3_ps].sort_values("anio")
    hist_pn_ps = df_inter[df_inter["iso3"] == iso3_ps].sort_values("anio")[["anio", "pn_valor"]]
    hist_se_ps = df_se[df_se["iso3"] == iso3_ps].sort_values("anio")

    if not hist_ps_gen.empty:
        merged_hist = hist_ps_gen.merge(hist_pn_ps, on="anio", how="left").merge(hist_se_ps[["anio", "s_e_pct_pib"]], on="anio", how="left")
        cg1, cg2 = st.columns(2)
        with cg1:
            fig_tres = go.Figure()
            # PN en azul claro punteado, PS en azul oscuro sólido
            fig_tres.add_trace(go.Scatter(x=merged_hist["anio"], y=merged_hist["pn_valor"], name="PN", line=dict(color="#3b82f6", dash="dot")))
            fig_tres.add_trace(go.Scatter(x=merged_hist["anio"], y=merged_hist["ps_valor"], name="PS", line=dict(color="#1e40af", width=2)))
            fig_tres.add_hline(y=0, line_dash="dash", line_color="gray")
            fig_tres.update_layout(title="PN (azul claro) y PS (azul oscuro)", height=320, margin=dict(t=40, b=0))
            st.plotly_chart(fig_tres, use_container_width=True)
        with cg2:
            hist_se_bar = merged_hist.copy()
            hist_se_bar["color"] = hist_se_bar["s_e_pct_pib"].apply(lambda v: "#16a34a" if (pd.notna(v) and v < 0) else "#dc2626")
            fig_se_hist = px.bar(hist_se_bar, x="anio", y="s_e_pct_pib", color="color", color_discrete_map="identity", title="S_E (% PIB)")
            fig_se_hist.add_hline(y=0, line_dash="dash", line_color="gray")
            fig_se_hist.update_layout(height=320, margin=dict(t=40, b=0), showlegend=False)
            st.plotly_chart(fig_se_hist, use_container_width=True)

    st.markdown("---")
    st.subheader(f"⚖️ Comparativa de PS en {anio_ps}")
    pre_ps = [p for p in ["España", "Alemania", "Francia", "Noruega", "Qatar"] if p in nombres_ps]
    sel_ps = st.multiselect("Países a comparar", nombres_ps, default=[pais_ps] + [p for p in pre_ps if p != pais_ps][:4], key="comp_ps")
    if sel_ps:
        dfa_comp = df_ps[(df_ps["anio"] == anio_ps) & (df_ps["pais"].isin(sel_ps))].copy()
        dfa_comp = dfa_comp.merge(df_se[(df_se["anio"] == anio_ps)][["iso3", "s_e_pct_pib"]], on="iso3", how="left")
        dfa_comp = dfa_comp.merge(df_inter[df_inter["anio"] == anio_ps][["iso3", "pn_valor"]], on="iso3", how="left")
        dfa_comp = dfa_comp.sort_values("ps_valor", ascending=False)
        dfa_comp["etiq"] = dfa_comp["iso3"].map(lambda x: bandera(x) + " " + nombre(x))

        fig_comp_ps = go.Figure()
        fig_comp_ps.add_trace(go.Bar(x=dfa_comp["etiq"], y=dfa_comp["pn_valor"], name="Prosperidad Neta (PN)", marker_color="#3b82f6"))
        fig_comp_ps.add_trace(go.Bar(x=dfa_comp["etiq"], y=dfa_comp["s_e_pct_pib"], name="Subsidio Exterior (S_E)", marker_color=dfa_comp["s_e_pct_pib"].apply(lambda v: "#16a34a" if (pd.notna(v) and v < 0) else "#f97316").tolist()))
        fig_comp_ps.add_scatter(x=dfa_comp["etiq"], y=dfa_comp["ps_valor"], mode="markers", marker=dict(size=10, color="#111", symbol="diamond"), name="PS")
        fig_comp_ps.update_layout(barmode="relative", title="Descomposición PS = PN + S_E por país", height=420, margin=dict(t=50, b=0), legend=dict(orientation="h", y=-0.25))
        fig_comp_ps.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_comp_ps, use_container_width=True)

    st.subheader(f"🗺️ Mapa mundial de la PS en {anio_ps}")
    dfa_ps_mapa = df_ps[df_ps["anio"] == anio_ps].copy()
    dfa_ps_mapa["ps_txt"] = dfa_ps_mapa["ps_valor"].map(lambda v: f"{v:.2f}")
    
    # 💥 ESTE ES EL CAMBIO CLAVE PARA EL MAPA DE LA PS 💥
    # En lugar de usar la PS en bruto, usamos el percentil "indice_ps" 
    # de 0 a 100 con la escala RdYlGn, exactamente igual que el mapa de la PN.
    fig_mapa_ps = px.choropleth(
        dfa_ps_mapa, locations="iso3", color="indice_ps", hover_name="pais", 
        color_continuous_scale="RdYlGn", range_color=(0, 100), custom_data=["ps_txt"]
    )
    
    fig_mapa_ps.update_traces(hovertemplate="<b>%{hovertext}</b><br>PS: %{customdata[0]}<extra></extra>")
    fig_mapa_ps.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=450, geo=dict(showframe=False, projection_type="natural earth"))
    st.plotly_chart(fig_mapa_ps, use_container_width=True)
    st.caption("Verde = mayor Prosperidad Sostenible (percentil alto). Rojo = menor PS. "
               "El mapa utiliza el índice relativo (0-100) igual que la PN para hacerlos comparables.")


elif vista == "autor":
    st.markdown(
        """
        <style>
        .tab-hero { background: radial-gradient(circle at 20% 20%, #3a0d0d 0%, #1a0808 70%); border: 1px solid #c9a227; border-radius: 18px; padding: 34px 30px; color: #f5ede0; margin-bottom: 22px; display: flex; gap: 26px; align-items: center; flex-wrap: wrap; }
        .tab-hero h1 { color: #ffffff; margin: 0 0 4px 0; font-size: 1.9rem; }
        .tab-tagline { color: #c9a227; font-weight: 700; letter-spacing: .5px; text-transform: uppercase; font-size: .9rem; margin-bottom: 8px; }
        .tab-hero p { margin: 0; color: #e7dcc8; max-width: 640px; line-height: 1.5; }
        .tab-maximas { display: flex; gap: 14px; flex-wrap: wrap; margin: 6px 0 22px; }
        .tab-maxima { flex: 1 1 200px; background: #fbf7ee; border-left: 4px solid #c9a227; border-radius: 8px; padding: 16px 18px; font-style: italic; font-size: 1.05rem; color: #3a2e10; }
        .tab-cards { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 22px; }
        .tab-card { flex: 1 1 260px; border: 1px solid #e6e0d2; border-radius: 14px; padding: 20px 22px; background: #ffffff; }
        .tab-card h3 { margin: 0 0 8px 0; }
        .tab-card.quiosco { border-top: 5px solid #c0392b; }
        .tab-card.forjador { border-top: 5px solid #5b3a8c; }
        .tab-libro { display: flex; gap: 22px; flex-wrap: wrap; align-items: center; background: linear-gradient(135deg, #1a0808, #3a0d0d); color: #f5ede0; border: 1px solid #c9a227; border-radius: 16px; padding: 26px 28px; margin-bottom: 22px; }
        .tab-libro h2 { color: #fff; margin: 0 0 6px 0; }
        .tab-badge { display: inline-block; background: #c9a227; color: #1a0808; font-weight: 700; border-radius: 999px; padding: 3px 14px; font-size: .8rem; margin-bottom: 10px; }
        .tab-btn { display: inline-block; background: #c9a227; color: #1a0808 !important; text-decoration: none; font-weight: 700; padding: 10px 20px; border-radius: 8px; margin-top: 6px; }
        .tab-foto { width: 132px; height: 132px; flex: 0 0 132px; border-radius: 50%; object-fit: cover; border: 4px solid #c9a227; box-shadow: 0 0 0 5px rgba(201,162,39,.2); }
        .tab-portada-img { flex: 0 0 150px; width: 150px; border-radius: 8px; box-shadow: 0 12px 30px rgba(0,0,0,.5); }
        .tab-libros2 { display: flex; gap: 24px; flex-wrap: wrap; margin: 6px 0 4px; }
        .tab-libro2 { width: 150px; text-decoration: none; color: #2b2b2b !important; }
        .tab-libro2 img { width: 150px; border-radius: 8px; display: block; box-shadow: 0 6px 18px rgba(0,0,0,.18); }
        .tab-libro2 span { display: block; margin-top: 10px; font-weight: 600; font-size: .9rem; text-align: center; line-height: 1.3; }
        .tab-redes { display: flex; gap: 22px; flex-wrap: wrap; margin: 4px 0; }
        .tab-red { display: flex; flex-direction: column; align-items: center; gap: 9px; text-decoration: none; color: #444 !important; font-weight: 600; font-size: .85rem; }
        .tab-red img { width: 58px; height: 58px; padding: 15px; border-radius: 50%; background: #fff; border: 1px solid #ece7da; box-sizing: border-box; box-shadow: 0 2px 10px rgba(0,0,0,.07); }
        </style>

        <div class="tab-hero">
            <img class="tab-foto" src="assets/pedro.jpg" alt="Pedro Andrés Aranda Muñoz" />
            <div>
                <div class="tab-tagline">Bienvenido al Tablinum</div>
                <h1>Pedro Andrés Aranda Muñoz</h1>
                <p><b>Jurista, analista y creador.</b> Autor del <b>Modelo de Prosperidad Sostenible (MPS)</b>. «El dato mata al relato»: aquí se auditan las cuentas del poder y se mide cuánto pesa de verdad la fricción estatal.</p>
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
                <p>Análisis diario de prensa y geopolítica midiendo matemáticamente la <b>Carga Parasitaria Total</b>.</p>
            </div>
            <div class="tab-card forjador">
                <h3>🌌 El Forjador</h3>
                <p>Ciencia ficción y <i>lore</i>. El último refugio que no pueden regular.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="tab-libro">
            <img class="tab-portada-img" src="assets/libro-genealogia.jpg" alt="Genealogía del Conflicto Eterno" />
            <div>
                <div class="tab-badge">📚 Disponible el 12 de octubre</div>
                <h2>Genealogía del Conflicto Eterno</h2>
                <a class="tab-btn" href="https://www.amazon.es/dp/B0GMLH9NL2" target="_blank" rel="noopener">Verlo en Amazon →</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.subheader("📺 Canal de YouTube")
    st.markdown('<a class="tab-btn" href="https://www.youtube.com/@pedroandresaranda" target="_blank" rel="noopener">▶ El Tablinum — @pedroandresaranda</a>', unsafe_allow_html=True)
    st.subheader("📚 Más libros")
    st.markdown(
        """
        <div class="tab-libros2">
            <a class="tab-libro2" href="https://amzn.eu/d/0gzMv98Y" target="_blank" rel="noopener">
                <img src="assets/libro-politico.jpg" alt="¿Cuánto cuesta tu político?" />
                <span>¿Cuánto cuesta tu político?</span>
            </a>
            <a class="tab-libro2" href="https://amzn.eu/d/4Si0xvm" target="_blank" rel="noopener">
                <img src="assets/libro-eva.jpg" alt="Las Realidades de Eva" />
                <span>Las Realidades de Eva</span>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.subheader("🔗 Síguelo")
    st.markdown(
        """
        <div class="tab-redes">
            <a class="tab-red" href="https://www.youtube.com/@pedroandresaranda" target="_blank"><img src="assets/icon-youtube.svg" alt="YouTube" /><span>YouTube</span></a>
            <a class="tab-red" href="https://www.tiktok.com/@andrs.muoz646" target="_blank"><img src="assets/icon-tiktok.svg" alt="TikTok" /><span>TikTok</span></a>
            <a class="tab-red" href="https://www.instagram.com/amopoemp" target="_blank"><img src="assets/icon-instagram.svg" alt="Instagram" /><span>Instagram</span></a>
            <a class="tab-red" href="https://www.facebook.com/pedroandres.arandamunoz" target="_blank"><img src="assets/icon-facebook.svg" alt="Facebook" /><span>Facebook</span></a>
        </div><div style="height:34px"></div>
        """,
        unsafe_allow_html=True,
    )
    st.info("El **Modelo de Prosperidad Sostenible** y su metodología son obra de Pedro Andrés Aranda Muñoz. *Pan, Patria y Justicia.*")

# --- Pie ---
st.markdown("---")
with st.expander("🆕 Novedades de la Versión Completa"):
    st.markdown(
        "- **Vistas recuperadas**: Vuelve la *Vista económica (datos crudos)* y la vista del *ERI (Inversión y eficiencia)* de la v2.0.\n"
        "- **🔄 Subsidio Exterior (S_E)**: S_E negativo = exportador neto (verde/bueno); S_E positivo = importador neto (rojo/dependiente).\n"
        "- **🌱 Prosperidad Sostenible (PS)**: Fórmula PS = PN + S_E explicada con barra de descomposición. La línea de PS se pinta en **azul oscuro sólido** y el mapa de PS usa el percentil (0-100) para asegurar total coherencia con la PN.\n"
        "- **Integración total**: La Ficha y el Ranking muestran ahora todos los parámetros (PN, PS y S_E) de un solo vistazo."
    )
with st.expander("⚠️ Metodología y fuentes"):
    st.warning(
        "**Fórmula central**: PS = PN + S_E. S_E negativo indica que el país exporta más valor neto del que importa (exportador neto). "
        "La PN descuenta el lastre institucional (TPL = estructura + transferencias + carga oculta). "
        "Datos armonizados de BM, FMI, BCE y OCDE. Pan, Patria y Justicia."
    )
