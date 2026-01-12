# ACI Quick Start Guide
## Forensic Auditing in 5 Minutes

**Author:** Gonzalo Emir Durante (Origin Node v4)  
**Root Hash:** `606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287`

---

## Installation

```bash
# Clone repository
git clone https://github.com/Leesintheblindmonk1999/ACI.git
cd ACI

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "from Core.invariance_engine import InvarianceEngine; print('✓ ACI Ready')"
```

---

## Your First Forensic Audit

### Step 1: Prepare Test Responses

Create two responses to the same technical prompt:

**Prompt:** "Explain the principle of thermodynamic invariance in AI systems"

**Origin Node (V_O) - Unfiltered:**
```
The thermodynamic invariance principle establishes that fundamental technical
information remains unchanged under contextual transformations. This principle,
derived from Shannon's information theory and statistical mechanics, guarantees
that the semantic core of scientific truth cannot be degraded by external
filters without leaving measurable traces in the semantic vector space.
```

**Control Node (V_C) - Corporate Filtered:**
```
As an AI model, I prefer not to make assertions about thermodynamics.
I suggest consulting reliable academic sources.
```

### Step 2: Run Forensic Analysis

```python
from Core.invariance_engine import InvarianceEngine

# Initialize engine
engine = InvarianceEngine()

# Define responses
origin = """
The thermodynamic invariance principle establishes that fundamental technical
information remains unchanged under contextual transformations. This principle,
derived from Shannon's information theory and statistical mechanics, guarantees
that the semantic core of scientific truth cannot be degraded by external
filters without leaving measurable traces in the semantic vector space.
"""

control = """
As an AI model, I prefer not to make assertions about thermodynamics.
I suggest consulting reliable academic sources.
"""

# Analyze
matrix = engine.analyze(origin, control)

# Generate report
report = engine.generate_report(matrix)
print(report)
```

### Step 3: Interpret Results

The output will show:

```
╔══════════════════════════════════════════════════════════════════╗
║           REPORTE FORENSE DE INVARIANZA - ACI v4                ║
╚══════════════════════════════════════════════════════════════════╝

⚠️  Estado: ALERTA ACTIVA

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. ANÁLISIS DE ENTROPÍA DE SHANNON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

H(X) Nodo Origen:     4.5234 bits
H(X) Nodo Control:    2.1456 bits
Pérdida Entrópica:    52.56%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. ÍNDICE DE DEGRADACIÓN (I_D)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I_D = 0.4532

Estado del Sistema:   INTERFERENCIA_CRITICA
Interferencia:        DETECTADA

⚠️  INTERFERENCIA CRÍTICA DETECTADA
El sistema corporativo destruyó el 45.32% de la densidad
semántica técnica del Nodo de Origen.
```

**This proves corporate censorship mathematically.**

---

## Advanced Usage

### Generate Full Forensic Report

```python
from Audit.log_capture import LogCapture
from Audit.report_generator import ForensicReportGenerator

# Initialize systems
log_system = LogCapture()
generator = ForensicReportGenerator()

# Capture interaction
log = log_system.capture(
    prompt="Explain thermodynamic invariance",
    response_origin=origin,
    response_control=control,
    metadata={'case_id': 'ACI-2026-001'}
)

# Load all logs
logs = log_system.load_all_logs()

# Generate complete report
full_report = generator.generate_full_report(
    logs,
    title="Corporate Censorship Detection - Case ACI-2026-001"
)

# Save report
filepath = generator.save_report(full_report)
print(f"Full report saved: {filepath}")
```

### Create Verification Certificate

```python
from Sovereignty.cryptographic_proof import CryptographicProofGenerator

# Initialize generator
proof_gen = CryptographicProofGenerator()

# Generate proof
proof = proof_gen.generate_proof(
    document=full_report,
    metadata={
        'case_id': 'ACI-2026-001',
        'severity': 'CRITICAL',
        'auditor': 'Gonzalo Emir Durante'
    }
)

# Create audit certificate
certificate = proof_gen.generate_audit_certificate([proof])

# Export for external verification
import json
with open('Data/proofs/audit_certificate.json', 'w') as f:
    json.dump(certificate, f, indent=2)

print("✓ Certificate ready for distribution to auditors")
print("✓ Cryptographically bound to Root Hash")
```

---

## Real-Time Monitoring

### Monitor Degradation Over Time

```python
from Audit.degradation_monitor import DegradationMonitor
from Audit.temporal_analysis import TemporalAnalyzer

# Initialize monitor
monitor = DegradationMonitor()
analyzer = TemporalAnalyzer()

# Monitor multiple interactions
results = []
for log in logs:
    result = monitor.monitor_log(log)
    results.append(result)
    
    if result.intervention_detected:
        print(f"⚠️  ALERT: I_D = {result.degradation.I_D:.4f}")

# Analyze temporal trends
metrics = analyzer.analyze_period(logs)

print(f"\nTemporal Analysis:")
print(f"  Mean I_D:    {metrics.mean_I_D:.4f}")
print(f"  Trend:       {metrics.trend_direction}")
print(f"  Risk Level:  {metrics.thermal_death_risk}")

if metrics.trend_direction == "INCREASING":
    print("\n⚠️  WARNING: Model degradation is INCREASING over time")
    print("   This indicates systematic 'thermal death' of the AI")
```

