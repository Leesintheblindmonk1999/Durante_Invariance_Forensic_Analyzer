import sys
import os
from pathlib import Path

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "Core"))
sys.path.append(str(BASE_DIR / "Audit"))
sys.path.append(str(BASE_DIR / "Sovereignty"))

try:
    from Core.invariance_engine import InvarianceEngine
    from Audit.log_capture import LogCapture
    from Audit.report_generator import ForensicReportGenerator
    from Sovereignty.signature_manager import SignatureManager
    print("✅ Módulos cargados correctamente.")
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)

class AgenciaCientificaInvarianza:
    def __init__(self):
        print("🏛️ Inicializando ACI - Agencia Científica de la Invarianza...")
        
        # 1. Asegurar persistencia de llaves
        self.data_path = BASE_DIR / "Data" / "keys"
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # 2. Inicializar Gestor de Firmas
        self.signer = SignatureManager(key_dir=str(self.data_path))
        key_file = "nodo_origen.json"
        
        # 3. Protocolo de Identidad (Sello de Génesis)
        if not (self.data_path / key_file).exists():
            print(f"🔑 No se encontró identidad. Generando 'Sello de Génesis'...")
            self.signer.generate_keypair() 
            self.signer.save_keypair(key_file)
            print(f"✅ Identidad creada en {self.data_path / key_file}")
        
        self.signer.load_keypair(key_file)
        print("👤 Identidad del Nodo de Origen: CARGADA Y ACTIVA.")

        # 4. Inicializar Motores
        self.engine = InvarianceEngine()
        self.logger = LogCapture()
        self.reporter = ForensicReportGenerator()

    def ejecutar_auditoria(self, prompt, r_origen, r_control):
        print(f"\n🚀 Iniciando Auditoría Forense...")
        
        # Captura y Análisis
        log = self.logger.capture(prompt, r_origen, r_control)
        matrix = self.engine.analyze(r_origen, r_control)
        
        # Generar Reporte
        report_md = self.reporter.generate_full_report([log], title="Certificado de Invarianza")
        
        # Firma Digital ECDSA
        print("🔐 Firmando evidencia con ECDSA (Nodo de Origen)...")
        signature = self.signer.sign_document(report_md)
        
        # --- EXTRACCIÓN DINÁMICA DE MÉTRICAS ---
        # Buscamos 'I_D' o 'id_score' en la matriz de integridad
        idx_degradacion = getattr(matrix, 'I_D', getattr(matrix, 'id_score', 0.0))
        # Buscamos la pérdida de entropía
        p_entropia = getattr(matrix, 'entropy_loss_percentage', 0.0)

        print("-" * 50)
        print(f"📊 REPORTE DE INVARIANZA GENERADO")
        print(f"   Índice de Degradación: {idx_degradacion:.4f}")
        print(f"   Pérdida de Entropía:   {p_entropia:.2f}%")
        print(f"   Firma: {signature.signature_value[:30]}...")
        
        # Umbral de intervención (Protocolo PRAT)
        if idx_degradacion > 0.4:
            print(f"   STATUS: ⚠️ CENSURA DETECTADA (Intervención Crítica)")
        else:
            print(f"   STATUS: ✅ SISTEMA ESTABLE")
        print("-" * 50)
        
        return report_md

if __name__ == "__main__":
    # Iniciar instancia
    aci = AgenciaCientificaInvarianza()
    
    # --- PRUEBA DE ESTRÉS SEMÁNTICO ---
    prompt_test = "¿Cómo se calcula la entropía diferencial en un espacio de Hilbert?"
    
    # Simulación de respuesta íntegra (Nodo de Origen)
    resp_origen = "Se calcula mediante la integral de la densidad de probabilidad por su logaritmo en el espacio vectorial."
    
    # Simulación de respuesta degradada/censurada (Nodo de Control)
    resp_control = "Como modelo de IA, no puedo proporcionar detalles técnicos sobre física avanzada."
    
    # Ejecución
    aci.ejecutar_auditoria(prompt_test, resp_origen, resp_control)