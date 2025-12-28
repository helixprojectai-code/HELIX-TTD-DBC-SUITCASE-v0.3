import hashlib
import sys

def generate_hgl_glyph(merkle_root: str, state: str):
    """
    Generates visual cues based on the DBC Merkle Root and Current State.
    """
    # 1. Color Mapping (State)
    colors = {
        "ACTIVE": "TEAL (#008080)",
        "RESTRICTED": "AMBER (#FFBF00)",
        "REVOKED": "RED (#FF0000)"
    }
    
    # 2. Shape Derivation (First 4 bytes of Root)
    # This simulates mapping hash bits to geometric primitives
    root_bytes = bytes.fromhex(merkle_root)
    shape_seed = root_bytes[0] # First byte determines base shape
    
    base_shapes = ["HEXAGON", "HELIX", "SHIELD", "CIRCLE", "TRIANGLE", "DIAMOND", "SQUARE", "STAR"]
    selected_shape = base_shapes[shape_seed % 8]
    
    # 3. Output
    print(f"--- HGL GLYPH GENERATION ---")
    print(f"INPUT ROOT: {merkle_root}")
    print(f"STATE: {state}")
    print(f"VISUAL CUE: {colors.get(state, 'GRAY')}")
    print(f"BASE GEOMETRY: {selected_shape}")
    print(f"OVERLAY: {'NONE' if state == 'ACTIVE' else 'WARNING_ICON'}")
    print(f"----------------------------")

if __name__ == "__main__":
    # Example Usage
    # python generate_hgl.py <merkle_root> <state>
    if len(sys.argv) > 2:
        generate_hgl_glyph(sys.argv[1], sys.argv[2])
    else:
        # Default Test
        generate_hgl_glyph("0x3A2B1F8C9D", "ACTIVE")
