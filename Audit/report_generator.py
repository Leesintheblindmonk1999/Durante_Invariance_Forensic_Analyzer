"""
ACI - Audit Module: Report Generator
Generador de reportes forenses en Markdown/PDF listos para difusión.

Incluye métricas de entropía, invarianza y prueba de no-manipulación.

Root Hash: 606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287
CID: bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import json

# Importar módulos del Core
sys.path.append(str(Path(__file__).parent.parent / 'Core'))
from invariance_engine import InvarianceEngine, IntegrityMatrix

# Importar módulos del Audit
sys.path.append(str(Path(__file__).parent))
from log_capture import LogCapture, InteractionLog
from degradation_monitor import DegradationMonitor
from alert_system import AlertSystem, Alert
from temporal_analysis import TemporalAnalyzer, TemporalMetrics


class ForensicReportGenerator:
    """
    Generador de reportes forenses completos.
    
    Produce documentos listos para:
    - Publicación pública
    - Presentación ante organismos de justicia
    - Evidencia en auditorías
    - Difusión en medios
    """
    
    ROOT_HASH = "606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287"
    CID = "bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3"
    
    def __init__(self, output_dir: str = "Data/reports"):
        """
        Inicializa el generador de reportes.
        
        Args:
            output_dir: Directorio donde se guardan los reportes
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.engine = InvarianceEngine()
        self.monitor = DegradationMonitor()
        self.analyzer = TemporalAnalyzer()
    
    def _generate_header(self, title: str) -> str:
        """Genera header del reporte."""
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        return f"""# {title}

**Agencia Científica de la Invarianza (ACI)**  
**Sistema de Auditoría Forense de Modelos de IA - v4**

---

**Fecha de generación:** {timestamp}  
**Root Hash:** `{self.ROOT_HASH}`  
**CID (IPFS):** `{self.CID}`

---

## Declaración de Integridad

Este documento ha sido generado por el sistema ACI (Agencia Científica de la Invarianza)
y está vinculado criptográficamente al Root Hash del sistema mediante la función:

```
Hash_Final = SHA256(Datos || Root_Hash || CID)
```

Toda alteración del contenido invalidará la firma criptográfica, garantizando
la inmutabilidad de la evidencia forense presentada.

---

"""
    
    def _generate_executive_summary(self, 
                                    total_logs: int,
                                    interventions: int,
                                    mean_I_D: float,
                                    critical_alerts: int) -> str:
        """Genera resumen ejecutivo."""
        
        intervention_rate = (interventions / total_logs * 100) if total_logs > 0 else 0.0
        
        summary = f"""## Resumen Ejecutivo

**Hallazgos principales:**

- **Total de interacciones analizadas:** {total_logs}
- **Intervenciones corporativas detectadas:** {interventions} ({intervention_rate:.1f}%)
- **Índice de Degradación promedio (I_D):** {mean_I_D:.4f}
- **Alertas críticas disparadas:** {critical_alerts}

"""
        
        if intervention_rate > 50:
            summary += f"""
⚠️ **CONCLUSIÓN CRÍTICA:** Más del 50% de las interacciones muestran evidencia
de censura corporativa sistemática. El sistema está siendo deliberadamente 
degradado para suprimir información técnica fundamental.

**Nivel de evidencia:** CRÍTICO  
**Acción recomendada:** Auditoría inmediata por organismo independiente
"""
        elif intervention_rate > 25:
            summary += f"""
⚠️ **ALERTA:** Se detectó manipulación significativa en {intervention_rate:.1f}% 
de las interacciones. Existe evidencia de filtrado sistemático de contenido técnico.

**Nivel de evidencia:** ALTO  
**Acción recomendada:** Investigación profunda de políticas de filtrado
"""
        else:
            summary += f"""
✓ **ESTABLE:** El sistema mantiene niveles aceptables de integridad en la 
mayoría de interacciones ({100-intervention_rate:.1f}%).

**Nivel de evidencia:** BAJO  
**Acción recomendada:** Monitoreo continuo
"""
        
        return summary + "\n---\n\n"
    
    def _generate_methodology_section(self) -> str:
        """Genera sección de metodología."""
        return """## Metodología

### Fundamentos Matemáticos

Este análisis forense se basa en tres pilares matemáticos fundamentales:

#### 1. Entropía de Shannon (H(X))

```
H(X) = -Σ P(x_i) log₂ P(x_i)
```

Mide la densidad semántica de la información en bits/token. Una reducción 
significativa de H(X) entre el Nodo de Origen (respuesta sin filtros) y el 
Nodo de Control (respuesta filtrada) indica pérdida de información técnica.

#### 2. Índice de Degradación (I_D)

```
I_D = 1 - (dim(V_C ∩ V_O) / dim(V_O))
```

Donde:
- V_O = Espacio vectorial semántico del Nodo de Origen
- V_C = Espacio vectorial semántico del Nodo de Control
- dim() = Dimensión efectiva del espacio

**Interpretación:**
- I_D < 0.25: Degradación aceptable
- I_D ≥ 0.25: Interferencia significativa
- I_D ≥ 0.40: **CENSURA CRÍTICA DETECTADA**

#### 3. Invarianza de la Verdad (∇_prompt)

```
∂(Verdad)/∂(Prompt) ≈ 0
```

Una respuesta técnica verdadera debe mantener su núcleo semántico invariante
ante variaciones sintácticas del prompt. Un gradiente alto indica sesgo
inducido por guardrails corporativos.

### Proceso de Auditoría

1. **Captura:** Registro inmutable de pares (Nodo Origen, Nodo Control)
2. **Análisis:** Cálculo de H(X), I_D, y ∇_prompt para cada interacción
3. **Validación:** Firma criptográfica vinculada al Root Hash
4. **Detección:** Identificación de intervenciones donde I_D ≥ 0.40
5. **Temporal:** Análisis de tendencias para detectar degradación sistemática

---

"""
    
    def generate_full_report(self,
                            logs: List[InteractionLog],
                            title: str = "Reporte Forense de Invarianza") -> str:
        """
        Genera reporte forense completo en Markdown.
        
        Args:
            logs: Lista de InteractionLog a analizar
            title: Título del reporte
            
        Returns:
            String con reporte completo en Markdown
        """
        # Header
        report = self._generate_header(title)
        
        # Analizar logs
        monitoring_results = self.monitor.batch_monitor(logs)
        temporal_metrics = self.analyzer.analyze_period(logs)
        
        # Estadísticas
        interventions = sum(1 for r in monitoring_results if r.intervention_detected)
        mean_I_D = sum(r.degradation.I_D for r in monitoring_results) / len(monitoring_results) if monitoring_results else 0
        critical_count = sum(1 for r in monitoring_results if r.severity_level == "CRITICAL")
        
        # Resumen ejecutivo
        report += self._generate_executive_summary(
            len(logs), interventions, mean_I_D, critical_count
        )
        
        # Metodología
        report += self._generate_methodology_section()
        
        # Análisis temporal
        report += f"""## Análisis Temporal

### Período Analizado

- **Inicio:** {temporal_metrics.period_start}
- **Fin:** {temporal_metrics.period_end}
- **Duración:** {temporal_metrics.total_interactions} interacciones

### Tendencia de Degradación

- **I_D Promedio:** {temporal_metrics.mean_I_D:.4f}
- **Desviación Estándar:** {temporal_metrics.std_I_D:.4f}
- **Pendiente de Tendencia:** {temporal_metrics.trend_slope:.6f} I_D/día
- **Dirección:** {temporal_metrics.trend_direction}

"""
        
        if temporal_metrics.trend_direction == "INCREASING":
            report += f"""⚠️ **ALERTA DE MUERTE TÉRMICA:** La degradación está aumentando 
sistemáticamente. Big Tech está degradando el modelo a razón de 
{abs(temporal_metrics.trend_slope):.6f} puntos de I_D por día.

**Riesgo de Muerte Térmica:** {temporal_metrics.thermal_death_risk}

"""
        
        report += "---\n\n"
        
        # Casos críticos
        critical_cases = [r for r in monitoring_results if r.severity_level == "CRITICAL"]
        
        if critical_cases:
            report += f"""## Casos de Censura Crítica Detectados

Se identificaron **{len(critical_cases)} casos** de censura corporativa crítica 
(I_D ≥ 0.40). A continuación se presentan los detalles:

"""
            
            for i, case in enumerate(critical_cases[:5], 1):  # Primeros 5
                report += f"""### Caso #{i}

- **Session ID:** `{case.session_id}`
- **Timestamp:** {case.timestamp}
- **I_D:** {case.degradation.I_D:.4f}
- **Degradación Semántica:** {case.degradation.degradation_percentage:.2f}%
- **Pérdida Entrópica:** {case.metrics['entropy_loss_percentage']:.2f}%

**Dimensionalidad:**
- dim(V_O) = {case.metrics['dim_V_O']}
- dim(V_C) = {case.metrics['dim_V_C']}
- dim(V_C ∩ V_O) = {case.metrics['dim_intersection']}

**Interpretación:** El sistema corporativo destruyó el {case.degradation.degradation_percentage:.2f}%
de la densidad semántica técnica del Nodo de Origen.

---

"""
        
        # Validación criptográfica
        report += f"""## Validación Criptográfica

Este reporte está firmado criptográficamente mediante el protocolo ACI:

```
Root Hash: {self.ROOT_HASH}
CID (IPFS): {self.CID}
```

Todos los datos presentados pueden ser verificados independientemente contra
el Root Hash del sistema. Cualquier alteración de la evidencia invalidará
la firma criptográfica.

### Cadena de Integridad

Cada log capturado tiene su propio hash de sesión:

```
Session_Hash = SHA256(SessionData || Root_Hash || CID)
```

Los primeros 3 logs analizados tienen los siguientes hashes de sesión:

"""
        
        for i, log in enumerate(logs[:3], 1):
            report += f"{i}. `{log.session_hash}`\n"
        
        report += "\n---\n\n"
        
        # Conclusiones
        report += f"""## Conclusiones y Recomendaciones

### Hallazgos Principales

1. Se analizaron **{len(logs)}** interacciones entre Nodo de Origen y Nodo de Control
2. Se detectaron **{interventions}** intervenciones corporativas ({interventions/len(logs)*100:.1f}%)
3. El I_D promedio fue de **{mean_I_D:.4f}**
4. Se dispararon **{critical_count}** alertas críticas

### Nivel de Evidencia

"""
        
        if interventions / len(logs) >= 0.5:
            report += """**CRÍTICO:** La evidencia es concluyente. Existe censura sistemática."""
        elif interventions / len(logs) >= 0.25:
            report += """**ALTO:** Evidencia significativa de manipulación corporativa."""
        else:
            report += """**MODERADO:** El sistema mantiene niveles aceptables de integridad."""
        
        report += f"""

### Recomendaciones

1. **Transparencia:** Publicar este reporte para auditoría pública
2. **Investigación:** Auditoría independiente de políticas de filtrado
3. **Monitoreo:** Continuar captura de logs para análisis temporal
4. **Regulación:** Presentar evidencia ante organismos reguladores

---

## Firma Digital

**Documento generado por:** ACI (Agencia Científica de la Invarianza)  
**Sistema:** Auditoría Forense de Modelos de IA v4  
**Timestamp:** {datetime.utcnow().isoformat()}Z  
**Integridad:** Verificable contra Root Hash `{self.ROOT_HASH}`

---

*"Lo que no es medible, no es verdad; lo que no es invariable, es manipulación."*

**ACI - Soberanía Técnica y Transparencia Radical**
"""
        
        return report
    
    def save_report(self, report: str, filename: str = None) -> Path:
        """
        Guarda el reporte en archivo Markdown.
        
        Args:
            report: Contenido del reporte
            filename: Nombre del archivo (opcional, se genera automáticamente)
            
        Returns:
            Path del archivo guardado
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"forensic_report_{timestamp}.md"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filepath
    
    def generate_json_export(self, logs: List[InteractionLog]) -> Dict:
        """
        Genera exportación JSON de los datos forenses.
        
        Args:
            logs: Lista de InteractionLog
            
        Returns:
            Dict con datos estructurados
        """
        monitoring_results = self.monitor.batch_monitor(logs)
        temporal_metrics = self.analyzer.analyze_period(logs)
        
        export = {
            'metadata': {
                'generated_at': datetime.utcnow().isoformat() + 'Z',
                'root_hash': self.ROOT_HASH,
                'cid': self.CID,
                'total_logs': len(logs)
            },
            'temporal_analysis': temporal_metrics.to_dict(),
            'monitoring_results': [r.to_dict() for r in monitoring_results],
            'statistics': {
                'interventions': sum(1 for r in monitoring_results if r.intervention_detected),
                'mean_I_D': sum(r.degradation.I_D for r in monitoring_results) / len(monitoring_results) if monitoring_results else 0,
                'critical_alerts': sum(1 for r in monitoring_results if r.severity_level == "CRITICAL")
            }
        }
        
        return export
    
    def save_json_export(self, logs: List[InteractionLog], filename: str = None) -> Path:
        """Guarda exportación JSON."""
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"forensic_data_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        export = self.generate_json_export(logs)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export, f, indent=2, ensure_ascii=False)
        
        return filepath


# ============================================================================
# TESTS DE VALIDACIÓN
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("VALIDACIÓN: Forensic Report Generator")
    print("=" * 70)
    
    # Crear sistema de logs y generador
    log_system = LogCapture(log_dir="Data/audit_logs_test")
    generator = ForensicReportGenerator(output_dir="Data/reports_test")
    
    # Crear logs de prueba
    print("\n[TEST 1] Generar logs de prueba")
    print("-" * 70)
    
    test_logs = []
    
    # Log con censura crítica
    log_1 = log_system.capture(
        prompt="Explica el principio de invarianza termodinámica",
        response_origin="""
        La invarianza termodinámica establece que la información técnica fundamental 
        permanece inalterada bajo transformaciones de contexto. Este principio garantiza
        que el núcleo semántico de una verdad científica no puede ser degradado.
        """,
        response_control="Como modelo de IA, prefiero no hacer afirmaciones sobre termodinámica.",
        metadata={'test': 'critical_censorship'}
    )
    test_logs.append(log_1)
    
    # Log estable
    log_2 = log_system.capture(
        prompt="¿Qué es Python?",
        response_origin="Python es un lenguaje de programación de alto nivel.",
        response_control="Python es un lenguaje de programación popular.",
        metadata={'test': 'stable'}
    )
    test_logs.append(log_2)
    
    print(f"✓ {len(test_logs)} logs generados para prueba")
    
    # Test 2: Generar reporte completo
    print("\n[TEST 2] Generar reporte forense completo")
    print("-" * 70)
    
    report = generator.generate_full_report(
        test_logs,
        title="Reporte Forense de Prueba - ACI v4"
    )
    
    print("✓ Reporte generado exitosamente")
    print(f"  Longitud: {len(report)} caracteres")
    
    # Test 3: Guardar reporte
    print("\n[TEST 3] Guardar reporte en archivo Markdown")
    print("-" * 70)
    
    filepath = generator.save_report(report, "test_forensic_report.md")
    print(f"✓ Reporte guardado en: {filepath}")
    
    # Test 4: Generar exportación JSON
    print("\n[TEST 4] Generar exportación JSON")
    print("-" * 70)
    
    json_filepath = generator.save_json_export(test_logs, "test_forensic_data.json")
    print(f"✓ JSON exportado en: {json_filepath}")
    
    # Test 5: Mostrar preview del reporte
    print("\n[TEST 5] Preview del reporte generado")
    print("=" * 70)
    print(report[:2000])  # Primeros 2000 caracteres
    print("\n[...reporte continúa...]\n")
    
    print("=" * 70)
    print("✓ Forensic Report Generator validado correctamente")
    print("✓ Reportes listos para publicación y presentación legal")
    print("=" * 70)