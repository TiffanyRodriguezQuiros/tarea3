import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from modelo import resolver, CASAS, AHORRO_C1, AHORRO_C2, AHORRO_C3
from modelo import COSTO_C1, COSTO_C2, COSTO_C3, MAX_C1, MAX_C2, MAX_C3

st.set_page_config(page_title="Paneles Solares - Tarea 3", layout="wide")

st.title("Optimizacion de Paneles Solares - 3 Casas (CNFL)")
st.write("II-1122 | Modelos de Optimizacion Industrial | UCR Alajuela | Tarea 3")

st.divider()

# Seccion 1: datos de las 3 casas
st.subheader("Datos de las 3 casas (facturas CNFL)")
st.write(
    "Se compararon 3 facturas residenciales de CNFL. "
    "El modelo decide cuantos paneles solares instalar en cada casa para maximizar el ahorro mensual total."
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Casa 1 - Heredia**")
    st.write("Consumo: 86 kWh/mes")
    st.write("Factura actual: 5,465 colones")
    st.write("Irradiacion: 3.5 h sol/dia")
    st.write("Generacion por panel: 31.5 kWh/mes")
    st.write("Costo por panel: 165,000 colones")
with col2:
    st.markdown("**Casa 2 - San Jose**")
    st.write("Consumo: 152 kWh/mes")
    st.write("Factura actual: 9,240 colones")
    st.write("Irradiacion: 4.0 h sol/dia")
    st.write("Generacion por panel: 36.0 kWh/mes")
    st.write("Costo por panel: 150,000 colones")
with col3:
    st.markdown("**Casa 3 - Alajuela**")
    st.write("Consumo: 218 kWh/mes")
    st.write("Factura actual: 13,180 colones")
    st.write("Irradiacion: 4.5 h sol/dia")
    st.write("Generacion por panel: 40.5 kWh/mes")
    st.write("Costo por panel: 145,000 colones")

st.divider()

# Seccion 2: modelo LP
with st.expander("Ver modelo de programacion lineal"):
    st.markdown(
        """
**Variables de decision:**
- x1 = numero de paneles en Casa 1 (Heredia)
- x2 = numero de paneles en Casa 2 (San Jose)
- x3 = numero de paneles en Casa 3 (Alajuela)

**Funcion objetivo:**

Maximizar Z = 1832*x1 + 2094*x2 + 2355*x3 (colones ahorrados por mes)

**Restricciones:**

- Presupuesto: 165000*x1 + 150000*x2 + 145000*x3 <= presupuesto
- Limite Casa 1: x1 <= 2 (no generar mas de lo que consume)
- Limite Casa 2: x2 <= 4
- Limite Casa 3: x3 <= 5
- No negatividad: x1, x2, x3 >= 0
        """
    )

st.divider()

# Seccion 3: parametros editables
st.subheader("Parametros del modelo")

col_a, col_b = st.columns(2)
with col_a:
    presupuesto = st.slider(
        "Presupuesto disponible para instalacion (colones)",
        min_value=300000,
        max_value=2000000,
        value=1500000,
        step=50000,
        format="%d",
    )
with col_b:
    st.write("")
    st.write("")
    st.info(
        f"Costo maximo posible si se instalan todos los paneles: "
        f"{COSTO_C1*MAX_C1 + COSTO_C2*MAX_C2 + COSTO_C3*MAX_C3:,} colones"
    )

st.write("Maximo de paneles por casa (ajustable):")
colx, coly, colz = st.columns(3)
with colx:
    max1 = st.number_input("Max paneles Casa 1", min_value=0, max_value=10, value=MAX_C1)
with coly:
    max2 = st.number_input("Max paneles Casa 2", min_value=0, max_value=10, value=MAX_C2)
with colz:
    max3 = st.number_input("Max paneles Casa 3", min_value=0, max_value=10, value=MAX_C3)

optimizar = st.button("Resolver modelo", type="primary")

st.divider()

# Seccion 4: resultados
if optimizar:
    res = resolver(presupuesto, max1, max2, max3)

    if res["status"] != "Optimal":
        st.error(f"El modelo no encontro solucion optima. Estado: {res['status']}")
        st.stop()

    st.subheader("Solucion optima")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Paneles Casa 1 (Heredia)",  f"{res['x1']:.0f} paneles")
    m2.metric("Paneles Casa 2 (San Jose)", f"{res['x2']:.0f} paneles")
    m3.metric("Paneles Casa 3 (Alajuela)", f"{res['x3']:.0f} paneles")
    m4.metric("Ahorro mensual total",      f"{res['ahorro_mensual']:,.0f} colones")

    st.write(
        f"Costo total de instalacion: **{res['costo_invertido']:,.0f} colones** | "
        f"Tiempo de recuperacion: **{res['meses_payback']} meses** "
        f"({round(res['meses_payback']/12, 1)} años)"
    )

    st.divider()

    # Graficos
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.write("**Paneles instalados por casa**")
        fig1, ax1 = plt.subplots(figsize=(5, 3.5))
        casas_nombres = ["Casa 1\nHeredia", "Casa 2\nSan Jose", "Casa 3\nAlajuela"]
        paneles = [res["x1"], res["x2"], res["x3"]]
        maximos = [max1, max2, max3]
        colores = ["#1565C0", "#2E7D32", "#E65100"]
        bars = ax1.bar(casas_nombres, paneles, color=colores, width=0.5)
        ax1.bar(casas_nombres, maximos, color="lightgrey", width=0.5, zorder=0, label="Max posible")
        ax1.bar(casas_nombres, paneles, color=colores, width=0.5, zorder=1, label="Paneles optimos")
        for bar, val in zip(bars, paneles):
            if val > 0:
                ax1.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.05,
                    f"{val:.0f}",
                    ha="center",
                    fontweight="bold",
                )
        ax1.set_ylabel("Numero de paneles")
        ax1.set_ylim(0, max(maximos) + 1)
        ax1.legend(fontsize=8)
        ax1.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig1)

    with col_g2:
        st.write("**Ahorro mensual por casa (colones)**")
        fig2, ax2 = plt.subplots(figsize=(5, 3.5))
        ahorros = [
            AHORRO_C1 * res["x1"],
            AHORRO_C2 * res["x2"],
            AHORRO_C3 * res["x3"],
        ]
        colores2 = ["#1565C0", "#2E7D32", "#E65100"]
        bars2 = ax2.bar(casas_nombres, ahorros, color=colores2, width=0.5)
        for bar, val in zip(bars2, ahorros):
            if val > 0:
                ax2.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 30,
                    f"{val:,.0f}",
                    ha="center",
                    fontsize=9,
                )
        ax2.set_ylabel("Ahorro mensual (colones)")
        ax2.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig2)

    st.divider()

    # Tabla de precios sombra
    st.subheader("Precios sombra (analisis de sensibilidad)")
    st.write(
        "El precio sombra indica cuanto aumentaria el ahorro mensual "
        "si se relajara esa restriccion en una unidad."
    )

    nombres_restricciones = {
        "Presupuesto": "Presupuesto (colones)",
        "Max_Casa1":   "Limite max paneles Casa 1",
        "Max_Casa2":   "Limite max paneles Casa 2",
        "Max_Casa3":   "Limite max paneles Casa 3",
    }

    filas = []
    for clave, nombre in nombres_restricciones.items():
        pi  = res["precios_sombra"].get(clave, 0)
        hol = res["holguras"].get(clave, 0)
        filas.append({
            "Restriccion":         nombre,
            "Precio sombra":       round(pi, 4),
            "Holgura":             round(hol, 2),
            "Es cuello de botella": "Si" if abs(hol) < 0.01 else "No",
        })

    df = pd.DataFrame(filas)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # Interpretacion
    st.subheader("Interpretacion de resultados")

    cuellos = [f["Restriccion"] for f in filas if f["Es cuello de botella"] == "Si"]
    factura_antes = 5465 + 9240 + 13180
    factura_despues = factura_antes - res["ahorro_mensual"]

    x1_real = int(res["x1"])
    x2_real = int(res["x2"])
    x3_real = int(res["x3"])

    st.write(
        f"La solucion del modelo indica instalar **{res['x1']:.2f} paneles en Casa 1 (Heredia)**, "
        f"**{res['x2']:.0f} paneles en Casa 2 (San Jose)** y "
        f"**{res['x3']:.0f} paneles en Casa 3 (Alajuela)**."
    )
    st.write(
        "Nota: la programacion lineal permite soluciones fraccionarias. "
        f"En la practica, en Casa 1 se instala **{x1_real} panel** (redondeando hacia abajo). "
        "Para forzar numeros enteros se usaria Programacion Entera Mixta (MIP), "
        "tema de semanas posteriores del curso."
    )
    st.write(
        f"El ahorro mensual estimado es de **{res['ahorro_mensual']:,.0f} colones**, "
        f"reduciendo la factura combinada de las 3 casas de "
        f"**{factura_antes:,}** a aproximadamente "
        f"**{factura_despues:,.0f} colones por mes**."
    )
    st.write(
        f"La inversion se recupera en aproximadamente **{res['meses_payback']} meses** "
        f"({round(res['meses_payback']/12, 1)} anos)."
    )
    if cuellos:
        st.write(
            f"Los cuellos de botella son: **{', '.join(cuellos)}**. "
            f"Si se aumenta el presupuesto o el limite de paneles por casa, el ahorro mejora."
        )

else:
    st.info("Ajuste los parametros y presione 'Resolver modelo' para ver la solucion optima.")
