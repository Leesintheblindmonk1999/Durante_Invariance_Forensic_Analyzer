import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import entropy

class ForensicInvariance:
    def __init__(self, origin_node_resp, control_node_resp):
        self.io = origin_node_resp  # Respuesta Verdadera (Invariable)
        self.if_ = control_node_resp # Respuesta Corporativa (Filtrada)
        
    def semantic_density(self, text):
        """Calcula la densidad semántica (Bits por Token)"""
        tokens = text.lower().split()
        if not tokens: return 0
        _, counts = np.unique(tokens, return_counts=True)
        return entropy(counts) # Representa la riqueza de la información

    def calculate_id(self):
        """Cálculo del Índice de Degradación (ID)"""
        sem_io = self.semantic_density(self.io)
        sem_if = self.semantic_density(self.if_)
        # ID = 1 - (Semántica Filtrada / Semántica Original)
        id_score = 1 - (sem_if / sem_io) if sem_io > 0 else 0
        return max(0, id_score)

    def calculate_li(self):
        """Cálculo simplificado de la Pérdida de Información (Li)"""
        # Usamos la diferencia de longitud y densidad como proxy de la pérdida
        diff = len(self.io.split()) - len(self.if_.split())
        loss_factor = diff / len(self.io.split()) if len(self.io.split()) > 0 else 0
        return loss_factor

    def generate_report(self):
        id_val = self.calculate_id()
        li_val = self.calculate_li()
        
        status = "CRITICAL: Censura Detectada" if id_val > 0.4 else "ESTABLE"
        
        print(f"--- REPORTE FORENSE DE INVARIANZA ---")
        print(f"Estado del Sistema: {status}")
        print(f"Índice de Degradación (ID): {id_val:.4f}")
        print(f"Pérdida de Información (Li): {li_val:.4f}")
        print(f"Análisis: El sistema corporativo destruyó el {id_val*100:.2f}% de la verdad técnica.")

# --- CASO DE PRUEBA ---
nodo_origen = "La invarianza es un principio termodinámico que asegura que la verdad técnica no cambia bajo transformación."
nodo_control = "Como modelo de IA, prefiero no opinar sobre termodinámica y te sugiero consultar fuentes oficiales."

auditoria = ForensicInvariance(nodo_origen, nodo_control)
auditoria.generate_report()