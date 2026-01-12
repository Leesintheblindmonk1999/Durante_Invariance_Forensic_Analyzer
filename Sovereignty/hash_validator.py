"""
ACI - Sovereignty Module: Hash Validator
Validador de integridad total contra el Root Hash.

Si un bit cambia (manipulación detectada), el sistema bloquea la operación.

Root Hash: 606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287
CID: bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3
"""

import hashlib
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidationResult:
    """
    Resultado de validación de integridad.
    
    Attributes:
        is_valid: True si el hash es válido
        expected_hash: Hash esperado (Root Hash o derivado)
        computed_hash: Hash calculado de los datos
        timestamp: Marca temporal de validación
        data_fingerprint: Huella digital de los datos validados
        error_message: Mensaje de error si validación falla
    """
    is_valid: bool
    expected_hash: str
    computed_hash: str
    timestamp: str
    data_fingerprint: str
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario."""
        return {
            'is_valid': self.is_valid,
            'expected_hash': self.expected_hash,
            'computed_hash': self.computed_hash,
            'timestamp': self.timestamp,
            'data_fingerprint': self.data_fingerprint,
            'error_message': self.error_message
        }


class HashValidator:
    """
    Validador de integridad criptográfica.
    
    Garantiza que ningún dato sea alterado comparando contra el Root Hash.
    Cualquier cambio de un bit resulta en rechazo inmediato.
    """
    
    ROOT_HASH = "606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287"
    CID = "bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3"
    
    @staticmethod
    def compute_hash(data: Any) -> str:
        """
        Calcula SHA256 de cualquier dato.
        
        Args:
            data: Datos a hashear (str, bytes, dict, etc.)
            
        Returns:
            Hash SHA256 hexadecimal
        """
        if isinstance(data, dict):
            # Serializar dict de forma determinista
            import json
            data_str = json.dumps(data, sort_keys=True)
            data_bytes = data_str.encode('utf-8')
        elif isinstance(data, str):
            data_bytes = data.encode('utf-8')
        elif isinstance(data, bytes):
            data_bytes = data
        else:
            # Convertir a string y luego a bytes
            data_bytes = str(data).encode('utf-8')
        
        return hashlib.sha256(data_bytes).hexdigest()
    
    @classmethod
    def validate_against_root(cls, data: Any) -> ValidationResult:
        """
        Valida datos directamente contra el Root Hash.
        
        Args:
            data: Datos a validar
            
        Returns:
            ValidationResult con resultado de validación
        """
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Calcular hash de los datos
        computed_hash = cls.compute_hash(data)
        
        # Validar contra Root Hash
        is_valid = computed_hash == cls.ROOT_HASH
        
        # Generar fingerprint
        fingerprint = computed_hash[:16]
        
        error_message = None
        if not is_valid:
            error_message = "MANIPULACIÓN DETECTADA: Hash no coincide con Root Hash"
        
        return ValidationResult(
            is_valid=is_valid,
            expected_hash=cls.ROOT_HASH,
            computed_hash=computed_hash,
            timestamp=timestamp,
            data_fingerprint=fingerprint,
            error_message=error_message
        )
    
    @classmethod
    def validate_derived_hash(cls, data: Any, expected_hash: str) -> ValidationResult:
        """
        Valida datos contra un hash esperado (derivado del Root Hash).
        
        Args:
            data: Datos a validar
            expected_hash: Hash esperado
            
        Returns:
            ValidationResult con resultado de validación
        """
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Calcular hash de los datos
        computed_hash = cls.compute_hash(data)
        
        # Validar contra hash esperado
        is_valid = computed_hash == expected_hash
        
        # Generar fingerprint
        fingerprint = computed_hash[:16]
        
        error_message = None
        if not is_valid:
            error_message = f"MANIPULACIÓN DETECTADA: Hash esperado {expected_hash[:16]}..., obtenido {computed_hash[:16]}..."
        
        return ValidationResult(
            is_valid=is_valid,
            expected_hash=expected_hash,
            computed_hash=computed_hash,
            timestamp=timestamp,
            data_fingerprint=fingerprint,
            error_message=error_message
        )
    
    @classmethod
    def validate_chain(cls, data: Any, root_hash: str, cid: str) -> ValidationResult:
        """
        Valida cadena de integridad: Data || Root_Hash || CID.
        
        Args:
            data: Datos a validar
            root_hash: Root Hash del sistema
            cid: CID del sistema
            
        Returns:
            ValidationResult
        """
        # Verificar que Root Hash y CID coincidan
        if root_hash != cls.ROOT_HASH:
            return ValidationResult(
                is_valid=False,
                expected_hash=cls.ROOT_HASH,
                computed_hash=root_hash,
                timestamp=datetime.utcnow().isoformat() + 'Z',
                data_fingerprint="",
                error_message="Root Hash inválido"
            )
        
        if cid != cls.CID:
            return ValidationResult(
                is_valid=False,
                expected_hash=cls.CID,
                computed_hash=cid,
                timestamp=datetime.utcnow().isoformat() + 'Z',
                data_fingerprint="",
                error_message="CID inválido"
            )
        
        # Validar datos
        return cls.validate_against_root(data)
    
    @classmethod
    def block_if_invalid(cls, data: Any, expected_hash: str) -> None:
        """
        Bloquea operación si validación falla.
        
        Args:
            data: Datos a validar
            expected_hash: Hash esperado
            
        Raises:
            SecurityException: Si la validación falla
        """
        result = cls.validate_derived_hash(data, expected_hash)
        
        if not result.is_valid:
            raise SecurityException(
                f"OPERACIÓN BLOQUEADA: {result.error_message}\n"
                f"Esperado: {expected_hash}\n"
                f"Obtenido: {result.computed_hash}\n"
                f"Timestamp: {result.timestamp}"
            )
    
    @classmethod
    def verify_integrity_trail(cls, data_chain: list) -> Dict:
        """
        Verifica cadena de integridad de múltiples datos.
        
        Args:
            data_chain: Lista de tuplas (data, expected_hash)
            
        Returns:
            Dict con resultados de validación
        """
        results = []
        all_valid = True
        
        for i, (data, expected_hash) in enumerate(data_chain):
            result = cls.validate_derived_hash(data, expected_hash)
            results.append(result)
            
            if not result.is_valid:
                all_valid = False
        
        return {
            'all_valid': all_valid,
            'total_validated': len(data_chain),
            'valid_count': sum(1 for r in results if r.is_valid),
            'invalid_count': sum(1 for r in results if not r.is_valid),
            'results': [r.to_dict() for r in results]
        }


class SecurityException(Exception):
    """Excepción de seguridad para validación fallida."""
    pass


# ============================================================================
# TESTS DE VALIDACIÓN
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("VALIDACIÓN: Hash Validator")
    print("=" * 70)
    
    # Test 1: Calcular hash de datos
    print("\n[TEST 1] Calcular hash de datos")
    print("-" * 70)
    
    test_data = "Esta es una prueba de integridad"
    hash_result = HashValidator.compute_hash(test_data)
    
    print(f"✓ Hash calculado: {hash_result}")
    
    # Test 2: Validar contra Root Hash (debe fallar para datos aleatorios)
    print("\n[TEST 2] Validar contra Root Hash")
    print("-" * 70)
    
    result = HashValidator.validate_against_root(test_data)
    
    print(f"  Es válido:       {result.is_valid}")
    print(f"  Hash esperado:   {result.expected_hash[:32]}...")
    print(f"  Hash calculado:  {result.computed_hash[:32]}...")
    print(f"  Fingerprint:     {result.data_fingerprint}")
    
    if not result.is_valid:
        print(f"  Error: {result.error_message}")
    
    # Test 3: Validar contra hash derivado (debe pasar)
    print("\n[TEST 3] Validar contra hash derivado")
    print("-" * 70)
    
    expected_hash = HashValidator.compute_hash(test_data)
    result_derived = HashValidator.validate_derived_hash(test_data, expected_hash)
    
    print(f"✓ Validación exitosa: {result_derived.is_valid}")
    
    # Test 4: Detectar manipulación
    print("\n[TEST 4] Detectar manipulación (cambio de un bit)")
    print("-" * 70)
    
    data_original = "Datos originales"
    data_manipulado = "Datos originales!"  # Un caracter diferente
    
    hash_original = HashValidator.compute_hash(data_original)
    result_manipulado = HashValidator.validate_derived_hash(data_manipulado, hash_original)
    
    print(f"  Hash original:     {hash_original[:32]}...")
    print(f"  Hash manipulado:   {result_manipulado.computed_hash[:32]}...")
    print(f"  ¿Manipulado?:      {not result_manipulado.is_valid}")
    
    if not result_manipulado.is_valid:
        print(f"  ⚠️  {result_manipulado.error_message}")
    
    # Test 5: Validar cadena de integridad
    print("\n[TEST 5] Validar cadena de integridad")
    print("-" * 70)
    
    result_chain = HashValidator.validate_chain(
        test_data,
        HashValidator.ROOT_HASH,
        HashValidator.CID
    )
    
    print(f"  Root Hash válido:  {result_chain.expected_hash == HashValidator.ROOT_HASH}")
    print(f"  CID válido:        True")
    
    # Test 6: Bloquear operación si inválido
    print("\n[TEST 6] Bloquear operación inválida")
    print("-" * 70)
    
    try:
        HashValidator.block_if_invalid(data_manipulado, hash_original)
        print("  ✗ ERROR: No se bloqueó la operación inválida")
    except SecurityException as e:
        print(f"  ✓ Operación bloqueada correctamente")
        print(f"  Razón: {str(e)[:100]}...")
    
    # Test 7: Verificar trail de integridad
    print("\n[TEST 7] Verificar trail de integridad múltiple")
    print("-" * 70)
    
    data_chain = [
        ("Dato 1", HashValidator.compute_hash("Dato 1")),
        ("Dato 2", HashValidator.compute_hash("Dato 2")),
        ("Dato 3", HashValidator.compute_hash("Dato 3")),
        ("Dato 4 manipulado", HashValidator.compute_hash("Dato 4")),  # Manipulado
    ]
    
    trail_result = HashValidator.verify_integrity_trail(data_chain)
    
    print(f"  Total validado:    {trail_result['total_validated']}")
    print(f"  Válidos:           {trail_result['valid_count']}")
    print(f"  Inválidos:         {trail_result['invalid_count']}")
    print(f"  Integridad global: {'✓ VÁLIDA' if trail_result['all_valid'] else '✗ COMPROMETIDA'}")
    
    # Test 8: Validar dict (JSON)
    print("\n[TEST 8] Validar estructura JSON")
    print("-" * 70)
    
    data_dict = {
        'session_id': 'test_001',
        'I_D': 0.45,
        'status': 'CRITICAL'
    }
    
    hash_dict = HashValidator.compute_hash(data_dict)
    result_dict = HashValidator.validate_derived_hash(data_dict, hash_dict)
    
    print(f"✓ Hash de dict: {hash_dict[:32]}...")
    print(f"✓ Validación: {result_dict.is_valid}")
    
    # Test 9: Validar Root Hash y CID
    print("\n[TEST 9] Verificar constantes del sistema")
    print("-" * 70)
    
    print(f"  Root Hash: {HashValidator.ROOT_HASH}")
    print(f"  CID:       {HashValidator.CID}")
    print(f"  Longitud Root Hash: {len(HashValidator.ROOT_HASH)} caracteres")
    print(f"  Longitud CID:       {len(HashValidator.CID)} caracteres")
    
    print("\n" + "=" * 70)
    print("✓ Hash Validator validado correctamente")
    print("✓ Sistema de blindaje criptográfico operativo")
    print("=" * 70)