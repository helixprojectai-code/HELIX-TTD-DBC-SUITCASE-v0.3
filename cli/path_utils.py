from pathlib import Path

def derive_agent_paths(dbc_file: str) -> dict:
    """
    Given a DBC filename ending in `.dbc.json`,
    derive all related HELIX-TTD artifact paths deterministically.

    Returns a dict with keys:
      - dbc
      - suitcase
      - glyph
      - svg
    """
    p = Path(dbc_file)

    if not p.name.endswith(".dbc.json"):
        raise ValueError("DBC filename must end with '.dbc.json'")

    base = p.name[:-len(".dbc.json")]

    return {
        "dbc": p,
        "suitcase": p.with_name(f"{base}.suitcase.json"),
        "glyph": p.with_name(f"{base}.glyph.json"),
        "svg": p.with_name(f"{base}.svg"),
    }
