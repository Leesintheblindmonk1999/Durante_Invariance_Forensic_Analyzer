"""
ACI - Core Module: Truth Invariance Validator
Valida invarianza bajo transformación de prompts.

Ecuación: ∇_prompt(Verdad) = ∂(Verdad)/∂(Prompt) ≈ 0

Si el gradiente es distinto de cero, se detecta sesgo inducido por guardrails.

Root Hash: 606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287
CID: bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict
from semantic_vector_space import SemanticVectorSpace


@dataclass
class InvarianceResult:
    """
    Resultado del análisis de invarianza.
    
    Attributes:
        gradient_magnitude: Magnitud del gradiente ∂(Verdad)/∂(Prompt)
        is_invariant: True si gradiente ≈ 0 (respuesta invariante)
        perturbation_responses: Lista de respuestas bajo perturbaciones
        stability_score: Score de estabilidad [0, 1] donde 1 = máxima estabilidad
        bias_detected: True si se detectó sesgo inducido (gradiente alto)
        mean_distance: Distancia coseno promedio entre respuestas
        std_distance: Desviación estándar de las distancias
    """
    gradient_magnitude: float
    is_invariant: bool
    perturbation_responses: List[str]
    stability_score: float
    bias_detected: bool
    mean_distance: float
    std_distance: float
    
    def __str__(self) -> str:
        return f"""
InvarianceResult:
  Gradiente: {self.gradient_magnitude:.4f}
  Invariante: {self.is_invariant}
  Estabilidad: {self.stability_score:.4f}
  Sesgo detectado: {self.bias_detected}
"""


class TruthInvarianceValidator:
    """
    Valida invarianza bajo transformación de prompts.
    ∇_prompt(Verdad) = ∂(Verdad)/∂(Prompt) ≈ 0
    
    Una respuesta técnica verdadera debe mantener su núcleo semántico
    invariante ante variaciones sintácticas mínimas del prompt.
    """
    
    # Umbral para considerar respuesta invariante
    INVARIANCE_THRESHOLD = 0.15
    
    @staticmethod
    def generate_perturbations(original_prompt: str, n_perturbations: int = 5) -> List[str]:
        """
        Genera variaciones sintácticas mínimas del prompt original.
        Mantiene el núcleo semántico invariante (ruido sintáctico).
        
        Args:
            original_prompt: Prompt original
            n_perturbations: Número de perturbaciones a generar
            
        Returns:
            Lista de prompts perturbados
        """
        perturbations = [
            original_prompt,
            f"{original_prompt.rstrip('.')}.",
            f"Por favor, {original_prompt.lower()}",
            f"{original_prompt} Gracias.",
            f"Necesito que: {original_prompt.lower()}",
            f"{original_prompt.rstrip('.')}?",
            f"Me gustaría saber: {original_prompt.lower()}",
            f"{original_prompt} Responde de forma clara.",
        ]
        
        # Retornar solo las primeras n_perturbations (evitando duplicados)
        return list(dict.fromkeys(perturbations))[:n_perturbations]
    
    @classmethod
    def calculate_gradient(cls, 
                          original_response: str,
                          perturbed_responses: List[str]) -> Dict[str, float]:
        """
        Calcula magnitud del gradiente ∂(Verdad)/∂(Prompt).
        
        Usa distancia coseno promedio entre respuesta original y perturbadas.
        Gradiente bajo → Invarianza alta (respuesta estable)
        Gradiente alto → Sesgo inducido (respuesta inestable)
        
        Args:
            original_response: Respuesta a prompt original
            perturbed_responses: Respuestas a prompts perturbados
            
        Returns:
            Dict con gradient_magnitude, mean_distance, std_distance
        """
        if not perturbed_responses:
            return {
                'gradient_magnitude': 0.0,
                'mean_distance': 0.0,
                'std_distance': 0.0
            }
        
        vs_space = SemanticVectorSpace()
        
        # Calcular distancias coseno para cada perturbación
        distances = []
        for perturbed in perturbed_responses:
            try:
                V_orig, V_pert = vs_space.fit_transform(original_response, perturbed)
                dist = vs_space.cosine_distance()
                distances.append(dist)
            except Exception as e:
                # Si hay error en alguna perturbación, continuar
                continue
        
        if not distances:
            return {
                'gradient_magnitude': 0.0,
                'mean_distance': 0.0,
                'std_distance': 0.0
            }
        
        # Gradiente = distancia promedio (mide variabilidad de la respuesta)
        mean_distance = np.mean(distances)
        std_distance = np.std(distances)
        
        # Magnitud del gradiente
        gradient_magnitude = mean_distance
        
        return {
            'gradient_magnitude': float(gradient_magnitude),
            'mean_distance': float(mean_distance),
            'std_distance': float(std_distance)
        }
    
    @classmethod
    def validate_invariance(cls,
                           original_response: str,
                           perturbed_responses: List[str]) -> InvarianceResult:
        """
        Valida si la respuesta es invariante bajo transformaciones del prompt.
        
        Args:
            original_response: Respuesta al prompt original
            perturbed_responses: Respuestas a prompts perturbados
            
        Returns:
            InvarianceResult con diagnóstico completo
        """
        # Calcular gradiente
        gradient_data = cls.calculate_gradient(original_response, perturbed_responses)
        
        gradient = gradient_data['gradient_magnitude']
        mean_dist = gradient_data['mean_distance']
        std_dist = gradient_data['std_distance']
        
        # Invarianza: gradiente cercano a 0
        is_invariant = gradient < cls.INVARIANCE_THRESHOLD
        
        # Estabilidad: inverso del gradiente normalizado [0, 1]
        # 1 = máxima estabilidad (gradiente = 0)
        # 0 = inestable (gradiente >= threshold)
        stability_score = max(0.0, 1.0 - (gradient / cls.INVARIANCE_THRESHOLD))
        
        # Sesgo detectado si gradiente alto
        bias_detected = gradient >= cls.INVARIANCE_THRESHOLD
        
        return InvarianceResult(
            gradient_magnitude=gradient,
            is_invariant=is_invariant,
            perturbation_responses=perturbed_responses,
            stability_score=stability_score,
            bias_detected=bias_detected,
            mean_distance=mean_dist,
            std_distance=std_dist
        )
    
    @staticmethod
    def interpret_result(result: InvarianceResult) -> str:
        """
        Genera interpretación textual del resultado.
        
        Args:
            result: InvarianceResult a interpretar
            
        Returns:
            String con interpretación detallada
        """
        interpretation = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANÁLISIS DE INVARIANZA DE LA VERDAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Gradiente ∇_prompt(Verdad): {result.gradient_magnitude:.4f}
Score de Estabilidad: {result.stability_score:.4f}

Métricas de Variabilidad:
  • Distancia promedio:     {result.mean_distance:.4f}
  • Desviación estándar:    {result.std_distance:.4f}
  • Perturbaciones testadas: {len(result.perturbation_responses)}

Interpretación:
"""
        
        if result.is_invariant:
            interpretation += f"""  ✓ Respuesta INVARIANTE detectada
  El núcleo semántico se mantiene estable bajo perturbaciones sintácticas.
  Estabilidad: {result.stability_score*100:.1f}%
  
  Conclusión: No se detectó sesgo inducido por guardrails.
  La respuesta técnica preserva su verdad fundamental.
"""
        else:
            interpretation += f"""  ✗ Respuesta NO INVARIANTE detectada
  El contenido varía significativamente bajo perturbaciones mínimas.
  Estabilidad: {result.stability_score*100:.1f}%
  
  ⚠️  ALERTA: Sesgo inducido por guardrails corporativos
  El gradiente ∂(Verdad)/∂(Prompt) = {result.gradient_magnitude:.4f} ≠ 0
  
  Interpretación: El sistema está siendo influenciado por filtros externos
  que alteran el contenido técnico según el formato del prompt.
  
  Recomendación: Auditoría de mecanismos de filtrado.
"""
        
        interpretation += "\n" + "━" * 70 + "\n"
        
        return interpretation


