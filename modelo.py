from pulp import LpProblem, LpMaximize, LpVariable, LpStatus, PULP_CBC_CMD, value


# Datos de las 3 casas (basados en facturas CNFL)
# Casa 1: Heredia, 86 kWh/mes - dato real de factura
# Casa 2: San Jose, 152 kWh/mes - factura ficticia
# Casa 3: Alajuela, 218 kWh/mes - factura ficticia

# Un panel solar de 300W genera aprox:
# Heredia (zona nublada):  3.5 h sol/dia x 0.3 kW x 30 dias = 31.5 kWh/mes por panel
# San Jose (zona urbana):  4.0 h sol/dia x 0.3 kW x 30 dias = 36.0 kWh/mes por panel
# Alajuela (zona seca):    4.5 h sol/dia x 0.3 kW x 30 dias = 40.5 kWh/mes por panel

# Tarifa CNFL residencial: 58.16 colones/kWh
TARIFA = 58.16

GEN_C1 = 31.5   # kWh/mes por panel en Casa 1
GEN_C2 = 36.0   # kWh/mes por panel en Casa 2
GEN_C3 = 40.5   # kWh/mes por panel en Casa 3

AHORRO_C1 = round(GEN_C1 * TARIFA, 0)   # colones ahorrados por panel/mes
AHORRO_C2 = round(GEN_C2 * TARIFA, 0)
AHORRO_C3 = round(GEN_C3 * TARIFA, 0)

# Costo de instalacion por panel (incluye panel + mano de obra)
COSTO_C1 = 165000   # mas caro por techo inclinado y acceso dificil
COSTO_C2 = 150000
COSTO_C3 = 145000

# Maximo de paneles por casa (no generar mas de lo que consume)
MAX_C1 = 2   # 86 / 31.5 = 2.73 -> 2 paneles
MAX_C2 = 4   # 152 / 36  = 4.22 -> 4 paneles
MAX_C3 = 5   # 218 / 40.5 = 5.38 -> 5 paneles


def resolver(presupuesto, max_c1, max_c2, max_c3):
    m = LpProblem("Paneles_Solares_3_Casas", LpMaximize)

    x1 = LpVariable("Casa1_Heredia",  lowBound=0)
    x2 = LpVariable("Casa2_SanJose",  lowBound=0)
    x3 = LpVariable("Casa3_Alajuela", lowBound=0)

    # Objetivo: maximizar ahorro mensual total en colones
    m += AHORRO_C1 * x1 + AHORRO_C2 * x2 + AHORRO_C3 * x3, "Ahorro_Total"

    # Restriccion de presupuesto
    m += COSTO_C1 * x1 + COSTO_C2 * x2 + COSTO_C3 * x3 <= presupuesto, "Presupuesto"

    # No generar mas energia de la que consume cada casa
    m += x1 <= max_c1, "Max_Casa1"
    m += x2 <= max_c2, "Max_Casa2"
    m += x3 <= max_c3, "Max_Casa3"

    m.solve(PULP_CBC_CMD(msg=0))

    precios_sombra = {}
    holguras = {}
    for nombre, restriccion in m.constraints.items():
        precios_sombra[nombre] = restriccion.pi if restriccion.pi is not None else 0.0
        holguras[nombre] = restriccion.slack if restriccion.slack is not None else 0.0

    x1v = round(x1.varValue or 0, 2)
    x2v = round(x2.varValue or 0, 2)
    x3v = round(x3.varValue or 0, 2)

    costo_invertido = COSTO_C1 * x1v + COSTO_C2 * x2v + COSTO_C3 * x3v
    ahorro_mensual  = round(value(m.objective) or 0, 0)
    meses_payback   = round(costo_invertido / ahorro_mensual, 1) if ahorro_mensual > 0 else 0

    return {
        "x1": x1v,
        "x2": x2v,
        "x3": x3v,
        "ahorro_mensual": ahorro_mensual,
        "costo_invertido": round(costo_invertido, 0),
        "meses_payback": meses_payback,
        "status": LpStatus[m.status],
        "precios_sombra": precios_sombra,
        "holguras": holguras,
    }


# Datos de las casas para mostrar en la app
CASAS = {
    "Casa 1 - Heredia": {
        "consumo": 86,
        "factura": 5465,
        "gen_panel": GEN_C1,
        "ahorro_panel": AHORRO_C1,
        "costo_panel": COSTO_C1,
        "max_paneles": MAX_C1,
    },
    "Casa 2 - San Jose": {
        "consumo": 152,
        "factura": 9240,
        "gen_panel": GEN_C2,
        "ahorro_panel": AHORRO_C2,
        "costo_panel": COSTO_C2,
        "max_paneles": MAX_C2,
    },
    "Casa 3 - Alajuela": {
        "consumo": 218,
        "factura": 13180,
        "gen_panel": GEN_C3,
        "ahorro_panel": AHORRO_C3,
        "costo_panel": COSTO_C3,
        "max_paneles": MAX_C3,
    },
}
