# 07_portafolio/PF07_graficos_complementarios.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("../graficos", exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# 1. GRAFICO: COMPONENTES DEL TCO (COSTO UNICO VS OPERATIVO A 5 AÑOS)
tco = pd.read_csv("PF02_tco.csv")
cand = pd.read_csv("PF01_portafolio_candidatos.csv")
df_tco = tco.merge(cand, on="codigo").sort_values("tco_5", ascending=True)

fig, ax = plt.subplots(figsize=(12, 7))
y_pos = np.arange(len(df_tco))
p_unico = ax.barh(y_pos, df_tco["costo_unico"], color="#3B82F6", label="Costo Único (Capex + Cap + Mig + Int)", height=0.65)
p_operativo = ax.barh(y_pos, df_tco["costo_anual"] * 5, left=df_tco["costo_unico"], color="#1E293B", label="Costo Operativo a 5 años (Opex recurrente)", height=0.65)

ax.set_yticks(y_pos)
ax.set_yticklabels([f"{c} - {n[:28]}" for c, n in zip(df_tco["codigo"], df_tco["nombre"])], fontsize=9)
ax.set_xlabel("Soles (S/)", fontsize=11, labelpad=8)
ax.set_title("Estructura del TCO a 5 Años: Capex Único vs. Compromiso Operativo Recurrente\n(Factor multiplicador global: 5.17×)", fontsize=13, fontweight='bold', pad=15)
ax.legend(loc="lower right", frameon=True, fontsize=10)
ax.grid(axis='x', linestyle='--', alpha=0.5)

for i, total in enumerate(df_tco["tco_5"]):
    pct = df_tco["pct_operativo"].iloc[i]
    ax.text(total + 12000, i, f"S/ {total/1000:,.0f}k ({pct:.0f}% Opex)", va='center', fontsize=8.5, fontweight='bold', color='#0F172A')

plt.tight_layout()
plt.savefig("../graficos/PF_tco_componentes.png", dpi=160)
plt.close()
print("✔ Gráfico ../graficos/PF_tco_componentes.png generado.")

# 2. GRAFICO: EVALUACION DE ALTERNATIVAS Y COSTO DE LA INACCION
alt = pd.read_csv("PF04_alternativas.csv")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

# PR-09
alt_pr09 = alt[alt["proyecto"] == "PR-09"].copy()
labels_09 = ["A. Inacción", "B. Migrar Prov.", "C. Reemplazo Nube"]
x = np.arange(len(labels_09))
w = 0.35

ax1.bar(x - w/2, alt_pr09["costo_5"], width=w, label="Costo a 5 años", color="#EF4444")
ax1.bar(x + w/2, alt_pr09["beneficio_5"], width=w, label="Beneficio a 5 años", color="#10B981")
ax1.axhline(0, color='black', linewidth=0.8)
ax1.set_xticks(x)
ax1.set_xticklabels(labels_09, fontsize=9.5, fontweight='bold')
ax1.set_title("PR-09: Respaldo y Continuidad\n(Costo Inacción: -S/ 900k | Opción C: Mayor beneficio)", fontsize=11, fontweight='bold')
ax1.set_ylabel("Soles (S/)", fontsize=10)
ax1.legend(loc="upper left")
ax1.grid(axis='y', linestyle='--', alpha=0.4)

# PR-04
alt_pr04 = alt[alt["proyecto"] == "PR-04"].copy()
labels_04 = ["A. Inacción", "B. Rediseño API", "C. Paquete B2B"]
x2 = np.arange(len(labels_04))

ax2.bar(x2 - w/2, alt_pr04["costo_5"], width=w, label="Costo a 5 años", color="#EF4444")
ax2.bar(x2 + w/2, alt_pr04["beneficio_5"], width=w, label="Beneficio a 5 años", color="#10B981")
ax2.axhline(0, color='black', linewidth=0.8)
ax2.set_xticks(x2)
ax2.set_xticklabels(labels_04, fontsize=9.5, fontweight='bold')
ax2.set_title("PR-04: Canal Digital y Recaudación\n(Opción B: Mayor retorno neto +S/ 345k, ROI +90.8%)", fontsize=11, fontweight='bold')
ax2.set_ylabel("Soles (S/)", fontsize=10)
ax2.legend(loc="upper left")
ax2.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig("../graficos/PF_alternativas_analisis.png", dpi=160)
plt.close()
print("✔ Gráfico ../graficos/PF_alternativas_analisis.png generado.")

# 3. GRAFICO: INVERSIONES HISTORICAS CERRADAS Y DESVIACIONES
inv = pd.read_csv("../Recursos/inversiones_cerradas.csv")
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(inv))
w = 0.35

