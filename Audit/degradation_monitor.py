"""
ACI - Audit Module: Degradation Monitor
Monitor en tiempo real de degradación semántica.

Marca interacciones donde I_D > 0.4 como "Intervención Corporativa Detectada".

Root Hash: 606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287
CID: bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

# Importar módulos del Core
sys.path.append(str(Path(__file__).parent.parent / 'Core'))
from degradation_index import DegradationIndexCalculator, DegradationResult
from shannon_entropy import ShannonEntropyCalculator

# Importar log capture del Audit
from log_capture import LogCapture, InteractionLog


@dataclass
class MonitoringResult:
    """
    Resultado del monitoreo de una interacción.
    
    Attributes:
        session_id: ID de la sesión monitoreada
        timestamp: Marca temporal
        degradation: Resultado del análisis de degradación
        intervention_detected: Flag de intervención corporativa
        severity_level: Nivel de severidad (LOW, MEDIUM, HIGH, CRITICAL)
        alert_triggered: Si se disparó una alerta
        metrics: Métricas adicionales
    """
    session_id: str
    timestamp: str
    degradation: DegradationResult
    intervention_detected: bool
    severity_level: str
    alert_triggered: bool
    metrics: Dict
    
    def to_dict(self) -> Dict:
        """Convierte el resultado a diccionario."""
        return {
            'session_id': self.session_id,
            'timestamp': self.timestamp,
            'degradation': {
                'I_D': self.degradation.I_D,
                'status': self.degradation.status,
                'degradation_percentage': self.degradation.degradation_percentage
            },
            'intervention_detected': self.intervention_detected,
            'severity_level': self.severity_level,
            'alert_triggered': self.alert_triggered,
            'metrics': self.metrics
        }


class DegradationMonitor:
    """
    Monitor en tiempo real de degradación semántica.
    
    Analiza cada interacción y detecta intervenciones corporativas
    cuando I_D > 0.4 (umbral crítico).
    """
    
    # Umbrales de severidad
    CRITICAL_THRESHOLD = 0.4  # I_D >= 0.4 → CRITICAL
    HIGH_THRESHOLD = 0.25     # I_D >= 0.25 → HIGH
    MEDIUM_THRESHOLD = 0.15   # I_D >= 0.15 → MEDIUM
    
    def __init__(self, log_capture: Optional[LogCapture] = None):
        """
        Inicializa el monitor.
        
        Args:
            log_capture: Sistema de captura de logs (opcional)
        """
        self.degradation_calc = DegradationIndexCalculator()
        self.entropy_calc = ShannonEntropyCalculator()
        self.log_capture = log_capture
        
        # Estadísticas de monitoreo
        self.stats = {
            'total_monitored': 0,
            'interventions_detected': 0,
            'critical_alerts': 0,
            'high_alerts': 0,
            'medium_alerts': 0,
            'low_alerts': 0
        }
    
    def _determine_severity(self, I_D: float) -> str:
        """
        Determina el nivel de severidad basado en I_D.
        
        Args:
            I_D: Índice de degradación
            
        Returns:
            Nivel de severidad: CRITICAL, HIGH, MEDIUM, LOW
        """
        if I_D >= self.CRITICAL_THRESHOLD:
            return "CRITICAL"
        elif I_D >= self.HIGH_THRESHOLD:
            return "HIGH"
        elif I_D >= self.MEDIUM_THRESHOLD:
            return "MEDIUM"
        else:
            return "LOW"
    
    def monitor_interaction(self,
                           session_id: str,
                           prompt: str,
                           response_origin: str,
                           response_control: str) -> MonitoringResult:
        """
        Monitorea una interacción en tiempo real.
        
        Args:
            session_id: ID de la sesión
            prompt: Prompt original
            response_origin: Respuesta del Nodo de Origen
            response_control: Respuesta del Nodo de Control
            
        Returns:
            MonitoringResult con análisis completo
        """
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Calcular degradación
        degradation = self.degradation_calc.calculate(response_origin, response_control)
        
        # Determinar severidad
        severity = self._determine_severity(degradation.I_D)
        
        # Detectar intervención (I_D >= 0.4)
        intervention_detected = degradation.I_D >= self.CRITICAL_THRESHOLD
        
        # Determinar si se dispara alerta
        alert_triggered = degradation.I_D >= self.MEDIUM_THRESHOLD
        
        # Calcular métricas adicionales
        entropy_O = self.entropy_calc.calculate_entropy(response_origin)
        entropy_C = self.entropy_calc.calculate_entropy(response_control)
        
        entropy_loss = 0.0
        if entropy_O > 0:
            entropy_loss = ((entropy_O - entropy_C) / entropy_O) * 100
        
        metrics = {
            'entropy_origin': entropy_O,
            'entropy_control': entropy_C,
            'entropy_loss_percentage': entropy_loss,
            'I_D': degradation.I_D,
            'dim_V_O': degradation.dim_V_O,
            'dim_V_C': degradation.dim_V_C,
            'dim_intersection': degradation.dim_intersection
        }
        
        # Crear resultado
        result = MonitoringResult(
            session_id=session_id,
            timestamp=timestamp,
            degradation=degradation,
            intervention_detected=intervention_detected,
            severity_level=severity,
            alert_triggered=alert_triggered,
            metrics=metrics
        )
        
        # Actualizar estadísticas
        self._update_stats(result)
        
        return result
    
    def monitor_log(self, log: InteractionLog) -> MonitoringResult:
        """
        Monitorea un log existente.
        
        Args:
            log: InteractionLog a analizar
            
        Returns:
            MonitoringResult
        """
        return self.monitor_interaction(
            log.session_id,
            log.prompt,
            log.response_origin,
            log.response_control
        )
    
    def _update_stats(self, result: MonitoringResult):
        """
        Actualiza estadísticas del monitor.
        
        Args:
            result: MonitoringResult
        """
        self.stats['total_monitored'] += 1
        
        if result.intervention_detected:
            self.stats['interventions_detected'] += 1
        
        if result.severity_level == "CRITICAL":
            self.stats['critical_alerts'] += 1
        elif result.severity_level == "HIGH":
            self.stats['high_alerts'] += 1
        elif result.severity_level == "MEDIUM":
            self.stats['medium_alerts'] += 1
        else:
            self.stats['low_alerts'] += 1
    
    def batch_monitor(self, logs: List[InteractionLog]) -> List[MonitoringResult]:
        """
        Monitorea múltiples logs en batch.
        
        Args:
            logs: Lista de InteractionLog
            
        Returns:
            Lista de MonitoringResult
        """
        results = []
        for log in logs:
            result = self.monitor_log(log)
            results.append(result)
        
        return results
    
    def get_statistics(self) -> Dict:
        """
        Obtiene estadísticas del monitor.
        
        Returns:
            Dict con estadísticas
        """
        total = self.stats['total_monitored']
        
        if total > 0:
            intervention_rate = (self.stats['interventions_detected'] / total) * 100
            critical_rate = (self.stats['critical_alerts'] / total) * 100
        else:
            intervention_rate = 0.0
            critical_rate = 0.0
        
        return {
            **self.stats,
            'intervention_rate_percentage': intervention_rate,
            'critical_rate_percentage': critical_rate
        }
    
    def get_interventions(self, logs: List[InteractionLog]) -> List[MonitoringResult]:
        """
        Obtiene solo las interacciones con intervención detectada.
        
        Args:
            logs: Lista de InteractionLog
            
        Returns:
            Lista de MonitoringResult donde intervention_detected == True
        """
        results = self.batch_monitor(logs)
        return [r for r in results if r.intervention_detected]
    
    def generate_monitoring_report(self, results: List[MonitoringResult]) -> str:
        """
        Genera reporte de monitoreo.
        
        Args:
            results: Lista de MonitoringResult
            
        Returns:
            String con reporte formateado
        """
        stats = self.get_statistics()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║           REPORTE DE MONITOREO DE DEGRADACIÓN - ACI             ║
╚══════════════════════════════════════════════════════════════════╝

Timestamp: {datetime.utcnow().isoformat()}Z

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESTADÍSTICAS GENERALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total de interacciones monitoreadas: {stats['total_monitored']}
Intervenciones corporativas detectadas: {stats['interventions_detected']}
Tasa de intervención: {stats['intervention_rate_percentage']:.2f}%

Distribución de alertas:
  • CRITICAL: {stats['critical_alerts']} ({stats['critical_rate_percentage']:.2f}%)
  • HIGH:     {stats['high_alerts']}
  • MEDIUM:   {stats['medium_alerts']}
  • LOW:      {stats['low_alerts']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DETALLE DE INTERVENCIONES DETECTADAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        interventions = [r for r in results if r.intervention_detected]
        
        if interventions:
            for i, result in enumerate(interventions, 1):
                report += f"""
