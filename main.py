"""
BOLETÍN ACADÉMICO - Estilo PePE (fondo claro)
Hero/Main FINALIZADO con tus últimos ajustes
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="El mapa de la desigualdad", page_icon="🗺️", layout="wide")

# ====================== ESTILOS ======================
st.markdown("""
<style>
    .main { background-color: #f8f5f0; color: #222222; }
    .block-container { padding-top: 2.5rem; padding-bottom: 3rem; }
    h1 { font-size: 2.4rem; font-weight: 700; color: #1a3c6e; margin-bottom: 0.4rem; }
    .subtitulo { font-size: 1.15rem; color: #555; font-weight: 400; margin-bottom: 2.5rem; line-height: 1.4; }
    .card-pastel {
        background: #C8DAFF;
        padding: 2rem 2.2rem;
        border-radius: 12px;
        color: #1a3c6e;
        margin-bottom: 2.8rem;
        line-height: 1.65;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .kpi-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.4rem 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        height: 100%;
    }
    .kpi-number { font-size: 2.1rem; font-weight: 700; color: #1a3c6e; margin: 0.2rem 0; }
    .kpi-delta { font-size: 1.05rem; font-weight: 500; }
    .kpi-label { font-size: 0.95rem; color: #555; margin-top: 0.8rem; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

# ====================== CARGA DE DATOS ======================
@st.cache_data
def cargar_indicadores():
    df = pd.read_excel("indicadores_dept.xlsx", sheet_name="Hoja1")
    df.columns = ['Año', 'Departamento', 'Pob_monetaria', 'Pob_extrema', 'Gini', 'Ocupacion', 'Desocupacion']
    df["Departamento"] = df["Departamento"].str.strip()
    df["Año"] = df["Año"].astype(int)
    return df

@st.cache_data
def cargar_ingresos():
    df = pd.read_excel("ejec_ing_Dep.xlsx", sheet_name="Hoja1")
    df.columns = ['Año Vigencia', 'Codigo_DANE', 'Codigo_FUT', 'Entidad', 'Region', 'Total_Recaudo']
    df["Entidad"] = df["Entidad"].str.strip()
    df["Region"] = df["Region"].str.strip()
    df["Año Vigencia"] = df["Año Vigencia"].astype(int)
    df["Recaudo_billones"] = (df["Total_Recaudo"] / 1000).round(3)
    df["Entidad"] = df["Entidad"].replace("Bogotá, D.C.", "Bogotá D.C.")
    return df

df_soc = cargar_indicadores()
df_ing = cargar_ingresos()

# ====================== NAVEGACIÓN ======================
st.markdown("# El mapa de la desigualdad")
st.markdown('<p class="subtitulo">indicadores sociales y fiscales en los departamentos de Colombia</p>', unsafe_allow_html=True)
st.caption("Análisis regional de indicadores socioeconómicos y capacidad fiscal departamental • 2019–2025 • Proyecto académico")

tab_main, tab_indicadores, tab_ingresos, tab_cruzado, tab_novedad= st.tabs([
    " ☑︎ Main", " 📊 Indicadores Socioeconómicos", " Ingresos Departamentales", 
    " 🔀 Análisis Cruzado", " 💡 Novedades y conclusiones"
])

# ====================== MAIN ======================
with tab_main:
    # Tarjeta pastel #C8DAFF
    st.markdown("""
    <div class="card-pastel">
        <h2 style="margin-bottom:1rem;">Sobre este boletín</h2>
        <p>Este boletín interactivo analiza la evolución de la pobreza, la desigualdad y los ingresos departamentales 
        en Colombia, con énfasis en el impacto asimétrico de la pandemia COVID-19 y la recuperación heterogénea 
        entre territorios (2019–2025).</p>
        <p>Se utilizan <strong>8 departamentos representativos</strong> de las principales regiones del país 
        (Atlántico, Santander, Huila, Risaralda, Meta, Valle del Cauca, Cundinamarca y Bogotá D.C.) 
        y se comparan con la ejecución de ingresos de los 32 departamentos de Colombia.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Panorama general (promedio de los 8 departamentos seleccionados)")
    st.caption("**Nota:** Los valores que ves abajo son el promedio simple de los 8 departamentos analizados. Sirven como resumen nacional representativo.")

    año_ini = df_soc[df_soc["Año"] == 2019]
    año_fin = df_soc[df_soc["Año"] == 2024]
    cols = st.columns(5)

    metricas = [
        ("Pobreza monetaria (%)", "Pob_monetaria", "%", "↓", "Porcentaje de personas con ingresos por debajo de la línea de pobreza."),
        ("Pobreza extrema (%)", "Pob_extrema", "%", "↓", "Porcentaje de personas sin ingresos suficientes para cubrir la canasta básica alimentaria."),
        ("Coeficiente de Gini", "Gini", "", "", "Medida de desigualdad de ingresos (0 = igualdad perfecta, 1 = máxima desigualdad)."),
        ("Tasa de ocupación (%)", "Ocupacion", "%", "↑", "Porcentaje de la población en edad de trabajar que tiene empleo."),
        ("Tasa de desocupación (%)", "Desocupacion", "%", "↓", "Porcentaje de la población económicamente activa que busca empleo sin encontrarlo."),
    ]

    for col, (title, campo, unidad, arrow, explicacion) in zip(cols, metricas):
        v0 = año_ini[campo].mean()
        v1 = año_fin[campo].mean()
        delta = v1 - v0
        
        if campo == "Gini":
            delta_color = "#27ae60"
            delta_text = "- 0.0% vs 2019"
        else:
            delta_color = "#27ae60"
            delta_text = f"{arrow} {delta:+.1f} vs 2019"
        
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size:0.95rem; color:#555;">{title}</div>
                <div class="kpi-number">{v1:.1f}{unidad}</div>
                <div class="kpi-delta" style="color:{delta_color};">{delta_text}</div>
                <div class="kpi-label">{explicacion}</div>
            </div>
            """, unsafe_allow_html=True)

st.divider()
st.caption("**Datos:** DANE (ECV/GEIH) y Ministerio de Hacienda (FUT) • Desarrollado como boletín académico - Facultad de Economía de la Universidad Santo Tomás (USTA)")

# ====================== DEFINICIONES NECESARIAS (pega esto primero) ======================
COLORES_DEPT = {
    "Bogotá,D.C.": "#1B4F72",
    "Cundinamarca": "#2E86C1",
    "Atlántico": "#E74C3C",
    "Santander": "#27AE60",
    "Huila": "#8E44AD",
    "Risaralda": "#F39C12",
    "Meta": "#D35400",
    "ValledelCauca": "#16A085"
}

NOMBRES_IND = {
    "Pob_monetaria": "Pobreza monetaria (%)",
    "Pob_extrema": "Pobreza extrema (%)",
    "Gini": "Coeficiente de Gini",
    "Ocupacion": "Tasa de ocupación (%)",
    "Desocupacion": "Tasa de desocupación (%)",
}

def insight_box(texto):
    st.markdown(f'<div class="insight-box"> {texto}</div>', unsafe_allow_html=True)

def agregar_banda_pandemia(fig):
    fig.add_vrect(x0=2019.5, x1=2020.5, fillcolor="rgba(231,76,60,0.12)", layer="below", line_width=0,
                  annotation_text="COVID-19", annotation_position="top left", annotation_font_size=10, annotation_font_color="#E74C3C")
    return fig

def layout_limpio(fig, height=420):
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", hovermode="x unified",
                      font=dict(family="Arial", size=12), height=height, margin=dict(t=55, b=30, l=10, r=10))
    return fig

# ====================== INDICADORES SOCIOECONÓMICOS ======================
with tab_indicadores:
    st.markdown("### Indicadores Socioeconómicos (2019–2024)")

    # Filtros
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        opciones_depts = sorted(df_soc["Departamento"].unique())
        depts_sel = st.multiselect(
            "Departamentos a mostrar",
            options=opciones_depts,
            default=["Bogotá,D.C.", "Atlántico", "Huila", "ValledelCauca"]
        )
    with col_f2:
        rango_años = st.select_slider(
            "Rango de años",
            options=sorted(df_soc["Año"].unique()),
            value=(2019, 2024)
        )

    df_f = df_soc[
        (df_soc["Departamento"].isin(depts_sel)) &
        (df_soc["Año"].between(rango_años[0], rango_años[1]))
    ]

    # Sub-pestañas
    sub_tabs = st.tabs(["Pobreza Monetaria", "Pobreza Extrema", "Gini", "Mercado Laboral", "Comparador VS", "Heatmap"])

    # 1. Pobreza Monetaria
    with sub_tabs[0]:
        insight_box("La pobreza monetaria registró su mayor salto histórico en 2020. La recuperación fue generalizada pero con velocidades muy distintas entre departamentos.")
        fig_line = px.line(df_f, x="Año", y="Pob_monetaria", color="Departamento", markers=True,
                           color_discrete_map=COLORES_DEPT, title="Evolución de la pobreza monetaria (%)")
        fig_line = agregar_banda_pandemia(fig_line)
        fig_line = layout_limpio(fig_line)
        st.plotly_chart(fig_line, use_container_width=True)

    # 2. Pobreza Extrema
    with sub_tabs[1]:
        insight_box("La pobreza extrema es el indicador más sensible al choque pandémico.")
        fig_ext = px.line(df_f, x="Año", y="Pob_extrema", color="Departamento", markers=True,
                          color_discrete_map=COLORES_DEPT, title="Evolución de la pobreza extrema (%)")
        fig_ext = agregar_banda_pandemia(fig_ext)
        fig_ext = layout_limpio(fig_ext)
        st.plotly_chart(fig_ext, use_container_width=True)

    # 3. Gini
    with sub_tabs[2]:
        insight_box("El Gini es el indicador más persistente: ningún departamento del grupo bajó de 0.45.")
        fig_gini = px.line(df_f, x="Año", y="Gini", color="Departamento", markers=True,
                           color_discrete_map=COLORES_DEPT, title="Evolución del Coeficiente de Gini")
        fig_gini = agregar_banda_pandemia(fig_gini)
        fig_gini = layout_limpio(fig_gini)
        st.plotly_chart(fig_gini, use_container_width=True)

    # 4. Mercado Laboral
    with sub_tabs[3]:
        col_oc, col_des = st.columns(2)
        with col_oc:
            fig_oc = px.line(df_f, x="Año", y="Ocupacion", color="Departamento", markers=True,
                             color_discrete_map=COLORES_DEPT, title="Tasa de ocupación (%)")
            fig_oc = agregar_banda_pandemia(fig_oc)
            st.plotly_chart(layout_limpio(fig_oc), use_container_width=True)
        with col_des:
            fig_des = px.line(df_f, x="Año", y="Desocupacion", color="Departamento", markers=True,
                              color_discrete_map=COLORES_DEPT, title="Tasa de desocupación (%)")
            fig_des = agregar_banda_pandemia(fig_des)
            st.plotly_chart(layout_limpio(fig_des), use_container_width=True)

    # 5. Comparador VS
    with sub_tabs[4]:
        st.markdown("#### Comparador departamental directo")
        c1, c2, c3 = st.columns(3)
        with c1:
            da = st.selectbox("Departamento A", opciones_depts, index=0, key="da")
        with c2:
            db = st.selectbox("Departamento B", opciones_depts, index=1, key="db")
        with c3:
            ind_vs = st.selectbox("Indicador", list(NOMBRES_IND.keys()), format_func=lambda x: NOMBRES_IND[x])
        fig_vs = go.Figure()
        for dept, color in [(da, "#1B4F72"), (db, "#E74C3C")]:
            sub = df_soc[df_soc["Departamento"] == dept]
            fig_vs.add_trace(go.Scatter(x=sub["Año"], y=sub[ind_vs], mode="lines+markers", name=dept, line=dict(color=color, width=3)))
        fig_vs = agregar_banda_pandemia(fig_vs)
        fig_vs.update_layout(title=f"{NOMBRES_IND[ind_vs]}: {da} vs {db}", height=430)
        st.plotly_chart(fig_vs, use_container_width=True)

    # 6. Heatmap
    with sub_tabs[5]:
        insight_box("Mapa de calor: visión general de todos los departamentos y años.")
        ind_h = st.selectbox("Indicador para heatmap", list(NOMBRES_IND.keys()), format_func=lambda x: NOMBRES_IND[x])
        df_heat = df_soc.pivot_table(index="Departamento", columns="Año", values=ind_h)
        fig_h = px.imshow(df_heat, color_continuous_scale="RdYlGn_r" if ind_h != "Ocupacion" else "RdYlGn",
                          title=f"Heatmap — {NOMBRES_IND[ind_h]}")
        st.plotly_chart(fig_h, use_container_width=True)

# ====================== INGRESOS DEPARTAMENTALES ======================
with tab_ingresos:
    st.markdown("### Ingresos Departamentales (2021–2025)")

    insight_box("Los ingresos departamentales dependen principalmente de transferencias nacionales (SGP) y regalías. Bogotá concentra una gran parte del recaudo total.")
    st.divider()


    # Filtros
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        año_ing_sel = st.selectbox("Año de referencia", options=sorted(df_ing["Año Vigencia"].unique()), index=3)
    with col_f2:
        depts_ing_sel = st.multiselect(
            "Departamentos para evolución",
            options=sorted(df_ing["Entidad"].unique()),
            default=["Bogotá,D.C.", "Atlántico", "Cundinamarca", "ValledelCauca", "Santander"]
        )

    # Sub-pestañas
    sub_tabs_ing = st.tabs(["🏆 Ranking", "📈 Evolución Temporal", "🗂️ Concentración (Treemap)", "📊 Por Región"])

    # 1. Ranking
    with sub_tabs_ing[0]:
        df_año = df_ing[df_ing["Año Vigencia"] == año_ing_sel].sort_values("Recaudo_billones", ascending=False)
        fig_rank = px.bar(
            df_año.head(15),
            x="Recaudo_billones",
            y="Entidad",
            orientation="h",
            color="Region",
            title=f"Ranking de Ingresos Departamentales - {año_ing_sel} (billones COP)",
            labels={"Recaudo_billones": "Billones COP", "Entidad": ""}
        )
        fig_rank.update_layout(height=600)
        st.plotly_chart(fig_rank, use_container_width=True)

    # 2. Evolución Temporal
    with sub_tabs_ing[1]:
        df_evo = df_ing[df_ing["Entidad"].isin(depts_ing_sel)]
        fig_evo = px.line(
            df_evo,
            x="Año Vigencia",
            y="Recaudo_billones",
            color="Entidad",
            markers=True,
            title="Evolución de ingresos departamentales (billones COP)"
        )
        st.plotly_chart(fig_evo, use_container_width=True)

    # 3. Treemap (Concentración)
    with sub_tabs_ing[2]:
        df_tree = df_ing[df_ing["Año Vigencia"] == año_ing_sel]
        fig_tree = px.treemap(
            df_tree,
            path=["Region", "Entidad"],
            values="Recaudo_billones",
            title=f"Concentración de Ingresos por Región y Departamento - {año_ing_sel}"
        )
        st.plotly_chart(fig_tree, use_container_width=True)

    # 4. Por Región (barras apiladas)
    with sub_tabs_ing[3]:
        df_reg = df_ing.groupby(["Año Vigencia", "Region"])["Recaudo_billones"].sum().reset_index()
        fig_reg = px.bar(
            df_reg,
            x="Año Vigencia",
            y="Recaudo_billones",
            color="Region",
            barmode="stack",
            title="Ingresos totales por región (billones COP)"
        )
        st.plotly_chart(fig_reg, use_container_width=True)

st.divider()

# ====================== ANÁLISIS CRUZADO ======================
with tab_cruzado:
    st.markdown("###  Análisis Exploratorio Cruzado")

    insight_box("""
    Las relaciones mostradas son exploratorias y no implican causalidad. 
    Un mayor recaudo no necesariamente causa menor pobreza.
    """)
    st.divider()

    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        años_comunes = sorted(set(df_soc["Año"]) & set(df_ing["Año Vigencia"]))
        año_cruce = st.selectbox("Año de análisis", options=años_comunes, index=len(años_comunes)-1)
    with col2:
        ind_cruce = st.selectbox(
            "Indicador social",
            options=list(NOMBRES_IND.keys()),
            format_func=lambda x: NOMBRES_IND[x]
        )

    # Departamentos comunes
    depts_comunes = sorted(set(df_soc["Departamento"]) & set(df_ing["Entidad"]))

    # Mapa de regiones (porque df_soc no tiene la columna Region)
    REGION_MAP = {
        "Bogotá,D.C.": "Capital",
        "Cundinamarca": "Centro",
        "Atlántico": "Caribe",
        "Santander": "Centro Oriente",
        "Huila": "Centro Sur",
        "Risaralda": "Eje Cafetero",
        "Meta": "Llano",
        "ValledelCauca": "Pacífico"
    }

    df_soc_c = df_soc[
        (df_soc["Año"] == año_cruce) & 
        (df_soc["Departamento"].isin(depts_comunes))
    ][["Departamento", ind_cruce]].copy()
    df_soc_c["Region"] = df_soc_c["Departamento"].map(REGION_MAP)

    df_ing_c = df_ing[
        (df_ing["Año Vigencia"] == año_cruce) & 
        (df_ing["Entidad"].isin(depts_comunes))
    ][["Entidad", "Recaudo_billones"]].rename(columns={"Entidad": "Departamento"})

    df_cruce = df_soc_c.merge(df_ing_c, on="Departamento")

    if not df_cruce.empty:
        fig_sc = px.scatter(
            df_cruce,
            x="Recaudo_billones",
            y=ind_cruce,
            color="Region",
            text="Departamento",
            title=f"Ingresos (billones COP) vs {NOMBRES_IND[ind_cruce]} — {año_cruce}",
            labels={"Recaudo_billones": "Ingresos (billones COP)"}
        )
        fig_sc.update_traces(textposition="top center", marker=dict(size=12, opacity=0.85))
        fig_sc.update_layout(height=550)
        st.plotly_chart(fig_sc, use_container_width=True)

        st.caption("Bogotá suele aparecer como outlier por su tamaño poblacional y económico.")
        

# ====================== NOVEDADES / HALLAZGOS Y CONCLUSIONES ======================
with tab_novedad:   
    st.markdown("###  Novedades ")

    st.markdown("""
    La pandemia generó un **shock asimétrico** en los territorios. 
    Todos los departamentos sufrieron un fuerte deterioro en 2020, pero la velocidad y profundidad de la recuperación fue muy diferente.
    """)

    # Explicación clara de recuperación
    st.markdown("#### ¿Cómo se recuperó cada departamento?")
    st.caption("El gráfico muestra la **reducción neta** de cada indicador entre 2020 y 2024. Valores positivos = mejora.")

    # Cálculo de recuperación para TODOS los indicadores
    df_rec = df_soc[df_soc["Año"].isin([2020, 2024])].copy()
    df_rec = df_rec.pivot(index="Departamento", columns="Año", values=["Pob_monetaria", "Pob_extrema", "Gini", "Ocupacion", "Desocupacion"])

    # Reducción / mejora
    rec = pd.DataFrame()
    rec["Pobreza Monetaria (pp)"] = df_rec[("Pob_monetaria", 2020)] - df_rec[("Pob_monetaria", 2024)]
    rec["Pobreza Extrema (pp)"] = df_rec[("Pob_extrema", 2020)] - df_rec[("Pob_extrema", 2024)]
    rec["Gini (puntos)"] = df_rec[("Gini", 2020)] - df_rec[("Gini", 2024)]
    rec["Ocupación (pp)"] = df_rec[("Ocupacion", 2024)] - df_rec[("Ocupacion", 2020)]
    rec["Desocupación (pp)"] = df_rec[("Desocupacion", 2020)] - df_rec[("Desocupacion", 2024)]

    # Gráfico de barras agrupadas
    fig_rec = px.bar(
        rec.reset_index().melt(id_vars="Departamento", var_name="Indicador", value_name="Cambio"),
        x="Cambio",
        y="Departamento",
        color="Indicador",
        orientation="h",
        barmode="group",
        title="Recuperación post-pandemia por indicador y departamento (2020 → 2024)",
        labels={"Cambio": "Cambio neto"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_rec.update_layout(height=650, legend_title="Indicador")
    st.plotly_chart(fig_rec, use_container_width=True)

    # Insights clave
    st.markdown("### Principales hallazgos")
    col1, col2 = st.columns(2)
    with col1:
        st.success("**Recuperación más rápida**")
        st.markdown("""
        - **Atlántico** y **Meta** lideraron la reducción de pobreza monetaria.
        - **Bogotá** y **Valle del Cauca** mostraron la mejor recuperación en empleo.
        """)
    with col2:
        st.warning("**Brechas que persisten**")
        st.markdown("""
        - El **Gini** apenas se movió en casi todos los departamentos.
        - La recuperación del empleo fue más lenta que la de la pobreza.
        """)

    st.divider()

    st.markdown("""
    ### Reflexión final
    La pandemia amplificó las desigualdades territoriales preexistentes.  
    Aunque la mayoría de departamentos ya mejoraron los niveles de 2019 en pobreza, **las brechas estructurales** (desigualdad y calidad del empleo) se mantienen.  
    Los recursos fiscales (ingresos departamentales) se concentran en pocos territorios, lo que limita la capacidad redistributiva en las regiones más vulnerables.
    """)
    st.divider()


    st.caption("**A pesar de los avances observados en la recuperación post-pandemia, este boletín pone de manifiesto una" \
    " limitación estructural persistente del sistema estadístico colombiano: " \
    "la escasa disponibilidad de indicadores socioeconómicos desagregados y " \
    "actualizados a nivel departamental. La mayoría de los datos utilizados " \
    "corresponden a estimaciones estadísticas, reflejando la precaria infraestructura" \
    " de información regional del país. Esta realidad no solo condiciona la" \
    " precisión y profundidad de los análisis sobre desigualdad y pobreza " \
    "territorial, sino que también limita seriamente la capacidad del Estado" \
    " para diseñar políticas públicas verdaderamente diferenciadas y efectivas." \
    " Fortalecer la producción y el acceso oportuno a estadísticas regionales " \
    "confiables constituye, por tanto, un desafío prioritario para avanzar hacia" \
    " una reducción efectiva de las brechas de exclusión en Colombia.** ")

