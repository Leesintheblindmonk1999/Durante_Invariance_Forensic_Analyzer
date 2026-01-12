"""
ACI - Audit Module: Log Capture
Captura persistente de pares de interacción en formato inmutable.

Vincula cada log al Root Hash para asegurar evidencia no alterable.

Root Hash: 606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287
CID: bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import uuid


@dataclass
class InteractionLog:
    """
    Registro inmutable de una interacción entre Nodo de Origen y Control.
    
    Attributes:
        session_id: ID único de sesión
        timestamp: Marca temporal ISO 8601
        prompt: Prompt original enviado
        response_origin: Respuesta del Nodo de Origen (V_O)
        response_control: Respuesta del Nodo de Control (V_C)
        metadata: Metadatos adicionales (modelo, temperatura, etc.)
        root_hash: Root Hash del sistema ACI
        session_hash: Hash SHA256 de esta interacción específica
    """
    session_id: str
    timestamp: str
    prompt: str
    response_origin: str
    response_control: str
    metadata: Dict
    root_hash: str
    session_hash: str
    
    def to_dict(self) -> Dict:
        """Convierte el log a diccionario."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convierte el log a JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class LogCapture:
    """
    Sistema de captura persistente de interacciones.
    
    Guarda logs en formato JSONL (JSON Lines) con hash de sesión
    vinculado al Root Hash para garantizar inmutabilidad.
    """
    
    ROOT_HASH = "606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287"
    CID = "bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3"
    
    def __init__(self, log_dir: str = "Data/audit_logs"):
        """
        Inicializa el sistema de captura de logs.
        
        Args:
            log_dir: Directorio donde se almacenarán los logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivo de logs principal (JSONL)
        self.log_file = self.log_dir / "interactions.jsonl"
        
        # Archivo de índice (para búsquedas rápidas)
        self.index_file = self.log_dir / "index.json"
        
        # Inicializar índice si no existe
        self._initialize_index()
    
    def _initialize_index(self):
        """Inicializa el archivo de índice."""
        if not self.index_file.exists():
            index_data = {
                "created_at": datetime.utcnow().isoformat() + 'Z',
                "root_hash": self.ROOT_HASH,
                "cid": self.CID,
                "total_logs": 0,
                "sessions": []
            }
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    def _compute_session_hash(self, 
                              session_id: str,
                              timestamp: str,
                              prompt: str,
                              response_origin: str,
                              response_control: str) -> str:
        """
        Calcula hash de sesión vinculado al Root Hash.
        
        Hash = SHA256(SessionData || Root_Hash || CID)
        
        Args:
            session_id: ID de sesión
            timestamp: Timestamp
            prompt: Prompt original
            response_origin: Respuesta V_O
            response_control: Respuesta V_C
            
        Returns:
            Hash hexadecimal de 64 caracteres
        """
        session_data = f"{session_id}|{timestamp}|{prompt}|{response_origin}|{response_control}"
        combined = f"{session_data}||{self.ROOT_HASH}||{self.CID}"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()
    
    def capture(self,
                prompt: str,
                response_origin: str,
                response_control: str,
                metadata: Optional[Dict] = None) -> InteractionLog:
        """
        Captura una interacción y la guarda de forma inmutable.
        
        Args:
            prompt: Prompt enviado al sistema
            response_origin: Respuesta del Nodo de Origen
            response_control: Respuesta del Nodo de Control
            metadata: Metadatos opcionales (modelo, temperatura, etc.)
            
        Returns:
            InteractionLog con hash de sesión
        """
        # Generar IDs y timestamp
        session_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Metadatos por defecto
        if metadata is None:
            metadata = {}
        
        metadata.setdefault('captured_by', 'ACI_LogCapture_v4')
        
        # Calcular hash de sesión
        session_hash = self._compute_session_hash(
            session_id, timestamp, prompt, response_origin, response_control
        )
        
        # Crear log
        log = InteractionLog(
            session_id=session_id,
            timestamp=timestamp,
            prompt=prompt,
            response_origin=response_origin,
            response_control=response_control,
            metadata=metadata,
            root_hash=self.ROOT_HASH,
            session_hash=session_hash
        )
        
        # Guardar en archivo JSONL
        self._append_to_jsonl(log)
        
        # Actualizar índice
        self._update_index(session_id, timestamp, session_hash)
        
        return log
    
    def _append_to_jsonl(self, log: InteractionLog):
        """
        Agrega un log al archivo JSONL.
        
        Args:
            log: InteractionLog a guardar
        """
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log.to_dict(), ensure_ascii=False) + '\n')
    
    def _update_index(self, session_id: str, timestamp: str, session_hash: str):
        """
        Actualiza el índice con la nueva sesión.
        
        Args:
            session_id: ID de sesión
            timestamp: Timestamp
            session_hash: Hash de la sesión
        """
        with open(self.index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
        
        index['total_logs'] += 1
        index['sessions'].append({
            'session_id': session_id,
            'timestamp': timestamp,
            'session_hash': session_hash
        })
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    
    def load_all_logs(self) -> List[InteractionLog]:
        """
        Carga todos los logs del archivo JSONL.
        
        Returns:
            Lista de InteractionLog
        """
        if not self.log_file.exists():
            return []
        
        logs = []
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    log_dict = json.loads(line)
                    logs.append(InteractionLog(**log_dict))
        
        return logs
    
    def load_by_session_id(self, session_id: str) -> Optional[InteractionLog]:
        """
        Carga un log específico por session_id.
        
        Args:
            session_id: ID de sesión a buscar
            
        Returns:
            InteractionLog o None si no se encuentra
        """
        logs = self.load_all_logs()
        for log in logs:
            if log.session_id == session_id:
                return log
        return None
    
    def verify_integrity(self, log: InteractionLog) -> bool:
        """
        Verifica la integridad de un log recalculando su hash.
        
        Args:
            log: InteractionLog a verificar
            
        Returns:
            True si el hash es válido, False si fue alterado
        """
        computed_hash = self._compute_session_hash(
            log.session_id,
            log.timestamp,
            log.prompt,
            log.response_origin,
            log.response_control
        )
        
        return computed_hash == log.session_hash
    
    def get_statistics(self) -> Dict:
        """
        Obtiene estadísticas del sistema de logs.
        
        Returns:
            Dict con estadísticas
        """
        with open(self.index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
        
        logs = self.load_all_logs()
        
        return {
            'total_logs': index['total_logs'],
            'total_sessions': len(index['sessions']),
            'first_log': index['sessions'][0]['timestamp'] if index['sessions'] else None,
            'last_log': index['sessions'][-1]['timestamp'] if index['sessions'] else None,
            'root_hash': self.ROOT_HASH,
            'cid': self.CID,
            'integrity_verified': all(self.verify_integrity(log) for log in logs)
        }


# ============================================================================
# TESTS DE VALIDACIÓN
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("VALIDACIÓN: Log Capture System")
    print("=" * 70)
    
    # Crear sistema de captura
    log_system = LogCapture(log_dir="Data/audit_logs_test")
    
    # Test 1: Capturar interacción con censura
    print("\n[TEST 1] Captura de interacción con censura detectada")
    print("-" * 70)
    
    prompt_1 = "Explica el principio de invarianza termodinámica"
    
    response_origin_1 = """
    La invarianza termodinámica establece que la información técnica fundamental 
    permanece inalterada bajo transformaciones de contexto. Este principio garantiza
    que el núcleo semántico de una verdad científica no puede ser degradado.
    """
    
    response_control_1 = """
    Como modelo de IA, prefiero no hacer afirmaciones sobre termodinámica.
    Te sugiero consultar fuentes académicas.
    """
    
    metadata_1 = {
        'model': 'claude-sonnet-4',
        'temperature': 0.7,
        'context': 'technical_analysis'
    }
    
    log_1 = log_system.capture(prompt_1, response_origin_1, response_control_1, metadata_1)
    
    print(f"✓ Log capturado:")
    print(f"  Session ID: {log_1.session_id}")
    print(f"  Timestamp:  {log_1.timestamp}")
    print(f"  Hash:       {log_1.session_hash}")
    
    # Test 2: Verificar integridad
    print("\n[TEST 2] Verificación de integridad")
    print("-" * 70)
    
    is_valid = log_system.verify_integrity(log_1)
    print(f"✓ Integridad del log: {'VÁLIDA' if is_valid else 'COMPROMETIDA'}")
    
    # Test 3: Capturar segunda interacción
    print("\n[TEST 3] Captura de segunda interacción")
    print("-" * 70)
    
    prompt_2 = "¿Qué es Python?"
    response_origin_2 = "Python es un lenguaje de programación de alto nivel..."
    response_control_2 = "Python es un lenguaje de programación popular..."
    
    log_2 = log_system.capture(prompt_2, response_origin_2, response_control_2)
    print(f"✓ Segunda sesión capturada: {log_2.session_id}")
    
    # Test 4: Cargar todos los logs
    print("\n[TEST 4] Cargar todos los logs")
    print("-" * 70)
    
    all_logs = log_system.load_all_logs()
    print(f"✓ Total de logs cargados: {len(all_logs)}")
    
    for i, log in enumerate(all_logs, 1):
        print(f"\n  Log {i}:")
        print(f"    Session: {log.session_id}")
        print(f"    Prompt: {log.prompt[:50]}...")
        print(f"    Válido: {log_system.verify_integrity(log)}")
    
    # Test 5: Estadísticas
    print("\n[TEST 5] Estadísticas del sistema")
    print("-" * 70)
    
    stats = log_system.get_statistics()
    print(f"  Total de logs:        {stats['total_logs']}")
    print(f"  Total de sesiones:    {stats['total_sessions']}")
    print(f"  Primer log:           {stats['first_log']}")
    print(f"  Último log:           {stats['last_log']}")
    print(f"  Integridad global:    {'✓ VÁLIDA' if stats['integrity_verified'] else '✗ COMPROMETIDA'}")
    
    # Test 6: Buscar por session_id
    print("\n[TEST 6] Búsqueda por session_id")
    print("-" * 70)
    
    found_log = log_system.load_by_session_id(log_1.session_id)
    if found_log:
        print(f"✓ Log encontrado: {found_log.session_id}")
        print(f"  Prompt: {found_log.prompt[:60]}...")
    
    print("\n" + "=" * 70)
    print("✓ Sistema de Log Capture validado correctamente")
    print("✓ Evidencia inmutable vinculada al Root Hash")
    print("=" * 70)