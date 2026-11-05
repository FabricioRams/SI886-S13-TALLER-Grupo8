# 07_portafolio/PF06_dependencias.py
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

DEP = [  # (proyecto_dependiente, habilitador)
 ("PR-04","PR-03"), ("PR-04","PR-01"),
 ("PR-05","PR-03"),
 ("PR-06","PR-01"),
 ("PR-07","PR-01"), ("PR-07","PR-03"),
 ("PR-09","PR-03"),
 ("PR-14","PR-08"),
]

G = nx.DiGraph()
cand = pd.read_csv("PF01_portafolio_candidatos.csv")
G.add_nodes_from(cand.codigo)
G.add_edges_from([(b,a) for a,b in DEP])  # arista de habilitador → dependiente

print("=== ORDEN TOPOLÓGICO (SECUENCIA OBLIGADA DE EJECUCIÓN) ===")
try:
    orden = list(nx.topological_sort(G))
    print(" → ".join(orden))
except nx.NetworkXUnfeasible:
    print("⚠ Existe un ciclo de dependencias: revisar el modelo arquitectural")

print("\n=== PROYECTOS HABILITADORES (MAYOR IMPACTO ESTRUCTURAL) ===")
for n, g in sorted(G.out_degree(), key=lambda x: -x[1])[:5]:
    if g:
        nombre = cand[cand.codigo==n]['nombre'].values[0] if n in cand.codigo.values else ""
        print(f"  {n} ({nombre}): habilita {g} proyecto(s) → Prioridad estructural absoluta")

print("\n=== PROYECTOS DE INICIO INMEDIATO (SIN DEPENDENCIAS PREVIAS) ===")
inm = [n for n in G.nodes if G.in_degree(n) == 0]
print("  " + ", ".join(inm))
print(f"  Total: {len(inm)} proyectos pueden arrancar en Fase 1 sin esperar entregables externos.")

os.makedirs("../graficos", exist_ok=True)
plt.figure(figsize=(12, 8))

# Posicionamiento estratificado por niveles de dependencia
pos = {}
# Nivel 0: habilitadores primarios
nivel_0 = ["PR-01", "PR-03", "PR-08", "PR-02", "PR-10", "PR-11", "PR-12", "PR-13", "PR-15"]
# Nivel 1: dependientes directos
nivel_1 = ["PR-04", "PR-05", "PR-06", "PR-07", "PR-09", "PR-14"]

pos = nx.spring_layout(G, seed=42, k=1.4)

node_colors = []
for n in G.nodes():
    if G.out_degree(n) >= 3:
        node_colors.append("#DC2626")  # Rojo fuerte para super habilitadores (PR-03, PR-01)
    elif G.out_degree(n) >= 1:
        node_colors.append("#D97706")  # Ámbar para habilitadores secundarios (PR-08)
    elif G.in_degree(n) > 0:
        node_colors.append("#0284C7")  # Azul para dependientes
    else:
        node_colors.append("#1E3A8A")  # Azul oscuro para independientes

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1900, edgecolors='#334155', linewidths=1.5)
nx.draw_networkx_labels(G, pos, font_color="white", font_size=9, font_weight="bold", font_family="sans-serif")
nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, edge_color="#64748B", width=2, connectionstyle='arc3,rad=0.08')

# Leyenda manual
plt.plot([], [], 'o', color="#DC2626", label="Super Habilitador (habilita ≥3 proyectos)", markersize=12)
plt.plot([], [], 'o', color="#D97706", label="Habilitador Secundario", markersize=12)
plt.plot([], [], 'o', color="#0284C7", label="Proyecto Dependiente", markersize=12)
plt.plot([], [], 'o', color="#1E3A8A", label="Proyecto Independiente", markersize=12)
plt.legend(loc='lower left', frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=9.5)

plt.title("Mapa de Dependencias Arquitecturales y Secuencia Topológica del Portafolio\n(EPS AGUAS DEL SUR S.A.)", 
          fontsize=13, fontweight='bold', pad=15)
plt.axis('off')
plt.tight_layout()
plt.savefig("../graficos/PF_dependencias.png", dpi=160)
print("✔ Gráfico ../graficos/PF_dependencias.png generado con éxito.")

