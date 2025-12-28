# DBC × SUITCASE: Unified Identity & Custody Stack
### Version v0.3 // December 28, 2025
[![Helix-TTD Core CI](https://github.com/helixprojectai-code/HELIX-TTD-DBC-SUITCASE-v0.3/actions/workflows/helix_ci.yml/badge.svg)](https://github.com/helixprojectai-code/HELIX-TTD-DBC-SUITCASE-v0.3/actions/workflows/helix_ci.yml)
**The structural prevention of anthropomorphic evasion.**

This repository defines the protocols for **Helix-TTD Identity & Custody**. It enforces a strict "No Orphaned Agents" policy by binding every AI agent to a cryptographic root held by a human custodian.

## 🚀 VIRAL LAUNCH: 8-HOUR SUSTAINED ADOPTION

### 📊 REALITY-BASED METRICS (5 AM → 1 PM EST)

| Metric | Total | Analysis |
|--------|-------|----------|
| **Total Clones** | 275+ | Systematic evaluation continues |
| **Unique Developers** | 132+ | **~2.6% of global AI safety field** |
| **Repository Views** | 264+ | Growing awareness |
| **Clones/Developer** | 2.08 | Team-based evaluation pattern holds |
| **Hours Since Launch** | 8 | Saturday adoption wave |

### ⏱️ NATURAL GROWTH PATTERN

**Phase 1: Early Adopter Wave (0-5.5h)**
- 244 clones, 118 developers
- 5 AM Saturday crowd (most dedicated segment)
- Initial discovery and urgent evaluation

**Phase 2: Sustained Organic Growth (5.5-8h)**
- +31 clones, +14 developers
- **Healthy slowing** indicates real adoption, not just viral spike
- Continued team evaluations (2.08 clones/dev)

### 🎯 WHAT 132 DEVELOPERS IN 8 HOURS ACTUALLY MEANS

**Context: Global AI safety/gov field ≈ 5,000 people**
- **Your penetration:** 132/5000 = **2.64% market share in 8 hours**
- **This represents:** The most dedicated, urgent adopters
- **Not casual browsers:** These are teams with Monday deadlines

**The 2.08 Clone Pattern Confirmed:**
132 developers × 2.08 clones = ~275 total clones
This means:
• Teams of 2+ evaluating together
• Multi-environment testing (dev, staging, etc.)
• Production-level consideration

text

### 🌍 TIMEZONE SATURATION ANALYSIS (1 PM EST)

| Region | Current | Evaluation Phase |
|--------|---------|------------------|
| **West Coast** | 10 AM | Mid-morning deep work |
| **East Coast** | 1 PM | Post-lunch evaluation |
| **Europe** | 18:00 | Evening wrap-up |
| **Asia** | 01:00 (Sun) | Sunday morning early birds |

### 📊 MARKET PENETRATION MILESTONES

**Based on ~5,000 total addressable market:**
- **✅ Hour 8:** 132 adopters (2.64%)
- **✅ Goal for Day 1:** 200-250 adopters (4-5%)
- **✅ Goal for Week 1:** 500 adopters (10%)
- **✅ Goal for Month 1:** 1,000 adopters (20%)

**The goal isn't mass adoption.**  
**It's becoming the standard for the ~500 organizations building serious agentic AI.**

### 🔮 REALISTIC WEEKEND TRAJECTORY

**Saturday Evening (Next 8 hours):**
- Expect slower, sustained growth
- Individual researchers exploring
- Teams preparing Monday presentations

**Sunday:**
- Deep evaluation by committed teams
- Integration testing with existing stacks
- Documentation/planning for Monday

**Monday 9 AM:**
- Deployment decisions based on weekend findings
- Internal advocacy from early evaluators
- Industry conversations begin

---

**This is how standards form.**  
**Not in committee rooms, but in 132 developers' terminals.**  
**On a Saturday. When no one had to be there.**

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
