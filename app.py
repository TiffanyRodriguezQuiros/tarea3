import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from modelo import resolver_paneles

st.set_page_config(
    page_title="Paneles Solares CR — Solver LP",
    page_icon="☀️",
    layout="wide",
)

# ── Encabezado ────────────────────────────────────────────────────────────────
st.title("☀️ Optimización de Producción — Paneles Solares CR")
st.caption("II-1122 · Modelos de Optimización Industrial · UCR Alajuela · Tarea 3")

st.markdown(
    """
**Empresa:** Paneles Solares CR S.A.
**Decisión:** Mix de producción semanal de tres tipos de panel solar
**Objetivo:** Maximizar el margen de contribución total (₡ miles/semana)
"""
)

st.divider()

# ── Sidebar: parámetros editables ─────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Parámetros del modelo")

    st.subheader("Margen de contribución (₡ miles/unidad)")
    margen_r = st.number_input("Panel Residencial (100 W)", value=85.0, min_value=0.0, step=5.0)
    margen_c = st.number_input("Panel Comercial (300 W)",   value=220.0, min_value=0.0, step=10.0)
    margen_i = st.number_input("Panel Industrial (500 W)",  value=380.0, min_value=0.0, step=10.0)

    st.subheader("Capacidad semanal de recursos")
    cap_silicio  = st.slider("Silicio disponible (kg)",       100, 1000, 480, step=10)
    cap_ensamble = st.slider("Horas de ensamble",             100, 1200, 700, step=20)
    cap_calidad  = st.slider("Horas de control de calidad",    50,  400, 180, step=10)

    st.subheader("Demanda máxima (unidades/semana)")
    dem_res = st.number_input("Demanda Residencial", value=150, min_value=0, step=10)
    dem_com = st.number_input("Demanda Comercial",   value=80,  min_value=0, step=5)
    dem_ind = st.number_input("Demanda Industrial",  value=30,  min_value=0, step=5)

    optimizar = st.button("🔍 Optimizar", type="primary", use_container_width=True)

# ── Modelo LP — descripción ────────────────────────────────────────────────────
with st.expander("📐 Ver modelo LP completo"):
    st.markdown(
        f"""
**Variables de decisión:**
- x₁ = unidades de Panel Residencial (100 W)
- x₂ = unidades de Panel Comercial (300 W)
- x₃ = unidades de Panel Industrial (500 W)

**Función objetivo:**

$$\\max Z = {margen_r}x_1 + {margen_c}x_2 + {margen_i}x_3$$

**Restricciones:**

| Restricción | Coeficientes | Límite |
|---|---|---|
| Silicio (kg) | 1.2 x₁ + 3.0 x₂ + 5.5 x₃ | ≤ {cap_silicio} |
| Ensamble (hr) | 2.5 x₁ + 5.0 x₂ + 9.0 x₃ | ≤ {cap_ensamble} |
| Calidad (hr) | 0.5 x₁ + 1.5 x₂ + 2.5 x₃ | ≤ {cap_calidad} |
| Demanda residencial | x₁ | ≤ {dem_res} |
| Demanda comercial | x₂ | ≤ {dem_com} |
| Demanda industrial | x₃ | ≤ {dem_ind} |
| No negatividad | x₁, x₂, x₃ | ≥ 0 |
"""
    )

