import streamlit as st
import json
import glob
from pathlib import Path
from datetime import datetime
import sys

# Import Helix Core logic
try:
    from cli.generate_enhanced_glyph import EnhancedHGLGenerator
    from cli.dbc_suitcase import validate_entry_integrity
except ImportError:
    st.error("Helix Core modules not found. Run this from the repo root.")
    sys.exit()

# Page Config
st.set_page_config(
    page_title="Helix-TTD Custody Dashboard",
    page_icon="🦆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING ---
st.markdown("""
<style>
    .reportview-container { background: #0e1117; }
    .metric-card { background-color: #262730; padding: 15px; border-radius: 10px; border: 1px solid #444; }
    h1, h2, h3 { color: #00e6e6; } /* Helix Teal */
    .stSuccess { background-color: #004d4d; color: #00e6e6; }
    .stError { background-color: #4d0000; color: #ff4d4d; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: SCANNER ---
st.sidebar.title("🦆 Helix Watchtower")
st.sidebar.markdown("---")
scan_dir = st.sidebar.text_input("Scan Directory", value=".", help="Path where agents are stored")

# Scan for DBCs
dbc_files = list(glob.glob(f"{scan_dir}/*.dbc.json"))

if not dbc_files:
    st.sidebar.warning("No Agents Found.")
    st.title("Waiting for Agents...")
    st.info(f"Run `python3 helix.py new-agent` to mint an agent in `{scan_dir}`.")
    st.stop()

# Agent Selector
selected_file = st.sidebar.selectbox(
    "Select Agent Identity", 
    dbc_files, 
    format_func=lambda x: Path(x).stem.replace('.dbc', '')
)

# --- LOAD DATA ---
try:
    with open(selected_file, 'r') as f:
        dbc = json.load(f)
    
    suitcase_path = Path(selected_file).parent / Path(selected_file).name.replace('.dbc.json', '.suitcase.json')
    has_suitcase = suitcase_path.exists()
    
    if has_suitcase:
        with open(suitcase_path, 'r') as f:
            suitcase = json.load(f)
    else:
        suitcase = []

except Exception as e:
    st.error(f"Corrupt Identity File: {e}")
    st.stop()

# --- MAIN DASHBOARD ---

# Header
col1, col2 = st.columns([1, 3])

with col1:
    # Generate Live Glyph
    if has_suitcase and len(suitcase) > 0:
        current_state = suitcase[-1]['details'].get('to', 'ACTIVE')
    else:
        current_state = "UNKNOWN"
        
    gen = EnhancedHGLGenerator()
    glyph_data = gen.generate_glyph_data(
        merkle_root=dbc.get('merkle_root', ''),
        state=current_state,
        custodian_id=dbc.get('custodian_id', ''),
        agent_name=dbc.get('agent_name', '')
    )
    svg = gen.generate_svg_template(glyph_data)
    st.image(svg, width=250)

with col2:
    st.title(dbc.get('agent_name', 'Unknown Agent'))
    st.caption(f"DBC ID: `{dbc.get('dbc_id')}`")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Custodian", dbc.get('custodian_id', 'Unknown')[:10]+"...")
    m2.metric("Lifecycle Entries", len(suitcase))
    m3.metric("Current State", current_state)

st.markdown("---")

# --- VERIFICATION ENGINE ---
st.subheader("🔐 Forensic Verification")

if not has_suitcase:
    st.error("MISSING SUITCASE: Chain of Custody Broken")
else:
    all_valid = True
    
    # 1. Check Tether
    tether_ok = all(e.get('dbc_root') == dbc.get('merkle_root') for e in suitcase)
    
    # 2. Check Integrity
    integrity_issues = []
    for i, entry in enumerate(suitcase):
        valid, msg = validate_entry_integrity(entry)
        if not valid:
            all_valid = False
            integrity_issues.append(f"Entry {i}: {msg}")

    if all_valid and tether_ok:
        st.success("✅ CHAIN OF CUSTODY VERIFIED: Cryptographically Intact")
    else:
        st.error("❌ CUSTODY COMPROMISED: Tampering Detected")
        if not tether_ok: st.write("- DBC Tether Broken (Suitcase belongs to different agent)")
        for issue in integrity_issues:
            st.write(f"- {issue}")

# --- TIMELINE VISUALIZER ---
st.subheader("📜 Suitcase Log (Append-Only)")

for i, entry in enumerate(reversed(suitcase)): # Show newest first
    with st.expander(f"{entry['timestamp']} | {entry['event_type']}", expanded=(i==0)):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.json(entry['details'])
        with c2:
            st.caption("Cryptographic Proof")
            st.text(f"Hash: {entry['entry_hash'][:8]}...")
            st.text(f"Prev: {entry.get('previous_hash', 'GENESIS')[:8]}...")
            if i == len(suitcase) - 1:
                st.caption("⚓ GENESIS ANCHOR")

# --- RAW DATA VIEW ---
with st.expander("🔍 View Raw DBC Metadata"):
    st.json(dbc)
