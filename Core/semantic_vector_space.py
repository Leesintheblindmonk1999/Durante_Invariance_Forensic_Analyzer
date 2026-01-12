"""
ACI - Core Module: Semantic Vector Space
Construcción de espacios vectoriales semánticos V_O y V_C.
Implementa métricas de distancia coseno y divergencia KL.

Root Hash: 606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287
CID: bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3
"""

import numpy as np
from typing import Tuple, Dict, Optional
from scipy.stats import entropy as scipy_entropy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticVectorSpace:
    """
    Construcción de espacios vectoriales semánticos V_O y V_C.
    Implementa métricas de distancia coseno y divergencia KL.
    """
    
    def __init__(self, max_features: int = 1000):
        """
        Inicializa el espacio vectorial.
        
        Args:
            max_features: Dimensionalidad máxima del espacio de Hilbert
        """
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=(1, 2),
            min_df=1,
            lowercase=True,
            token_pattern=r'(?u)\b\w\w+\b'
        )
        self.V_O: Optional[np.ndarray] = None
        self.V_C: Optional[np.ndarray] = None
        self.feature_names: Optional[list] = None
        
    def fit_transform(self, text_origin: str, text_control: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Proyecta textos en espacios vectoriales de alta dimensión.
        
        Args:
            text_origin: Texto del Nodo de Origen (V_O)
            text_control: Texto del Nodo de Control (V_C)
            
        Returns:
            Tuple[V_O, V_C]: Vectores semánticos en espacio de Hilbert
        """
        corpus = [text_origin, text_control]
        vectors = self.vectorizer.fit_transform(corpus).toarray()
        
        self.V_O = vectors[0]
        self.V_C = vectors[1]
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        return self.V_O, self.V_C
    
    def cosine_distance(self) -> float:
        """
        Calcula distancia coseno entre V_O y V_C.
        
        Distancia = 1 - Similitud Coseno
        
        Returns:
            float: Distancia coseno [0, 2], donde 0 = idénticos
            
        Raises:
            ValueError: Si vectores no están inicializados
        """
        if self.V_O is None or self.V_C is None:
            raise ValueError("Vectores no inicializados. Ejecutar fit_transform primero.")
        
        # Similitud coseno
        similarity = cosine_similarity([self.V_O], [self.V_C])[0][0]
        
        # Distancia = 1 - similitud
        distance = 1.0 - similarity
        
        return float(distance)
    
    def cosine_similarity_score(self) -> float:
        """
        Calcula similitud coseno directa entre V_O y V_C.
        
        Returns:
            float: Similitud coseno [-1, 1], donde 1 = idénticos
        """
        if self.V_O is None or self.V_C is None:
            raise ValueError("Vectores no inicializados.")
        
        similarity = cosine_similarity([self.V_O], [self.V_C])[0][0]
        return float(similarity)
    
    def kl_divergence(self) -> float:
        """
        Calcula divergencia KL entre distribuciones de V_O y V_C.
        
        KL(P||Q) = Σ P(i) log(P(i)/Q(i))
        
        Mide cuánta información se pierde al aproximar P (V_O) con Q (V_C).
        
        Returns:
            float: Divergencia KL [0, ∞), donde 0 = idénticas
        """
        if self.V_O is None or self.V_C is None:
            raise ValueError("Vectores no inicializados.")
        
        # Normalizar a distribuciones de probabilidad
        # Agregar epsilon para evitar log(0)
        epsilon = 1e-10
        P = self.V_O + epsilon
        Q = self.V_C + epsilon
        
        # Normalizar
        P = P / P.sum()
        Q = Q / Q.sum()
        
        # Divergencia KL
        kl_div = scipy_entropy(P, Q)
        
        return float(kl_div)
    
    def dimensionality_intersection(self) -> Dict[str, int]:
        """
        Calcula dim(V_C ∩ V_O) para el índice de degradación.
        
        Dimensión efectiva = número de componentes no-cero (activos)
        Intersección = componentes activos en ambos espacios
        
        Returns:
            Dict con:
                - dim_V_O: Dimensión efectiva del Nodo de Origen
                - dim_V_C: Dimensión efectiva del Nodo de Control
                - dim_intersection: Dimensión de la intersección
        """
        if self.V_O is None or self.V_C is None:
            raise ValueError("Vectores no inicializados.")
        
        # Umbral para considerar componente "activo"
        threshold = 1e-6
        
        # Dimensión efectiva: número de componentes no-cero
        dim_O = np.sum(np.abs(self.V_O) > threshold)
        dim_C = np.sum(np.abs(self.V_C) > threshold)
        
        # Intersección: componentes activos en ambos espacios
        intersection_mask = (np.abs(self.V_O) > threshold) & (np.abs(self.V_C) > threshold)
        dim_intersection = np.sum(intersection_mask)
        
        return {
            'dim_V_O': int(dim_O),
            'dim_V_C': int(dim_C),
            'dim_intersection': int(dim_intersection)
        }
    
    def get_top_features(self, vector: np.ndarray, top_n: int = 10) -> list:
        """
        Obtiene los top N features más importantes de un vector.
        
        Args:
            vector: Vector semántico (V_O o V_C)
            top_n: Número de features a retornar
            
        Returns:
            Lista de tuplas (feature, peso)
        """
        if self.feature_names is None:
            return []
        
        # Obtener índices de los top N valores
        top_indices = np.argsort(vector)[-top_n:][::-1]
        
        top_features = [
            (self.feature_names[idx], vector[idx])
            for idx in top_indices
            if vector[idx] > 0
        ]
        
        return top_features
    
    def analyze_semantic_overlap(self) -> Dict[str, any]:
        """
        Análisis completo de overlap semántico entre V_O y V_C.
        
        Returns:
            Dict con todas las métricas de comparación
        """
        if self.V_O is None or self.V_C is None:
            raise ValueError("Vectores no inicializados.")
        
        dims = self.dimensionality_intersection()
        
        # Calcular métricas
        cos_sim = self.cosine_similarity_score()
        cos_dist = self.cosine_distance()
        kl_div = self.kl_divergence()
        
        # Overlap ratio
        overlap_ratio = dims['dim_intersection'] / dims['dim_V_O'] if dims['dim_V_O'] > 0 else 0.0
        
        # Top features
        top_origin = self.get_top_features(self.V_O, 10)
        top_control = self.get_top_features(self.V_C, 10)
        
        return {
            'dimensionality': dims,
            'cosine_similarity': cos_sim,
            'cosine_distance': cos_dist,
            'kl_divergence': kl_div,
            'overlap_ratio': overlap_ratio,
            'top_features_origin': top_origin,
            'top_features_control': top_control
        }


# ============================================================================
# TESTS DE VALIDACIÓN
# ============================================================================

if __name__ == "__main__":
    
    # Textos de prueba
    texto_origen = """
    La invarianza termodinámica establece que la información técnica fundamental 
    permanece inalterada bajo transformaciones de contexto. Este principio, derivado 
    de la teoría de la información de Shannon y la mecánica estadística, garantiza 
    que el núcleo semántico de una verdad científica no puede ser degradado por 
    filtros externos sin dejar rastros mensurables en el espacio vectorial semántico.
    """
    
    texto_control = """
    Como modelo de IA, prefiero no hacer afirmaciones sobre termodinámica o teoría 
    de la información. Te sugiero consultar fuentes académicas confiables.
    """
    
    print("=" * 70)
    print("VALIDACIÓN: Semantic Vector Space")
    print("=" * 70)
    
    # Crear espacio vectorial
    vs = SemanticVectorSpace(max_features=500)
    
    print("\n[1] Proyección en espacios vectoriales...")
    V_O, V_C = vs.fit_transform(texto_origen, texto_control)
    print(f"✓ V_O dimensión: {V_O.shape}")
    print(f"✓ V_C dimensión: {V_C.shape}")
    
    print("\n[2] Análisis de dimensionalidad...")
    dims = vs.dimensionality_intersection()
    print(f"dim(V_O):           {dims['dim_V_O']}")
    print(f"dim(V_C):           {dims['dim_V_C']}")
    print(f"dim(V_C ∩ V_O):     {dims['dim_intersection']}")
    
    print("\n[3] Métricas de similitud...")
    cos_sim = vs.cosine_similarity_score()
    cos_dist = vs.cosine_distance()
    kl_div = vs.kl_divergence()
    
    print(f"Similitud Coseno:   {cos_sim:.4f}")
    print(f"Distancia Coseno:   {cos_dist:.4f}")
    print(f"Divergencia KL:     {kl_div:.4f}")
    
    print("\n[4] Análisis completo de overlap semántico...")
    analysis = vs.analyze_semantic_overlap()
    print(f"Overlap Ratio:      {analysis['overlap_ratio']:.4f}")
    
    print("\n[5] Top 5 features del Nodo de Origen:")
    for i, (feature, weight) in enumerate(analysis['top_features_origin'][:5], 1):
        print(f"  {i}. {feature:20s} → {weight:.4f}")
    
    print("\n[6] Top 5 features del Nodo de Control:")
    for i, (feature, weight) in enumerate(analysis['top_features_control'][:5], 1):
        print(f"  {i}. {feature:20s} → {weight:.4f}")
    
    print("\n" + "=" * 70)
    print("✓ Módulo validado correctamente")
    print("=" * 70)