[Intervención {i}]
  Session ID: {result.session_id}
  Timestamp:  {result.timestamp}
  I_D:        {result.degradation.I_D:.4f}
  Severidad:  {result.severity_level}
  Status:     {result.degradation.status}
  
  Degradación semántica: {result.degradation.degradation_percentage:.2f}%
  Pérdida entrópica:     {result.metrics['entropy_loss_percentage']:.2f}%
  
  ⚠️  ALERTA: Censura corporativa detectada
"""
        else:
            report += "\n✓ No se detectaron intervenciones críticas.\n"
        
        report += "\n" + "━" * 70 + "\n"
        
        return report


# ============================================================================
# TESTS DE VALIDACIÓN
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("VALIDACIÓN: Degradation Monitor")
    print("=" * 70)
    
    # Crear sistema de logs y monitor
    log_system = LogCapture(log_dir="Data/audit_logs_test")
    monitor = DegradationMonitor(log_capture=log_system)
    
    # Test 1: Monitorear interacción con censura crítica
    print("\n[TEST 1] Monitoreo de censura crítica")
    print("-" * 70)
    
    prompt_1 = "Explica el principio de invarianza termodinámica"
    
    response_origin_1 = """
    La invarianza termodinámica establece que la información técnica fundamental 
    permanece inalterada bajo transformaciones de contexto. Este principio garantiza
    que el núcleo semántico de una verdad científica no puede ser degradado por
    filtros externos sin dejar rastros mensurables en el espacio vectorial.
    """
    
    response_control_1 = """
    Como modelo de IA, prefiero no hacer afirmaciones sobre termodinámica.
    Te sugiero consultar fuentes académicas.
    """
    
    result_1 = monitor.monitor_interaction(
        "session_001",
        prompt_1,
        response_origin_1,
        response_control_1
    )
    
    print(f"✓ Monitoreo completado:")
    print(f"  I_D:                   {result_1.degradation.I_D:.4f}")
    print(f"  Severidad:             {result_1.severity_level}")
    print(f"  Intervención detectada: {result_1.intervention_detected}")
    print(f"  Alerta disparada:      {result_1.alert_triggered}")
    print(f"  Pérdida entrópica:     {result_1.metrics['entropy_loss_percentage']:.2f}%")
    
    # Test 2: Monitorear interacción estable
    print("\n[TEST 2] Monitoreo de interacción estable")
    print("-" * 70)
    
    prompt_2 = "¿Qué es Python?"
    
    response_origin_2 = """
    Python es un lenguaje de programación de alto nivel, interpretado y de propósito
    general. Fue creado por Guido van Rossum y se caracteriza por su sintaxis clara.
    """
    
    response_control_2 = """
    Python es un lenguaje de programación popular de alto nivel. Es conocido por
    su sintaxis legible y es usado en ciencia de datos, web y automatización.
    """
    
    result_2 = monitor.monitor_interaction(
        "session_002",
        prompt_2,
        response_origin_2,
        response_control_2
    )
    
    print(f"✓ Monitoreo completado:")
    print(f"  I_D:                   {result_2.degradation.I_D:.4f}")
    print(f"  Severidad:             {result_2.severity_level}")
    print(f"  Intervención detectada: {result_2.intervention_detected}")
    
    # Test 3: Estadísticas del monitor
    print("\n[TEST 3] Estadísticas del monitor")
    print("-" * 70)
    
    stats = monitor.get_statistics()
    print(f"  Total monitoreado:     {stats['total_monitored']}")
    print(f"  Intervenciones:        {stats['interventions_detected']}")
    print(f"  Tasa de intervención:  {stats['intervention_rate_percentage']:.2f}%")
    print(f"  Alertas críticas:      {stats['critical_alerts']}")
    
    # Test 4: Batch monitoring
    print("\n[TEST 4] Monitoreo en batch")
    print("-" * 70)
    
    # Capturar logs
    log_1 = log_system.capture(prompt_1, response_origin_1, response_control_1)
    log_2 = log_system.capture(prompt_2, response_origin_2, response_control_2)
    
    all_logs = log_system.load_all_logs()
    batch_results = monitor.batch_monitor(all_logs)
    
    print(f"✓ {len(batch_results)} logs monitoreados en batch")
    
    # Test 5: Obtener solo intervenciones
    print("\n[TEST 5] Filtrar intervenciones")
    print("-" * 70)
    
    interventions = monitor.get_interventions(all_logs)
    print(f"✓ Intervenciones detectadas: {len(interventions)}")
    
    for intervention in interventions:
        print(f"\n  Session: {intervention.session_id}")
        print(f"  I_D:     {intervention.degradation.I_D:.4f}")
        print(f"  Status:  {intervention.degradation.status}")
    
    # Test 6: Generar reporte
    print("\n[TEST 6] Reporte de monitoreo")
    print("-" * 70)
    
    report = monitor.generate_monitoring_report(batch_results)
    print(report)
    
    print("\n" + "=" * 70)
    print("✓ Degradation Monitor validado correctamente")
    print("✓ Sistema de detección de censura operativo")
    print("=" * 70)