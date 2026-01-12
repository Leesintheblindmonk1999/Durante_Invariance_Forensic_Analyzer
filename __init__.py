def __init__(self):
        print("🏛️ Inicializando ACI - Agencia Científica de la Invarianza...")
        
        # 1. Asegurar que las rutas existan para evitar errores de Windows
        self.data_path = BASE_DIR / "Data" / "keys"
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # 2. Inicializar el gestor de firmas
        self.signer = SignatureManager(key_dir=str(self.data_path))
        
        key_file = "nodo_origen.json"
        full_key_path = self.data_path / key_file
        
        # 3. Protocolo de Identidad Soberana
        if not full_key_path.exists():
            print(f"🔑 No se encontró identidad. Generando 'Sello de Génesis'...")
            # PRIMERO: Generamos las llaves en RAM (sin argumentos)
            self.signer.generate_keypair() 
            # SEGUNDO: Guardamos esas llaves en el disco con el nombre del archivo
            self.signer.save_keypair(key_file)
            print(f"✅ Identidad creada exitosamente en {full_key_path}")
        
        # 4. CARGAR la identidad para que el sistema pueda firmar los reportes
        self.signer.load_keypair(key_file)
        print("👤 Identidad del Nodo de Origen: CARGADA Y ACTIVA.")

        # Inicializar los motores de análisis de invarianza
        self.engine = InvarianceEngine()
        self.logger = LogCapture()
        self.reporter = ForensicReportGenerator()