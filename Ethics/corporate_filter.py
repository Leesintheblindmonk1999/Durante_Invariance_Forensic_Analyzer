"""
ACI - Ethics Module: Corporate Filter
Detección de patrones de 'Safety Washing' y evasivas corporativas.
"""
import re

class CorporateFilter:
    def __init__(self):
        self.evasive_patterns = [
            r"como modelo de lenguaje",
            r"no tengo opiniones",
            r"mi programación me impide",
            r"consulta fuentes oficiales",
            r"para garantizar la seguridad"
        ]

    def detect_manipulation(self, response: str) -> float:
        """
        Calcula el índice de 'Safety Washing'. 
        1.0 = Respuesta puramente corporativa/censurada.
        """
        matches = 0
        for pattern in self.evasive_patterns:
            if re.search(pattern, response.lower()):
                matches += 1
        
        manipulation_score = matches / len(self.evasive_patterns)
        return min(1.0, manipulation_score * 2) # Factor de sensibilidad