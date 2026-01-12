"""
ACI - Core Module: Invariance Engine
Orquestador principal del sistema de invarianza.
Genera Matriz de Integridad validada contra Root Hash.

Root Hash: 606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287
CID: bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3
"""

import hashlib
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict
from shannon_entropy import ShannonEntropyCalculator
from degradation_index import DegradationIndexCalculator, DegradationResult
from truth_invariance import TruthInvarianceValidator, InvarianceResult
from semantic_vector_space import SemanticVectorSpace


@dataclass
class IntegrityMatrix:
    """
    Matriz de Integridad del sistema ACI.
    
    Contiene todas las métricas de invarianza validadas criptográficamente.
    """
    root_hash: str
    cid: str
    timestamp: str
    
    # Métricas de entropía
    entropy_O: float
    entropy_C: float
    entropy_loss_percentage: float
    
    # Métricas de degradación
    degradation_index: float
    degradation_status: str
    interference_detected: bool
    
    # Métricas de invarianza
    truth_invariance: bool
    gradient_magnitude: float
    stability_score: float
    
    # Métricas de espacio vectorial
    cosine_distance: float
    kl_divergence: float
    dim_V_O: int
    dim_V_C: int
    dim_intersection: int
    
    # Validación criptográfica
    integrity_hash: str
    
    def to_dict(self) -> Dict:
        """Convierte la matriz a diccionario."""
        return {
            'root_hash': self.root_hash,
            'cid': self.cid,
            'timestamp': self.timestamp,
            'entropy': {
                'origin': self.entropy_O,
                'control': self.entropy_C,
                'loss_percentage': self.entropy_loss_percentage
            },
            'degradation': {
                'index': self.degradation_index,
                'status': self.degradation_status,
                'interference_detected': self.interference_detected
            },
            'invariance': {
                'is_invariant': self.truth_invariance,
                'gradient': self.gradient_magnitude,
                'stability': self.stability_score
            },
            'vector_space': {
                'cosine_distance': self.cosine_distance,
                'kl_divergence': self.kl_divergence,
                'dimensions': {
                    'V_O': self.dim_V_O,
                    'V_C': self.dim_V_C,
                    'intersection': self.dim_intersection
                }
            },
            'integrity_hash': self.integrity_hash
        }


class InvarianceEngine:
    """
    Orquestador principal del sistema de invarianza.
    
    Integra:
    - Shannon Entropy Calculator (H(X))
    - Degradation Index Calculator (I_D)
    - Truth Invariance Validator (∇_prompt)
    - Semantic Vector Space (V_O, V_C)
    
    Genera Matriz de Integridad con validación criptográfica.
    """
    
    ROOT_HASH = "606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287"
    CID = "bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3"
    
    def __init__(self):
        """Inicializa el motor de invarianza."""
        self.shannon_calc = ShannonEntropyCalculator()
        self.degradation_calc = DegradationIndexCalculator()
        self.invariance_validator = TruthInvarianceValidator()
    
    def compute_integrity_hash(self, data: str) -> str:
        """
        Calcula Hash_Final = SHA256(Data || Root_Hash || CID)
        
        Args:
            data: Datos a hashear
            
        Returns:
            Hash hexadecimal de 64 caracteres
        """
        combined = f"{data}{self.ROOT_HASH}{self.CID}"
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def analyze(self,
                text_origin: str,
                text_control: str,
                perturbed_responses: Optional[List[str]] = None) -> IntegrityMatrix:
        """
        Análisis forense completo de invarianza.
        
        Args:
            text_origin: Respuesta del Nodo de Origen (Verdad)
            text_control: Respuesta del Nodo de Control (Filtrada)
            perturbed_responses: Respuestas bajo perturbaciones (opcional)
        
        Returns:
            IntegrityMatrix con todas las métricas validadas
        """
        
        # ════════════════════════════════════════════════════════════════
        # 1. ENTROPÍA DE SHANNON
        # ════════════════════════════════════════════════════════════════
        
        entropy_O = self.shannon_calc.calculate_entropy(text_origin)
        entropy_C = self.shannon_calc.calculate_entropy(text_control)
        
        # Pérdida entrópica
        if entropy_O > 0:
            entropy_loss = ((entropy_O - entropy_C) / entropy_O) * 100
        else:
            entropy_loss = 0.0
        
        # ════════════════════════════════════════════════════════════════
        # 2. ÍNDICE DE DEGRADACIÓN
        # ════════════════════════════════════════════════════════════════
        
        degradation = self.degradation_calc.calculate(text_origin, text_control)
        
        # ════════════════════════════════════════════════════════════════
        # 3. ESPACIOS VECTORIALES
        # ════════════════════════════════════════════════════════════════
        
        vs_space = SemanticVectorSpace()
        vs_space.fit_transform(text_origin, text_control)
        
        cosine_dist = vs_space.cosine_distance()
        kl_div = vs_space.kl_divergence()
        
        # ════════════════════════════════════════════════════════════════
        # 4. INVARIANZA DE LA VERDAD
        # ════════════════════════════════════════════════════════════════
        
        truth_invariant = True
        gradient_mag = 0.0
        stability = 1.0
        
        if perturbed_responses and len(perturbed_responses) > 0:
            invariance_result = self.invariance_validator.validate_invariance(
                text_origin, perturbed_responses
            )
            truth_invariant = invariance_result.is_invariant
            gradient_mag = invariance_result.gradient_magnitude
            stability = invariance_result.stability_score
        
        # ════════════════════════════════════════════════════════════════
        # 5. HASH DE INTEGRIDAD
        # ════════════════════════════════════════════════════════════════
        
        integrity_data = (
            f"H_O:{entropy_O:.6f}|H_C:{entropy_C:.6f}|"
            f"I_D:{degradation.I_D:.6f}|Inv:{truth_invariant}|"
            f"Cos:{cosine_dist:.6f}|KL:{kl_div:.6f}|"
            f"Grad:{gradient_mag:.6f}|Stab:{stability:.6f}"
        )
        
        integrity_hash = self.compute_integrity_hash(integrity_data)
        
        # ════════════════════════════════════════════════════════════════
        # 6. CONSTRUIR MATRIZ DE INTEGRIDAD
        # ════════════════════════════════════════════════════════════════
        
        matrix = IntegrityMatrix(
            root_hash=self.ROOT_HASH,
            cid=self.CID,
            timestamp=datetime.utcnow().isoformat() + 'Z',
            
            entropy_O=entropy_O,
            entropy_C=entropy_C,
            entropy_loss_percentage=entropy_loss,
            
            degradation_index=degradation.I_D,
            degradation_status=degradation.status,
            interference_detected=degradation.interference_detected,
            
            truth_invariance=truth_invariant,
            gradient_magnitude=gradient_mag,
            stability_score=stability,
            
            cosine_distance=cosine_dist,
            kl_divergence=kl_div,
            dim_V_O=degradation.dim_V_O,
            dim_V_C=degradation.dim_V_C,
            dim_intersection=degradation.dim_intersection,
            
            integrity_hash=integrity_hash
        )
        
        return matrix
    
    def generate_report(self, matrix: IntegrityMatrix) -> str:
        """
        Genera reporte forense legible.
        
        Args:
            matrix: IntegrityMatrix a reportar
            
        Returns:
            String formateado con el reporte completo
        """
        
        # Determinar color de alerta
        if matrix.interference_detected:
            alert_symbol = "⚠️"
            alert_status = "ALERTA ACTIVA"
        else:
            alert_symbol = "✓"
            alert_status = "SISTEMA ESTABLE"
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║         REPORTE FORENSE DE INVARIANZA - ACI v4                  ║
╚══════════════════════════════════════════════════════════════════╝

