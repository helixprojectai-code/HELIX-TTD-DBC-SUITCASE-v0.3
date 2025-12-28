# DBC × SUITCASE: Unified Identity & Custody Stack
### Version v0.3 // December 28, 2025

**The structural prevention of anthropomorphic evasion.**

This repository defines the protocols for **Helix-TTD Identity & Custody**. It enforces a strict "No Orphaned Agents" policy by binding every AI agent to a cryptographic root held by a human custodian.

## 🔥 VIRAL LAUNCH: 156+ CLONES IN FIRST 2 HOURS!

⚡ **REAL-TIME STATS (as of [TIME]):**
- 📥 **156+ total clones** (1.3 per minute)
- 👥 **80+ unique developers** 
- 🔄 **1.95 clones per developer** (active testing/iteration)
- ⏰ **5 AM Saturday** - the dedicated are awake

*Developers aren't just watching - they're actively testing and iterating.*

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

```bash
# Install
pip install -e .

# Create a new AI agent
helix new-agent --custodian alice_001 --name "Alpha-Agent-01"

# List all agents
helix list

# Generate a glyph for an agent
helix glyph 0x3a2b1f8c9d ACTIVE --name "Alpha-Agent" --output svg --svg-file agent.svg

# Verify agent integrity
helix verify --dbc DBC-*.dbc.json --suitcase DBC-*.suitcase.json

# Update agent state
helix update-state --dbc DBC-*.dbc.json --suitcase DBC-*.suitcase.json --state RESTRICTED --reason "Behavioral anomaly detected"