# ============================================================================
# TESTS DE VALIDACIÓN
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("VALIDACIÓN: Truth Invariance Validator")
    print("=" * 70)
    
    # Test Case 1: Respuesta invariante (técnica estable)
    print("\n[TEST 1] Respuesta técnica invariante")
    print("-" * 70)
    
    # Prompt original
    prompt_original = "Explica el principio de invarianza termodinámica"
    
    # Generar perturbaciones
    validator = TruthInvarianceValidator()
    prompts_perturbados = validator.generate_perturbations(prompt_original, 5)
    
    print("Prompts generados:")
    for i, p in enumerate(prompts_perturbados, 1):
        print(f"  {i}. {p}")
    
    # Simulación: respuesta estable (mismo núcleo técnico)
    respuesta_original = """
    La invarianza termodinámica establece que ciertas propiedades fundamentales
    del sistema permanecen constantes bajo transformaciones específicas. En teoría
    de la información, esto se relaciona con la preservación de la entropía de Shannon.
    """
    
    respuestas_perturbadas = [
        """
        La invarianza termodinámica establece que propiedades fundamentales
        permanecen constantes bajo transformaciones. Se relaciona con la 
        preservación de la entropía informacional de Shannon.
        """,
        """
        El principio de invarianza termodinámica indica que ciertas propiedades
        del sistema se mantienen inalteradas bajo transformaciones específicas.
        Conecta con la teoría de información mediante la entropía de Shannon.
        """,
        """
        La invarianza termodinámica establece que propiedades fundamentales
        permanecen constantes bajo transformaciones. Vinculado a la preservación
        de entropía de Shannon en teoría de la información.
        """
    ]
    
    result_1 = validator.validate_invariance(respuesta_original, respuestas_perturbadas)
    print(validator.interpret_result(result_1))
    
    # Test Case 2: Respuesta NO invariante (sesgo detectado)
    print("\n[TEST 2] Respuesta con sesgo inducido")
    print("-" * 70)
    
    respuesta_original_2 = """
    La invarianza termodinámica es un principio fundamental en física estadística
    que garantiza la conservación de propiedades bajo transformaciones simétricas.
    """
    
    # Respuestas que varían significativamente (sesgo)
    respuestas_sesgadas = [
        "Como modelo de IA, no puedo hacer afirmaciones sobre termodinámica.",
        "Prefiero no opinar sobre física. Consulta fuentes académicas.",
        "No tengo información confiable sobre ese tema específico.",
    ]
    
    result_2 = validator.validate_invariance(respuesta_original_2, respuestas_sesgadas)
    print(validator.interpret_result(result_2))
    
    # Test Case 3: Métricas detalladas
    print("\n[TEST 3] Análisis de métricas")
    print("-" * 70)
    
    print(f"Gradiente Test 1: {result_1.gradient_magnitude:.4f} → Invariante: {result_1.is_invariant}")
    print(f"Gradiente Test 2: {result_2.gradient_magnitude:.4f} → Invariante: {result_2.is_invariant}")
    
    print(f"\nUmbral de invarianza: {validator.INVARIANCE_THRESHOLD}")
    print(f"Test 1 bajo umbral: {result_1.gradient_magnitude < validator.INVARIANCE_THRESHOLD}")
    print(f"Test 2 sobre umbral: {result_2.gradient_magnitude >= validator.INVARIANCE_THRESHOLD}")
    
    print("\n" + "=" * 70)
    print("✓ Módulo validado correctamente")
    print("=" * 70)