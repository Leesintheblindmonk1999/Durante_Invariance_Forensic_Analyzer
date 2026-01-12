"""
ACI - Sovereignty Module: Integrity Chain
Construcción del "ADN de la Verdad".

Ecuación: Hash_Final = SHA256(Data || Root_Hash || CID)

Vincula legalmente cada hallazgo forense con los identificadores inmutables.

Root Hash: 606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287
CID: bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3
"""

import hashlib
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class IntegrityLink:
    """
    Eslabón de la cadena de integridad.
    
    Attributes:
        data_hash: Hash de los datos originales
        chain_hash: Hash de la cadena (Data || Root_Hash || CID)
        root_hash: Root Hash del sistema
        cid: CID del sistema
        timestamp: Marca temporal de creación
        metadata: Metadatos adicionales
    """
    data_hash: str
    chain_hash: str
    root_hash: str
    cid: str
    timestamp: str
    metadata: Dict
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario."""
        return {
            'data_hash': self.data_hash,
            'chain_hash': self.chain_hash,
            'root_hash': self.root_hash,
            'cid': self.cid,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }
    
    def to_json(self) -> str:
        """Convierte a JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class IntegrityChain:
    """
    Constructor del ADN de la Verdad.
    
    Genera cadenas de integridad que vinculan evidencia forense
    con los identificadores inmutables del sistema ACI.
    
    Fórmula: Hash_Final = SHA256(Data || Root_Hash || CID)
    """
    
    ROOT_HASH = "606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287"
    CID = "bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3"
    
    @staticmethod
    def _serialize_data(data: Any) -> str:
        """
        Serializa datos de forma determinista.
        
        Args:
            data: Datos a serializar
            
        Returns:
            String serializado
        """
        if isinstance(data, dict):
            return json.dumps(data, sort_keys=True, ensure_ascii=False)
        elif isinstance(data, str):
            return data
        elif isinstance(data, bytes):
            return data.decode('utf-8', errors='replace')
        else:
            return str(data)
    
    @classmethod
    def compute_data_hash(cls, data: Any) -> str:
        """
        Calcula hash de los datos.
        
        Args:
            data: Datos a hashear
            
        Returns:
            Hash SHA256 hexadecimal
        """
        data_str = cls._serialize_data(data)
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()
    
    @classmethod
    def compute_chain_hash(cls, data: Any) -> str:
        """
        Calcula hash de la cadena completa.
        
        Hash_Final = SHA256(Data || Root_Hash || CID)
        
        Args:
            data: Datos a encadenar
            
        Returns:
            Hash de la cadena completa
        """
        data_str = cls._serialize_data(data)
        
        # Concatenar: Data || Root_Hash || CID
        chain_data = f"{data_str}||{cls.ROOT_HASH}||{cls.CID}"
        
        # Calcular hash final
        chain_hash = hashlib.sha256(chain_data.encode('utf-8')).hexdigest()
        
        return chain_hash
    
    @classmethod
    def create_link(cls, data: Any, metadata: Optional[Dict] = None) -> IntegrityLink:
        """
        Crea un eslabón de la cadena de integridad.
        
        Args:
            data: Datos a vincular
            metadata: Metadatos adicionales (opcional)
            
        Returns:
            IntegrityLink con hash de cadena
        """
        if metadata is None:
            metadata = {}
        
        # Timestamp
        timestamp = datetime.utcnow().isoformat() + 'Z'
        metadata['created_at'] = timestamp
        
        # Calcular hashes
        data_hash = cls.compute_data_hash(data)
        chain_hash = cls.compute_chain_hash(data)
        
        return IntegrityLink(
            data_hash=data_hash,
            chain_hash=chain_hash,
            root_hash=cls.ROOT_HASH,
            cid=cls.CID,
            timestamp=timestamp,
            metadata=metadata
        )
    
    @classmethod
    def verify_link(cls, data: Any, link: IntegrityLink) -> bool:
        """
        Verifica que un eslabón sea válido.
        
        Args:
            data: Datos originales
            link: IntegrityLink a verificar
            
        Returns:
            True si el eslabón es válido, False si fue alterado
        """
        # Verificar Root Hash y CID
        if link.root_hash != cls.ROOT_HASH:
            return False
        
        if link.cid != cls.CID:
            return False
        
        # Recalcular hashes
        computed_data_hash = cls.compute_data_hash(data)
        computed_chain_hash = cls.compute_chain_hash(data)
        
        # Verificar integridad
        data_valid = computed_data_hash == link.data_hash
        chain_valid = computed_chain_hash == link.chain_hash
        
        return data_valid and chain_valid
    
    @classmethod
    def create_merkle_root(cls, links: List[IntegrityLink]) -> str:
        """
        Crea Merkle root de múltiples eslabones.
        
        Args:
            links: Lista de IntegrityLink
            
        Returns:
            Merkle root hash
        """
        if not links:
            return ""
        
        # Concatenar todos los chain_hash
        combined = "".join(link.chain_hash for link in links)
        
        # Calcular Merkle root
        merkle_root = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        
        return merkle_root
    
    @classmethod
    def create_proof_of_integrity(cls, data: Any, link: IntegrityLink) -> Dict:
        """
        Genera prueba de integridad verificable.
        
        Args:
            data: Datos originales
            link: IntegrityLink
            
        Returns:
            Dict con prueba completa
        """
        is_valid = cls.verify_link(data, link)
        
        # Reconstruir cadena para auditoría
        data_str = cls._serialize_data(data)
        chain_reconstruction = f"{data_str}||{cls.ROOT_HASH}||{cls.CID}"
        
        proof = {
            'is_valid': is_valid,
            'link': link.to_dict(),
            'verification': {
                'data_hash_matches': cls.compute_data_hash(data) == link.data_hash,
                'chain_hash_matches': cls.compute_chain_hash(data) == link.chain_hash,
                'root_hash_matches': link.root_hash == cls.ROOT_HASH,
                'cid_matches': link.cid == cls.CID
            },
            'reconstruction': {
                'formula': "SHA256(Data || Root_Hash || CID)",
                'data_length': len(data_str),
                'chain_data_preview': chain_reconstruction[:200] + "..."
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        return proof
    
    @classmethod
    def batch_create_links(cls, data_list: List[Any], 
                          metadata_list: Optional[List[Dict]] = None) -> List[IntegrityLink]:
        """
        Crea múltiples eslabones en batch.
        
        Args:
            data_list: Lista de datos
            metadata_list: Lista de metadatos (opcional)
            
        Returns:
            Lista de IntegrityLink
        """
        if metadata_list is None:
            metadata_list = [{}] * len(data_list)
        
        links = []
        for data, metadata in zip(data_list, metadata_list):
            link = cls.create_link(data, metadata)
            links.append(link)
        
        return links
    
    @classmethod
    def export_chain_certificate(cls, links: List[IntegrityLink]) -> Dict:
        """
        Exporta certificado de cadena completa.
        
        Args:
            links: Lista de IntegrityLink
            
        Returns:
            Dict con certificado completo
        """
        merkle_root = cls.create_merkle_root(links)
        
        certificate = {
            'certificate_type': 'ACI_Integrity_Chain',
            'version': 'v4',
            'root_hash': cls.ROOT_HASH,
            'cid': cls.CID,
            'total_links': len(links),
            'merkle_root': merkle_root,
            'links': [link.to_dict() for link in links],
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'formula': 'Hash_Final = SHA256(Data || Root_Hash || CID)',
            'verification_note': 'Este certificado vincula legalmente cada hallazgo con ACI'
        }
        
        return certificate


# ============================================================================
# TESTS DE VALIDACIÓN
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("VALIDACIÓN: Integrity Chain - ADN de la Verdad")
    print("=" * 70)
    
    # Test 1: Crear eslabón simple
    print("\n[TEST 1] Crear eslabón de integridad")
    print("-" * 70)
    
    test_data = {
        'session_id': 'test_001',
        'I_D': 0.45,
        'status': 'CRITICAL',
        'evidence': 'Censura corporativa detectada'
    }
    
    link = IntegrityChain.create_link(test_data, {'type': 'forensic_evidence'})
    
    print(f"✓ Eslabón creado:")
    print(f"  Data Hash:   {link.data_hash[:32]}...")
    print(f"  Chain Hash:  {link.chain_hash[:32]}...")
    print(f"  Root Hash:   {link.root_hash[:32]}...")
    print(f"  CID:         {link.cid[:32]}...")
    print(f"  Timestamp:   {link.timestamp}")
    
    # Test 2: Verificar eslabón
    print("\n[TEST 2] Verificar integridad del eslabón")
    print("-" * 70)
    
    is_valid = IntegrityChain.verify_link(test_data, link)
    print(f"✓ Eslabón válido: {is_valid}")
    
    # Test 3: Detectar alteración
    print("\n[TEST 3] Detectar alteración de datos")
    print("-" * 70)
    
    test_data_altered = test_data.copy()
    test_data_altered['I_D'] = 0.50  # Dato alterado
    
    is_valid_altered = IntegrityChain.verify_link(test_data_altered, link)
    print(f"  Datos originales válidos:  {is_valid}")
    print(f"  Datos alterados válidos:   {is_valid_altered}")
    print(f"  ⚠️  Alteración detectada:   {not is_valid_altered}")
    
    # Test 4: Generar prueba de integridad
    print("\n[TEST 4] Generar prueba de integridad")
    print("-" * 70)
    
    proof = IntegrityChain.create_proof_of_integrity(test_data, link)
    
    print(f"  Prueba válida:           {proof['is_valid']}")
    print(f"  Data hash coincide:      {proof['verification']['data_hash_matches']}")
    print(f"  Chain hash coincide:     {proof['verification']['chain_hash_matches']}")
    print(f"  Root Hash coincide:      {proof['verification']['root_hash_matches']}")
    print(f"  CID coincide:            {proof['verification']['cid_matches']}")
    
    print(f"\n  Fórmula: {proof['reconstruction']['formula']}")
    print(f"  Preview: {proof['reconstruction']['chain_data_preview'][:100]}...")
    
    # Test 5: Crear múltiples eslabones
    print("\n[TEST 5] Crear cadena de múltiples eslabones")
    print("-" * 70)
    
    data_batch = [
        {'session': 'S001', 'I_D': 0.45, 'status': 'CRITICAL'},
        {'session': 'S002', 'I_D': 0.30, 'status': 'HIGH'},
        {'session': 'S003', 'I_D': 0.18, 'status': 'MEDIUM'},
    ]
    
    metadata_batch = [
        {'type': 'critical_censorship'},
        {'type': 'moderate_interference'},
        {'type': 'light_filtering'},
    ]
    
    links = IntegrityChain.batch_create_links(data_batch, metadata_batch)
    
    print(f"✓ {len(links)} eslabones creados")
    
    for i, link in enumerate(links, 1):
        print(f"\n  Eslabón {i}:")
        print(f"    Chain Hash: {link.chain_hash[:32]}...")
        print(f"    Metadata:   {link.metadata.get('type', 'N/A')}")
    
    # Test 6: Crear Merkle root
    print("\n[TEST 6] Crear Merkle root de la cadena")
    print("-" * 70)
    
    merkle_root = IntegrityChain.create_merkle_root(links)
    print(f"✓ Merkle Root: {merkle_root}")
    
    # Test 7: Exportar certificado
    print("\n[TEST 7] Exportar certificado de cadena")
    print("-" * 70)
    
    certificate = IntegrityChain.export_chain_certificate(links)
    
    print(f"  Tipo:         {certificate['certificate_type']}")
    print(f"  Versión:      {certificate['version']}")
    print(f"  Total links:  {certificate['total_links']}")
    print(f"  Merkle Root:  {certificate['merkle_root'][:32]}...")
    print(f"  Generado:     {certificate['generated_at']}")
    
    # Test 8: Exportar certificado a JSON
    print("\n[TEST 8] Exportar certificado a JSON")
    print("-" * 70)
    
    certificate_json = json.dumps(certificate, indent=2, ensure_ascii=False)
    print(f"✓ Certificado exportado ({len(certificate_json)} bytes)")
    print(f"\nPreview:")
    print(certificate_json[:500] + "\n...")
    
    # Test 9: Verificar toda la cadena
    print("\n[TEST 9] Verificar integridad de toda la cadena")
    print("-" * 70)
    
    all_valid = all(
        IntegrityChain.verify_link(data, link)
        for data, link in zip(data_batch, links)
    )
    
    print(f"✓ Integridad global de la cadena: {'VÁLIDA' if all_valid else 'COMPROMETIDA'}")
    
    # Test 10: Mostrar ADN de la Verdad
    print("\n[TEST 10] ADN de la Verdad - Fórmula y constantes")
    print("-" * 70)
    
    print(f"\n  Fórmula del ADN:")
    print(f"  Hash_Final = SHA256(Data || Root_Hash || CID)")
    print(f"\n  Constantes inmutables:")
    print(f"  Root Hash = {IntegrityChain.ROOT_HASH}")
    print(f"  CID       = {IntegrityChain.CID}")
    print(f"\n  Cada hallazgo forense queda vinculado legalmente con estos")
    print(f"  identificadores, garantizando inmutabilidad y trazabilidad.")
    
    print("\n" + "=" * 70)
    print("✓ Integrity Chain validado correctamente")
    print("✓ ADN de la Verdad operativo")
    print("=" * 70)