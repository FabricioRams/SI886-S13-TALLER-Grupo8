# 07_portafolio/PF10_priorizacion_scoring.py
"""
Modelo Multicriterio de Priorización y Matriz Estratégica de Portafolio (Val IT / COBIT APO05)
Ponderación por Alineamiento, Urgencia de Inacción, Criticidad Arquitectural y Eficiencia TCO
Autor: Rodrigo Colque (Grupo 08 - EPS Aguas del Sur S.A.)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Cargar fuentes del portafolio
CAND_PATH = "PF01_portafolio_candidatos.csv" if os.path.exists("PF01_portafolio_candidatos.csv") else "07_portafolio/PF01_portafolio_candidatos.csv"
TCO_PATH = "PF02_tco.csv" if os.path.exists("PF02_tco.csv") else "07_portafolio/PF02_tco.csv"

df_cand = pd.read_csv(CAND_PATH)
df_tco = pd.read_csv(TCO_PATH)
df = df_cand.merge(df_tco, on="codigo")

# Criterios de Evaluación Multicriterio (Escala 0 a 100)
# 1. Alineamiento Estratégico (30%): Cobertura de objetivos estratégicos OD y relevancia
# 2. Urgencia y Mitigación de Inacción (25%): Obligaciones legales SUNASS/LPDP y costo de inacción
# 3. Criticidad Arquitectural (25%): Capacidad de habilitar otros sistemas (Centralidad en grafo)
# 4. Viabilidad y Eficiencia TCO (20%): Facilidad de despliegue y retorno de valor

CRITERIOS = {
    # codigo: [Alineamiento, Urgencia_Inaccion, Criticidad_Arquit, Eficiencia_TCO]
    "PR-01": [95, 85, 95, 80],  # Gobierno dato maestro (Super habilitador)
    "PR-02": [80, 95, 60, 90],  # Registro de actividades (Normativa directa)
    "PR-03": [95, 90, 100, 75], # Capa de integración APIs (Super habilitador máximo)
    "PR-04": [90, 95, 75, 95],  # Canal digital recaudación (Alto retorno +90.8%)
    "PR-05": [85, 80, 70, 85],  # Consulta y reclamos autoservicio
    "PR-06": [80, 75, 65, 80],  # Rutas cuadrillas y SCADA
    "PR-07": [85, 70, 60, 85],  # Tablero comercial y analítica
    "PR-08": [75, 80, 80, 85],  # Mesa de servicio TI (Habilita PR-14)
    "PR-09": [90, 100, 80, 65], # Respaldo inmutable (Evita colapso S/ 900k)
    "PR-10": [75, 75, 65, 75],  # Renovación ERP
    "PR-11": [80, 95, 55, 95],  # LPDP (Obligación legal perentoria)
    "PR-12": [70, 65, 60, 80],  # Gestión del conocimiento (CMDB)
    "PR-13": [85, 85, 70, 85],  # Comité gobierno TI
    "PR-14": [75, 70, 60, 80],  # Instrumentación monitoreo
    "PR-15": [70, 65, 55, 85],  # Autoservicio trabajadores
}

df_crit = pd.DataFrame.from_dict(CRITERIOS, orient="index", 
                                columns=["alineamiento", "urgencia_inaccion", "criticidad_arquit", "eficiencia_tco"])
df_crit.index.name = "codigo"
df = df.merge(df_crit.reset_index(), on="codigo")

# Ponderaciones
W_ALIN = 0.30
W_URG  = 0.25
W_ARQ  = 0.25
W_TCO  = 0.20

df["score_total"] = (
    df["alineamiento"] * W_ALIN +
    df["urgencia_inaccion"] * W_URG +
    df["criticidad_arquit"] * W_ARQ +
    df["eficiencia_tco"] * W_TCO
).round(1)

# Dimensiones sintéticas para matriz 2x2
df["valor_estrategico"] = ((df["alineamiento"] * 0.5 + df["urgencia_inaccion"] * 0.5)).round(1)
df["complejidad_arquitectural"] = ((df["criticidad_arquit"] * 0.6 + (100 - df["eficiencia_tco"]) * 0.4)).round(1)

def clasificar_cuadrante(row):
    if row["valor_estrategico"] >= 82 and row["complejidad_arquitectural"] >= 65:
        return "Q1: Misión Crítica (Cimientos Transformacionales)"
    elif row["valor_estrategico"] >= 82 and row["complejidad_arquitectural"] < 65:
        return "Q2: Quick Wins (Alto Impacto / Rápida Adopción)"
    elif row["valor_estrategico"] < 82 and row["complejidad_arquitectural"] >= 65:
        return "Q3: Núcleo Operativo Estructural"
    else:
        return "Q4: Mejoras Graduales de Soporte"

df["cuadrante"] = df.apply(clasificar_cuadrante, axis=1)
df = df.sort_values("score_total", ascending=False).reset_index(drop=True)
df["ranking"] = df.index + 1

print("=" * 95)
print("MODELO MULTICRITERIO DE PRIORIZACIÓN DE INVERSIONES DE TI (VAL IT / COBIT 2019 APO05)")
print("EPS AGUAS DEL SUR S.A. — RANKING DE ASIGNACIÓN DE RECURSOS Y SELECCIÓN ESTRATÉGICA")
print("=" * 95)
print(df[["ranking", "codigo", "nombre", "categoria", "score_total", "cuadrante"]].to_string(index=False))

print("\n--- DISTRIBUCIÓN POR CUADRANTES ESTRATÉGICOS ---")
for q, g in df.groupby("cuadrante"):
    print(f"\n[{q}] ({len(g)} iniciativas):")
    for _, r in g.iterrows():
        print(f"  • {r['codigo']} - {r['nombre']} (Score: {r['score_total']} | TCO: S/ {r['tco_5']:,.0f})")

# Exportar matriz a CSV
df.to_csv("PF10_priorizacion_scoring.csv", index=False)

# Generación del gráfico de matriz de cuadrantes
out_dir = "../graficos" if os.path.exists("../graficos") else "graficos"
os.makedirs(out_dir, exist_ok=True)

fig, ax = plt.subplots(figsize=(13, 8))
COL = {"Operar":"#1E3A8A", "Crecer":"#0284C7", "Transformar":"#D97706"}

# Dibujar cuadrantes
ax.axvline(65, color="#94A3B8", linestyle="--", linewidth=1.2)
ax.axhline(82, color="#94A3B8", linestyle="--", linewidth=1.2)

# Fondo de cuadrantes
ax.fill_between([40, 65], 82, 100, color="#D1FAE5", alpha=0.35)  # Q2 Verde claro (Quick Wins)
ax.fill_between([65, 85], 82, 100, color="#FEF3C7", alpha=0.35)  # Q1 Amarillo/Ámbar (Misión Crítica)
ax.fill_between([40, 65], 60, 82, color="#F1F5F9", alpha=0.35)  # Q4 Gris/Soporte
ax.fill_between([65, 85], 60, 82, color="#E0F2FE", alpha=0.35)  # Q3 Azul claro (Núcleo Operativo)

# Textos de fondo
ax.text(52.5, 98, "CUADRANTE II: QUICK WINS\n(Alto Impacto / Menor Complejidad)", ha="center", fontsize=10, fontweight="bold", color="#065F46")
ax.text(75, 98, "CUADRANTE I: MISIÓN CRÍTICA\n(Transformación Estructural)", ha="center", fontsize=10, fontweight="bold", color="#92400E")
ax.text(52.5, 62, "CUADRANTE IV: MEJORAS GRADUALES\n(Soporte y Optimización)", ha="center", fontsize=10, fontweight="bold", color="#475569")
ax.text(75, 62, "CUADRANTE III: NÚCLEO OPERATIVO\n(Infraestructura y Procesos)", ha="center", fontsize=10, fontweight="bold", color="#0369A1")

# Graficar burbujas proporcionales al TCO
for _, r in df.iterrows():
    size = (r["tco_5"] / 1000) * 2.2 + 100
    ax.scatter(r["complejidad_arquitectural"], r["valor_estrategico"], 
               s=size, color=COL[r["categoria"]], alpha=0.85, edgecolors="#0F172A", linewidth=1.5)
    # Etiqueta
    ax.text(r["complejidad_arquitectural"], r["valor_estrategico"] + 0.65, 
            f"{r['codigo']}\n(S/ {r['tco_5']/1000:,.0f}k)", 
            ha="center", va="bottom", fontsize=8, fontweight="bold", color="#0F172A")

ax.set_xlim(42, 83)
ax.set_ylim(64, 100)
ax.set_xlabel("Complejidad y Dependencia Arquitectural (Mayor demanda de integración)", fontsize=11, labelpad=8)
ax.set_ylabel("Valor Estratégico y Urgencia Normativa / Inacción (Mayor beneficio)", fontsize=11, labelpad=8)
ax.set_title("Matriz Estratégica de Portafolio: Valor vs. Complejidad Arquitectural\n(Tamaño de burbuja = Magnitud del TCO a 5 años | EPS AGUAS DEL SUR S.A.)", 
             fontsize=13, fontweight="bold", pad=15)

# Leyenda manual
plt.plot([], [], 'o', color=COL["Transformar"], label="Transformar (Habilitadores)", markersize=10)
plt.plot([], [], 'o', color=COL["Crecer"], label="Crecer (Digitalización)", markersize=10)
plt.plot([], [], 'o', color=COL["Operar"], label="Operar (Continuidad y Ley)", markersize=10)
plt.legend(loc="lower left", frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", fontsize=9.5)

ax.grid(True, linestyle=":", alpha=0.4)
plt.tight_layout()
graph_path = os.path.join(out_dir, "PF_matriz_priorizacion.png")
plt.savefig(graph_path, dpi=160)
plt.close()

print(f"\n✔ Gráfico {graph_path} generado exitosamente.")
print("✔ Archivo PF10_priorizacion_scoring.csv generado exitosamente.")

