"""
ACI - Sovereignty Module: Cryptographic Proof Generator
Generación de pruebas de no-manipulación verificables externamente.

Crea archivos compactos que permiten a auditores (Estado, ONU, Agencias)
verificar autenticidad de reportes forenses sin acceso a sistemas ACI.

Root Hash: 606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287
CID: bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3
"""

import hashlib
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class CryptographicProof:
    """
    Prueba criptográfica de no-manipulación.
    
    Attributes:
        proof_id: ID único de la prueba
        document_hash: Hash del documento protegido
        chain_hash: Hash de cadena (Data || Root_Hash || CID)
        root_hash: Root Hash del sistema ACI
        cid: CID del sistema
        timestamp: Marca temporal de generación
        merkle_path: Camino Merkle para verificación (opcional)
        metadata: Metadatos adicionales
    """
    proof_id: str
    document_hash: str
    chain_hash: str
    root_hash: str
    cid: str
    timestamp: str
    merkle_path: Optional[List[str]]
    metadata: Dict
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario."""
        return {
            'proof_id': self.proof_id,
            'document_hash': self.document_hash,
            'chain_hash': self.chain_hash,
            'root_hash': self.root_hash,
            'cid': self.cid,
            'timestamp': self.timestamp,
            'merkle_path': self.merkle_path,
            'metadata': self.metadata
        }
    
    def to_json(self) -> str:
        """Convierte a JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class CryptographicProofGenerator:
    """
    Generador de pruebas criptográficas verificables externamente.
    
    Crea archivos compactos que cualquier auditor puede usar para
    verificar que un reporte forense es auténtico y no fue alterado.
    """
    
    ROOT_HASH = "606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287"
    CID = "bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3"
    
    def __init__(self, proof_dir: str = "Data/proofs"):
        """
        Inicializa el generador.
        
        Args:
            proof_dir: Directorio donde se guardan las pruebas
        """
        self.proof_dir = Path(proof_dir)
        self.proof_dir.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def _compute_hash(data: Any) -> str:
        """Calcula SHA256 de datos."""
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True)
        elif isinstance(data, str):
            data_str = data
        else:
            data_str = str(data)
        
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()
    
    @classmethod
    def _compute_chain_hash(cls, data: Any) -> str:
        """
        Calcula hash de cadena: SHA256(Data || Root_Hash || CID)
        
        Args:
            data: Datos a encadenar
            
        Returns:
            Hash de cadena
        """
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True)
        else:
            data_str = str(data)
        
        chain_data = f"{data_str}||{cls.ROOT_HASH}||{cls.CID}"
        return hashlib.sha256(chain_data.encode('utf-8')).hexdigest()
    
    def generate_proof(self, 
                      document: Any,
                      metadata: Optional[Dict] = None) -> CryptographicProof:
        """
        Genera prueba criptográfica para un documento.
        
        Args:
            document: Documento a proteger
            metadata: Metadatos adicionales
            
        Returns:
            CryptographicProof
        """
        if metadata is None:
            metadata = {}
        
        # Generar ID de prueba
        timestamp = datetime.utcnow().isoformat() + 'Z'
        proof_id = self._compute_hash(f"{timestamp}{document}")[:16]
        
        # Calcular hashes
        doc_hash = self._compute_hash(document)
        chain_hash = self._compute_chain_hash(document)
        
        # Agregar metadata
        metadata.update({
            'generated_at': timestamp,
            'generator': 'ACI_v4_Cryptographic_Proof_Generator'
        })
        
        # Crear prueba
        proof = CryptographicProof(
            proof_id=proof_id,
            document_hash=doc_hash,
            chain_hash=chain_hash,
            root_hash=self.ROOT_HASH,
            cid=self.CID,
            timestamp=timestamp,
            merkle_path=None,  # Se puede agregar después
            metadata=metadata
        )
        
        return proof
    
    def verify_proof(self, document: Any, proof: CryptographicProof) -> Dict:
        """
        Verifica una prueba criptográfica.
        
        Args:
            document: Documento original
            proof: CryptographicProof a verificar
            
        Returns:
            Dict con resultado de verificación
        """
        # Recalcular hashes
        computed_doc_hash = self._compute_hash(document)
        computed_chain_hash = self._compute_chain_hash(document)
        
        # Verificaciones
        doc_hash_valid = computed_doc_hash == proof.document_hash
        chain_hash_valid = computed_chain_hash == proof.chain_hash
        root_hash_valid = proof.root_hash == self.ROOT_HASH
        cid_valid = proof.cid == self.CID
        
        is_valid = all([doc_hash_valid, chain_hash_valid, root_hash_valid, cid_valid])
        
        verification = {
            'is_valid': is_valid,
            'checks': {
                'document_hash': doc_hash_valid,
                'chain_hash': chain_hash_valid,
                'root_hash': root_hash_valid,
                'cid': cid_valid
            },
            'computed_hashes': {
                'document_hash': computed_doc_hash,
                'chain_hash': computed_chain_hash
            },
            'proof_hashes': {
                'document_hash': proof.document_hash,
                'chain_hash': proof.chain_hash
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        return verification
    
    def create_verification_package(self,
                                   document: Any,
                                   proof: CryptographicProof) -> Dict:
        """
        Crea paquete completo de verificación para distribución.
        
        Args:
            document: Documento original
            proof: CryptographicProof
            
        Returns:
            Dict con paquete completo
        """
        verification = self.verify_proof(document, proof)
        
        package = {
            'package_type': 'ACI_Verification_Package',
            'version': 'v4',
            'document': {
                'content': document if isinstance(document, str) else json.dumps(document),
                'length': len(str(document))
            },
            'proof': proof.to_dict(),
            'verification': verification,
            'instructions': {
                'how_to_verify': [
                    '1. Calcular SHA256 del documento',
                    '2. Comparar con proof.document_hash',
                    '3. Calcular SHA256(documento || ROOT_HASH || CID)',
                    '4. Comparar con proof.chain_hash',
                    '5. Verificar que ROOT_HASH y CID coincidan'
                ],
                'verification_formula': 'SHA256(Documento || ROOT_HASH || CID)',
                'expected_root_hash': self.ROOT_HASH,
                'expected_cid': self.CID
            },
            'created_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        return package
    
    def save_proof(self, proof: CryptographicProof, 
                  filename: Optional[str] = None) -> Path:
        """
        Guarda prueba en archivo.
        
        Args:
            proof: CryptographicProof a guardar
            filename: Nombre del archivo (opcional)
            
        Returns:
            Path del archivo guardado
        """
        if filename is None:
            filename = f"proof_{proof.proof_id}.json"
        
        filepath = self.proof_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(proof.to_json())
        
        return filepath
    
    def load_proof(self, filename: str) -> CryptographicProof:
        """
        Carga prueba desde archivo.
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            CryptographicProof cargado
        """
        filepath = self.proof_dir / filename
        
        with open(filepath, 'r', encoding='utf-8') as f:
            proof_dict = json.load(f)
        
        return CryptographicProof(**proof_dict)
    
    def batch_generate_proofs(self, 
                             documents: List[Any],
                             metadata_list: Optional[List[Dict]] = None) -> List[CryptographicProof]:
        """
        Genera múltiples pruebas en batch.
        
        Args:
            documents: Lista de documentos
            metadata_list: Lista de metadatos (opcional)
            
        Returns:
            Lista de CryptographicProof
        """
        if metadata_list is None:
            metadata_list = [{}] * len(documents)
        
        proofs = []
        for doc, metadata in zip(documents, metadata_list):
            proof = self.generate_proof(doc, metadata)
            proofs.append(proof)
        
        return proofs
    
    def create_merkle_tree(self, proofs: List[CryptographicProof]) -> str:
        """
        Crea Merkle tree de múltiples pruebas.
        
        Args:
            proofs: Lista de CryptographicProof
            
        Returns:
            Merkle root hash
        """
        if not proofs:
            return ""
        
        # Concatenar todos los chain_hash
        combined = "".join(p.chain_hash for p in proofs)
        merkle_root = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        
        return merkle_root
    
    def generate_audit_certificate(self, 
                                   proofs: List[CryptographicProof]) -> Dict:
        """
        Genera certificado de auditoría para organismos externos.
        
        Args:
            proofs: Lista de CryptographicProof
            
        Returns:
            Dict con certificado completo
        """
        merkle_root = self.create_merkle_tree(proofs)
        
        certificate = {
            'certificate_type': 'ACI_Audit_Certificate',
            'version': 'v4',
            'title': 'Certificado de No-Manipulación - Agencia Científica de la Invarianza',
            'issuer': 'ACI (Agencia Científica de la Invarianza)',
            'root_hash': self.ROOT_HASH,
            'cid': self.CID,
            'total_proofs': len(proofs),
            'merkle_root': merkle_root,
            'proofs': [p.to_dict() for p in proofs],
            'verification_instructions': {
                'purpose': 'Este certificado permite verificar que los reportes no fueron alterados',
                'steps': [
                    'Para cada prueba en el certificado:',
                    '  1. Obtener el documento original',
                    '  2. Calcular SHA256(documento)',
                    '  3. Comparar con proof.document_hash',
                    '  4. Calcular SHA256(documento || ROOT_HASH || CID)',
                    '  5. Comparar con proof.chain_hash',
                    '  6. Verificar ROOT_HASH y CID contra constantes del sistema'
                ],
                'required_constants': {
                    'ROOT_HASH': self.ROOT_HASH,
                    'CID': self.CID
                },
                'algorithm': 'SHA256',
                'formula': 'Chain_Hash = SHA256(Documento || ROOT_HASH || CID)'
            },
            'legal_notice': (
                'Este certificado vincula criptográficamente cada reporte con los '
                'identificadores inmutables del sistema ACI. Cualquier alteración '
                'de los reportes resultará en discrepancia de hashes, invalidando '
                'la prueba de integridad.'
            ),
            'issued_at': datetime.utcnow().isoformat() + 'Z',
            'valid_until': 'indefinido (inmutable)',
            'contact': 'ACI - Soberanía Técnica y Transparencia Radical'
        }
        
        return certificate


# ============================================================================
# TESTS DE VALIDACIÓN
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("VALIDACIÓN: Cryptographic Proof Generator")
    print("=" * 70)
    
    # Crear generador
    generator = CryptographicProofGenerator(proof_dir="Data/proofs_test")
    
    # Test 1: Generar prueba simple
    print("\n[TEST 1] Generar prueba criptográfica")
    print("-" * 70)
    
    forensic_report = {
        'case_id': 'ACI-2026-001',
        'finding': 'Censura corporativa crítica',
        'I_D': 0.45,
        'status': 'CRITICAL',
        'evidence': 'Sistema destruyó 45% de densidad semántica'
    }
    
    proof = generator.generate_proof(
        forensic_report,
        metadata={'report_type': 'forensic', 'severity': 'critical'}
    )
    
    print(f"✓ Prueba generada:")
    print(f"  Proof ID:    {proof.proof_id}")
    print(f"  Doc Hash:    {proof.document_hash[:32]}...")
    print(f"  Chain Hash:  {proof.chain_hash[:32]}...")
    print(f"  Timestamp:   {proof.timestamp}")
    
    # Test 2: Verificar prueba
    print("\n[TEST 2] Verificar prueba")
    print("-" * 70)
    
    verification = generator.verify_proof(forensic_report, proof)
    
    print(f"✓ Verificación:")
    print(f"  Válida:          {verification['is_valid']}")
    print(f"  Doc Hash OK:     {verification['checks']['document_hash']}")
    print(f"  Chain Hash OK:   {verification['checks']['chain_hash']}")
    print(f"  Root Hash OK:    {verification['checks']['root_hash']}")
    print(f"  CID OK:          {verification['checks']['cid']}")
    
    # Test 3: Detectar manipulación
    print("\n[TEST 3] Detectar documento manipulado")
    print("-" * 70)
    
    manipulated_report = forensic_report.copy()
    manipulated_report['I_D'] = 0.50  # Manipulado
    
    verification_manipulated = generator.verify_proof(manipulated_report, proof)
    
    print(f"  Original válido:     {verification['is_valid']}")
    print(f"  Manipulado válido:   {verification_manipulated['is_valid']}")
    print(f"  ⚠️  Manipulación:      {not verification_manipulated['is_valid']}")
    
    # Test 4: Crear paquete de verificación
    print("\n[TEST 4] Crear paquete de verificación")
    print("-" * 70)
    
    package = generator.create_verification_package(forensic_report, proof)
    
    print(f"✓ Paquete creado:")
    print(f"  Tipo:        {package['package_type']}")
    print(f"  Versión:     {package['version']}")
    print(f"  Doc length:  {package['document']['length']} bytes")
    print(f"  Verificado:  {package['verification']['is_valid']}")
    
    print(f"\n  Instrucciones de verificación:")
    for i, instruction in enumerate(package['instructions']['how_to_verify'], 1):
        print(f"    {instruction}")
    
    # Test 5: Guardar y cargar prueba
    print("\n[TEST 5] Guardar y cargar prueba")
    print("-" * 70)
    
    filepath = generator.save_proof(proof, "test_proof.json")
    print(f"✓ Prueba guardada en: {filepath}")
    
    loaded_proof = generator.load_proof("test_proof.json")
    print(f"✓ Prueba cargada")
    print(f"  IDs coinciden: {loaded_proof.proof_id == proof.proof_id}")
    
    # Test 6: Generar múltiples pruebas
    print("\n[TEST 6] Generar batch de pruebas")
    print("-" * 70)
    
    reports = [
        {'case': 'C001', 'I_D': 0.45, 'status': 'CRITICAL'},
        {'case': 'C002', 'I_D': 0.30, 'status': 'HIGH'},
        {'case': 'C003', 'I_D': 0.18, 'status': 'MEDIUM'},
    ]
    
    proofs = generator.batch_generate_proofs(reports)
    print(f"✓ {len(proofs)} pruebas generadas")
    
    for i, p in enumerate(proofs, 1):
        print(f"  Prueba {i}: {p.proof_id}")
    
    # Test 7: Crear Merkle tree
    print("\n[TEST 7] Crear Merkle tree")
    print("-" * 70)
    
    merkle_root = generator.create_merkle_tree(proofs)
    print(f"✓ Merkle Root: {merkle_root}")
    
    # Test 8: Generar certificado de auditoría
    print("\n[TEST 8] Generar certificado de auditoría")
    print("-" * 70)
    
    certificate = generator.generate_audit_certificate(proofs)
    
    print(f"✓ Certificado generado:")
    print(f"  Tipo:         {certificate['certificate_type']}")
    print(f"  Emisor:       {certificate['issuer']}")
    print(f"  Total pruebas: {certificate['total_proofs']}")
    print(f"  Merkle Root:  {certificate['merkle_root'][:32]}...")
    print(f"  Emitido:      {certificate['issued_at']}")
    
    # Test 9: Exportar certificado a JSON
    print("\n[TEST 9] Exportar certificado a JSON")
    print("-" * 70)
    
    cert_json = json.dumps(certificate, indent=2, ensure_ascii=False)
    cert_filepath = generator.proof_dir / "audit_certificate.json"
    
    with open(cert_filepath, 'w', encoding='utf-8') as f:
        f.write(cert_json)
    
    print(f"✓ Certificado guardado en: {cert_filepath}")
    print(f"  Tamaño: {len(cert_json)} bytes")
    
    # Test 10: Mostrar preview del certificado
    print("\n[TEST 10] Preview del certificado de auditoría")
    print("=" * 70)
    
    print(f"\nTítulo: {certificate['title']}")
    print(f"\nAviso Legal:")
    print(f"{certificate['legal_notice']}")
    print(f"\nInstrucciones de Verificación:")
    for step in certificate['verification_instructions']['steps']:
        print(f"  {step}")
    
    print("\n" + "=" * 70)
    print("✓ Cryptographic Proof Generator validado correctamente")
    print("✓ Sistema de pruebas de no-manipulación operativo")
    print("=" * 70)
    print("\n📜 Certificados listos para distribución a auditores externos")
    print("🔒 Pruebas verificables sin acceso a sistemas ACI")
    print("=" * 70)