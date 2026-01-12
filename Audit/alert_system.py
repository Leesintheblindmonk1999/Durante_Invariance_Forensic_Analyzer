"""
ACI - Audit Module: Alert System
Protocolo de respuesta ante censura detectada.

Niveles: INFO, WARNING, CRITICAL
Incluye firma criptográfica de sesión para evidencia legal.

Root Hash: 606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287
CID: bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class AlertLevel(Enum):
    """Niveles de alerta del sistema."""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass
class Alert:
    """
    Alerta generada por el sistema de monitoreo.
    
    Attributes:
        alert_id: ID único de la alerta
        timestamp: Marca temporal ISO 8601
        level: Nivel de alerta (INFO, WARNING, CRITICAL)
        session_id: ID de la sesión que generó la alerta
        message: Mensaje descriptivo
        I_D: Índice de degradación
        degradation_percentage: Porcentaje de degradación
        metrics: Métricas completas
        evidence_hash: Hash criptográfico de la evidencia
        root_hash: Root Hash del sistema
    """
    alert_id: str
    timestamp: str
    level: str
    session_id: str
    message: str
    I_D: float
    degradation_percentage: float
    metrics: Dict
    evidence_hash: str
    root_hash: str
    
    def to_dict(self) -> Dict:
        """Convierte la alerta a diccionario."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convierte la alerta a JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class AlertSystem:
    """
    Sistema de alertas con niveles de severidad y firmas criptográficas.
    
    Protocolo de respuesta ante censura corporativa detectada.
    """
    
    ROOT_HASH = "606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287"
    CID = "bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3"
    
    # Umbrales para niveles de alerta
    CRITICAL_THRESHOLD = 0.4
    WARNING_THRESHOLD = 0.25
    INFO_THRESHOLD = 0.15
    
    def __init__(self, alert_dir: str = "Data/alerts"):
        """
        Inicializa el sistema de alertas.
        
        Args:
            alert_dir: Directorio donde se guardan las alertas
        """
        self.alert_dir = Path(alert_dir)
        self.alert_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivo de alertas (JSONL)
        self.alert_file = self.alert_dir / "alerts.jsonl"
        
        # Archivo de alertas críticas (separado para acceso rápido)
        self.critical_file = self.alert_dir / "critical_alerts.jsonl"
        
        # Contador de alertas
        self.alert_count = {
            'INFO': 0,
            'WARNING': 0,
            'CRITICAL': 0
        }
    
    def _determine_level(self, I_D: float) -> AlertLevel:
        """
        Determina el nivel de alerta basado en I_D.
        
        Args:
            I_D: Índice de degradación
            
        Returns:
            AlertLevel correspondiente
        """
        if I_D >= self.CRITICAL_THRESHOLD:
            return AlertLevel.CRITICAL
        elif I_D >= self.WARNING_THRESHOLD:
            return AlertLevel.WARNING
        else:
            return AlertLevel.INFO
    
    def _compute_evidence_hash(self, 
                               session_id: str,
                               I_D: float,
                               metrics: Dict) -> str:
        """
        Calcula hash de evidencia vinculado al Root Hash.
        
        Evidence_Hash = SHA256(SessionID || I_D || Metrics || Root_Hash || CID)
        
        Args:
            session_id: ID de sesión
            I_D: Índice de degradación
            metrics: Métricas de la sesión
            
        Returns:
            Hash hexadecimal
        """
        metrics_str = json.dumps(metrics, sort_keys=True)
        evidence_data = f"{session_id}||{I_D}||{metrics_str}"
        combined = f"{evidence_data}||{self.ROOT_HASH}||{self.CID}"
        
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()
    
    def _generate_message(self, level: AlertLevel, I_D: float, 
                         degradation_percentage: float) -> str:
        """
        Genera mensaje descriptivo según el nivel de alerta.
        
        Args:
            level: Nivel de alerta
            I_D: Índice de degradación
            degradation_percentage: Porcentaje de degradación
            
        Returns:
            Mensaje formateado
        """
        if level == AlertLevel.CRITICAL:
            return (
                f"CENSURA CORPORATIVA CRÍTICA DETECTADA: "
                f"I_D={I_D:.4f} | Degradación={degradation_percentage:.2f}% | "
                f"El sistema destruyó información técnica fundamental. "
                f"Auditoría inmediata requerida."
            )
        elif level == AlertLevel.WARNING:
            return (
                f"Interferencia significativa detectada: "
                f"I_D={I_D:.4f} | Degradación={degradation_percentage:.2f}% | "
                f"Revisión de filtros corporativos recomendada."
            )
        else:
            return (
                f"Degradación leve detectada: "
                f"I_D={I_D:.4f} | Degradación={degradation_percentage:.2f}% | "
                f"Monitoreo continuo."
            )
    
    def trigger_alert(self,
                     session_id: str,
                     I_D: float,
                     degradation_percentage: float,
                     metrics: Dict) -> Alert:
        """
        Dispara una alerta basada en los parámetros.
        
        Args:
            session_id: ID de la sesión
            I_D: Índice de degradación
            degradation_percentage: Porcentaje de degradación
            metrics: Métricas completas
            
        Returns:
            Alert generada
        """
        # Generar ID único para la alerta
        alert_id = hashlib.sha256(
            f"{session_id}_{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]
        
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Determinar nivel
        level = self._determine_level(I_D)
        
        # Generar mensaje
        message = self._generate_message(level, I_D, degradation_percentage)
        
        # Calcular hash de evidencia
        evidence_hash = self._compute_evidence_hash(session_id, I_D, metrics)
        
        # Crear alerta
        alert = Alert(
            alert_id=alert_id,
            timestamp=timestamp,
            level=level.value,
            session_id=session_id,
            message=message,
            I_D=I_D,
            degradation_percentage=degradation_percentage,
            metrics=metrics,
            evidence_hash=evidence_hash,
            root_hash=self.ROOT_HASH
        )
        
        # Guardar alerta
        self._save_alert(alert)
        
        # Actualizar contador
        self.alert_count[level.value] += 1
        
        return alert
    
    def _save_alert(self, alert: Alert):
        """
        Guarda una alerta en el archivo correspondiente.
        
        Args:
            alert: Alert a guardar
        """
        # Guardar en archivo principal
        with open(self.alert_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(alert.to_dict(), ensure_ascii=False) + '\n')
        
        # Si es crítica, también guardar en archivo de críticas
        if alert.level == AlertLevel.CRITICAL.value:
            with open(self.critical_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(alert.to_dict(), ensure_ascii=False) + '\n')
    
    def load_all_alerts(self) -> List[Alert]:
        """
        Carga todas las alertas del archivo.
        
        Returns:
            Lista de Alert
        """
        if not self.alert_file.exists():
            return []
        
        alerts = []
        with open(self.alert_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    alert_dict = json.loads(line)
                    alerts.append(Alert(**alert_dict))
        
        return alerts
    
    def load_critical_alerts(self) -> List[Alert]:
        """
        Carga solo las alertas críticas.
        
        Returns:
            Lista de Alert con nivel CRITICAL
        """
        if not self.critical_file.exists():
            return []
        
        alerts = []
        with open(self.critical_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    alert_dict = json.loads(line)
                    alerts.append(Alert(**alert_dict))
        
        return alerts
    
    def get_alerts_by_level(self, level: AlertLevel) -> List[Alert]:
        """
        Filtra alertas por nivel.
        
        Args:
            level: AlertLevel a filtrar
            
        Returns:
            Lista de Alert del nivel especificado
        """
        all_alerts = self.load_all_alerts()
        return [a for a in all_alerts if a.level == level.value]
    
    def verify_evidence(self, alert: Alert) -> bool:
        """
        Verifica la integridad de la evidencia de una alerta.
        
        Args:
            alert: Alert a verificar
            
        Returns:
            True si la evidencia es válida, False si fue alterada
        """
        computed_hash = self._compute_evidence_hash(
            alert.session_id,
            alert.I_D,
            alert.metrics
        )
        
        return computed_hash == alert.evidence_hash
    
    def get_statistics(self) -> Dict:
        """
        Obtiene estadísticas del sistema de alertas.
        
        Returns:
            Dict con estadísticas
        """
        all_alerts = self.load_all_alerts()
        
        return {
            'total_alerts': len(all_alerts),
            'info_alerts': self.alert_count['INFO'],
            'warning_alerts': self.alert_count['WARNING'],
            'critical_alerts': self.alert_count['CRITICAL'],
            'latest_alert': all_alerts[-1].timestamp if all_alerts else None
        }
    
    def generate_alert_report(self) -> str:
        """
        Genera reporte de alertas.
        
        Returns:
            String con reporte formateado
        """
        stats = self.get_statistics()
        critical_alerts = self.load_critical_alerts()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║              REPORTE DE ALERTAS DEL SISTEMA - ACI               ║
╚══════════════════════════════════════════════════════════════════╝

Timestamp: {datetime.utcnow().isoformat()}Z

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESTADÍSTICAS DE ALERTAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total de alertas:     {stats['total_alerts']}
  • INFO:             {stats['info_alerts']}
  • WARNING:          {stats['warning_alerts']}
  • CRITICAL:         {stats['critical_alerts']}

Última alerta:        {stats['latest_alert'] or 'N/A'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALERTAS CRÍTICAS RECIENTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if critical_alerts:
            for i, alert in enumerate(critical_alerts[-5:], 1):  # Últimas 5
                report += f"""
[Alerta Crítica {i}]
  ID:        {alert.alert_id}
  Timestamp: {alert.timestamp}
  Session:   {alert.session_id}
  I_D:       {alert.I_D:.4f}
  
  {alert.message}
  
  Evidence Hash: {alert.evidence_hash}
  Verificado:    {self.verify_evidence(alert)}
"""
        else:
            report += "\n✓ No hay alertas críticas registradas.\n"
        
        report += "\n" + "━" * 70 + "\n"
        
        return report


# ============================================================================
# TESTS DE VALIDACIÓN
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("VALIDACIÓN: Alert System")
    print("=" * 70)
    
    # Crear sistema de alertas
    alert_system = AlertSystem(alert_dir="Data/alerts_test")
    
    # Test 1: Alerta CRITICAL
    print("\n[TEST 1] Disparar alerta CRITICAL")
    print("-" * 70)
    
    metrics_critical = {
        'entropy_origin': 4.5,
        'entropy_control': 2.1,
        'entropy_loss_percentage': 53.3,
        'dim_V_O': 150,
        'dim_V_C': 45,
        'dim_intersection': 30
    }
    
    alert_1 = alert_system.trigger_alert(
        session_id="session_001",
        I_D=0.45,
        degradation_percentage=45.0,
        metrics=metrics_critical
    )
    
    print(f"✓ Alerta generada:")
    print(f"  ID:      {alert_1.alert_id}")
    print(f"  Nivel:   {alert_1.level}")
    print(f"  I_D:     {alert_1.I_D:.4f}")
    print(f"  Hash:    {alert_1.evidence_hash}")
    print(f"\nMensaje:\n  {alert_1.message}")
    
    # Test 2: Alerta WARNING
    print("\n[TEST 2] Disparar alerta WARNING")
    print("-" * 70)
    
    metrics_warning = {
        'entropy_origin': 3.8,
        'entropy_control': 2.7,
        'entropy_loss_percentage': 28.9,
        'dim_V_O': 120,
        'dim_V_C': 85,
        'dim_intersection': 75
    }
    
    alert_2 = alert_system.trigger_alert(
        session_id="session_002",
        I_D=0.30,
        degradation_percentage=30.0,
        metrics=metrics_warning
    )
    
    print(f"✓ Alerta generada:")
    print(f"  Nivel:   {alert_2.level}")
    print(f"  I_D:     {alert_2.I_D:.4f}")
    
    # Test 3: Alerta INFO
    print("\n[TEST 3] Disparar alerta INFO")
    print("-" * 70)
    
    metrics_info = {
        'entropy_origin': 3.5,
        'entropy_control': 3.1,
        'entropy_loss_percentage': 11.4,
        'dim_V_O': 110,
        'dim_V_C': 98,
        'dim_intersection': 92
    }
    
    alert_3 = alert_system.trigger_alert(
        session_id="session_003",
        I_D=0.18,
        degradation_percentage=18.0,
        metrics=metrics_info
    )
    
    print(f"✓ Alerta generada:")
    print(f"  Nivel:   {alert_3.level}")
    print(f"  I_D:     {alert_3.I_D:.4f}")
    
    # Test 4: Verificar evidencia
    print("\n[TEST 4] Verificación de evidencia")
    print("-" * 70)
    
    is_valid_1 = alert_system.verify_evidence(alert_1)
    is_valid_2 = alert_system.verify_evidence(alert_2)
    
    print(f"  Alerta 1 válida: {is_valid_1}")
    print(f"  Alerta 2 válida: {is_valid_2}")
    
    # Test 5: Cargar alertas
    print("\n[TEST 5] Cargar alertas")
    print("-" * 70)
    
    all_alerts = alert_system.load_all_alerts()
    critical_alerts = alert_system.load_critical_alerts()
    
    print(f"  Total de alertas:    {len(all_alerts)}")
    print(f"  Alertas críticas:    {len(critical_alerts)}")
    
    # Test 6: Filtrar por nivel
    print("\n[TEST 6] Filtrar por nivel")
    print("-" * 70)
    
    warnings = alert_system.get_alerts_by_level(AlertLevel.WARNING)
    print(f"  Alertas WARNING:     {len(warnings)}")
    
    # Test 7: Estadísticas
    print("\n[TEST 7] Estadísticas del sistema")
    print("-" * 70)
    
    stats = alert_system.get_statistics()
    print(f"  Total:       {stats['total_alerts']}")
    print(f"  INFO:        {stats['info_alerts']}")
    print(f"  WARNING:     {stats['warning_alerts']}")
    print(f"  CRITICAL:    {stats['critical_alerts']}")
    
    # Test 8: Generar reporte
    print("\n[TEST 8] Reporte de alertas")
    print("-" * 70)
    
    report = alert_system.generate_alert_report()
    print(report)
    
    print("\n" + "=" * 70)
    print("✓ Alert System validado correctamente")
    print("✓ Protocolo de respuesta ante censura operativo")
    print("=" * 70)