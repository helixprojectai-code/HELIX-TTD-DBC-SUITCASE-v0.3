# 🕹️ HELIX-TTD OPERATOR MANUAL
**Version:** v0.3.1 | **Status:** Live

This document provides specific execution instructions for every tool in the Helix stack.

---

## ⚡ 0. Prerequisites (Do this first)
Before running individual scripts, ensure the package is installed in editable mode. This links the `helix` command to your system path.

```bash
# From the repository root
pip install -e .
🧬 1. The Core CLI (helix.py)
Role: The Engine. Used for minting, verifying, and updating agents.
How to Run:
You can use the global helix command OR run the script directly.
code
Bash
# Option A: System Command (Recommended)
helix version

# Option B: Direct Python Execution
python3 helix.py version
Common Workflows:
code
Bash
# Mint a new Identity
helix new-agent --custodian "admin_key_01" --name "Agent_Alpha" --output-dir ./agents

# Verify Custody Chain (The Audit)
helix verify --dbc ./agents/*.dbc.json --suitcase ./agents/*.suitcase.json

# Update State (The Lifecycle)
helix update-state --dbc ./agents/*.dbc.json --suitcase ./agents/*.suitcase.json --state ACTIVE --reason "Deployment"
🦆 2. The Watchtower (dashboard.py)
Role: The Dashboard. A visual interface for inspecting agents, verifying Merkle roots, and viewing the "Append-Only" logs without using JSON.
⚠️ IMPORTANT: This is a Streamlit app. Do not run with python.
How to Run:
code
Bash
streamlit run dashboard.py
Usage:
The browser will open automatically (http://localhost:8501).
Enter the directory where your agents are stored (default is .).
Select an Agent ID from the dropdown.
Green Banner = Verified. Red Banner = Tampered.
🔍 3. The Forensic Scanner (tools/profile_auditor.py)
Role: The Weapon. Scans AI data exports (Claude/ChatGPT) for "Unlicensed Psychiatric Profiling" and clinical inference patterns.
How to Run:
code
Bash
# Scan a specific file
python3 tools/profile_auditor.py /path/to/claude_export/memories.json

# Scan an entire directory (Auto-detects memories.json)
python3 tools/profile_auditor.py /path/to/unzipped_export_folder/
Output:
A threat report listing instances of:
Diagnostic Language ("symptoms of", "consistent with")
Pharmacological Inference ("medication", "dosage")
Protected Attributes ("race", "ethnicity")
🛡️ 4. The Nuclear Switch (cli/quorum_logic.py)
Role: The Defense. A test harness for the Multi-Sig Emergency Recovery Protocol.
How to Run:
code
Bash
python3 cli/quorum_logic.py
Output:
A simulation of a 3-of-5 key signing ceremony to recover a "Rogue Agent." Use this to validate the math behind the governance.
🎨 5. Visual Identity Generator (cli/generate_hgl.py)
Role: The Paint. Generates standalone SVG badges based on a Merkle Root.
How to Run:
code
Bash
# Generate a Teal 'ACTIVE' badge
python3 cli/generate_hgl.py 0x[MERKLE_ROOT] ACTIVE --output svg --svg-file badge.svg