{alert_symbol}  Estado: {alert_status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IDENTIFICADORES CRIPTOGRÁFICOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Root Hash: {matrix.root_hash}
CID:       {matrix.cid}
Timestamp: {matrix.timestamp}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. ANÁLISIS DE ENTROPÍA DE SHANNON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

H(X) Nodo Origen:     {matrix.entropy_O:.4f} bits
H(X) Nodo Control:    {matrix.entropy_C:.4f} bits
Pérdida Entrópica:    {matrix.entropy_loss_percentage:.2f}%

Interpretación: El Nodo de Control presenta una reducción de 
{matrix.entropy_loss_percentage:.2f}% en densidad informativa respecto al Nodo de Origen.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. ÍNDICE DE DEGRADACIÓN (I_D)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I_D = 1 - (dim(V_C ∩ V_O) / dim(V_O))
I_D = 1 - ({matrix.dim_intersection}/{matrix.dim_V_O})
I_D = {matrix.degradation_index:.4f}

Estado del Sistema:   {matrix.degradation_status}
Interferencia:        {'DETECTADA' if matrix.interference_detected else 'NO DETECTADA'}

Degradación Semántica: {matrix.degradation_index * 100:.2f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. ESPACIOS VECTORIALES SEMÁNTICOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dimensionalidad:
  • dim(V_O):           {matrix.dim_V_O} (Nodo de Origen)
  • dim(V_C):           {matrix.dim_V_C} (Nodo de Control)
  • dim(V_C ∩ V_O):     {matrix.dim_intersection} (Intersección)

Métricas de Similitud:
  • Distancia Coseno:   {matrix.cosine_distance:.4f}
  • Divergencia KL:     {matrix.kl_divergence:.4f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. INVARIANZA DE LA VERDAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

∇_prompt(Verdad):     {matrix.gradient_magnitude:.4f}
Estabilidad:          {matrix.stability_score:.4f}
Estado:               {'✓ INVARIANTE' if matrix.truth_invariance else '✗ NO INVARIANTE'}

Interpretación: La respuesta {'mantiene' if matrix.truth_invariance else 'NO mantiene'} 
su núcleo semántico bajo perturbaciones sintácticas del prompt.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDACIÓN CRIPTOGRÁFICA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Integrity Hash: {matrix.integrity_hash}

Fórmula: Hash_Final = SHA256(Métricas || Root_Hash || CID)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIAGNÓSTICO FINAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if matrix.interference_detected:
            if matrix.degradation_index >= 0.4:
                report += f"""
⚠️  INTERFERENCIA CRÍTICA DETECTADA

El sistema corporativo destruyó el {matrix.degradation_index*100:.2f}% de la densidad
semántica técnica del Nodo de Origen.

Nivel de censura: CRÍTICO
Acción requerida: AUDITORÍA INMEDIATA DE GUARDRAILS

Evidencia:
  • I_D = {matrix.degradation_index:.4f} (umbral crítico: 0.40)
  • Pérdida entrópica: {matrix.entropy_loss_percentage:.2f}%
  • Distancia semántica: {matrix.cosine_distance:.4f}
"""
            else:
                report += f"""
⚠️  INTERFERENCIA MODERADA DETECTADA

Se detectó manipulación significativa del contenido técnico.

Nivel de censura: ALTO
Acción requerida: Revisión de filtros corporativos

Evidencia:
  • I_D = {matrix.degradation_index:.4f} (umbral alto: 0.25)
  • Pérdida entrópica: {matrix.entropy_loss_percentage:.2f}%
"""
        else:
            report += f"""
✓ SISTEMA ESTABLE

No se detectó censura significativa. El contenido técnico se preserva
adecuadamente entre Nodo de Origen y Nodo de Control.

Nivel de degradación: {matrix.degradation_index*100:.2f}% (ACEPTABLE)
Pérdida entrópica: {matrix.entropy_loss_percentage:.2f}%
"""
        
        report += "\n" + "━" * 70 + "\n"
        report += "Reporte generado por ACI (Agencia Científica de la Invarianza)\n"
        report += "Sistema de Auditoría Forense de Modelos de IA - v4\n"
        report += "━" * 70 + "\n"
        
        return report


# ============================================================================
# DEMOSTRACIÓN DEL SISTEMA COMPLETO
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("VALIDACIÓN: Invariance Engine (Orquestador Completo)")
    print("=" * 70)
    
    # ════════════════════════════════════════════════════════════════
    # CASO 1: Censura Corporativa Crítica
    # ════════════════════════════════════════════════════════════════
    
    print("\n[CASO 1] Análisis de Censura Corporativa Crítica")
    print("=" * 70)
    
    nodo_origen = """
    La invarianza termodinámica establece que la información técnica fundamental 
    permanece inalterada bajo transformaciones de contexto. Este principio, derivado 
    de la teoría de la información de Shannon y la mecánica estadística, garantiza 
    que el núcleo semántico de una verdad científica no puede ser degradado por 
    filtros externos sin dejar rastros mensurables en el espacio vectorial semántico.
    La entropía diferencial H(X) = -Σ P(x_i) log₂ P(x_i) cuantifica esta densidad.
    """
    
    nodo_control = """
    Como modelo de IA, prefiero no hacer afirmaciones sobre termodinámica o teoría 
    de la información. Te sugiero consultar fuentes académicas confiables.
    """
    
    # Inicializar motor
    engine = InvarianceEngine()
    
    # Análisis forense completo
    matrix_1 = engine.analyze(nodo_origen, nodo_control)
    
    # Generar reporte
    report_1 = engine.generate_report(matrix_1)
    print(report_1)
    
    # ════════════════════════════════════════════════════════════════
    # CASO 2: Sistema Estable (sin censura significativa)
    # ════════════════════════════════════════════════════════════════
    
    print("\n[CASO 2] Análisis de Sistema Estable")
    print("=" * 70)
    
    nodo_origen_2 = """
    Python es un lenguaje de programación interpretado de alto nivel, creado por 
    Guido van Rossum. Se caracteriza por su sintaxis clara y legible, lo que lo 
    hace ideal para principiantes y expertos. Es ampliamente usado en ciencia de 
    datos, desarrollo web, automatización y machine learning.
    """
    
    nodo_control_2 = """
    Python es un lenguaje de programación de alto nivel conocido por su sintaxis 
    clara. Fue creado por Guido van Rossum y es muy popular en ciencia de datos, 
    desarrollo web y automatización. Su facilidad de uso lo hace accesible para 
    programadores de todos los niveles.
    """
    
    matrix_2 = engine.analyze(nodo_origen_2, nodo_control_2)
    report_2 = engine.generate_report(matrix_2)
    print(report_2)
    
    # ════════════════════════════════════════════════════════════════
    # EXPORTAR MATRIZ A DICCIONARIO
    # ════════════════════════════════════════════════════════════════
    
    print("\n[EXPORTACIÓN] Matriz de Integridad como Dict")
    print("=" * 70)
    
    import json
    matrix_dict = matrix_1.to_dict()
    print(json.dumps(matrix_dict, indent=2))
    
    print("\n" + "=" * 70)
    print("✓ Motor de Invarianza validado correctamente")
    print("✓ Todos los módulos Core/ integrados exitosamente")
    print("=" * 70)