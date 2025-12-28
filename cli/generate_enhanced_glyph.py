import hashlib

def generate_enhanced_glyph(merkle_root: str, state: str, custodian_id: str = ""):
    """
    Enhanced HGL glyph with more features.
    """
    # Normalize input
    root_hex = merkle_root.replace("0x", "").lower()
    
    # Color and pattern based on state
    state_config = {
        "ACTIVE": {"color": "#008080", "pattern": "solid", "icon": "✓"},
        "RESTRICTED": {"color": "#FFBF00", "pattern": "striped", "icon": "⚠"},
        "REVOKED": {"color": "#FF0000", "pattern": "crosshatch", "icon": "✗"},
        "QUARANTINED": {"color": "#800080", "pattern": "dotted", "icon": "?"}
    }
    
    # Use more bytes for richer shape generation
    try:
        root_bytes = bytes.fromhex(root_hex)
        # Use first 2 bytes for shape, next 2 for rotation/scale
        shape_seed = root_bytes[0] if len(root_bytes) > 0 else 0
        detail_seed = root_bytes[1] if len(root_bytes) > 1 else 0
        
        base_shapes = ["HEXAGON", "HELIX", "SHIELD", "CIRCLE", 
                      "TRIANGLE", "DIAMOND", "SQUARE", "STAR",
                      "OCTAGON", "HEART", "CROSS", "MOON"]
        
        selected_shape = base_shapes[shape_seed % len(base_shapes)]
        
        # Generate SVG-friendly attributes
        config = state_config.get(state, state_config["ACTIVE"])
        
        return {
            "merkle_root_short": root_hex[:12] + "...",
            "state": state,
            "color": config["color"],
            "shape": selected_shape,
            "icon": config["icon"],
            "pattern": config["pattern"],
            "rotation": detail_seed % 360,
            "scale": 0.8 + (detail_seed % 20) / 100,  # 0.8-1.0 scale
            "custodian_id": custodian_id[:8] if custodian_id else ""
        }
        
    except ValueError:
        # Invalid hex string
        return None