# ── Resultados ────────────────────────────────────────────────────────────────
if optimizar:
    res = resolver_paneles(
        margen_r, margen_c, margen_i,
        cap_silicio, cap_ensamble, cap_calidad,
        dem_res, dem_com, dem_ind,
    )

    estado = res["status"]
    color_estado = "🟢" if estado == "Optimal" else "🔴"
    st.markdown(f"### {color_estado} Estado del solver: **{estado}**")

    if estado != "Optimal":
        st.error("El modelo no tiene solución óptima. Revise los parámetros.")
        st.stop()

    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Panel Residencial (x₁)", f"{res['x1']:.0f} und")
    col2.metric("Panel Comercial (x₂)",   f"{res['x2']:.0f} und")
    col3.metric("Panel Industrial (x₃)",  f"{res['x3']:.0f} und")
    col4.metric("Z* — Margen Total",       f"₡{res['Z']:,.1f} miles")

    st.divider()

    # Gráficos
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Producción óptima por tipo de panel")
        fig1, ax1 = plt.subplots(figsize=(5, 3.5))
        tipos  = ["Residencial\n(x₁)", "Comercial\n(x₂)", "Industrial\n(x₃)"]
        valores = [res["x1"], res["x2"], res["x3"]]
        colores = ["#1E88E5", "#FDD835", "#43A047"]
        bars = ax1.bar(tipos, valores, color=colores, width=0.5)
        for bar, val in zip(bars, valores):
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                     f"{val:.0f}", ha="center", va="bottom", fontweight="bold")
        ax1.set_ylabel("Unidades / semana")
        ax1.set_ylim(0, max(valores) * 1.2 + 5)
        ax1.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig1)

    with col_b:
        st.subheader("Uso de recursos vs. capacidad")
        x1v, x2v, x3v = res["x1"], res["x2"], res["x3"]
        uso_sil = 1.2 * x1v + 3.0 * x2v + 5.5 * x3v
        uso_ens = 2.5 * x1v + 5.0 * x2v + 9.0 * x3v
        uso_cal = 0.5 * x1v + 1.5 * x2v + 2.5 * x3v
        recursos = ["Silicio", "Ensamble", "Calidad"]
        uso      = [uso_sil, uso_ens, uso_cal]
        cap      = [cap_silicio, cap_ensamble, cap_calidad]
        pct      = [u / c * 100 for u, c in zip(uso, cap)]

        fig2, ax2 = plt.subplots(figsize=(5, 3.5))
        y_pos = range(len(recursos))
        ax2.barh(y_pos, cap,  color="#E0E0E0", label="Capacidad")
        ax2.barh(y_pos, uso,  color=["#E53935" if p > 99 else "#1E88E5" for p in pct], label="Uso")
        ax2.set_yticks(list(y_pos))
        ax2.set_yticklabels(recursos)
        for i, (u, p) in enumerate(zip(uso, pct)):
            ax2.text(u + 2, i, f"{p:.0f}%", va="center", fontsize=9)
        ax2.spines[["top", "right"]].set_visible(False)
        ax2.legend(loc="lower right", fontsize=8)
        st.pyplot(fig2)

    st.divider()

    # Precios sombra
    st.subheader("📊 Análisis de sensibilidad — Precios sombra")
    labels_ps = {
        "Silicio_kg":            "Silicio (kg)",
        "Ensamble_hr":           "Ensamble (hr)",
        "Calidad_hr":            "Calidad (hr)",
        "Demanda_Residencial":   "Demanda Residencial",
        "Demanda_Comercial":     "Demanda Comercial",
        "Demanda_Industrial":    "Demanda Industrial",
    }
    ps_data = []
    for key, label in labels_ps.items():
        pi     = res["precios_sombra"].get(key, 0)
        holgura = res["holguras"].get(key, 0)
        ps_data.append({
            "Restricción":    label,
            "Precio sombra (₡ miles)": round(pi, 4),
            "Holgura (unidad recurso)": round(holgura, 2),
            "¿Cuello de botella?": "🔴 Sí" if abs(holgura) < 0.01 else "🟢 No",
        })
    df_ps = pd.DataFrame(ps_data)
    st.dataframe(df_ps, use_container_width=True, hide_index=True)

    st.divider()

    # Interpretación gerencial
    st.subheader("🧑‍💼 Interpretación gerencial")

    cuello = [r["Restricción"] for r in ps_data if "Sí" in r["¿Cuello de botella?"]]
    cuello_str = ", ".join(cuello) if cuello else "ninguno"

    margen_total = res["Z"]
    st.success(
        f"**Recomendación de producción semanal óptima:**  \n"
        f"Producir **{res['x1']:.0f}** paneles residenciales, "
        f"**{res['x2']:.0f}** paneles comerciales y "
        f"**{res['x3']:.0f}** paneles industriales genera un **margen de contribución "
        f"de ₡{margen_total:,.1f} miles** por semana."
    )

    if cuello:
        ps_vals = {r["Restricción"]: r["Precio sombra (₡ miles)"] for r in ps_data}
        mejor = max(cuello, key=lambda r: abs(ps_vals.get(r, 0)))
        mejor_pi = ps_vals.get(mejor, 0)
        st.info(
            f"**Recurso prioritario para ampliar:** {mejor}  \n"
            f"Cada unidad adicional de este recurso incrementa el margen en "
            f"**₡{mejor_pi:,.2f} miles**. Se recomienda negociar mayor capacidad "
            f"en este recurso antes de cualquier otra inversión."
        )
    else:
        st.info("Ningún recurso está completamente agotado. Existen holguras en todos los cuellos de botella.")

    st.markdown(
        f"> **Cuello(s) de botella identificado(s):** {cuello_str}  \n"
        f"> Los recursos con precio sombra > 0 son los que limitan la rentabilidad."
    )

else:
    st.info("Ajusta los parámetros en el panel izquierdo y presiona **Optimizar**.")
