from pulp import (
    LpProblem, LpMaximize, LpVariable, LpStatus,
    PULP_CBC_CMD, value
)


def resolver_paneles(
    margen_r: float,
    margen_c: float,
    margen_i: float,
    cap_silicio: float,
    cap_ensamble: float,
    cap_calidad: float,
    dem_res: float,
    dem_com: float,
    dem_ind: float,
) -> dict:
    """
    Modelo LP: mix de producción semanal de paneles solares.

    Variables de decision:
        x1 = unidades de Panel Residencial (100 W)
        x2 = unidades de Panel Comercial   (300 W)
        x3 = unidades de Panel Industrial  (500 W)

    Retorna dict con x1, x2, x3, Z, status, precios_sombra.
    """
    m = LpProblem("PanelesSolaresCR", LpMaximize)

    x1 = LpVariable("Panel_Residencial", lowBound=0)
    x2 = LpVariable("Panel_Comercial",   lowBound=0)
    x3 = LpVariable("Panel_Industrial",  lowBound=0)

    # Función objetivo — maximizar margen de contribución (₡ miles/unidad)
    m += margen_r * x1 + margen_c * x2 + margen_i * x3, "Margen_Total"

    # Restricciones de recursos
    m += 1.2 * x1 + 3.0 * x2 + 5.5 * x3 <= cap_silicio,  "Silicio_kg"
    m += 2.5 * x1 + 5.0 * x2 + 9.0 * x3 <= cap_ensamble, "Ensamble_hr"
    m += 0.5 * x1 + 1.5 * x2 + 2.5 * x3 <= cap_calidad,  "Calidad_hr"

    # Restricciones de demanda máxima
    m += x1 <= dem_res, "Demanda_Residencial"
    m += x2 <= dem_com, "Demanda_Comercial"
    m += x3 <= dem_ind, "Demanda_Industrial"

    m.solve(PULP_CBC_CMD(msg=0))

    precios_sombra = {}
    holguras = {}
    for name, constr in m.constraints.items():
        precios_sombra[name] = constr.pi if constr.pi is not None else 0.0
        holguras[name] = constr.slack if constr.slack is not None else 0.0

    return {
        "x1": round(x1.varValue or 0, 2),
        "x2": round(x2.varValue or 0, 2),
        "x3": round(x3.varValue or 0, 2),
        "Z":  round(value(m.objective) or 0, 2),
        "status": LpStatus[m.status],
        "precios_sombra": precios_sombra,
        "holguras": holguras,
    }