b1 = ax.bar(x - w/2, inv["presupuesto"], width=w, label="Presupuesto Aprobado", color="#94A3B8")
b2 = ax.bar(x + w/2, inv["ejecutado"], width=w, label="Costo Real Ejecutado", color="#DC2626")

ax.set_xticks(x)
ax.set_xticklabels([f"{id_}\n{nom}\n({med})" for id_, nom, med in zip(inv["id"], inv["nombre"], inv["beneficio_medido"])], fontsize=9.5, fontweight='bold')
ax.set_ylabel("Soles (S/)", fontsize=11)
ax.set_title("Desviación Presupuestal Severa en Inversiones Históricas Cerradas (EPS Aguas del Sur)\nSobrecosto medio de +47.5% sin medición formal de beneficios (Línea Base Val IT / COBIT)", fontsize=12, fontweight='bold', pad=15)
ax.legend(loc="upper right", frameon=True)
ax.grid(axis='y', linestyle='--', alpha=0.4)

for i in range(len(inv)):
    dif_pct = ((inv["ejecutado"].iloc[i] - inv["presupuesto"].iloc[i]) / inv["presupuesto"].iloc[i]) * 100
    dif_monto = inv["ejecutado"].iloc[i] - inv["presupuesto"].iloc[i]
    ax.text(x[i] + w/2, inv["ejecutado"].iloc[i] + 12000, f"+{dif_pct:.1f}%\n(+S/ {dif_monto/1000:,.0f}k)", ha='center', fontsize=9, fontweight='bold', color='#DC2626')

plt.tight_layout()
plt.savefig("../graficos/PF_inversiones_historicas.png", dpi=160)
plt.close()
print("✔ Gráfico ../graficos/PF_inversiones_historicas.png generado.")

# 4. GRAFICO: COMPARACION DE BALANCE ACTUAL VS PROPUESTO
presup = pd.read_csv("../Recursos/presupuesto_ti.csv")
cat_actual = {"Operar": presup[presup["tipo"]=="Operación"]["ejecutado"].sum(),
              "Crecer": presup[presup["tipo"]=="Inversión"]["ejecutado"].sum(),
              "Transformar": 0.0}
tot_act = sum(cat_actual.values())
pct_act = [cat_actual["Operar"]/tot_act * 100, cat_actual["Crecer"]/tot_act * 100, 0.0]

# Propuesto TCO
p_prop = [46.2, 30.3, 23.5]
ref_min = [50, 20, 10]
ref_max = [70, 30, 20]

fig, ax = plt.subplots(figsize=(10, 5.5))
cats = ["Operar (Mantener el negocio)", "Crecer (Mejorar y expandir)", "Transformar (Nuevas capacidades)"]
x = np.arange(len(cats))
w = 0.35

ax.bar(x - w/2, pct_act, width=w, label="Balance Actual Ejecutado (presupuesto_ti.csv)", color="#EF4444")
ax.bar(x + w/2, p_prop, width=w, label="Balance Propuesto PETI (TCO 5 años)", color="#2563EB")

# Franjas de referencia
for i in range(len(cats)):
    ax.plot([x[i] - 0.4, x[i] + 0.4], [ref_min[i], ref_min[i]], color="#059669", linestyle=":", linewidth=1.5)
    ax.plot([x[i] - 0.4, x[i] + 0.4], [ref_max[i], ref_max[i]], color="#059669", linestyle=":", linewidth=1.5)
    ax.fill_between([x[i] - 0.4, x[i] + 0.4], ref_min[i], ref_max[i], color="#10B981", alpha=0.1)

ax.set_xticks(x)
ax.set_xticklabels(cats, fontsize=10, fontweight='bold')
ax.set_ylabel("% del Gasto Total de TI", fontsize=11)
ax.set_title("Cambio Estructural de Balance: Situación Actual Reactiva vs. Portafolio PETI\n(Áreas sombreadas en verde = Rangos de referencia de la industria)", fontsize=12, fontweight='bold', pad=15)
ax.legend(loc="upper right", frameon=True)
ax.grid(axis='y', linestyle='--', alpha=0.4)

for i in range(len(cats)):
    ax.text(x[i] - w/2, pct_act[i] + 1.5, f"{pct_act[i]:.1f}%", ha='center', fontsize=9.5, fontweight='bold', color='#B91C1C')
    ax.text(x[i] + w/2, p_prop[i] + 1.5, f"{p_prop[i]:.1f}%", ha='center', fontsize=9.5, fontweight='bold', color='#1D4ED8')

plt.tight_layout()
plt.savefig("../graficos/PF_presupuesto_balance.png", dpi=160)
plt.close()
print("✔ Gráfico ../graficos/PF_presupuesto_balance.png generado.")

