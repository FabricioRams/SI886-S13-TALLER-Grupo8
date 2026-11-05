# run_all.py
"""
Suite de Ejecución y Validación Automatizada del Portafolio de TI (Semana 13)
SI-886 · Planeamiento Estratégico de TI · EPS AGUAS DEL SUR S.A.
Autor: Rodrigo Colque (Grupo 08)
"""

import subprocess
import os
import sys

SCRIPTS = [
    ("PF01_consolidacion.py", "salida_PF01_consolidacion.txt", "Paso A: Control de admisión y consolidación de candidatos"),
    ("PF02_tco.py", "salida_PF02_tco.txt", "Paso B: Cálculo matricial de TCO a 5 años"),
    ("PF03_auditoria_pagos.py", "salida_PF03_auditoria_pagos.txt", "Paso B (Auditoría): Análisis forense de pagos.csv y telemetría de TI"),
    ("PF04_alternativas.py", "salida_PF04_alternativas.txt", "Paso C: Evaluación de alternativas y costo de inacción (Val IT)"),
    ("PF05_balance.py", "salida_PF05_balance.txt", "Paso D: Balance estratégico Operar / Crecer / Transformar"),
    ("PF06_dependencias.py", "salida_PF06_dependencias.txt", "Paso E: Grafo acíclico y secuenciamiento topológico (NetworkX)"),
    ("PF07_graficos_complementarios.py", "salida_PF07_graficos.txt", "Generación de gráficos de TCO, alternativas e histórico"),
    ("PF08_roadmap_ejecucion.py", None, "Generación de hoja de ruta temporal (Roadmap)"),
    ("PF09_sensibilidad_montecarlo.py", "salida_PF09_sensibilidad_montecarlo.txt", "Análisis estocástico Monte Carlo y reserva de contingencia"),
    ("PF10_priorizacion_scoring.py", "salida_PF10_priorizacion.txt", "Modelo multicriterio de priorización y matriz estratégica"),
]

GRAFICOS_ESPERADOS = [
    "PF_tco_componentes.png",
    "PF_alternativas_analisis.png",
    "PF_inversiones_historicas.png",
    "PF_presupuesto_balance.png",
    "PF_balance.png",
    "PF_dependencias.png",
    "PF_roadmap_ejecucion.png",
    "PF_auditoria_pagos_ti.png",
    "PF_sensibilidad_montecarlo.png",
    "PF_matriz_priorizacion.png",
]

def main():
    print("=" * 90)
    print("EJECUTANDO SUITE INTEGRAL DE PROCESAMIENTO ANALÍTICO · PORTAFOLIO PETI S13")
    print("EPS AGUAS DEL SUR S.A. — UNIVERSIDAD PRIVADA DE TACNA")
    print("=" * 90)
    
    script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "07_portafolio")
    evidencias_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidencias", "S13", "salidas")
    graficos_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficos")
    os.makedirs(evidencias_dir, exist_ok=True)
    os.makedirs(graficos_dir, exist_ok=True)
    
    exito_total = True
    
    for script_name, salida_log, descripcion in SCRIPTS:
        script_path = os.path.join(script_dir, script_name)
        print(f"▶ Ejecutando: {script_name:<32} | {descripcion}")
        
        if not os.path.exists(script_path):
            print(f"  ❌ Error: Script no encontrado en {script_path}")
            exito_total = False
            continue
            
        res = subprocess.run([sys.executable, script_name], cwd=script_dir, capture_output=True, text=True)
        
        if res.returncode != 0:
            print(f"  ❌ Error de ejecución en {script_name}:\n{res.stderr}")
            exito_total = False
        else:
            print(f"  ✔ Ejecución exitosa.")
            if salida_log:
                log_path = os.path.join(evidencias_dir, salida_log)
                with open(log_path, "w", encoding="utf-8") as f:
                    f.write(res.stdout)
                print(f"    → Evidencia archivada en: evidencias/S13/salidas/{salida_log}")
                
    print("\n" + "=" * 90)
    print("VERIFICACIÓN DE ARTEFACTOS GRÁFICOS GENERADOS (CARPETA graficos/)")
    print("=" * 90)
    
    graficos_faltantes = 0
    for g in GRAFICOS_ESPERADOS:
        gpath = os.path.join(graficos_dir, g)
        if os.path.exists(gpath):
            size_kb = os.path.getsize(gpath) / 1024
            print(f"  ✔ {g:<35} : OK ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ {g:<35} : NO ENCONTRADO")
            graficos_faltantes += 1
            
    print("\n" + "=" * 90)
    if exito_total and graficos_faltantes == 0:
        print("✔ TODAS LAS COMPROBACIONES Y MODELOS SE EJECUTARON SATISFACTORIAMENTE (10/10).")
    else:
        print("⚠ SE DETECTARON ADVERTENCIAS O DISCREPANCIAS EN LA SUITE DE VALIDACIÓN.")
    print("=" * 90)

if __name__ == "__main__":
    main()

