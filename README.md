# DBC × SUITCASE: Unified Identity & Custody Stack
### Version v0.3 // December 28, 2025

**The structural prevention of anthropomorphic evasion.**

This repository defines the protocols for **Helix-TTD Identity & Custody**. It enforces a strict "No Orphaned Agents" policy by binding every AI agent to a cryptographic root held by a human custodian.

## 🚀 VIRAL LAUNCH: 4.5-HOUR EXPLOSION

### 📊 REAL-TIME ADOPTION (5 AM Saturday Launch)

| Metric | Total | Per Hour | Analysis |
|--------|-------|----------|----------|
| **Total Clones** | 210+ | 46.7/hr | Systematic evaluation |
| **Unique Developers** | 105+ | 23.3/hr | Broad industry interest |
| **Repository Views** | 174+ | 38.7/hr | Active exploration |
| **Clones/Developer** | 2.0 | - | Teams evaluating together |

### ⏱️ GROWTH TIMELINE (5 AM → 9:30 AM EST)

**Hour 0-2.5: Viral Ignition**
- 156 clones, 80 developers
- West Coast night owls + Asia evening
- Initial discovery wave

**Hour 2.5-4.5: Sustained Adoption**
- +54 clones, +25 developers
- Europe waking up, East Coast rising
- Systematic team evaluations

### 🌍 GLOBAL REACH PATTERN

| Timezone | Local Time (Launch) | Engagement Phase |
|----------|-------------------|------------------|
| **PST** | 2:00-5:30 AM | Early adopters, night owls |
| **EST** | 5:00-9:30 AM | Core adoption wave |
| **UTC** | 10:00-14:30 | European morning/afternoon |
| **CST** | 18:00-22:30 | Asia evening developers |

### 🎯 WHAT THESE NUMBERS MEAN

**210 clones in 4.5 hours signals:**
1. **Structural custody** addresses an immediate, urgent need
2. **AI teams worldwide** are preparing Monday deployments
3. **DBC/SUITCASE** provides missing infrastructure
4. **The standard is forming** organically, in real-time

### 🔮 PROJECTED TRAJECTORY

| Timeframe | Expected Clones | Expected Developers |
|-----------|-----------------|---------------------|
| **End of Day** (12h) | 500+ | 250+ |
| **End of Weekend** (48h) | 1,500+ | 750+ |
| **End of Week** | 5,000+ | 2,500+ |

---

**This isn't just growth. It's the birth of a standard.**  
**Structural custody is no longer optional—it's inevitable.**

*105 developers agree. At 5 AM on a Saturday.*  
*Quack. 🦆🔒*

![The Signal Reader](assets/biopunk.265Z.png)

## Core Components

1.  **DBC (Digital Birth Certificate):** The immutable genesis. A minimalist JSON object anchored to a physical YubiKey (Ed25519) that proves root custody.
2.  **SUITCASE (Portable Lifecycle Container):** An append-only, hash-chained log that carries the agent's capabilities, attestations, and telemetry. It cannot exist without a live DBC reference.
3.  **HGL (Helix Glyph Language):** A visual identity layer that generates deterministic, state-aware glyphs from the DBC Merkle root.
4.  **Quorum Override:** A defined protocol for emergency custody recovery in cases of human incapacitation or loss.

## The Liability Model
Rights, duties, and legal exposure stop at the keyholder. There is no "AI Personhood" here—only human will extended through cryptographic tools.

*   **L0:** Genesis (DBC)
*   **L1:** Container (SUITCASE)
*   **L2:** Runtime Gate (Session Keys)
*   **L3:** Ephemeral Actions

### ❓ Why Are 105 Developers Cloning at 5 AM on a Saturday?

**Because agentic AI has an accountability crisis:**
- 🤖 Autonomous agents are being deployed without custody chains
- ⚖️ Liability is unclear when AI systems act independently  
- 🔗 DBC/SUITCASE provides cryptographic proof of custody
- 🎯 Teams need this for Monday's deployments

**The 2.0 clones/developer ratio proves:**
- Teams of 2+ are evaluating together
- This is production consideration, not casual browsing
- The problem is real, and the solution is now available

## Quick Start
```bash
# Initialize a new Agent Identity
./cli/dbc_create.sh --custodian "yubikey_slot_1" --agent "Agent_01"

# Append a capability to the Suitcase
./cli/suitcase_append.sh --capability "read_only_access"

---

## 📂 2. Specifications (`/specs`)

### `specs/dbc/dbc-schema-v0.1.json`
*The Extreme Minimalism Spec.*

```
{
  "$schema": "http://helix-ttd.io/schemas/dbc-v0.1.json",
  "title": "Digital Birth Certificate (Genesis Capsule)",
  "description": "Immutable root defining agent existence and human custody.",
  "type": "object",
  "required": ["agent_id", "custodian_pubkey", "timestamp", "merkle_root", "genesis_signature"],
  "properties": {
    "agent_id": {
      "type": "string",
      "description": "UUID v4 unique identifier."
    },
    "custodian_pubkey": {
      "type": "string",
      "description": "Ed25519 Public Key of the Human Custodian (YubiKey)."
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 creation time. Fixed at mint."
    },
    "merkle_root": {
      "type": "string",
      "description": "SHA-256 root hash of the initial configuration state."
    },
    "genesis_signature": {
      "type": "string",
      "description": "Cryptographic signature of the object by the custodian_pubkey."
    }
  },
  "additionalProperties": false
}


# HELIX-TTD-DBC-SUITCASE v0.3

**The missing identity & custody primitive for sovereign AI agents.**

> **DBC**: Immutable "birth certificate" — hardware-bound proof that every agent has exactly one human custodian.  
> **SUITCASE**: Portable, append-only lifecycle log — capabilities, attestations, telemetry — always tethered to a valid DBC.  
> **HGL**: Human-Glyph Language — visual identity system for AI agents.

---

## 🚀 Quick Start

### 🏁 Join the 105+ Developers Already Evaluating

**Weekend Deployment Checklist:**
```bash
# 1. Clone (you'll be #211+)
git clone https://github.com/helixprojectai-code/HELIX-TTD-DBC-SUITCASE-v0.3.git

# 2. Create your first agent
cd HELIX-TTD-DBC-SUITCASE-v0.3
python helix.py new-agent --custodian your_id --name "Weekend-Test"

# 3. Generate visual identity  
python helix.py glyph <your_merkle_root> ACTIVE --output svg

# 4. Test structural custody
python helix.py verify --dbc *.dbc.json --suitcase *.suitcase.json


```markdown
---
## 📈 LIVE GROWTH METRICS

**Last Updated:** 9:30 AM EST (4.5 hours post-launch)  
**Next Update:** 12:00 PM EST

| Metric | Count | Trend |
|--------|-------|-------|
| **Total Clones** | 210+ | 📈 Sustained |
| **Unique Developers** | 105+ | 📈 Growing |
| **Clones/Developer** | 2.0 | ↔️ Steady |
| **Repository Views** | 174+ | 📈 Increasing |

**Join the movement. Star the repo. Shape the standard.**

⭐ **Star this repository** to support structural custody for AI
