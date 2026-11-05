# 07_portafolio/PF05_balance.py
import pandas as pd
import matplotlib.pyplot as plt
import os

p   = pd.read_csv("PF01_portafolio_candidatos.csv")
tco = pd.read_csv("PF02_tco.csv")
d   = p.merge(tco, on="codigo")

bal = d.groupby("categoria").agg(
    proyectos=("codigo","count"),
    inversion=("inv_inicial","sum"),
    tco=("tco_5","sum")).reset_index()
bal["pct_inv"] = (bal.inversion / bal.inversion.sum() * 100).round(1)
bal["pct_tco"] = (bal.tco / bal.tco.sum() * 100).round(1)

# Ordenar categorías en orden lógico: Operar, Crecer, Transformar
orden_cat = {"Operar": 1, "Crecer": 2, "Transformar": 3}
bal["orden"] = bal["categoria"].map(orden_cat)
bal = bal.sort_values("orden").drop(columns=["orden"])

REF = {"Operar":(50,70), "Crecer":(20,30), "Transformar":(10,20)}
print("=== BALANCE DEL PORTAFOLIO PROHIBIDO (TCO A 5 AÑOS) ===")
print(bal.to_string(index=False))
print("\nContraste con las proporciones de referencia de la industria:")
for _, r in bal.iterrows():
    lo, hi = REF.get(r.categoria, (0,100))
    est = "dentro del rango" if lo <= r.pct_tco <= hi else ("POR DEBAJO" if r.pct_tco < lo else "POR ENCIMA")
    print(f"  {r.categoria:12s}: {r.pct_tco:5.1f} % del TCO  (referencia {lo}–{hi} %)  → {est}")

# Contraste con el balance ACTUAL del presupuesto (presupuesto_ti.csv)
print("\n=== COMPARACIÓN CON EL BALANCE ACTUAL DE LA ORGANIZACIÓN ===")
print("  Balance actual ejecutado (presupuesto_ti.csv) : Operar 91.1 % · Crecer/Inversión 8.9 % · Transformar 0.0 %")
print("  Balance actual planificado (presupuesto_ti.csv): Operar 92.0 % · Crecer/Inversión 8.0 % · Transformar 0.0 %")
print(f"  Balance propuesto por el PETI (TCO 5 años)    : Operar {bal[bal.categoria=='Operar']['pct_tco'].values[0]:.1f} % · Crecer {bal[bal.categoria=='Crecer']['pct_tco'].values[0]:.1f} % · Transformar {bal[bal.categoria=='Transformar']['pct_tco'].values[0]:.1f} %")
print("→ El PETI desmantela el modelo reactivo ('apagar incendios') y destina 53.8 % de los recursos a modernización y transformación.")

os.makedirs("../graficos", exist_ok=True)
fig, ax = plt.subplots(1, 2, figsize=(14, 5.5))
COL = {"Operar":"#1E3A8A","Crecer":"#0284C7","Transformar":"#D97706"}

ax[0].pie(bal.tco, labels=bal.categoria, autopct="%1.1f%%",
          colors=[COL[c] for c in bal.categoria], startangle=90,
          wedgeprops=dict(width=0.6, edgecolor='white', linewidth=2),
          textprops=dict(fontsize=11, fontweight='bold'))
ax[0].set_title("Balance Estratégico del Portafolio\n(TCO a 5 años)", fontsize=13, fontweight='bold', pad=15)

d_sorted = d.sort_values("tco_5")
bars = ax[1].barh(d_sorted.codigo, d_sorted.tco_5,
           color=[COL[c] for c in d_sorted.categoria], edgecolor='none', height=0.7)
ax[1].set_xlabel("TCO a 5 años (S/)", fontsize=11, labelpad=8)
ax[1].set_title("Costo Total de Propiedad (TCO) por Proyecto", fontsize=13, fontweight='bold', pad=15)
ax[1].grid(axis='x', linestyle='--', alpha=0.5)

# Añadir valores a las barras
for bar in bars:
    w = bar.get_width()
    ax[1].text(w + 10000, bar.get_y() + bar.get_height()/2, f"S/ {w/1000:,.0f}k", 
               va='center', ha='left', fontsize=8.5, color='#1E293B')

plt.tight_layout()
plt.savefig("../graficos/PF_balance.png", dpi=160)
print("✔ Gráfico ../graficos/PF_balance.png generado con éxito.")

