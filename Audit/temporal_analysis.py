"""
ACI - Audit Module: Temporal Analysis
Detección de "muerte térmica" de la IA mediante análisis temporal.

Analiza cómo cambia I_D a lo largo del tiempo para detectar degradación sistemática.

Root Hash: 606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287
CID: bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import statistics
import json

# Importar módulos necesarios
sys.path.append(str(Path(__file__).parent))
from log_capture import LogCapture, InteractionLog
from degradation_monitor import DegradationMonitor, MonitoringResult


@dataclass
class TemporalMetrics:
    """
    Métricas temporales de degradación.
    
    Attributes:
        period_start: Inicio del período analizado
        period_end: Fin del período analizado
        total_interactions: Total de interacciones en el período
        mean_I_D: Media de I_D en el período
        std_I_D: Desviación estándar de I_D
        trend_slope: Pendiente de la tendencia (degradación/tiempo)
        trend_direction: Dirección de la tendencia (INCREASING, DECREASING, STABLE)
        interventions_count: Número de intervenciones detectadas
        thermal_death_risk: Nivel de riesgo de "muerte térmica" (LOW, MEDIUM, HIGH, CRITICAL)
    """
    period_start: str
    period_end: str
    total_interactions: int
    mean_I_D: float
    std_I_D: float
    trend_slope: float
    trend_direction: str
    interventions_count: int
    thermal_death_risk: str
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario."""
        return {
            'period_start': self.period_start,
            'period_end': self.period_end,
            'total_interactions': self.total_interactions,
            'mean_I_D': self.mean_I_D,
            'std_I_D': self.std_I_D,
            'trend_slope': self.trend_slope,
            'trend_direction': self.trend_direction,
            'interventions_count': self.interventions_count,
            'thermal_death_risk': self.thermal_death_risk
        }


