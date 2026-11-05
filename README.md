# Planeamiento Estratégico de TI (SI-886)
## Taller de Laboratorio Semana 13 · Construcción del Portafolio de Proyectos

---

<div align="center">

### UNIVERSIDAD PRIVADA DE TACNA
**FACULTAD DE INGENIERÍA**  
**Escuela Profesional de Ingeniería de Sistemas**

**Docente:** Dr. Oscar Juan Jimenez Flores  
**Caso de Estudio:** EMPRESA 08 — **EPS AGUAS DEL SUR S.A.** *(Servicio de Agua Potable y Alcantarillado)*  
**Equipo de Trabajo:** Grupo 08 — Fabricio Farid Edmilson Ramos Atahuachi (`2023076798`)  
**Repositorio GitHub:** [https://github.com/FabricioRams/SI886-S13-TALLER-Grupo8](https://github.com/FabricioRams/SI886-S13-TALLER-Grupo8)

</div>

---

## 📌 Documentos Principales

- 📄 **[INFORME COMPLETO DEL TALLER (INFORME-TALLER-SEMANA13.md)](INFORME-TALLER-SEMANA13.md)**: Informe académico detallado con desarrollo metodológico paso a paso, tablas cuantitativas, logs de ejecución, análisis forense de inversiones históricas cerradas, gráficos analíticos y conclusiones.
- 📋 **[Sección 7.1 del PETI (07_portafolio/7.1_portafolio_proyectos.md)](07_portafolio/7.1_portafolio_proyectos.md)**: Entregable formal del Plan Estratégico de TI con los 7 acápites requeridos por la metodología institucional.

---

## 📊 Síntesis Ejecutiva del Portafolio de TI (2026–2030)

| Métrica / Dimensión | Resultado Cuantitativo | Interpretación Estratégica |
|:---|:---:|:---|
| **Proyectos Candidatos Admitidos** | **15 iniciativas** | 100% trazables a fuentes válidas y cubriendo los 6 objetivos de TI (OD-01 a OD-06). |
| **Inversión Inicial Total (Capex)** | **S/ 618 000** | Monto requerido para compras iniciales e implantación de Fase 1. |
| **Costo Total de Propiedad (TCO 5 años)** | **S/ 3 193 450** | Compromiso financiero integral del ciclo de vida quinquenal. |
| **Factor Multiplicador TCO / Inversión** | **5.17×** | Por cada S/ 1 en Capex, se comprometen S/ 4.17 en gasto recurrente. |
| **Compromiso Operativo Recurrente (Opex)** | **72.4 % del TCO** | Licencias, soporte, infraestructura y personal (S/ 462 490/año). |
| **Consistencia con Pagos Históricos** | **S/ 470 000/año real** | Validado contra 1 556 pagos informáticos por S/ 2.35M en `pagos.csv`. |
| **Balance Estratégico Propuesto** | **46.2% Op · 30.3% Cr · 23.5% Tr** | Supera el modelo reactivo actual (91.1% en Operación y 0% Transformar). |
| **Super Habilitadores Estructurales** | **PR-03 (4 salidas) y PR-01 (3 salidas)** | Prioridad de ejecución: Capa de APIs y Gobierno del Dato Maestro. |
| **Desviación Media Histórica Mitigada** | **+47.5 % (+S/ 311 868)** | Erradicada mediante salvaguardas de COBIT EDM02 y Val IT. |

---

## 📂 Estructura del Repositorio

```text
SI886-S13-TALLER-Grupo8/
│
├── 07_portafolio/                             # Módulo oficial de Portafolio de TI
│   ├── PF01_consolidacion.py                  # Script de control de admisión y mapeo OD
│   ├── PF01_portafolio_candidatos.csv         # Matriz de 15 proyectos admitidos
│   ├── PF02_tco.py                            # Modelo financiero de TCO a 5 años
│   ├── PF02_tco.csv                           # Matriz de costos únicos, Opex y TCO
│   ├── PF04_alternativas.py                   # Evaluación de alternativas bajo Val IT
│   ├── PF04_alternativas.csv                  # Flujo a 5 años, ROI y costo de inacción
│   ├── PF05_balance.py                        # Balance Operar / Crecer / Transformar
│   ├── PF06_dependencias.py                   # Grafo NetworkX y orden topológico
│   ├── PF07_graficos_complementarios.py       # Generador de gráficos analíticos adicionales
│   ├── PF08_roadmap_ejecucion.py              # Hoja de ruta y cronograma por fases
│   └── 7.1_portafolio_proyectos.md            # Documento normativo oficial del PETI
│
├── graficos/                                  # Visualizaciones de alta resolución
│   ├── PF_balance.png                         # Balance del portafolio y TCO por proyecto
│   ├── PF_dependencias.png                    # Grafo acíclico y proyectos habilitadores
│   ├── PF_tco_componentes.png                 # Capex único vs. Opex recurrente a 5 años
│   ├── PF_alternativas_analisis.png           # Comparación de alternativas y costo inacción
│   ├── PF_inversiones_historicas.png          # Desviaciones de +47.5% en inversiones pasadas
│   ├── PF_presupuesto_balance.png             # Presupuesto reactivo actual vs. portafolio PETI
│   └── PF_roadmap_ejecucion.png               # Cronograma y roadmap de ejecución
│
├── evidencias/S13/salidas/                    # Logs de ejecución reproducibles
│   ├── salida_PF01_consolidacion.txt          # Log de control de admisión y cobertura
│   ├── salida_PF02_tco.txt                    # Log de cálculo de TCO a 5 años
│   ├── salida_PF04_alternativas.txt           # Log de casos de negocio y retornos
│   ├── salida_PF05_balance.txt                # Log de balance de gasto y rangos de industria
│   ├── salida_PF06_dependencias.txt           # Log de orden topológico y nodos de salida
│   └── salida_PF07_graficos.txt               # Log de generación de figuras
│
├── Recursos/                                  # Datos de entrada institucionales
│   ├── expedientes-de-inversion.md            # Detalle forense de las 3 inversiones cerradas
│   ├── inversiones_cerradas.csv               # Historial de inversiones y desviaciones
│   ├── pagos.csv                              # 19 281 transacciones reales del periodo
│   └── presupuesto_ti.csv                     # Presupuesto institucional planificado vs ejecutado
│
├── Recursos_Codigo/                           # Códigos fuente base provistos por la cátedra
│
├── INFORME-TALLER-SEMANA13.md                 # Informe académico final del taller
├── Ejemplo-Informe.md                         # Informe de referencia (Semana 11)
└── README.md                                  # Guía del repositorio
```

---

## 🛠️ Reproducibilidad y Ejecución

Para replicar el análisis completo y regenerar los artefactos:

```bash
# 1. Clonar el repositorio
git clone https://github.com/FabricioRams/SI886-S13-TALLER-Grupo8.git
cd SI886-S13-TALLER-Grupo8/07_portafolio

# 2. Instalar dependencias
python -m pip install pandas numpy matplotlib networkx

# 3. Ejecutar los programas en secuencia
python PF01_consolidacion.py
python PF02_tco.py
python PF04_alternativas.py
python PF05_balance.py
python PF06_dependencias.py
python PF07_graficos_complementarios.py
python PF08_roadmap_ejecucion.py
```
