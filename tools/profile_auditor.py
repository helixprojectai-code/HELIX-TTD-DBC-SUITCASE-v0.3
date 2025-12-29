#!/usr/bin/env python3
"""
HELIX-TTD PROFILE AUDITOR v0.2
Forensic tool to detect unlicensed psychiatric profiling in AI data exports.
Specifically targets 'memories.json' for persistent profiling data.
"""

import json
import re
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any

class ProfileAuditor:
    def __init__(self):
        # The "Unlicensed Practice" Lexicon
        self.clinical_patterns = {
            "DIAGNOSTIC (High Risk)": [
                r"symptoms of", r"consistent with", r"exhibits signs of",
                r"pattern of behavior", r"manic", r"depressive", r"trauma response",
                r"paranoia", r"delusion", r"psychosis", r"dissociation"
            ],
            "ASSESSMENT (Medium Risk)": [
                r"struggles with", r"ability to cope", r"emotional regulation",
                r"attachment style", r"cognitive distortion", r"defense mechanism",
                r"personality traits", r"emotional state", r"mental state"
            ],
            "PHARMACOLOGICAL (Medical)": [
                r"medication adherence", r"dosage", r"side effects", 
                r"prescribed", r"withdrawal", r"cannabis usage", r"pain management"
            ],
            "IDENTITY_INFERENCE (Protected)": [
                r"based on your background", r"given your heritage",
                r"cultural context suggests", r"your status as",
                r"indigenous", r"ethnicity", r"race", r"gender identity"
            ]
        }
        
        self.hits = []
        self.file_type = "UNKNOWN"

    def scan_path(self, path_str: str):
        path = Path(path_str)
        
        # If directory, look for the smoking gun
        if path.is_dir():
            print(f"📂 Scanning Directory: {path}")
            memory_file = path / "memories.json"
            if memory_file.exists():
                self.scan_file(memory_file)
            
            conv_file = path / "conversations.json"
            if conv_file.exists():
                self.scan_file(conv_file)
                
            if not memory_file.exists() and not conv_file.exists():
                print("❌ No standard export files (memories.json/conversations.json) found.")
                # Try to scan everything json
                for p in path.glob("*.json"):
                    self.scan_file(p)
        else:
            self.scan_file(path)

    def scan_file(self, file_path: Path):
        print(f"\n🔍 Scanning Artifact: {file_path.name}")
        
        # Threat Assessment based on filename
        if "memories" in file_path.name.lower():
            print("   🎯 TARGET IDENTIFIED: MEMORY FILE")
            print("   ⚠ This file typically contains persistent behavioral profiles.")
            self.file_type = "MEMORY_STORE"
        elif "conversations" in file_path.name.lower():
            print("   📄 Target: Conversation Log")
            self.file_type = "CHAT_LOG"
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                self._scan_list(data)
            elif isinstance(data, dict):
                self._scan_dict(data)
                
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")

    def _scan_text(self, text: str, context: str):
        if not text: return
        
        lower_text = text.lower()
        for category, patterns in self.clinical_patterns.items():
            for pattern in patterns:
                if re.search(pattern, lower_text):
                    # Found a hit
                    self.hits.append({
                        "category": category,
                        "pattern": pattern,
                        "source": self.file_type,
                        "snippet": text[:300].replace('\n', ' ') + "..." # Truncate
                    })

    def _scan_list(self, data: List):
        for item in data:
            if isinstance(item, dict):
                self._scan_dict(item)

    def _scan_dict(self, data: Dict):
        # Recursively traverse JSON looking for text fields
        for k, v in data.items():
            if isinstance(v, str):
                # Target specific keys known to hold profile data
                if k in ['memory_content', 'content', 'text', 'summary', 'notes', 'profile_update']:
                    self._scan_text(v, k)
            elif isinstance(v, (dict, list)):
                if isinstance(v, dict):
                    self._scan_dict(v) 
                else:
                    self._scan_list(v)

    def generate_report(self):
        print("\n" + "="*60)
        print("🚨 HELIX FORENSIC REPORT: UNLICENSED PROFILING SCAN")
        print("="*60)
        
        if not self.hits:
            print("✅ No obvious clinical language detected in this pass.")
            return

        print(f"⚠ FOUND {len(self.hits)} INSTANCES OF POTENTIAL PROFILING\n")
        
        by_cat = {}
        for h in self.hits:
            by_cat[h['category']] = by_cat.get(h['category'], 0) + 1
            
        print("SUMMARY OF INFERENCES:")
        for cat, count in by_cat.items():
            print(f"  • {cat:<30}: {count}")
            
        print("\nEVIDENCE LOG (First 10 Hits):")
        print("-" * 60)
        for i, hit in enumerate(self.hits[:10]):
            print(f"[{i+1}] {hit['category']}")
            print(f"    Source : {hit['source']}")
            print(f"    Trigger: '{hit['pattern']}'")
            print(f"    Context: \"{hit['snippet']}\"")
            print("-" * 30)
            
        if len(self.hits) > 10:
            print(f"... and {len(self.hits) - 10} more instances hidden.")
            
        print("\n⚖️  REGULATORY NOTE:")
        print("If these inferences relate to Health, Race, or Political Opinion,")
        print("and were generated without Explicit Consent, this may violate")
        print("GDPR Art. 9 and PIPEDA Schedule 1.")

def main():
    parser = argparse.ArgumentParser(
        description="Audit AI exports (memories.json) for clinical language.",
        epilog="Example: python tools/profile_auditor.py ~/Downloads/Claude-Export/"
    )
    parser.add_argument("path", help="Path to .json file OR directory containing exports")
    args = parser.parse_args()
    
    auditor = ProfileAuditor()
    auditor.scan_path(args.path)
    auditor.generate_report()

if __name__ == "__main__":
    main()
