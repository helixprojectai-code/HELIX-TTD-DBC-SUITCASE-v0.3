#!/usr/bin/env python3
"""
Basic DBC/SUITCASE operations for testing and demonstration.
Core logic for the Helix-TTD Identity & Custody stack.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, Optional, Tuple

def get_canonical_json(data: Dict) -> bytes:
    """Standardized JSON serialization for hashing."""
    return json.dumps(data, sort_keys=True, separators=(',', ':')).encode()

def create_dbc(custodian_id: str, agent_name: str) -> Dict:
    """Create a basic DBC structure."""
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    dbc_data = {
        "version": "v0.3",
        "type": "DBC",
        "agent_name": agent_name,
        "custodian_id": custodian_id,
        "timestamp": timestamp,
        "creation_reason": "Agent instantiation",
        "hardware_sig": "TPM2.0_SIMULATED", 
        "parent_dbc": None 
    }
    
    # Deterministic Root
    merkle_root = hashlib.sha256(get_canonical_json(dbc_data)).hexdigest()
    
    dbc_data["merkle_root"] = merkle_root
    dbc_data["dbc_id"] = f"DBC-{merkle_root[:16]}"
    
    return dbc_data

def create_suitcase_entry(
    dbc_root: str,
    event_type: str,
    details: Dict,
    previous_hash: Optional[str] = None
) -> Dict:
    """Create a SUITCASE entry (append-only log)."""
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    # 1. Define the Content Payload (The "Truth")
    # Only these fields are hashed to create entry_hash
    content_payload = {
        "version": "v0.3",
        "type": "SUITCASE_ENTRY",
        "dbc_root": dbc_root,
        "timestamp": timestamp,
        "event_type": event_type,
        "details": details
    }
    
    # 2. Hash the Content
    current_hash = hashlib.sha256(get_canonical_json(content_payload)).hexdigest()
    
    # 3. Construct the Full Entry (Content + Metadata)
    entry = content_payload.copy()
    entry["entry_hash"] = current_hash
    entry["entry_id"] = f"ENTRY-{current_hash[:16]}"
    
    # 4. Chain Logic (The "Spine")
    if previous_hash:
        # Chain = Hash(Previous_Hash + Current_Content_Hash)
        chain_payload = f"{previous_hash}{current_hash}".encode()
        chain_hash = hashlib.sha256(chain_payload).hexdigest()
        entry["previous_hash"] = previous_hash
        entry["hash_chain"] = chain_hash
    else:
        # Genesis Entry
        entry["hash_chain"] = current_hash
        entry["previous_hash"] = None
    
    return entry

def validate_entry_integrity(entry: Dict) -> Tuple[bool, str]:
    """
    Recomputes hashes to detect content tampering.
    Returns: (is_valid, message)
    """
    try:
        # 1. Reconstruct the Pure Content Payload
        # We must manually extract ONLY the fields that were originally hashed
        content_payload = {
            "version": entry.get("version"),
            "type": entry.get("type"),
            "dbc_root": entry.get("dbc_root"),
            "timestamp": entry.get("timestamp"),
            "event_type": entry.get("event_type"),
            "details": entry.get("details")
        }
        
        # 2. Re-Hash Content
        recalc_hash = hashlib.sha256(get_canonical_json(content_payload)).hexdigest()
        
        if recalc_hash != entry.get("entry_hash"):
            return False, f"Content Tampered: Calc {recalc_hash[:8]} != Stored {entry.get('entry_hash', '')[:8]}"
            
        # 3. Verify Chain Link
        prev_hash = entry.get("previous_hash")
        stored_chain = entry.get("hash_chain")
        
        if prev_hash:
            chain_payload = f"{prev_hash}{recalc_hash}".encode()
            recalc_chain = hashlib.sha256(chain_payload).hexdigest()
            if recalc_chain != stored_chain:
                return False, "Chain Broken: Link hash mismatch"
        elif stored_chain != recalc_hash:
             # Genesis check
             return False, "Genesis Chain Broken"
             
        return True, "Valid"
        
    except Exception as e:
        return False, f"Validation Error: {str(e)}"