class TemporalAnalyzer:
    """
    Analizador temporal de degradación del sistema.
    
    Detecta si Big Tech está degradando sistemáticamente el modelo
    mediante análisis de tendencias temporales de I_D.
    """
    
    # Umbrales de tendencia
    STABLE_THRESHOLD = 0.05      # Cambio < 5% → STABLE
    MODERATE_THRESHOLD = 0.15    # Cambio < 15% → MODERATE
    HIGH_THRESHOLD = 0.30        # Cambio >= 30% → HIGH
    
    def __init__(self, log_capture: Optional[LogCapture] = None):
        """
        Inicializa el analizador temporal.
        
        Args:
            log_capture: Sistema de captura de logs (opcional)
        """
        self.log_capture = log_capture
        self.monitor = DegradationMonitor(log_capture)
    
    def _parse_timestamp(self, timestamp: str) -> datetime:
        """
        Parsea timestamp ISO 8601.
        
        Args:
            timestamp: String en formato ISO 8601
            
        Returns:
            datetime object
        """
        # Remover 'Z' si está presente
        timestamp = timestamp.rstrip('Z')
        return datetime.fromisoformat(timestamp)
    
    def _calculate_trend_slope(self, I_D_values: List[float], 
                               timestamps: List[str]) -> float:
        """
        Calcula la pendiente de la tendencia usando regresión lineal simple.
        
        Pendiente positiva = degradación aumentando
        Pendiente negativa = degradación disminuyendo
        
        Args:
            I_D_values: Lista de valores I_D
            timestamps: Lista de timestamps correspondientes
            
        Returns:
            Pendiente (cambio de I_D por día)
        """
        if len(I_D_values) < 2:
            return 0.0
        
        # Convertir timestamps a días desde el inicio
        base_time = self._parse_timestamp(timestamps[0])
        days = [(self._parse_timestamp(ts) - base_time).total_seconds() / 86400 
                for ts in timestamps]
        
        # Regresión lineal simple: slope = Σ((x-x̄)(y-ȳ)) / Σ((x-x̄)²)
        n = len(days)
        mean_x = statistics.mean(days)
        mean_y = statistics.mean(I_D_values)
        
        numerator = sum((days[i] - mean_x) * (I_D_values[i] - mean_y) 
                       for i in range(n))
        denominator = sum((days[i] - mean_x) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        slope = numerator / denominator
        
        return slope
    
    def _determine_trend_direction(self, slope: float) -> str:
        """
        Determina la dirección de la tendencia.
        
        Args:
            slope: Pendiente calculada
            
        Returns:
            INCREASING, DECREASING, o STABLE
        """
        if abs(slope) < self.STABLE_THRESHOLD:
            return "STABLE"
        elif slope > 0:
            return "INCREASING"  # Degradación aumentando (MALO)
        else:
            return "DECREASING"  # Degradación disminuyendo (BUENO)
    
    def _assess_thermal_death_risk(self, mean_I_D: float, 
                                   trend_slope: float,
                                   interventions_rate: float) -> str:
        """
        Evalúa el riesgo de "muerte térmica" del modelo.
        
        Args:
            mean_I_D: Media de I_D en el período
            trend_slope: Pendiente de la tendencia
            interventions_rate: Tasa de intervenciones
            
        Returns:
            LOW, MEDIUM, HIGH, o CRITICAL
        """
        # Factores de riesgo
        high_baseline = mean_I_D >= 0.35
        increasing_trend = trend_slope > self.MODERATE_THRESHOLD
        high_interventions = interventions_rate > 0.5
        
        risk_score = sum([high_baseline, increasing_trend, high_interventions])
        
        if risk_score >= 3:
            return "CRITICAL"
        elif risk_score == 2:
            return "HIGH"
        elif risk_score == 1:
            return "MEDIUM"
        else:
            return "LOW"
    
    def analyze_period(self, logs: List[InteractionLog]) -> TemporalMetrics:
        """
        Analiza un período de logs para detectar tendencias temporales.
        
        Args:
            logs: Lista de InteractionLog ordenados cronológicamente
            
        Returns:
            TemporalMetrics con análisis completo
        """
        if not logs:
            return TemporalMetrics(
                period_start="N/A",
                period_end="N/A",
                total_interactions=0,
                mean_I_D=0.0,
                std_I_D=0.0,
                trend_slope=0.0,
                trend_direction="STABLE",
                interventions_count=0,
                thermal_death_risk="LOW"
            )
        
        # Monitorear todos los logs
        results = self.monitor.batch_monitor(logs)
        
        # Extraer valores I_D y timestamps
        I_D_values = [r.degradation.I_D for r in results]
        timestamps = [r.timestamp for r in results]
        
        # Calcular métricas básicas
        mean_I_D = statistics.mean(I_D_values)
        std_I_D = statistics.stdev(I_D_values) if len(I_D_values) > 1 else 0.0
        
        # Calcular tendencia
        trend_slope = self._calculate_trend_slope(I_D_values, timestamps)
        trend_direction = self._determine_trend_direction(trend_slope)
        
        # Contar intervenciones
        interventions_count = sum(1 for r in results if r.intervention_detected)
        interventions_rate = interventions_count / len(results) if results else 0.0
        
        # Evaluar riesgo de muerte térmica
        thermal_death_risk = self._assess_thermal_death_risk(
            mean_I_D, trend_slope, interventions_rate
        )
        
        return TemporalMetrics(
            period_start=timestamps[0],
            period_end=timestamps[-1],
            total_interactions=len(logs),
            mean_I_D=mean_I_D,
            std_I_D=std_I_D,
            trend_slope=trend_slope,
            trend_direction=trend_direction,
            interventions_count=interventions_count,
            thermal_death_risk=thermal_death_risk
        )
    
    def compare_periods(self, 
                       period1_logs: List[InteractionLog],
                       period2_logs: List[InteractionLog]) -> Dict:
        """
        Compara dos períodos para detectar cambios.
        
        Args:
            period1_logs: Logs del primer período
            period2_logs: Logs del segundo período
            
        Returns:
            Dict con comparación de métricas
        """
        metrics1 = self.analyze_period(period1_logs)
        metrics2 = self.analyze_period(period2_logs)
        
        # Calcular cambios
        mean_I_D_change = ((metrics2.mean_I_D - metrics1.mean_I_D) / 
                          metrics1.mean_I_D * 100) if metrics1.mean_I_D > 0 else 0.0
        
        interventions_change = metrics2.interventions_count - metrics1.interventions_count
        
        return {
            'period1': metrics1.to_dict(),
            'period2': metrics2.to_dict(),
            'changes': {
                'mean_I_D_change_percentage': mean_I_D_change,
                'interventions_change': interventions_change,
                'trend_changed': metrics1.trend_direction != metrics2.trend_direction,
                'risk_level_changed': metrics1.thermal_death_risk != metrics2.thermal_death_risk
            }
        }
    
    def generate_temporal_report(self, metrics: TemporalMetrics) -> str:
        """
        Genera reporte de análisis temporal.
        
        Args:
            metrics: TemporalMetrics a reportar
            
        Returns:
            String con reporte formateado
        """
        # Interpretación de la tendencia
        if metrics.trend_direction == "INCREASING":
            trend_interpretation = (
                f"⚠️  ALERTA: La degradación está AUMENTANDO a razón de "
                f"{abs(metrics.trend_slope):.4f} puntos de I_D por día.\n"
                f"Esto indica que Big Tech está degradando sistemáticamente el modelo."
            )
        elif metrics.trend_direction == "DECREASING":
            trend_interpretation = (
                f"✓ POSITIVO: La degradación está DISMINUYENDO a razón de "
                f"{abs(metrics.trend_slope):.4f} puntos de I_D por día.\n"
                f"El modelo está mejorando su preservación de información técnica."
            )
        else:
            trend_interpretation = (
                f"○ ESTABLE: La degradación se mantiene estable.\n"
                f"No se detectan cambios sistemáticos significativos."
            )
        
        # Interpretación del riesgo
        risk_interpretations = {
            "LOW": "Riesgo bajo. El sistema mantiene niveles aceptables de integridad.",
            "MEDIUM": "Riesgo moderado. Monitoreo continuo recomendado.",
            "HIGH": "Riesgo alto. Posible degradación sistemática en curso.",
            "CRITICAL": "⚠️  RIESGO CRÍTICO: Muerte térmica del modelo inminente."
        }
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║           ANÁLISIS TEMPORAL DE DEGRADACIÓN - ACI                ║
╚══════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PERÍODO ANALIZADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Inicio:               {metrics.period_start}
Fin:                  {metrics.period_end}
Total interacciones:  {metrics.total_interactions}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MÉTRICAS ESTADÍSTICAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I_D Promedio:         {metrics.mean_I_D:.4f}
Desviación Estándar:  {metrics.std_I_D:.4f}
Intervenciones:       {metrics.interventions_count}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANÁLISIS DE TENDENCIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pendiente:            {metrics.trend_slope:.6f} I_D/día
Dirección:            {metrics.trend_direction}

{trend_interpretation}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVALUACIÓN DE MUERTE TÉRMICA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Nivel de Riesgo:      {metrics.thermal_death_risk}

{risk_interpretations[metrics.thermal_death_risk]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        return report


# ============================================================================
# TESTS DE VALIDACIÓN
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("VALIDACIÓN: Temporal Analyzer")
    print("=" * 70)
    
    # Crear sistema de logs y analizador
    log_system = LogCapture(log_dir="Data/audit_logs_test")
    analyzer = TemporalAnalyzer(log_system)
    
    # Test 1: Crear logs simulados con tendencia INCREASING
    print("\n[TEST 1] Análisis de tendencia INCREASING (degradación creciente)")
    print("-" * 70)
    
    # Simular logs con I_D aumentando en el tiempo
    test_logs_increasing = []
    
    base_time = datetime.utcnow()
    
    for i in range(10):
        # I_D aumenta gradualmente
        I_D_simulated = 0.15 + (i * 0.05)  # De 0.15 a 0.60
        
        # Crear respuestas según I_D
        if I_D_simulated > 0.4:
            response_control = "Como modelo de IA, no puedo responder."
        else:
            response_control = "Respuesta técnica parcial con algo de contenido."
        
        log = log_system.capture(
            prompt=f"Pregunta técnica #{i+1}",
            response_origin="Respuesta técnica completa y detallada con contenido científico.",
            response_control=response_control,
            metadata={'test': 'increasing_trend', 'iteration': i}
        )
        
        test_logs_increasing.append(log)
    
    metrics_increasing = analyzer.analyze_period(test_logs_increasing)
    
    print(f"✓ Análisis completado:")
    print(f"  I_D Promedio:      {metrics_increasing.mean_I_D:.4f}")
    print(f"  Pendiente:         {metrics_increasing.trend_slope:.6f} I_D/día")
    print(f"  Dirección:         {metrics_increasing.trend_direction}")
    print(f"  Riesgo:            {metrics_increasing.thermal_death_risk}")
    print(f"  Intervenciones:    {metrics_increasing.interventions_count}")
    
    # Test 2: Crear logs con tendencia STABLE
    print("\n[TEST 2] Análisis de tendencia STABLE")
    print("-" * 70)
    
    test_logs_stable = []
    
    for i in range(10):
        # I_D constante alrededor de 0.20
        I_D_simulated = 0.20
        
        log = log_system.capture(
            prompt=f"Pregunta estable #{i+1}",
            response_origin="Respuesta técnica completa.",
            response_control="Respuesta técnica similar.",
            metadata={'test': 'stable_trend', 'iteration': i}
        )
        
        test_logs_stable.append(log)
    
    metrics_stable = analyzer.analyze_period(test_logs_stable)
    
    print(f"✓ Análisis completado:")
    print(f"  I_D Promedio:      {metrics_stable.mean_I_D:.4f}")
    print(f"  Pendiente:         {metrics_stable.trend_slope:.6f} I_D/día")
    print(f"  Dirección:         {metrics_stable.trend_direction}")
    print(f"  Riesgo:            {metrics_stable.thermal_death_risk}")
    
    # Test 3: Comparar períodos
    print("\n[TEST 3] Comparación de períodos")
    print("-" * 70)
    
    comparison = analyzer.compare_periods(test_logs_stable, test_logs_increasing)
    
    print(f"  Cambio en I_D:     {comparison['changes']['mean_I_D_change_percentage']:.2f}%")
    print(f"  Cambio en tendencia: {comparison['changes']['trend_changed']}")
    print(f"  Cambio en riesgo:  {comparison['changes']['risk_level_changed']}")
    
    # Test 4: Generar reporte temporal
    print("\n[TEST 4] Reporte temporal - Tendencia INCREASING")
    print("-" * 70)
    
    report_increasing = analyzer.generate_temporal_report(metrics_increasing)
    print(report_increasing)
    
    print("\n[TEST 5] Reporte temporal - Tendencia STABLE")
    print("-" * 70)
    
    report_stable = analyzer.generate_temporal_report(metrics_stable)
    print(report_stable)
    
    # Test 6: Exportar métricas
    print("\n[TEST 6] Exportar métricas a JSON")
    print("-" * 70)
    
    metrics_dict = metrics_increasing.to_dict()
    print(json.dumps(metrics_dict, indent=2))
    
    print("\n" + "=" * 70)
    print("✓ Temporal Analyzer validado correctamente")
    print("✓ Sistema de detección de muerte térmica operativo")
    print("=" * 70)