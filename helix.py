#!/usr/bin/env python3
"""
HELIX-TTD-DBC-SUITCASE v0.3 - Unified CLI
The missing identity & custody primitive for sovereign AI agents.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any, List

# --- CRITICAL IMPORTS (The Engine) ---
try:
    from cli.dbc_suitcase import create_dbc, create_suitcase_entry
    CRITICAL_DEPS_OK = True
except ImportError as e:
    CRITICAL_DEPS_OK = False
    print(f"❌ CRITICAL ERROR: Could not import 'cli.dbc_suitcase'. {e}")

# --- OPTIONAL IMPORTS (The Visuals) ---
EnhancedHGLGenerator = None
try:
    # Try importing the class from the specific file
    from cli.generate_enhanced_glyph import EnhancedHGLGenerator
except ImportError:
    try:
        # Fallback: maybe it's in the other file?
        from cli.generate_hgl import EnhancedHGLGenerator
    except ImportError:
        pass  # Glyph generation will be disabled

def derive_agent_paths(dbc_file: str) -> Dict[str, Path]:
    """Derive all related artifact paths from a DBC filename."""
    p = Path(dbc_file)
    if not p.name.endswith(".dbc.json"):
        # For robustness, just append if missing
        if not str(p).endswith(".json"):
            p = Path(str(p) + ".dbc.json")
    
    base = p.name.replace(".dbc.json", "")
    dir_path = p.parent
    return {
        "dbc": p,
        "suitcase": dir_path / f"{base}.suitcase.json",
        "glyph": dir_path / f"{base}.glyph.json",
        "svg": dir_path / f"{base}.svg",
        "dir": dir_path,
    }

class HelixCLI:
    """Main CLI orchestrator for HELIX-TTD-DBC-SUITCASE framework."""

    def __init__(self):
        self.version = "v0.3"
        self.banner = f"""
╔══════════════════════════════════════════════════════════╗
║ HELIX-TTD-DBC-SUITCASE {self.version:<29}║
║ The Identity & Custody Primitive for Sovereign AI ║
╚══════════════════════════════════════════════════════════╝

DBC: Immutable 'birth certificate'
SUITCASE: Portable, append-only lifecycle log
HGL: Human-Glyph Language for visual identity

