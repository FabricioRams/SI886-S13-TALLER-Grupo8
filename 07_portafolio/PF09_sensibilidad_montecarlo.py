# 07_portafolio/PF09_sensibilidad_montecarlo.py
"""
Análisis Estocástico de Sensibilidad y Simulación Monte Carlo del TCO Quinquenal
Determinación de la Reserva de Contingencia y Análisis de Tornado
Autor: Rodrigo Colque (Grupo 08 - EPS Aguas del Sur S.A.)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Configuración de reproducibilidad
np.random.seed(42)
N_SIMULACIONES = 10000

# Cargar TCO calculado en PF02
TCO_PATH = "PF02_tco.csv" if os.path.exists("PF02_tco.csv") else "07_portafolio/PF02_tco.csv"
CAND_PATH = "PF01_portafolio_candidatos.csv" if os.path.exists("PF01_portafolio_candidatos.csv") else "07_portafolio/PF01_portafolio_candidatos.csv"

df_tco = pd.read_csv(TCO_PATH)
df_cand = pd.read_csv(CAND_PATH)
df_merged = df_tco.merge(df_cand[["codigo", "nombre"]], on="codigo")

# Parsear incertidumbre (ej. "±30 %" -> 0.30)
df_merged["margen_num"] = df_merged["incertidumbre"].str.extract(r'(\d+)').astype(float) / 100.0
df_merged["tco_min"] = df_merged["tco_5"] * (1 - df_merged["margen_num"])
df_merged["tco_max"] = df_merged["tco_5"] * (1 + df_merged["margen_num"])
df_merged["rango_varianza"] = df_merged["tco_max"] - df_merged["tco_min"]

tco_base_total = df_merged["tco_5"].sum()

# Simulación de Monte Carlo con distribución triangular (min, moda=base, max)
simulaciones_proyectos = np.zeros((len(df_merged), N_SIMULACIONES))

for i, row in df_merged.iterrows():
    simulaciones_proyectos[i, :] = np.random.triangular(
        left=row["tco_min"],
        mode=row["tco_5"],
        right=row["tco_max"],
        size=N_SIMULACIONES
    )

# TCO total por simulación
tco_simulado_total = simulaciones_proyectos.sum(axis=0)

# Métricas estadísticas
media_tco = np.mean(tco_simulado_total)
mediana_tco = np.median(tco_simulado_total)
desv_tco = np.std(tco_simulado_total)
p05 = np.percentile(tco_simulado_total, 5)
p10 = np.percentile(tco_simulado_total, 10)
p50 = np.percentile(tco_simulado_total, 50)
p75 = np.percentile(tco_simulado_total, 75)
p90 = np.percentile(tco_simulado_total, 90)
p95 = np.percentile(tco_simulado_total, 95)
p99 = np.percentile(tco_simulado_total, 99)

reserva_contingencia_p90 = p90 - tco_base_total
pct_reserva_p90 = (reserva_contingencia_p90 / tco_base_total) * 100

prob_superar_base = (np.sum(tco_simulado_total > tco_base_total) / N_SIMULACIONES) * 100

print("=" * 90)
print("SIMULACIÓN MONTE CARLO Y ANÁLISIS DE SENSIBILIDAD DEL TCO (10 000 ITERACIONES)")
print("EPS AGUAS DEL SUR S.A. — MARGEN DE CONFIANZA FINANCIERA BAJO VAL IT / COBIT 2019")
print("=" * 90)
print(f"TCO Base Determinístico del Portafolio : S/ {tco_base_total:,.2f}")
print(f"TCO Medio Simulado (Valor Esperado)     : S/ {media_tco:,.2f}")
print(f"Desviación Estándar del Portafolio     : S/ {desv_tco:,.2f}")
print(f"Coeficiente de Variación (CV)          : {(desv_tco / media_tco)*100:.2f} %")
print(f"Probabilidad de Superar Presupuesto Base: {prob_superar_base:.1f} %")

print("\n--- DISTRIBUCIÓN POR PERCENTILES DEL COMPROMISO QUINQUENAL ---")
print(f"  P05 (Escenario Altamente Optimista)   : S/ {p05:,.2f} ({(p05 - tco_base_total)/tco_base_total*100:+.1f} %)")
print(f"  P10 (Escenario Optimista)             : S/ {p10:,.2f} ({(p10 - tco_base_total)/tco_base_total*100:+.1f} %)")
print(f"  P50 (Mediana / Escenario Central)     : S/ {p50:,.2f} ({(p50 - tco_base_total)/tco_base_total*100:+.1f} %)")
print(f"  P75 (Escenario Conservador)           : S/ {p75:,.2f} ({(p75 - tco_base_total)/tco_base_total*100:+.1f} %)")
print(f"  P90 (Techo de Autorización / 90% Conf): S/ {p90:,.2f} ({(p90 - tco_base_total)/tco_base_total*100:+.1f} %)")
print(f"  P95 (Valor en Riesgo - VaR 95%)       : S/ {p95:,.2f} ({(p95 - tco_base_total)/tco_base_total*100:+.1f} %)")
print(f"  P99 (Escenario de Estrés Máximo)      : S/ {p99:,.2f} ({(p99 - tco_base_total)/tco_base_total*100:+.1f} %)")

print("\n--- RECOMENDACIÓN DE GOBERNANZA PRESUPUESTAL (RESERVA DE CONTINGENCIA) ---")
print(f"Reserva de Contingencia Financiera sugerida (P90 - Base): S/ {reserva_contingencia_p90:,.2f}")
print(f"Porcentaje de amortiguamiento presupuestal requerido     : {pct_reserva_p90:.2f} % del TCO base")
print("→ Dictamen Financiero: Para blindar al Directorio ante desvíos históricos (+47.5%),")
print(f"  se recomienda aprobar un techo quinquenal de S/ {p90:,.0f} con una reserva blindada de S/ {reserva_contingencia_p90:,.0f}.")

# Análisis de sensibilidad de Tornado (Varianza aportada por cada proyecto)
# En distribución triangular simétrica: Var = (b - a)^2 / 24
varianzas_proyectos = np.var(simulaciones_proyectos, axis=1)
total_var = np.sum(varianzas_proyectos)
df_merged["varianza"] = varianzas_proyectos
df_merged["contribucion_riesgo_pct"] = (df_merged["varianza"] / total_var) * 100
df_tornado = df_merged.sort_values("contribucion_riesgo_pct", ascending=False)

print("\n--- TOP PROYECTOS GENERADORES DE RIESGO FINANCIERO (ANÁLISIS DE TORNADO) ---")
print(df_tornado[["codigo", "nombre", "tco_5", "incertidumbre", "contribucion_riesgo_pct"]].to_string(index=False))

top2_riesgo = df_tornado.iloc[:2]["contribucion_riesgo_pct"].sum()
print(f"\n→ Concentración de volatilidad: {df_tornado.iloc[0]['codigo']} y {df_tornado.iloc[1]['codigo']} explican el {top2_riesgo:.1f} %")
print("  de todo el riesgo presupuestal del portafolio quinquenal.")

# Guardar métricas en CSV
df_tornado.to_csv("PF09_sensibilidad_proyectos.csv", index=False)

# Generación de figura gráfica
out_dir = "../graficos" if os.path.exists("../graficos") else "graficos"
os.makedirs(out_dir, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Panel 1: Histograma de Monte Carlo
counts, bins, patches = ax1.hist(tco_simulado_total / 1000, bins=50, color="#0284C7", edgecolor="#0369A1", alpha=0.75, density=True)
ax1.axvline(tco_base_total / 1000, color="#0F172A", linestyle="-", linewidth=2, label=f"TCO Base: S/ {tco_base_total/1000:,.0f}k")
ax1.axvline(p50 / 1000, color="#2563EB", linestyle="--", linewidth=1.5, label=f"Mediana (P50): S/ {p50/1000:,.0f}k")
ax1.axvline(p90 / 1000, color="#DC2626", linestyle="-.", linewidth=2, label=f"Techo P90: S/ {p90/1000:,.0f}k (+{pct_reserva_p90:.1f}%)")
ax1.axvspan(tco_base_total / 1000, p90 / 1000, color="#FCA5A5", alpha=0.3, label=f"Reserva Contingencia: S/ {reserva_contingencia_p90/1000:,.0f}k")

ax1.set_title("Distribución Probabilística del TCO a 5 Años\n(Simulación Monte Carlo — 10 000 iteraciones)", fontsize=11, fontweight="bold")
ax1.set_xlabel("TCO Total Quinquenal (Miles de Soles - S/ k)", fontsize=10)
ax1.set_ylabel("Densidad de Probabilidad", fontsize=10)
ax1.legend(loc="upper right", fontsize=8.5)
ax1.grid(axis="x", linestyle=":", alpha=0.6)

# Panel 2: Diagrama de Tornado (Top 8 proyectos más volátiles)
top8_tornado = df_tornado.head(8).sort_values("contribucion_riesgo_pct", ascending=True)
y_pos = np.arange(len(top8_tornado))

# Desviación respecto a la base (min y max)
deltas_min = (top8_tornado["tco_min"] - top8_tornado["tco_5"]) / 1000
deltas_max = (top8_tornado["tco_max"] - top8_tornado["tco_5"]) / 1000

ax2.barh(y_pos, deltas_min, color="#10B981", height=0.55, label="Oscilación Mínima (- Margen)")
ax2.barh(y_pos, deltas_max, color="#EF4444", height=0.55, label="Oscilación Máxima (+ Margen)")
ax2.axvline(0, color="black", linewidth=1)

labels_tornado = [f"{c}: {n[:22]} ({pct:.1f}% riesgo)" for c, n, pct in zip(top8_tornado["codigo"], top8_tornado["nombre"], top8_tornado["contribucion_riesgo_pct"])]
ax2.set_yticks(y_pos)
ax2.set_yticklabels(labels_tornado, fontsize=8.5)
ax2.set_xlabel("Desviación del TCO respecto al valor base (S/ k)", fontsize=10)
ax2.set_title("Diagrama de Tornado: Sensibilidad de Proyectos al Riesgo\n(Aporte individual a la varianza total del portafolio)", fontsize=11, fontweight="bold")
ax2.legend(loc="lower right", fontsize=8.5)
ax2.grid(axis="x", linestyle="--", alpha=0.4)

plt.suptitle("Evaluación Cuantitativa de Riesgo Financiero e Incertidumbre del Portafolio PETI\n(EPS AGUAS DEL SUR S.A. — Metodología Val IT / COBIT APO05)", 
             fontsize=12.5, fontweight="bold", y=0.98)
plt.tight_layout()
graph_path = os.path.join(out_dir, "PF_sensibilidad_montecarlo.png")
plt.savefig(graph_path, dpi=160)
plt.close()
print(f"\n✔ Gráfico {graph_path} generado exitosamente.")
print("✔ Archivo PF09_sensibilidad_proyectos.csv exportado con éxito.")
