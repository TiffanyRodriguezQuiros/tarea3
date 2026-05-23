# ☀️ Paneles Solares CR — Solver LP

**II-1122 · Modelos de Optimización Industrial · UCR Alajuela · Tarea 3**

App interactiva para optimizar el mix de producción semanal de paneles solares usando Programación Lineal (PuLP + Streamlit).

---

## Caso de negocio

**Empresa:** Paneles Solares CR S.A., fabricante costarricense de paneles fotovoltaicos.

**Decisión:** ¿Cuántas unidades de cada tipo de panel producir por semana para maximizar el margen de contribución?

**Tipos de panel:**

| Tipo | Potencia | Margen base (₡ miles) |
|------|----------|----------------------|
| Residencial | 100 W | 85 |
| Comercial | 300 W | 220 |
| Industrial | 500 W | 380 |

---

## Modelo de Programación Lineal

### Variables de decisión

- **x₁** = unidades de Panel Residencial (100 W) producidas por semana
- **x₂** = unidades de Panel Comercial (300 W) producidas por semana
- **x₃** = unidades de Panel Industrial (500 W) producidas por semana

### Función objetivo

$$\max Z = 85x_1 + 220x_2 + 380x_3 \quad [\text{₡ miles / semana}]$$

### Restricciones

| Recurso | Restricción | Límite base |
|---------|-------------|-------------|
| Silicio (kg) | 1.2x₁ + 3.0x₂ + 5.5x₃ ≤ cap | 480 kg |
| Ensamble (hr) | 2.5x₁ + 5.0x₂ + 9.0x₃ ≤ cap | 600 hr |
| Control de calidad (hr) | 0.5x₁ + 1.5x₂ + 2.5x₃ ≤ cap | 180 hr |
| Demanda residencial | x₁ ≤ dem | 150 und |
| Demanda comercial | x₂ ≤ dem | 80 und |
| Demanda industrial | x₃ ≤ dem | 30 und |
| No negatividad | x₁, x₂, x₃ ≥ 0 | — |

---

## Solución óptima (parámetros base)

| Variable | Valor | Descripción |
|----------|-------|-------------|
| x₁* | 96 und | Panel Residencial |
| x₂* | 38 und | Panel Comercial |
| x₃* | 30 und | Panel Industrial (cota de demanda activa) |
| **Z*** | **27,920 ₡ miles** | Margen semanal máximo |

**Cuellos de botella:** Horas de Ensamble (π = ₡14 mil/hr) y Horas de Calidad (π = ₡100 mil/hr).


---

## Estructura del proyecto

```
tarea3_paneles_solares/
├── app.py            ← Interfaz Streamlit
├── modelo.py         ← Modelo LP con PuLP
├── requirements.txt  ← Dependencias
└── README.md         ← Este archivo
```

---

## Cómo ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Deploy en Streamlit Cloud

1. Subir este repositorio a GitHub (público).
2. Ir a [share.streamlit.io](https://share.streamlit.io) → conectar con GitHub.
3. Seleccionar este repo, rama `main`, archivo `app.py`.
4. Presionar **Deploy** — la URL pública estará lista en ~2 minutos.

---

## Interpretación gerencial

El modelo recomienda producir **96 paneles residenciales, 38 comerciales y 30 industriales** para alcanzar el margen máximo de ₡27,920 miles/semana.

Los recursos más escasos son las **horas de calidad** (precio sombra ₡100 mil/hr) y las **horas de ensamble** (₡14 mil/hr). Ampliar el personal de control de calidad es la inversión con mayor retorno marginal antes de cualquier otra decisión de capacidad.

---

*Curso II-1122 · Semanas 5-6 · Simplex Avanzado y Software Industrial*