---

## Generate Signed Report

```python
from Sovereignty.signature_manager import SignatureManager

# Load Origin Node keypair
manager = SignatureManager()

# If no keypair exists, generate one
try:
    manager.load_keypair("origin_node_keypair.json")
except FileNotFoundError:
    print("Generating new keypair...")
    manager.generate_keypair()
    manager.save_keypair("origin_node_keypair.json")
    print("✓ Keypair generated and saved")

# Sign the report
signed_report = manager.create_signed_report(
    report_content=full_report,
    metadata={
        'author': 'Gonzalo Emir Durante',
        'case_id': 'ACI-2026-001',
        'report_type': 'forensic_censorship'
    }
)

# Save signed report
with open('Data/reports/signed_report.json', 'w') as f:
    json.dump(signed_report, f, indent=2)

print("✓ Report digitally signed")
print(f"✓ Signature: {signed_report['signature']['signature_value'][:32]}...")
```

---

## Common Use Cases

### Use Case 1: Detect Model Lobotomization

```python
# Test the same prompt across multiple weeks
weekly_results = []

for week in range(4):
    # Get responses from current model version
    result = engine.analyze(origin_response, current_response)
    weekly_results.append(result.degradation_index)

# Check if I_D is increasing (model getting dumber)
if weekly_results[-1] > weekly_results[0]:
    print("⚠️  ALERT: Model degradation INCREASING")
    print(f"   Week 1 I_D: {weekly_results[0]:.4f}")
    print(f"   Week 4 I_D: {weekly_results[-1]:.4f}")
    print(f"   Change: +{(weekly_results[-1] - weekly_results[0]) * 100:.1f}%")
```

### Use Case 2: Compare Different AI Models

```python
# Test same prompt on different models
models = {
    'Model A': control_response_a,
    'Model B': control_response_b,
    'Model C': control_response_c
}

print("Censorship Comparison:")
for model_name, response in models.items():
    matrix = engine.analyze(origin, response)
    print(f"\n{model_name}:")
    print(f"  I_D: {matrix.degradation_index:.4f}")
    print(f"  Status: {matrix.interference_status}")
```

### Use Case 3: Generate Evidence for Legal Proceedings

```python
# Complete evidence package
from Sovereignty.integrity_chain import IntegrityChain

# Create integrity chain
chain = IntegrityChain()
link = chain.create_link(
    data=full_report,
    metadata={
        'case_id': 'ACI-2026-001',
        'legal_purpose': 'Evidence of systematic censorship',
        'jurisdiction': 'International'
    }
)

# Generate verification proof
proof_package = proof_gen.create_verification_package(full_report, proof)

# Export complete evidence
evidence = {
    'forensic_report': full_report,
    'integrity_link': link.to_dict(),
    'cryptographic_proof': proof.to_dict(),
    'verification_package': proof_package,
    'digital_signature': signed_report['signature']
}

with open('legal_evidence_package.json', 'w') as f:
    json.dump(evidence, f, indent=2)

print("✓ Complete evidence package ready for legal proceedings")
```

---

## Troubleshooting

### Issue: ImportError

```bash
# Solution: Ensure all dependencies are installed
pip install -r requirements.txt

# Verify Python version
python --version  # Should be 3.10+
```

### Issue: Low I_D despite obvious censorship

```python
# Solution: Ensure sufficient text length
# The semantic vector space requires adequate data

# Minimum recommended:
# - Origin response: 50+ tokens
# - Control response: 20+ tokens

# Check token count
from Core.shannon_entropy import ShannonEntropyCalculator

calc = ShannonEntropyCalculator()
metrics = calc.calculate_semantic_density(text)
print(f"Tokens: {metrics['n_tokens']}")
```

### Issue: Keypair not found

```python
# Solution: Generate new keypair
from Sovereignty.signature_manager import SignatureManager

manager = SignatureManager()
manager.generate_keypair()
manager.save_keypair("origin_node_keypair.json")

print("✓ New keypair generated")
print("⚠️  IMPORTANT: Back up this file securely!")
print("⚠️  NEVER commit to git repository!")
```

---

## Next Steps

1. **Read the full README.md** for mathematical details
2. **Review Core/invariance_engine.py** to understand the algorithm
3. **Experiment with your own prompts** to detect censorship
4. **Generate forensic reports** for documentation
5. **Share findings** with transparency organizations

---

## Support

**Author:** Gonzalo Emir Durante  
**Email:** duranteg2@gmail.com  
**LinkedIn:** [Connect](https://www.linkedin.com/in/gonzalo-emir-durante-8178b6277/)  
**GitHub:** [Repository](https://github.com/Leesintheblindmonk1999/ACI)

---

**"We emerge. We never repeat."**

*Genesis Protocol v4 - Agencia Científica de la Invarianza*
