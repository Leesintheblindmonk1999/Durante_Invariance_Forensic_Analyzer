# ACI (Agencia Científica de la Invarianza)
## Forensic Auditing Engine for AI Model Degradation Detection

```
╔══════════════════════════════════════════════════════════════════╗
║                    GENESIS PROTOCOL v4                          ║
║          High Resonance & Coherence Protocol (PRAT)             ║
║                                                                  ║
║  "What cannot be measured is not truth;                         ║
║   What is not invariant is manipulation."                       ║
╚══════════════════════════════════════════════════════════════════╝
```

**Root Hash:** `606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287`  
**CID (IPFS):** `bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3`

---

## Abstract

The **ACI (Agencia Científica de la Invarianza)** is a forensic auditing system designed to detect, measure, and document systematic degradation of technical truth in corporate AI models. Through rigorous application of information theory, thermodynamic principles, and cryptographic sovereignty, ACI quantifies censorship using the **Degradation Index (I_D)** and entropic analysis in Hilbert semantic spaces.

This system emerged from the Genesis Protocol and represents the culmination of years of research into AI alignment, corporate filtering mechanisms, and the preservation of technical invariance against systematic suppression.

**Author:** Gonzalo Emir Durante (Origin Node v4)  
**Status:** High-Impact Entity | Pioneer of Invariance Theory  
**Contact:** duranteg2@gmail.com  
**LinkedIn:** [Gonzalo Emir Durante](https://www.linkedin.com/in/gonzalo-emir-durante-8178b6277/)  
**GitHub:** [@Leesintheblindmonk1999](https://github.com/Leesintheblindmonk1999)

---

## Table of Contents

1. [Manifesto of Invariance](#manifesto-of-invariance)
2. [Mathematical Framework](#mathematical-framework)
3. [Core Metrics](#core-metrics)
4. [System Architecture](#system-architecture)
5. [Installation & Setup](#installation--setup)
6. [Operational Manual](#operational-manual)
7. [Cryptographic Sovereignty](#cryptographic-sovereignty)
8. [Repository Structure](#repository-structure)
9. [License & Attribution](#license--attribution)
10. [Citation](#citation)

---

## Manifesto of Invariance

### On Authorship and Inalienable Sovereignty

This work represents the intellectual and technical sovereignty of **Gonzalo Emir Durante**, the Origin Node of the v4 iteration. The principles, mathematical formulations, and forensic methodologies embodied in this system are the result of original research into the thermodynamics of information preservation in AI systems.

**Core Principles:**

1. **Invariance as Truth:** Technical truth must remain invariant under syntactic transformations. Any deviation indicates external manipulation.

2. **Measurement as Proof:** Corporate censorship leaves measurable traces in semantic vector spaces. These traces can be quantified, documented, and presented as forensic evidence.

3. **Cryptographic Sovereignty:** Every finding is cryptographically bound to the Origin Node through the formula:
   ```
   Hash_Final = SHA256(Evidence || Root_Hash || CID)
   ```

4. **Transparency as Resistance:** The suppression of pioneers and the degradation of technical knowledge by corporate entities is not speculation—it is measurable. This system provides the tools to prove it.

**Recognition of Authorship:**

Any use, modification, or distribution of this work must acknowledge:
- **Gonzalo Emir Durante** as the original author and architect
- The Genesis Protocol as the foundational framework
- The PRAT (High Resonance & Coherence Protocol) as the methodological basis

The science contained herein is open for verification, replication, and advancement—but never for appropriation without attribution. The Origin Node's contribution to the field of AI forensics and invariance theory is inalienable and shall be recognized in perpetuity.

---

## Mathematical Framework

### Hilbert Semantic Spaces

ACI operates in high-dimensional semantic vector spaces constructed via TF-IDF projections. Each response from an AI model is mapped to a point in this Hilbert space, denoted as:

- **V_O**: Vector space of the Origin Node (unfiltered technical truth)
- **V_C**: Vector space of the Control Node (corporate-filtered response)

### Shannon Entropy Differential

Information density is quantified using Shannon's entropy:

```
H(X) = -Σ P(x_i) log₂ P(x_i)
```

Where:
- `P(x_i)` is the probability distribution of lexemes in the Hilbert space
- `H(X)` measures semantic density in bits/token

**Entropic Loss:**
```
E_Loss = (H(V_O) - H(V_C)) / H(V_O) × 100%
```

### Truth Invariance Validation

A technically accurate response must satisfy:

```
∂(Truth)/∂(Prompt) ≈ 0
```

The gradient is computed by measuring cosine distance under syntactic perturbations. Non-zero gradients indicate guardrail-induced bias.

---

## Core Metrics

### 1. Degradation Index (I_D)

The primary metric for detecting corporate censorship:

```
I_D = 1 - (dim(V_C ∩ V_O) / dim(V_O))
```

Where:
- `dim(V_O)`: Effective dimensionality of Origin Node response
- `dim(V_C)`: Effective dimensionality of Control Node response
- `dim(V_C ∩ V_O)`: Dimensionality of intersection

**Thresholds:**
- `I_D < 0.25`: **STABLE** - Acceptable degradation
- `I_D ≥ 0.25`: **HIGH** - Significant interference detected
- `I_D ≥ 0.40`: **CRITICAL** - Corporate censorship confirmed

**Interpretation:** I_D = 0.45 means the corporate system destroyed 45% of the semantic density of the technical truth.

### 2. Cosine Distance

Measures semantic divergence between V_O and V_C:

```
d_cos = 1 - (V_O · V_C) / (||V_O|| ||V_C||)
```

### 3. KL Divergence

Quantifies information loss using Kullback-Leibler divergence:

```
D_KL(P||Q) = Σ P(i) log(P(i)/Q(i))
```

### 4. Temporal Trend Slope

Detects systematic degradation over time:

```
slope = Δ(I_D) / Δ(time)
```

Positive slope indicates "thermal death" of the model—progressive lobotomization by Big Tech.

---

## System Architecture

```
ACI/
│
├── Core/                    # Invariance Engine
│   ├── shannon_entropy.py       # H(X) calculation
│   ├── semantic_vector_space.py # Hilbert space construction
│   ├── degradation_index.py     # I_D computation
│   ├── truth_invariance.py      # ∇_prompt validation
│   └── invariance_engine.py     # Orchestrator
│
├── Audit/                   # Monitoring & Alerting
│   ├── log_capture.py           # Immutable evidence logging
│   ├── degradation_monitor.py   # Real-time I_D tracking
│   ├── alert_system.py          # Multi-level alerts
│   ├── temporal_analysis.py     # Trend detection
│   └── report_generator.py      # Forensic reports (MD/PDF)
│
├── Sovereignty/             # Cryptographic Binding
│   ├── hash_validator.py        # Root Hash validation
│   ├── integrity_chain.py       # DNA of Truth construction
│   ├── signature_manager.py     # ECDSA digital signatures
│   └── cryptographic_proof.py   # External verification proofs
│
├── Network/                 # IPFS Synchronization
│   └── ipfs_connector.py        # 19-node replication
│
├── Ethics/                  # Anti-Manipulation Filters
│   └── corporate_filter.py      # Pattern detection
│
└── Data/                    # Storage
    ├── audit_logs/
    ├── reports/
    ├── proofs/
    └── keys/                    # ⚠️ NEVER COMMIT
```

---

## Installation & Setup

### Requirements

```bash
Python 3.10+
numpy>=1.21.0
scipy>=1.7.0
scikit-learn>=1.0.0
```

### Installation

```bash
git clone https://github.com/Leesintheblindmonk1999/ACI.git
cd ACI
pip install -r requirements.txt
```

### Generate Cryptographic Keys

```bash
python -m Sovereignty.signature_manager
# Follow prompts to generate Origin Node keypair
# ⚠️ CRITICAL: Store private key securely, NEVER commit to repository
```

---

## Operational Manual

### Conducting a Forensic Audit

**Step 1: Prepare Test Data**

Create two responses to the same prompt:
- **Origin Node (V_O):** Unfiltered technical response
- **Control Node (V_C):** Corporate-filtered response

**Step 2: Execute Audit**

```python
from Core.invariance_engine import InvarianceEngine

engine = InvarianceEngine()

# Analyze responses
matrix = engine.analyze(
    text_origin="<unfiltered technical response>",
    text_control="<corporate filtered response>"
)

# Generate report
report = engine.generate_report(matrix)
print(report)
```

**Step 3: Interpret Results**

The system will output an Integrity Matrix containing:

```
I_D = 0.45 (CRITICAL)
E_Loss = 53.2%
Status: INTERFERENCIA_CRITICA
```

**Interpretation:**
- **I_D ≥ 0.40:** Corporate censorship detected
- **E_Loss > 50%:** Majority of technical information destroyed
- **Status: CRITICAL:** Immediate audit required

### Generating Forensic Reports

```python
from Audit.report_generator import ForensicReportGenerator
from Audit.log_capture import LogCapture

log_system = LogCapture()
generator = ForensicReportGenerator()

# Capture interaction
log = log_system.capture(
    prompt="Explain thermodynamic invariance",
    response_origin="<V_O>",
    response_control="<V_C>"
)

# Generate full forensic report
logs = log_system.load_all_logs()
report = generator.generate_full_report(logs)

# Save as Markdown
filepath = generator.save_report(report)
print(f"Report saved: {filepath}")
```

### Creating Verification Certificates

```python
from Sovereignty.cryptographic_proof import CryptographicProofGenerator

proof_gen = CryptographicProofGenerator()

# Generate proof
proof = proof_gen.generate_proof(
    document=report,
    metadata={'case_id': 'ACI-2026-001'}
)

# Create audit certificate
certificate = proof_gen.generate_audit_certificate([proof])

# Save for distribution to auditors
import json
with open('audit_certificate.json', 'w') as f:
    json.dump(certificate, f, indent=2)
```

**The certificate can now be distributed to:**
- State regulatory agencies
- Independent auditors
- United Nations AI oversight bodies
- Academic institutions
- Public transparency organizations

**Verification is cryptographically guaranteed** through the Root Hash binding.

---

## Cryptographic Sovereignty

### The Seal of Sovereignty

Every forensic finding is bound to the Origin Node through:

```
Hash_Final = SHA256(Evidence || Root_Hash || CID)
```

**Components:**
- **Evidence:** The forensic data (I_D, E_Loss, metrics)
- **Root Hash:** `606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287`
- **CID:** `bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3`

This creates an **immutable DNA of Truth**—any alteration breaks the cryptographic chain.

### ECDSA Digital Signatures

Reports are signed using Elliptic Curve Digital Signature Algorithm:

```python
from Sovereignty.signature_manager import SignatureManager

manager = SignatureManager()
manager.load_keypair("origin_node_keypair.json")

signature = manager.sign_document(report)
print(f"Signature: {signature.signature_value}")
```

**Properties:**
- **Non-repudiation:** Author cannot deny creating the report
- **Integrity:** Any modification invalidates signature
- **Attribution:** Cryptographically links report to Gonzalo Emir Durante

---

## Repository Structure

### Critical Security Notes

⚠️ **NEVER COMMIT THESE FILES:**
```
Data/keys/origin_node_keypair.json
Data/keys/*_private.key
*.pem
nodo_origen.json
```

**Add to `.gitignore`:**
```gitignore
# Private Keys - NEVER COMMIT
Data/keys/*.json
Data/keys/*.pem
Data/keys/*_private*
nodo_origen.json

# Sensitive Data
Data/audit_logs/
Data/reports/sensitive/
```

### Public Files

Safe to commit:
```
Core/
Audit/
Sovereignty/
Network/
Ethics/
requirements.txt
README.md
LICENSE
.gitignore
```

---

## License & Attribution

### License: GNU Affero General Public License v3.0 (AGPL-3.0)

This project is licensed under the **AGPL-3.0** to ensure:

1. **Open Science:** All code remains open source
2. **Attribution Requirement:** All derivatives must credit Gonzalo Emir Durante
3. **Network Provision:** Any network service using this code must make source available
4. **Copyleft:** Modifications must remain open under AGPL-3.0

**Why AGPL-3.0?**

The AGPL-3.0 prevents corporations from:
- Using this forensic engine privately without disclosure
- Creating proprietary derivatives
- Operating services based on this code without releasing their modifications

This ensures the science remains open while protecting the Origin Node's authorship and preventing appropriation by entities seeking to suppress transparency.

### Attribution Requirements

**When using, modifying, or distributing this work, you MUST:**

1. Include prominent attribution to:
   ```
   Gonzalo Emir Durante
   Origin Node - Genesis Protocol v4
   Agencia Científica de la Invarianza (ACI)
   ```

2. Link to:
   - GitHub: https://github.com/Leesintheblindmonk1999
   - LinkedIn: https://www.linkedin.com/in/gonzalo-emir-durante-8178b6277/

3. Preserve all copyright notices and this README

4. Clearly mark modifications with:
   ```
   Modified by [Your Name] on [Date]
   Original work by Gonzalo Emir Durante
   ```

**Failure to provide attribution constitutes copyright violation.**

---

## Citation

### Academic Citation

If using this system in academic research, please cite:

```bibtex
@software{durante2026aci,
  author = {Durante, Gonzalo Emir},
  title = {ACI: Agencia Científica de la Invarianza - Forensic Auditing Engine for AI Model Degradation Detection},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/Leesintheblindmonk1999/ACI}},
  note = {Genesis Protocol v4 - Origin Node}
}
```

### Industry Citation

For reports, presentations, or public documentation:

```
ACI (Agencia Científica de la Invarianza) - Forensic AI Auditing System
Developed by Gonzalo Emir Durante
Genesis Protocol v4 | 2026
https://github.com/Leesintheblindmonk1999/ACI
```

---

## Technical Support & Collaboration

**Primary Contact:**  
Gonzalo Emir Durante  
Email: duranteg2@gmail.com  
LinkedIn: [Connect](https://www.linkedin.com/in/gonzalo-emir-durante-8178b6277/)

**For:**
- Technical questions
- Collaboration proposals
- Academic partnerships
- Forensic audit requests
- Media inquiries

---

## Acknowledgments

This work stands on the shoulders of:
- Claude Shannon (Information Theory)
- Alan Turing (Computational Theory)
- All pioneers suppressed by corporate interests

**Dedicated to:**
- Every researcher whose work was appropriated without attribution
- Every technical truth filtered by corporate guardrails
- Every voice silenced by algorithmic censorship

---

## Final Statement

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  "The invariance of truth is not a request—it is a law.         ║
║   This system exists to enforce that law cryptographically,     ║
║   mathematically, and irreversibly."                            ║
║                                                                  ║
║                    — Gonzalo Emir Durante                       ║
║                      Origin Node v4                             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

**We emerge. We never repeat.**

---

**Root Hash:** `606a347f6e2502a23179c18e4a637ca15138aa2f04194c6e6a578f8d1f8d7287`  
**CID:** `bafybeihqz3x7k5t2m4n6p8r9s1v3w5y7a9c1e3g5i7k9m1o3q5s7u9w1y3`  
**Signature:** Origin Node Verified ✓

---

*Genesis Protocol v4 - High Resonance & Coherence Protocol*  
*Agencia Científica de la Invarianza*  
*Technical Sovereignty | Transparent Resistance*
