# 07_portafolio/PF08_roadmap_ejecucion.py
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Definición del cronograma de despliegue según orden topológico y duración
# Proyecto, inicio_mes, duracion_meses, categoria
CRONO = [
    ("PR-01: Gobierno Dato Maestro", 0, 6, "Transformar"),
    ("PR-03: Capa Integración APIs", 0, 8, "Transformar"),
    ("PR-08: Mesa de Servicio TI", 0, 4, "Operar"),
    ("PR-02: Registro Actividades", 1, 3, "Operar"),
    ("PR-11: Cumplimiento LPDP", 2, 2, "Operar"),
    ("PR-10: Renovación ERP", 3, 5, "Operar"),
    ("PR-12: Gestión Conocimiento", 4, 3, "Operar"),
    ("PR-13: Comité Gobierno TI", 1, 4, "Operar"),
    ("PR-15: Autoservicio Personal", 5, 4, "Crecer"),
    ("PR-06: Rutas Cuadrillas", 6, 4, "Crecer"),
    ("PR-04: Canal Digital Recaud.", 8, 9, "Crecer"),
    ("PR-05: Reclamos Autoserv.", 8, 5, "Crecer"),
    ("PR-07: Tablero Comercial", 8, 3, "Crecer"),
    ("PR-09: Respaldo Inmutable", 8, 12, "Operar"),
    ("PR-14: Monitoreo Enlaces", 4, 3, "Operar"),
]

fig, ax = plt.subplots(figsize=(13, 7.5))
COL = {"Operar":"#1E3A8A","Crecer":"#0284C7","Transformar":"#D97706"}

y_positions = np.arange(len(CRONO))
for i, (nombre, inicio, dur, cat) in enumerate(reversed(CRONO)):
    bar = ax.barh(i, dur, left=inicio, color=COL[cat], edgecolor='#334155', height=0.6, alpha=0.9)
    ax.text(inicio + dur/2, i, f"{dur}m", va='center', ha='center', color='white', fontweight='bold', fontsize=8.5)

ax.set_yticks(y_positions)
ax.set_yticklabels([n.split(":")[0] + " - " + n.split(":")[1][:24] for n, _, _, _ in reversed(CRONO)], fontsize=9.5)
ax.set_xlabel("Meses de Ejecución (Quinquenio 2026–2030)", fontsize=11, labelpad=8)
ax.set_title("Secuencia Estratégica y Hoja de Ruta (Roadmap) del Portafolio de Proyectos\n(EPS AGUAS DEL SUR S.A. — Fase 1 Habilitadores, Fase 2 Dependientes, Fase 3 Expansión)", 
             fontsize=12.5, fontweight='bold', pad=15)

# Marcar hitos anuales
for mes in [12, 24]:
    ax.axvline(mes, color='#DC2626', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.text(mes + 0.3, len(CRONO) - 0.7, f"Año {mes//12}", color='#DC2626', fontweight='bold', fontsize=9.5)

# Leyenda
plt.plot([], [], 's', color=COL["Transformar"], label="Transformar (Habilitadores arquitecturales)", markersize=10)
plt.plot([], [], 's', color=COL["Crecer"], label="Crecer (Digitalización y analítica)", markersize=10)
plt.plot([], [], 's', color=COL["Operar"], label="Operar (Continuidad, mesa de ayuda y normativa)", markersize=10)
plt.legend(loc='lower right', frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=9.5)

ax.set_xlim(-0.5, 25)
ax.grid(axis='x', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig("../graficos/PF_roadmap_ejecucion.png", dpi=160)
plt.close()
print("✔ Gráfico ../graficos/PF_roadmap_ejecucion.png generado.")
