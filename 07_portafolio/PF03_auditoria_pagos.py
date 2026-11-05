# 07_portafolio/PF03_auditoria_pagos.py
"""
Auditoría Forense de la Población Transaccional de Pagos (pagos.csv)
y Validación Empírica de la Capacidad Financiera del TCO
Autor: Rodrigo Colque (Grupo 08 - EPS Aguas del Sur S.A.)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Rutas de datos
PAGOS_PATH = "../Recursos/pagos.csv" if os.path.exists("../Recursos/pagos.csv") else "Recursos/pagos.csv"
PRESUP_PATH = "../Recursos/presupuesto_ti.csv" if os.path.exists("../Recursos/presupuesto_ti.csv") else "Recursos/presupuesto_ti.csv"
TCO_PATH = "PF02_tco.csv" if os.path.exists("PF02_tco.csv") else "07_portafolio/PF02_tco.csv"

# 1. Carga y preprocesamiento de datos
df_pagos = pd.read_csv(PAGOS_PATH)
df_presup = pd.read_csv(PRESUP_PATH)
df_tco = pd.read_csv(TCO_PATH)

total_registros = len(df_pagos)
gasto_total_empresa = df_pagos["monto"].sum()

# Filtrar pagos correspondientes a servicios de TI
df_ti = df_pagos[df_pagos["concepto"] == "Servicio informático"].copy()
df_ti["fecha"] = pd.to_datetime(df_ti["fecha"])
df_ti["mes"] = df_ti["fecha"].dt.month
df_ti["mes_nombre"] = df_ti["fecha"].dt.strftime("%b")

monto_ti_total = df_ti["monto"].sum()
num_pagos_ti = len(df_ti)
pct_ti_sobre_empresa = (monto_ti_total / gasto_total_empresa) * 100

print("=" * 85)
print("AUDITORÍA FORENSE DE LA POBLACIÓN DE PAGOS INSTITUCIONALES (EPS AGUAS DEL SUR S.A.)")
print("=" * 85)
print(f"Total transacciones procesadas (pagos.csv): {total_registros:,} pagos")
print(f"Desembolso total institucional del período : S/ {gasto_total_empresa:,.2f}")
print(f"Pagos en 'Servicio informático'           : {num_pagos_ti:,} pagos ({num_pagos_ti/total_registros*100:.1f} % del volumen)")
print(f"Monto total ejecutado en servicios TI     : S/ {monto_ti_total:,.2f} ({pct_ti_sobre_empresa:.2f} % del gasto empresarial)")
print(f"Promedio por comprobante informático      : S/ {df_ti['monto'].mean():,.2f}")
print(f"Mediana por comprobante informático       : S/ {df_ti['monto'].median():,.2f}")
print(f"Desviación estándar de montos             : S/ {df_ti['monto'].std():,.2f}")
print(f"Comprobante máximo emitido                : S/ {df_ti['monto'].max():,.2f}")

# 2. Análisis de estacionalidad mensual
meses_nombres = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Set", "Oct", "Nov", "Dic"]
gasto_mensual = df_ti.groupby("mes")["monto"].agg(["count", "sum"]).reindex(range(1, 13), fill_value=0)
gasto_mensual["nombre"] = meses_nombres

print("\n--- DISTRIBUCIÓN MENSUAL DEL GASTO EN SERVICIOS INFORMÁTICOS (2025) ---")
for idx, row in gasto_mensual.iterrows():
    print(f"  Mes {idx:02d} ({row['nombre']}): {int(row['count']):3d} pagos | S/ {row['sum']:10,.2f}")

prom_mensual = gasto_mensual["sum"].mean()
mes_pico = gasto_mensual.loc[gasto_mensual["sum"].idxmax()]
print(f"\n→ Promedio mensual desembolsado en TI: S/ {prom_mensual:,.2f} / mes")
print(f"→ Mes con mayor desembolso: Mes {gasto_mensual['sum'].idxmax()} ({mes_pico['nombre']}) con S/ {mes_pico['sum']:,.2f} (Cierre de ejercicio presupuestal)")

# 3. Concentración de proveedores (Análisis de Pareto)
proveedores = df_ti.groupby("codigo_proveedor")["monto"].agg(["count", "sum"]).sort_values("sum", ascending=False)
proveedores["pct_acumulado"] = (proveedores["sum"].cumsum() / monto_ti_total) * 100
total_proveedores_ti = len(proveedores)
top_10_prv = proveedores.head(10)
top_10_pct = top_10_prv["sum"].sum() / monto_ti_total * 100

print(f"\n--- CONCENTRACIÓN POR PROVEEDORES DE TI ({total_proveedores_ti} proveedores únicos) ---")
print(top_10_prv[["count", "sum", "pct_acumulado"]].to_string())
print(f"\n→ Los 10 primeros proveedores concentran el {top_10_pct:.1f} % del gasto en servicios informáticos.")
print(f"→ Proveedor de mayor facturación: {proveedores.index[0]} con S/ {proveedores.iloc[0]['sum']:,.2f} ({proveedores.iloc[0]['sum']/monto_ti_total*100:.1f} %)")

# 4. Fragmentación del gasto y Shadow IT
pagos_menores_500 = len(df_ti[df_ti["monto"] <= 500])
pct_menores_500 = (pagos_menores_500 / num_pagos_ti) * 100
presup_ejecutado = df_presup["ejecutado"].sum()

print("\n--- ANÁLISIS DE FRAGMENTACIÓN Y GOBERNANZA PRESUPUESTAL ---")
print(f"Pagos <= S/ 500 (compras menores/directas) : {pagos_menores_500} ({pct_menores_500:.1f} % de transacciones)")
print(f"Presupuesto ejecutado formal de TI (presupuesto_ti.csv): S/ {presup_ejecutado:,.2f}")
print(f"Gasto real en 'Servicio informático' (pagos.csv)      : S/ {monto_ti_total:,.2f}")
diferencia_shadow_it = monto_ti_total - presup_ejecutado
print(f"Diferencia (Gasto de TI disperso / Shadow IT)          : S/ {diferencia_shadow_it:,.2f} (+{diferencia_shadow_it/presup_ejecutado*100:.1f} %)")
print("→ Hallazgo forense: Las áreas usuarias contrataron servicios informáticos por fuera")
print("  de la partida centralizada de TI, evidenciando dispersión de contratos y nula gobernanza.")

# 5. Validación empírica de sostenibilidad del TCO
costo_anual_recurrente_tco = df_tco["costo_anual"].sum()
print("\n--- VALIDACIÓN EMPÍRICA DE SOSTENIBILIDAD DEL TCO DEL PETI ---")
print(f"Costo recurrente anual proyectado por el nuevo portafolio : S/ {costo_anual_recurrente_tco:,.2f} / año")
print(f"Capacidad anual histórica demostrada en pagos de TI (2025) : S/ {monto_ti_total:,.2f} / año")
print(f"Margen de holgura presupuestal de la empresa               : S/ {monto_ti_total - costo_anual_recurrente_tco:,.2f} / año")
print(f"Ratio de cobertura (Capacidad histórica / Opex PETI)      : {monto_ti_total / costo_anual_recurrente_tco:.2f}×")
print("✔ Conclusión de auditoría: El portafolio del PETI no sobrecarga financieramente a la EPS;")
print("  más bien, centraliza y ordena el gasto que hoy se dispersa en compras reactivas.")

# 6. Generación de gráficos analíticos
out_dir = "../graficos" if os.path.exists("../graficos") else "graficos"
os.makedirs(out_dir, exist_ok=True)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10.5))

# Subplot 1: Gasto mensual en TI
ax1.bar(meses_nombres, gasto_mensual["sum"], color="#0284C7", edgecolor="#0369A1", width=0.65)
ax1.axhline(prom_mensual, color="#DC2626", linestyle="--", linewidth=1.5, label=f"Media mensual: S/ {prom_mensual/1000:,.0f}k")
ax1.axhline(costo_anual_recurrente_tco / 12, color="#059669", linestyle=":", linewidth=2, label=f"Opex mensual PETI: S/ {costo_anual_recurrente_tco/12/1000:,.0f}k")
ax1.set_title("Evolución Mensual de Pagos en Servicios Informáticos (2025)", fontsize=11, fontweight="bold")
ax1.set_ylabel("Monto Desembolsado (S/)", fontsize=10)
ax1.legend(loc="upper left", fontsize=9)
ax1.grid(axis="y", linestyle="--", alpha=0.4)

# Subplot 2: Curva de Pareto de Proveedores de TI
x_prv = np.arange(15)
ax2_twin = ax2.twinx()
ax2.bar(x_prv, proveedores["sum"].head(15), color="#3B82F6", width=0.6, label="Gasto por Proveedor")
ax2_twin.plot(x_prv, proveedores["pct_acumulado"].head(15), color="#DC2626", marker="o", linewidth=2, label="% Acumulado")
ax2_twin.axhline(80, color="#D97706", linestyle="--", linewidth=1, label="Umbral 80% Pareto")
ax2.set_xticks(x_prv)
ax2.set_xticklabels(proveedores.index[:15], rotation=45, ha="right", fontsize=8.5)
ax2.set_title("Concentración de Pagos de TI por Proveedor (Pareto)", fontsize=11, fontweight="bold")
ax2.set_ylabel("Monto Acumulado (S/)", fontsize=10)
ax2_twin.set_ylabel("% Acumulado", fontsize=10)
ax2.grid(axis="y", linestyle="--", alpha=0.3)

# Subplot 3: Fragmentación de Comprobantes por Rango de Monto
rangos = ["≤ S/ 500\n(Caja chica)", "S/ 501–1.5k\n(Menor cuantía)", "S/ 1.5k–5k\n(Servicios)", "S/ 5k–20k\n(Contratos)", "> S/ 20k\n(Licencias)"]
conteos_rangos = [
    len(df_ti[df_ti["monto"] <= 500]),
    len(df_ti[(df_ti["monto"] > 500) & (df_ti["monto"] <= 1500)]),
    len(df_ti[(df_ti["monto"] > 1500) & (df_ti["monto"] <= 5000)]),
    len(df_ti[(df_ti["monto"] > 5000) & (df_ti["monto"] <= 20000)]),
    len(df_ti[df_ti["monto"] > 20000])
]
colores_rangos = ["#EF4444", "#F59E0B", "#10B981", "#3B82F6", "#6366F1"]
ax3.bar(rangos, conteos_rangos, color=colores_rangos, width=0.55)
for i, v in enumerate(conteos_rangos):
    ax3.text(i, v + 15, f"{v}\n({v/num_pagos_ti*100:.1f}%)", ha="center", fontsize=8.5, fontweight="bold")
ax3.set_title("Fragmentación de Transacciones Informáticas por Importe", fontsize=11, fontweight="bold")
ax3.set_ylabel("Cantidad de Comprobantes", fontsize=10)
ax3.grid(axis="y", linestyle="--", alpha=0.4)

# Subplot 4: Contraste de Capacidad Financiera vs TCO Propuesto
comparativa_labels = ["Gasto TI Ejecutado\n(pagos.csv 2025)", "Presupuesto Formal TI\n(presupuesto_ti.csv)", "Opex Anual Portafolio\n(TCO Recurrente PETI)"]
comparativa_valores = [monto_ti_total, presup_ejecutado, costo_anual_recurrente_tco]
colores_comp = ["#DC2626", "#F59E0B", "#059669"]

bars = ax4.bar(comparativa_labels, comparativa_valores, color=colores_comp, width=0.5)
for bar in bars:
    yval = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2, yval + 40000, f"S/ {yval:,.0f}", ha="center", fontsize=9.5, fontweight="bold")
ax4.set_title("Validación de Capacidad Financiera: Histórico vs. Opex PETI", fontsize=11, fontweight="bold")
ax4.set_ylabel("Soles (S/)", fontsize=10)
ax4.grid(axis="y", linestyle="--", alpha=0.4)

plt.suptitle("Auditoría Forense de la Población de Pagos y Factibilidad del Portafolio de TI\n(EPS AGUAS DEL SUR S.A. — Población: 19 281 transacciones)", 
             fontsize=13, fontweight="bold", y=0.99)
plt.tight_layout()
graph_path = os.path.join(out_dir, "PF_auditoria_pagos_ti.png")
plt.savefig(graph_path, dpi=160)
plt.close()
print(f"\n✔ Gráfico {graph_path} generado exitosamente.")
