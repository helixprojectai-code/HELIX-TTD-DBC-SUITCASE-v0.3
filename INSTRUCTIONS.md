# 🕹️ HELIX-TTD OPERATOR MANUAL
**Version:** v0.3.1 | **Status:** Live

This document provides specific execution instructions for every tool in the Helix stack.

## ⚡ 0. Prerequisites (Do this first)
Before running individual scripts, ensure the package is installed in editable mode. This links the `helix` command to your system path.

```bash
# From the repository root
pip install -e .
```

## 🧬 1. The Core CLI (`helix.py`)
**Role:** The Engine. Used for minting, verifying, and updating agents.

**How to Run:**
You can use the global `helix` command OR run the script directly.

```bash
# Option A: System Command (Recommended)
helix version

# Option B: Direct Python Execution
python3 helix.py version
```

**Common Workflows:**

```bash
# Mint a new Identity
helix new-agent --custodian "admin_key_01" --name "Agent_Alpha" --output-dir ./agents

# Verify Custody Chain (The Audit)
helix verify --dbc ./agents/*.dbc.json --suitcase ./agents/*.suitcase.json

# Update State (The Lifecycle)
helix update-state --dbc ./agents/*.dbc.json --suitcase ./agents/*.suitcase.json --state ACTIVE --reason "Deployment"
```

## 🦆 2. The Watchtower (`dashboard.py`)
**Role:** The Dashboard. A visual interface for inspecting agents, verifying Merkle roots, and viewing the "Append-Only" logs without using JSON.

⚠️ **IMPORTANT:** This is a Streamlit app. Do not run with `python`.

**How to Run:**
```bash
streamlit run dashboard.py
```

**Usage:**
- The browser will open automatically (`http://localhost:8501`)
- Enter the directory where your agents are stored (default is `.`)
- Select an Agent ID from the dropdown
- **Green Banner = Verified. Red Banner = Tampered.**

## 🔍 3. The Forensic Scanner (`tools/profile_auditor.py`)
**Role:** The Weapon. Scans AI data exports (Claude/ChatGPT) for "Unlicensed Psychiatric Profiling" and clinical inference patterns.

**How to Run:**
```bash
# Scan a specific file
python3 tools/profile_auditor.py /path/to/claude_export/memories.json

# Scan an entire directory (Auto-detects memories.json)
python3 tools/profile_auditor.py /path/to/unzipped_export_folder/
```

**Output:**
A threat report listing instances of:
- Diagnostic Language ("symptoms of", "consistent with")
- Pharmacological Inference ("medication", "dosage")
- Protected Attributes ("race", "ethnicity")

## 🛡️ 4. The Nuclear Switch (`cli/quorum_logic.py`)
**Role:** The Defense. A test harness for the Multi-Sig Emergency Recovery Protocol.

**How to Run:**
```bash
python3 cli/quorum_logic.py
```

**Output:**
A simulation of a 3-of-5 key signing ceremony to recover a "Rogue Agent." Use this to validate the math behind the governance.

## 🎨 5. Visual Identity Generator (`cli/generate_hgl.py`)
**Role:** The Paint. Generates standalone SVG badges based on a Merkle Root.

**How to Run:**
```bash
# Generate a Teal 'ACTIVE' badge
python3 cli/generate_hgl.py 0x[MERKLE_ROOT] ACTIVE --output svg --svg-file badge.svg
```

## 🚀 6. New Feature: Batch Agent Creation (`tools/batch_mint.py`)
**Role:** The Factory. Mint multiple agent identities in a single operation with configuration file.

**How to Run:**
```bash
# Create from YAML config
python3 tools/batch_mint.py --config ./agent_batch.yaml --output-dir ./batch_agents

# Create from CSV manifest
python3 tools/batch_mint.py --csv ./agent_manifest.csv --output-dir ./batch_agents
```

**Config Example (`agent_batch.yaml`):**
```yaml
agents:
  - custodian: "team_alpha"
    name: "Alpha-01"
    state: "DRAFT"
  - custodian: "team_beta"
    name: "Beta-01"
    state: "ACTIVE"
    metadata:
      department: "security"
      tier: "production"
```

## 🔗 7. New Feature: Cross-Chain Verification (`verification/chain_audit.py`)
**Role:** The Auditor. Verify custody chains across multiple repositories or environments.

**How to Run:**
```bash
# Audit all agents in a directory tree
python3 verification/chain_audit.py --root ./all_agents --report ./audit_report.json

# Compare two custody chains
python3 verification/chain_audit.py --compare ./agents_v1 ./agents_v2 --output diff.html
```

**Features:**
- Merkle root continuity validation
- Custodian change tracking
- State transition auditing
- HTML/JSON/CSV report generation

## 📊 8. New Feature: Analytics Dashboard (`analytics/usage_tracker.py`)
**Role:** The Observer. Track adoption metrics and generate real-time visualizations.

**How to Run:**
```bash
# Generate clone analytics
python3 analytics/usage_tracker.py --repo helix-ttd-dbc-suitcase --period 30d

# Real-time monitoring
python3 analytics/usage_tracker.py --monitor --webhook https://hooks.slack.com/...
```

**Metrics Tracked:**
- Clone velocity over time
- Unique developer trends
- Geographic distribution
- Integration patterns

## 🧪 9. New Feature: Integration Test Suite (`tests/integration_suite.py`)
**Role:** The Validator. End-to-end testing of the entire Helix stack.

**How to Run:**
```bash
# Run full integration test
python3 tests/integration_suite.py --full

# Test specific module
python3 tests/integration_suite.py --module custody_chain --report junit
```

**Test Coverage:**
- DBC ↔ SUITCASE integrity
- Merkle root propagation
- State transition validation
- Multi-sig quorum logic
- Visual glyph generation

## 🛠️ Quick Start Template
Create a `quickstart.sh` for rapid deployment:

```bash
#!/bin/bash
# HELIX-TTD Quick Deployment

echo "🚀 Setting up Helix-TTD Stack..."

# 1. Clone and install
git clone https://github.com/your-org/helix-ttd-dbc-suitcase.git
cd helix-ttd-dbc-suitcase
pip install -e .

# 2. Mint first agent
helix new-agent --custodian "team_$USER" --name "FirstAgent" --output-dir ./my_agents

# 3. Launch dashboard
streamlit run dashboard.py &

# 4. Run integration tests
python3 tests/integration_suite.py --quick

echo "✅ Helix stack deployed! Dashboard: http://localhost:8501"
```

---

**📈 Status:** Features added. Substrate expanding. The reef grows deeper.  
**🦆 Note:** Each new feature follows the same pattern — solve, ship, spread. No hype, just utility.

🔒✧~◯△