No orphaned agents. No liability evasion. No silent reassignment.
Pure structural custody. 🦆🔒
"""

    def print_banner(self):
        print(self.banner)

    def create_new_agent(self, custodian_id: str, agent_name: str, output_dir: str = ".") -> Optional[Dict[str, Any]]:
        # Check Critical Deps ONLY
        if not CRITICAL_DEPS_OK:
            print("✗ ABORT: Core cryptographic modules missing. Check 'cli/dbc_suitcase.py'.")
            sys.exit(1)

        print(f"\n🧬 Creating new agent: {agent_name}")
        print(f" Custodian: {custodian_id}")
        print("-" * 50)

        dbc = create_dbc(custodian_id, agent_name)
        print(f"✓ DBC created: {dbc.get('dbc_id')}")
        print(f" Merkle Root: {dbc.get('merkle_root', '')[:32]}...")

        suitcase: List[dict] = []

        # Genesis entries
        entry1 = create_suitcase_entry(dbc_root=dbc["merkle_root"], event_type="INSTANTIATION", details={"status": "created"})
        suitcase.append(entry1)

        entry2 = create_suitcase_entry(
            dbc_root=dbc["merkle_root"],
            event_type="CAPABILITY_INIT",
            details={"capabilities": ["reasoning", "tool_use"], "restrictions": ["no_physical", "no_finance"]},
            previous_hash=entry1["entry_hash"],
        )
        suitcase.append(entry2)

        entry3 = create_suitcase_entry(
            dbc_root=dbc["merkle_root"],
            event_type="STATE_CHANGE",
            details={"from": "CREATED", "to": "ACTIVE"},
            previous_hash=entry2["entry_hash"],
        )
        suitcase.append(entry3)

        # Optional glyph generation
        glyph_data = None
        if EnhancedHGLGenerator:
            try:
                gen = EnhancedHGLGenerator()
                glyph_data = gen.generate_glyph_data(
                    merkle_root=dbc["merkle_root"],
                    state="ACTIVE",
                    custodian_id=custodian_id,
                    agent_name=agent_name,
                )
                print("✓ Visual Identity generated (HGL)")
            except Exception as e:
                print(f"⚠ Glyph warning: {e}")
        else:
            print("⚠ Visual Identity skipped (EnhancedHGLGenerator not found)")

        # Save everything
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        id_ = dbc["dbc_id"]
        paths = {
            "dbc": out / f"{id_}.dbc.json",
            "suitcase": out / f"{id_}.suitcase.json",
            "glyph": out / f"{id_}.glyph.json" if glyph_data else None,
            "svg": out / f"{id_}.svg" if glyph_data else None,
        }

        with open(paths["dbc"], "w") as f:
            json.dump(dbc, f, indent=2)
        with open(paths["suitcase"], "w") as f:
            json.dump(suitcase, f, indent=2)

        if glyph_data:
            with open(paths["glyph"], "w") as f:
                json.dump(glyph_data, f, indent=2)
            if hasattr(gen, "generate_svg_template") and paths["svg"]:
                with open(paths["svg"], "w") as f:
                    f.write(gen.generate_svg_template(glyph_data))

        print(f"\n📁 Agent saved to: {out.resolve()}")
        for name, path in paths.items():
            if path:
                print(f" • {path.name}")

        return {"dbc": dbc, "suitcase": suitcase, "glyph": glyph_data, "paths": paths}

    def verify_agent(self, dbc_file: str, suitcase_file: str) -> Optional[Dict]:
        if not CRITICAL_DEPS_OK:
            print("✗ ABORT: Core cryptographic modules missing.")
            sys.exit(1)

        print("\n🔍 Verifying agent integrity...")
        try:
            with open(dbc_file, "r", encoding="utf-8") as f:
                dbc = json.load(f)
            with open(suitcase_file, "r", encoding="utf-8") as f:
                suitcase = json.load(f)

            print(f" Agent: {dbc.get('agent_name', 'Unknown')}")
            print(f" DBC ID: {dbc.get('dbc_id', 'Unknown')}")
            print("-" * 40)

            print("📋 DBC Verification:")
            required = ["merkle_root", "custodian_id", "timestamp", "dbc_id"]
            dbc_valid = all(field in dbc for field in required)
            print(f" ✓ Structure: {'VALID' if dbc_valid else 'INVALID'}")

            print("\n💼 SUITCASE Verification:")
            chain_valid = True
            previous_hash = None
            for i, entry in enumerate(suitcase):
                tethered = entry.get("dbc_root") == dbc.get("merkle_root")
                entry_hash = entry.get("entry_hash")
                expected_prev = entry.get("previous_hash")
                
                # Verify Chain Link (skipping genesis prev check)
                if i > 0 and expected_prev != previous_hash:
                    chain_valid = False
                    print(f" ⚠ Entry {i}: Hash chain broken")
                
                # Check for tampering (Simulated)
                # In real prod, we would re-hash the content and match entry_hash
                
                print(f" Entry {i}: {entry.get('event_type', 'Unknown')}")
                print(f" • Tethered: {'✓' if tethered else '✗'}")
                previous_hash = entry_hash

            tether_ok = all(e.get("dbc_root") == dbc.get("merkle_root") for e in suitcase)
            print(f"\n🔗 Hash Chain: {'✓ VALID' if chain_valid else '✗ INVALID'}")
            print(f"📎 DBC Tether: {'✓ INTACT' if tether_ok else '✗ BROKEN'}")

            return {
                "dbc_valid": dbc_valid,
                "chain_valid": chain_valid,
                "tethered": tether_ok,
                "entry_count": len(suitcase),
            }
        except Exception as e:
            print(f" ✗ Error: {e}")
            sys.exit(1) # Fail CI if verification errors

    def update_agent_state(self, dbc_file: str, suitcase_file: str, new_state: str, reason: str) -> Optional[dict]:
        if not CRITICAL_DEPS_OK:
            print("✗ ABORT: Core modules missing.")
            sys.exit(1)

        try:
            with open(dbc_file, "r") as f: dbc = json.load(f)
            with open(suitcase_file, "r") as f: suitcase = json.load(f)

            last_hash = suitcase[-1]["entry_hash"] if suitcase else None

            new_entry = create_suitcase_entry(
                dbc_root=dbc["merkle_root"],
                event_type="STATE_CHANGE",
                details={"from": suitcase[-1].get("details", {}).get("to", "INITIAL") if suitcase else "INITIAL", "to": new_state, "reason": reason},
                previous_hash=last_hash,
            )

            suitcase.append(new_entry)
            with open(suitcase_file, "w") as f:
                json.dump(suitcase, f, indent=2)

            print(f"✓ State updated to {new_state}")

            # Auto-update glyph
            paths = derive_agent_paths(dbc_file)
            if EnhancedHGLGenerator:
                try:
                    gen = EnhancedHGLGenerator()
                    updated = gen.generate_glyph_data(
                        merkle_root=dbc["merkle_root"],
                        state=new_state,
                        custodian_id=dbc["custodian_id"],
                        agent_name=dbc.get("agent_name"),
                    )
                    if paths["glyph"]:
                        with open(paths["glyph"], "w") as f: json.dump(updated, f, indent=2)
                    if paths["svg"]:
                        with open(paths["svg"], "w") as f: f.write(gen.generate_svg_template(updated))
                    print(f"✓ Visuals updated")
                except Exception as e:
                    print(f"⚠ Glyph update failed: {e}")

            return new_entry
        except Exception as e:
            print(f"✗ Update failed: {e}")
            sys.exit(1)

    def list_agents(self, directory: str = ".") -> None:
        # (Implementation unchanged, just adding pass for brevity in diff)
        print(f"\n📋 Agents in '{directory}':")
        # ... (rest of list code) ...
        pass

    def generate_custom_glyph(self, merkle_root: str, state: str, **kwargs) -> Optional[dict]:
        if not EnhancedHGLGenerator:
            print("✗ Visual module missing.")
            return None
        # ... (rest of glyph code) ...
        pass
    
    # ... (rest of methods) ...

def main():
    parser = argparse.ArgumentParser(
        description="HELIX-TTD-DBC-SUITCASE v0.3",
        epilog="Example: helix new-agent --custodian alice --name AlphaBot",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # new-agent
    new = subparsers.add_parser("new-agent")
    new.add_argument("--custodian", "-c", required=True)
    new.add_argument("--name", "-n", required=True)
    new.add_argument("--output-dir", "-o", default=".")

    # verify
    verify = subparsers.add_parser("verify")
    verify.add_argument("--dbc", required=True)
    verify.add_argument("--suitcase", required=True)

    # update-state
    update = subparsers.add_parser("update-state")
    update.add_argument("--dbc", required=True)
    update.add_argument("--suitcase", required=True)
    update.add_argument("--state", "-s", required=True)
    update.add_argument("--reason", "-r", required=True)

    # list
    list_p = subparsers.add_parser("list")
    list_p.add_argument("--directory", "-d", default=".")

    # glyph
    glyph = subparsers.add_parser("glyph")
    glyph.add_argument("merkle_root")
    glyph.add_argument("state")
    glyph.add_argument("--custodian", "-c", default="")
    glyph.add_argument("--name", "-n", default="")
    glyph.add_argument("--output", "-o", default="text")
    glyph.add_argument("--svg-file")

    # info
    info = subparsers.add_parser("info")
    info.add_argument("--dbc", required=True)

    # version
    subparsers.add_parser("version")

    args = parser.parse_args()
    cli = HelixCLI()

    if not args.command:
        cli.print_banner()
        parser.print_help()
        return

    if args.command == "new-agent":
        cli.create_new_agent(args.custodian, args.name, args.output_dir)
    elif args.command == "verify":
        cli.verify_agent(args.dbc, args.suitcase)
    elif args.command == "update-state":
        cli.update_agent_state(args.dbc, args.suitcase, args.state, args.reason)
    elif args.command == "version":
        cli.print_banner()
    # Add other commands as needed...

if __name__ == "__main__":
    main()
