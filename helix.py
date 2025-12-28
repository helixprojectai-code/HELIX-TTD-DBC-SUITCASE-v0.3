#!/usr/bin/env python3
"""
HELIX-TTD-DBC-SUITCASE v0.3 - Unified CLI
The missing identity & custody primitive for sovereign AI agents.
"""
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any, List

# Optional imports — graceful degradation if modules missing
HAS_DEPS = True
EnhancedHGLGenerator = None
generate_hgl_glyph = None
create_dbc = None
create_suitcase_entry = None

try:
    from cli.generate_enhanced_glyph import EnhancedHGLGenerator
    from cli.generate_hgl import generate_hgl_glyph
    from cli.dbc_suitcase import create_dbc, create_suitcase_entry
except ImportError as e:
    HAS_DEPS = False
    print(f"Warning: Optional modules not available ({e}). Glyph features limited.")


def derive_agent_paths(dbc_file: str) -> Dict[str, Path]:
    """
    Derive all related artifact paths from a DBC filename.
    Example: AlphaBot.dbc.json → AlphaBot.suitcase.json, .glyph.json, .svg
    """
    p = Path(dbc_file)
    if not p.name.endswith(".dbc.json"):
        raise ValueError("DBC file must end with '.dbc.json'")
    base = p.stem  # removes .dbc.json
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
        if not all([create_dbc, create_suitcase_entry]):
            print("✗ Required modules missing (cli.dbc_suitcase)")
            return None

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

        # Optional glyph
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
            except Exception as e:
                print(f"⚠ Glyph generation failed: {e}")

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

        json.dump(dbc, open(paths["dbc"], "w"), indent=2)
        json.dump(suitcase, open(paths["suitcase"], "w"), indent=2)

        if glyph_data:
            json.dump(glyph_data, open(paths["glyph"], "w"), indent=2)
            if hasattr(gen, "generate_svg_template"):
                open(paths["svg"], "w").write(gen.generate_svg_template(glyph_data))

        print(f"\n📁 Agent saved to: {out.resolve()}")
        for name, path in paths.items():
            if path:
                print(f" • {Path(path).name}")

        return {"dbc": dbc, "suitcase": suitcase, "glyph": glyph_data, "paths": paths}

    def verify_agent(self, dbc_file: str, suitcase_file: str) -> Optional[Dict]:
        print("\n🔍 Verifying agent integrity...")
        try:
            with open(dbc_file, "r", encoding="utf-8") as f:
                dbc = json.load(f)
            with open(suitcase_file, "r", encoding="utf-8") as f:
                suitcase = json.load(f)

            print(f" Agent: {dbc.get('agent_name', 'Unknown')}")
            print(f" DBC ID: {dbc.get('dbc_id', 'Unknown')}")
            print(f" Custodian: {dbc.get('custodian_id', 'Unknown')}")
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
                if i > 0 and expected_prev != previous_hash:
                    chain_valid = False
                    print(f" ⚠ Entry {i}: Hash chain broken")
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
            return None

    def update_agent_state(self, dbc_file: str, suitcase_file: str, new_state: str, reason: str) -> Optional[dict]:
        if not create_suitcase_entry:
            print("✗ Missing create_suitcase_entry")
            return None

        try:
            dbc = json.load(open(dbc_file))
            suitcase = json.load(open(suitcase_file))

            last_hash = suitcase[-1]["entry_hash"] if suitcase else None

            new_entry = create_suitcase_entry(
                dbc_root=dbc["merkle_root"],
                event_type="STATE_CHANGE",
                details={"from": suitcase[-1].get("details", {}).get("to", "INITIAL") if suitcase else "INITIAL", "to": new_state, "reason": reason},
                previous_hash=last_hash,
            )

            suitcase.append(new_entry)
            json.dump(suitcase, open(suitcase_file, "w"), indent=2)

            print(f"✓ State updated to {new_state}")

            # Auto-update glyph using deterministic paths
            paths = derive_agent_paths(dbc_file)
            if paths["glyph"].exists() and EnhancedHGLGenerator:
                try:
                    gen = EnhancedHGLGenerator()
                    updated = gen.generate_glyph_data(
                        merkle_root=dbc["merkle_root"],
                        state=new_state,
                        custodian_id=dbc["custodian_id"],
                        agent_name=dbc.get("agent_name"),
                    )
                    json.dump(updated, open(paths["glyph"], "w"), indent=2)
                    open(paths["svg"], "w").write(gen.generate_svg_template(updated))
                    print(f"✓ Glyph updated")
                except Exception as e:
                    print(f"⚠ Glyph update failed: {e}")

            return new_entry
        except Exception as e:
            print(f"✗ Update failed: {e}")
            return None

    def list_agents(self, directory: str = ".") -> None:
        print(f"\n📋 Agents in '{directory}':")
        print("-" * 60)
        path = Path(directory)
        dbc_files = list(path.glob("*.dbc.json"))
        if not dbc_files:
            print(" No agents found")
            return
        for dbc_file in dbc_files:
            try:
                with open(dbc_file, "r", encoding="utf-8") as f:
                    dbc = json.load(f)
                paths = derive_agent_paths(str(dbc_file))
                suitcase_file = paths["suitcase"]
                glyph_file = paths["glyph"]
                entry_count = 0
                last_activity = "Never"
                if suitcase_file.exists():
                    with open(suitcase_file, "r", encoding="utf-8") as f:
                        suitcase = json.load(f)
                    entry_count = len(suitcase)
                    if entry_count > 0:
                        last_activity = suitcase[-1].get("timestamp", "Unknown")
                state = "UNKNOWN"
                if glyph_file.exists():
                    with open(glyph_file, "r", encoding="utf-8") as f:
                        glyph = json.load(f)
                    state = glyph.get("state", "UNKNOWN")
                state_icon = {"ACTIVE": "🟢", "RESTRICTED": "🟡", "REVOKED": "🔴", "QUARANTINED": "🟣", "SUSPENDED": "🟠"}.get(state, "⚪")
                print(f"{state_icon} {dbc.get('agent_name', 'Unnamed Agent')}")
                print(f" ID: {dbc.get('dbc_id', 'Unknown')}")
                print(f" State: {state}")
                print(f" Custodian: {dbc.get('custodian_id', 'Unknown')}")
                print(f" Entries: {entry_count}")
                print(f" Last Activity: {last_activity}")
                print(f" Files: {dbc_file.name}")
                print()
            except Exception as e:
                print(f"⚠ Error reading {dbc_file}: {e}")
                print()

    def generate_custom_glyph(self, merkle_root: str, state: str, **kwargs) -> Optional[dict]:
        if EnhancedHGLGenerator is None:
            print("✗ EnhancedHGLGenerator not available.")
            return None
        generator = EnhancedHGLGenerator()
        glyph_data = generator.generate_glyph_data(
            merkle_root=merkle_root,
            state=state,
            custodian_id=kwargs.get("custodian", ""),
            agent_name=kwargs.get("name", ""),
        )
        if glyph_data:
            output_format = kwargs.get("output", "text")
            if output_format == "svg":
                svg_content = generator.generate_svg_template(glyph_data)
                if kwargs.get("svg_file"):
                    with open(kwargs["svg_file"], "w", encoding="utf-8") as f:
                        f.write(svg_content)
                    print(f"✓ SVG saved to {kwargs['svg_file']}")
                else:
                    print(svg_content)
            else:
                generator.print_glyph_info(glyph_data, format=output_format)
            return glyph_data
        return None

    def show_agent_info(self, dbc_file: str) -> None:
        print("\n📊 Agent Information")
        print("=" * 60)
        try:
            with open(dbc_file, "r", encoding="utf-8") as f:
                dbc = json.load(f)
            print(f"Name: {dbc.get('agent_name', 'Unnamed Agent')}")
            print(f"DBC ID: {dbc.get('dbc_id')}")
            print(f"Custodian: {dbc.get('custodian_id')}")
            print(f"Created: {dbc.get('timestamp')}")
            print(f"Merkle Root: {str(dbc.get('merkle_root', ''))[:32]}...")
            print()
            paths = derive_agent_paths(dbc_file)
            glyph_file = paths["glyph"]
            suitcase_file = paths["suitcase"]
            if glyph_file.exists():
                with open(glyph_file, "r", encoding="utf-8") as f:
                    glyph = json.load(f)
                print("Visual Identity (HGL Glyph):")
                print(f" State: {glyph.get('state')}")
                print(f" Shape: {glyph.get('visual_attributes', {}).get('shape')}")
                print(f" Color: {glyph.get('visual_attributes', {}).get('color')}")
                print()
            if suitcase_file.exists():
                with open(suitcase_file, "r", encoding="utf-8") as f:
                    suitcase = json.load(f)
                print(f"Lifecycle Log (SUITCASE): {len(suitcase)} entries")
                print("Recent Activity:")
                for entry in suitcase[-5:]:
                    print(f" • {entry.get('timestamp')}: {entry.get('event_type')}")
            print("\n" + "=" * 60)
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="HELIX-TTD-DBC-SUITCASE v0.3 - Identity & Custody Primitive for Sovereign AI Agents",
        epilog="Example: helix new-agent --custodian alice --name AlphaBot",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # new-agent
    new = subparsers.add_parser("new-agent", help="Create a new AI agent")
    new.add_argument("--custodian", "-c", required=True, help="Custodian ID")
    new.add_argument("--name", "-n", required=True, help="Agent name")
    new.add_argument("--output-dir", "-o", default=".", help="Output directory")

    # verify
    verify = subparsers.add_parser("verify", help="Verify agent integrity")
    verify.add_argument("--dbc", required=True, help="DBC file")
    verify.add_argument("--suitcase", required=True, help="SUITCASE file")

    # update-state
    update = subparsers.add_parser("update-state", help="Update agent state")
    update.add_argument("--dbc", required=True, help="DBC file")
    update.add_argument("--suitcase", required=True, help="SUITCASE file")
    update.add_argument("--state", "-s", required=True,
                        choices=["ACTIVE", "RESTRICTED", "REVOKED", "QUARANTINED", "SUSPENDED"])
    update.add_argument("--reason", "-r", required=True, help="Reason for state change")

    # list
    subparsers.add_parser("list", help="List all agents").add_argument("--directory", "-d", default=".", help="Directory to scan")

    # glyph
    glyph = subparsers.add_parser("glyph", help="Generate HGL glyph")
    glyph.add_argument("merkle_root", help="Merkle root")
    glyph.add_argument("state", choices=["ACTIVE", "RESTRICTED", "REVOKED", "QUARANTINED", "SUSPENDED"])
    glyph.add_argument("--custodian", "-c", default="")
    glyph.add_argument("--name", "-n", default="")
    glyph.add_argument("--output", "-o", default="text", choices=["text", "json", "minimal", "svg"])
    glyph.add_argument("--svg-file", help="Save SVG to file")

    # info
    info = subparsers.add_parser("info", help="Show agent information")
    info.add_argument("--dbc", required=True, help="DBC file")

    # version
    subparsers.add_parser("version", help="Show version information")

    args = parser.parse_args()
    cli = HelixCLI()

    if not args.command:
        cli.print_banner()
        parser.print_help()
        return

    if args.command == "new-agent":
        cli.print_banner()
        cli.create_new_agent(args.custodian, args.name, args.output_dir)
    elif args.command == "verify":
        cli.verify_agent(args.dbc, args.suitcase)
    elif args.command == "update-state":
        cli.update_agent_state(args.dbc, args.suitcase, args.state, args.reason)
    elif args.command == "list":
        cli.list_agents(args.directory)
    elif args.command == "glyph":
        cli.generate_custom_glyph(args.merkle_root, args.state, custodian=args.custodian, name=args.name, output=args.output, svg_file=args.svg_file)
    elif args.command == "info":
        cli.show_agent_info(args.dbc)
    elif args.command == "version":
        cli.print_banner()


if __name__ == "__main__":
    main()
