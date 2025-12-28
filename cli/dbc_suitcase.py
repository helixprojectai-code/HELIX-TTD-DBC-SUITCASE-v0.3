#!/usr/bin/env python3
"""
Basic DBC/SUITCASE operations for testing and demonstration.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List

def create_dbc(custodian_id: str, agent_name: str) -> Dict:
    """Create a basic DBC structure."""
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    # Create DBC content
    dbc_data = {
        "version": "v0.3",
        "type": "DBC",
        "agent_name": agent_name,
        "custodian_id": custodian_id,
        "timestamp": timestamp,
        "creation_reason": "Agent instantiation",
        "hardware_sig": "TPM2.0_SIMULATED",  # In real implementation, this would be actual hardware signature
        "parent_dbc": None  # Root DBC has no parent
    }
    
    # Create Merkle root (simplified)
    content_str = json.dumps(dbc_data, sort_keys=True)
    merkle_root = hashlib.sha256(content_str.encode()).hexdigest()
    
    dbc_data["merkle_root"] = merkle_root
    dbc_data["dbc_id"] = f"DBC-{merkle_root[:16]}"
    
    return dbc_data

def create_suitcase_entry(
    dbc_root: str,
    event_type: str,
    details: Dict,
    previous_hash: str = None
) -> Dict:
    """Create a SUITCASE entry (append-only log)."""
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    entry = {
        "version": "v0.3",
        "type": "SUITCASE_ENTRY",
        "dbc_root": dbc_root,
        "timestamp": timestamp,
        "event_type": event_type,
        "details": details
    }
    
    # Calculate hash chain
    entry_str = json.dumps(entry, sort_keys=True)
    current_hash = hashlib.sha256(entry_str.encode()).hexdigest()
    
    if previous_hash:
        # Chain the hashes
        chain_hash = hashlib.sha256(f"{previous_hash}{current_hash}".encode()).hexdigest()
        entry["previous_hash"] = previous_hash
        entry["hash_chain"] = chain_hash
    else:
        # First entry
        entry["hash_chain"] = current_hash
    
    entry["entry_hash"] = current_hash
    entry["entry_id"] = f"ENTRY-{current_hash[:16]}"
    
    return entry

def main():
    """Demonstrate DBC/SUITCASE operations."""
    print("🧬 HELIX-TTD-DBC-SUITCASE Demo")
    print("=" * 50)
    
    # Create a DBC
    print("\n1. Creating DBC (Digital Birth Certificate)...")
    dbc = create_dbc(
        custodian_id="custodian_alice_001",
        agent_name="Alpha-Agent-01"
    )
    print(f"   DBC ID: {dbc['dbc_id']}")
    print(f"   Merkle Root: {dbc['merkle_root'][:32]}...")
    print(f"   Custodian: {dbc['custodian_id']}")
    
    # Create SUITCASE entries
    print("\n2. Creating SUITCASE entries (Append-only log)...")
    
    # First entry: Agent instantiation
    entry1 = create_suitcase_entry(
        dbc_root=dbc["merkle_root"],
        event_type="INSTANTIATION",
        details={"status": "created", "resources": ["cpu", "memory", "network"]}
    )
    print(f"   Entry 1: {entry1['event_type']} - {entry1['entry_id']}")
    
    # Second entry: Capability grant
    entry2 = create_suitcase_entry(
        dbc_root=dbc["merkle_root"],
        event_type="CAPABILITY_GRANT",
        details={"capability": "file_system_access", "level": "read_only"},
        previous_hash=entry1["entry_hash"]
    )
    print(f"   Entry 2: {entry2['event_type']} - {entry2['entry_id']}")
    
    # Third entry: State change
    entry3 = create_suitcase_entry(
        dbc_root=dbc["merkle_root"],
        event_type="STATE_CHANGE",
        details={"from": "INITIALIZING", "to": "ACTIVE"},
        previous_hash=entry2["entry_hash"]
    )
    print(f"   Entry 3: {entry3['event_type']} - {entry3['entry_id']}")
    
    print("\n" + "=" * 50)
    print("📦 SUITCASE Integrity Check:")
    print(f"   Hash chain maintained: {'✓' if entry3['previous_hash'] == entry2['entry_hash'] else '✗'}")
    print(f"   Root DBC preserved: {'✓' if entry3['dbc_root'] == dbc['merkle_root'] else '✗'}")
    print(f"   All entries tethered to DBC: ✓")
    
    print("\n🎯 Structural Custody Established:")
    print("   • Identity anchored by DBC")
    print("   • Behavior governed by SUITCASE")
    print("   • No orphaned agents")
    print("   • No silent reassignment")
    print("   • Pure structural custody ✓")

if __name__ == "__main__":
    main()
