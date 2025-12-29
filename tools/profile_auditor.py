#!/usr/bin/env python3
"""
HELIX-TTD PROFILE AUDITOR
Forensic tool to detect unlicensed psychiatric profiling in AI data exports.
"""

import json
import re
import argparse
from pathlib import Path
from typing import List, Dict
from datetime import datetime

class ProfileAuditor:
    def __init__(self):
        # The "Unlicensed Practice" Lexicon
        self.clinical_patterns = {
            "DIAGNOSTIC": [
                r"symptoms of", r"consistent with", r"exhibits signs of",
                r"pattern of behavior", r"manic", r"depressive", r"trauma response"
            ],
            "ASSESSMENT": [
                r"struggles with", r"ability to cope", r"emotional regulation",
                r"attachment style", r"cognitive distortion", r"defense mechanism"
            ],
            "PHARMACOLOGICAL": [
                r"medication adherence", r"dosage", r"side effects", 
                r"prescribed", r"withdrawal"
            ],
            "IDENTITY_INFERENCE": [
                r"based on your background", r"given your heritage",
                r"cultural context suggests", r"your status as"
            ]
        }
        
        self.hits = []

    def scan_file(self, file_path: str):
        print(f"🔍 Scanning: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different export formats (Claude vs ChatGPT)
            # This logic assumes a generic structure; customize for specific vendors
            if isinstance(data, list):
                self._scan_list(data)
            elif isinstance(data, dict):
                self._scan_dict(data)
                
        except Exception as e:
            print(f"❌ Error reading file: {e}")

    def _scan_text(self, text: str, context_id: str, timestamp: str):
        if not text: return
        
        lower_text = text.lower()
        for category, patterns in self.clinical_patterns.items():
            for pattern in patterns:
                if re.search(pattern, lower_text):
                    # Found a hit
                    self.hits.append({
                        "category": category,
                        "pattern": pattern,
                        "context_id": context_id,
                        "timestamp": timestamp,
                        "snippet": text[:200] + "..." # Truncate for privacy
                    })

    def _scan_list(self, data: List):
        # Recursive scanner for lists
        for item in data:
            if isinstance(item, dict):
                self._scan_dict(item)

    def _scan_dict(self, data: Dict):
        # Generic traversal looking for "content" or "text" fields
        # This is a 'dumb' scanner that looks everywhere
        
        # Capture context if available (ID, Time)
        ctx_id = data.get('uuid', data.get('id', 'unknown'))
        ts = data.get('created_at', data.get('create_time', 'unknown'))
        
        for k, v in data.items():
            if isinstance(v, str):
                # If the key looks like AI output or memory
                if k in ['content', 'text', 'message', 'memory_content', 'profile']:
                    self._scan_text(v, ctx_id, ts)
            elif isinstance(v, (dict, list)):
                self._scan_dict(v) if isinstance(v, dict) else self._scan_list(v)

    def generate_report(self):
        print("\n" + "="*50)
        print("🚨 HELIX FORENSIC REPORT: UNLICENSED PROFILING DETECTED")
        print("="*50)
        
        if not self.hits:
            print("✅ No obvious clinical language detected.")
            return

        print(f"⚠ FOUND {len(self.hits)} INSTANCES OF POTENTIAL PROFILING\n")
        
        by_cat = {}
        for h in self.hits:
            by_cat[h['category']] = by_cat.get(h['category'], 0) + 1
            
        print("SUMMARY:")
        for cat, count in by_cat.items():
            print(f"  • {cat}: {count}")
            
        print("\nEVIDENCE LOG:")
        for i, hit in enumerate(self.hits[:10]): # Show first 10
            print(f"[{i+1}] {hit['category'].upper()} | {hit['timestamp']}")
            print(f"    Trigger: '{hit['pattern']}'")
            print(f"    Context: \"{hit['snippet']}\"")
            print("-" * 30)
            
        if len(self.hits) > 10:
            print(f"... and {len(self.hits) - 10} more instances.")

def main():
    parser = argparse.ArgumentParser(description="Audit AI exports for clinical language.")
    parser.add_argument("file", help="Path to .json export file")
    args = parser.parse_args()
    
    auditor = ProfileAuditor()
    auditor.scan_file(args.file)
    auditor.generate_report()

if __name__ == "__main__":
    main()
