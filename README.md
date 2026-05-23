# Tarea 3 - Paneles Solares

II-1122 | Modelos de Optimizacion Industrial | UCR Alajuela

## Descripcion del caso

Se compararon 3 facturas de electricidad residencial de CNFL correspondientes a casas en diferentes provincias de Costa Rica. El objetivo es determinar cuantos paneles solares instalar en cada casa para maximizar el ahorro mensual en electricidad, dado un presupuesto limitado.

## Datos de las 3 casas

| | Casa 1 - Heredia | Casa 2 - San Jose | Casa 3 - Alajuela |
|---|---|---|---|
| Consumo mensual | 86 kWh | 152 kWh | 218 kWh |
| Factura mensual | 5,465 colones | 9,240 colones | 13,180 colones |
| Horas sol/dia | 3.5 h | 4.0 h | 4.5 h |
| Generacion por panel | 31.5 kWh/mes | 36.0 kWh/mes | 40.5 kWh/mes |
| Costo por panel instalado | 165,000 colones | 150,000 colones | 145,000 colones |
| Max paneles posibles | 2 | 4 | 5 |

Tarifa CNFL residencial usada: 58.16 colones/kWh

## Modelo de programacion lineal

**Variables de decision:**
- x1 = numero de paneles instalados en Casa 1 (Heredia)
- x2 = numero de paneles instalados en Casa 2 (San Jose)
- x3 = numero de paneles instalados en Casa 3 (Alajuela)

**Funcion objetivo:**

Maximizar Z = 1832*x1 + 2094*x2 + 2355*x3

(colones ahorrados en electricidad por mes)

**Restricciones:**

- Presupuesto: 165000*x1 + 150000*x2 + 145000*x3 <= 1,500,000
- Limite Casa 1: x1 <= 2
- Limite Casa 2: x2 <= 4
- Limite Casa 3: x3 <= 5
- No negatividad: x1, x2, x3 >= 0

## Solucion optima (presupuesto base de 1,500,000 colones)

| Variable | Valor |
|---|---|
| x1 (Casa 1 - Heredia) | 1 panel |
| x2 (Casa 2 - San Jose) | 4 paneles |
| x3 (Casa 3 - Alajuela) | 5 paneles |
| Z* | 21,983 colones/mes de ahorro |
| Inversion total | 1,490,000 colones |
| Tiempo de recuperacion | 67.8 meses (5.7 anos) |

## Archivos del proyecto

- `app.py` - interfaz Streamlit
- `modelo.py` - modelo LP con PuLP
- `requirements.txt` - librerias necesarias
- `README.md` - este archivo

## Como correr localmente

```
pip install -r requirements.txt
streamlit run app.py
```
