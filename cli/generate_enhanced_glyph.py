#!/usr/bin/env python3
"""
Enhanced HGL (Human-Glyph Language) Generator for DBC/SUITCASE Framework.
Generates visual identity glyphs for AI agents based on cryptographic roots and states.
"""

import hashlib
import json
import sys
from datetime import datetime
from typing import Dict, Optional, Tuple
import argparse

class EnhancedHGLGenerator:
    """
    Generate enhanced visual glyphs for DBC (Digital Birth Certificate) agents.
    Each glyph is a deterministic visual representation of an agent's identity and state.
    """
    
    # State configurations with color, pattern, and icon
    STATE_CONFIG = {
        "ACTIVE": {
            "color": "#008080",  # Teal
            "pattern": "solid",
            "icon": "✓",
            "opacity": 1.0,
            "border": "2px solid #008080"
        },
        "RESTRICTED": {
            "color": "#FFBF00",  # Amber
            "pattern": "striped",
            "icon": "⚠",
            "opacity": 0.8,
            "border": "2px dashed #FFBF00"
        },
        "REVOKED": {
            "color": "#FF0000",  # Red
            "pattern": "crosshatch",
            "icon": "✗",
            "opacity": 0.4,
            "border": "2px dotted #FF0000"
        },
        "QUARANTINED": {
            "color": "#800080",  # Purple
            "pattern": "dotted",
            "icon": "?",
            "opacity": 0.6,
            "border": "2px double #800080"
        },
        "SUSPENDED": {
            "color": "#FF8C00",  # Dark Orange
            "pattern": "zigzag",
            "icon": "⏸",
            "opacity": 0.5,
            "border": "2px wavy #FF8C00"
        }
    }
    
    # Base shapes for glyph generation
    BASE_SHAPES = [
        "HEXAGON", "HELIX", "SHIELD", "CIRCLE",
        "TRIANGLE", "DIAMOND", "SQUARE", "STAR",
        "OCTAGON", "HEART", "CROSS", "MOON",
        "GEAR", "LOCK", "KEY", "CLOUD"
    ]
    
    def __init__(self, version: str = "v0.3"):
        self.version = version
        self.glyph_cache = {}
        
    def normalize_root(self, merkle_root: str) -> str:
        """Normalize Merkle root input."""
        # Remove 0x prefix if present and ensure lowercase
        root = merkle_root.strip().lower()
        if root.startswith('0x'):
            root = root[2:]
        return root
    
    def validate_root(self, merkle_root: str) -> bool:
        """Validate Merkle root format."""
        root = self.normalize_root(merkle_root)
        try:
            # Check if it's valid hex
            bytes.fromhex(root)
            return True
        except ValueError:
            return False
    
    def generate_glyph_data(
        self,
        merkle_root: str,
        state: str,
        custodian_id: str = "",
        agent_name: str = ""
    ) -> Optional[Dict]:
        """
        Generate comprehensive glyph data for a DBC agent.
        
        Args:
            merkle_root: The DBC's Merkle root (hex string)
            state: Current state (ACTIVE, RESTRICTED, etc.)
            custodian_id: Optional custodian identifier
            agent_name: Optional agent name for display
            
        Returns:
            Dictionary with glyph data or None if invalid
        """
        # Validate inputs
        if not self.validate_root(merkle_root):
            print(f"ERROR: Invalid Merkle root format: {merkle_root}")
            return None
        
        if state not in self.STATE_CONFIG:
            print(f"WARNING: Unknown state '{state}', defaulting to ACTIVE")
            state = "ACTIVE"
        
        # Normalize root
        root_hex = self.normalize_root(merkle_root)
        
        try:
            # Convert to bytes
            root_bytes = bytes.fromhex(root_hex)
            
            # Generate cache key
            cache_key = f"{root_hex[:16]}_{state}_{custodian_id}"
            
            # Check cache
            if cache_key in self.glyph_cache:
                return self.glyph_cache[cache_key]
            
            # Use first 4 bytes for various attributes
            if len(root_bytes) < 4:
                # Pad if needed
                hash_obj = hashlib.sha256(root_bytes)
                root_bytes = hash_obj.digest()
            
            # Extract seeds
            shape_seed = root_bytes[0]
            detail_seed = root_bytes[1]
            rotation_seed = root_bytes[2]
            scale_seed = root_bytes[3]
            
            # Determine shape
            shape_index = shape_seed % len(self.BASE_SHAPES)
            selected_shape = self.BASE_SHAPES[shape_index]
            
            # Get state configuration
            config = self.STATE_CONFIG[state]
            
            # Calculate derived attributes
            rotation = rotation_seed % 360
            scale = 0.7 + (scale_seed % 30) / 100  # 0.7-1.0
            
            # Generate unique pattern seed
            pattern_seed = detail_seed % 4
            
            # Create short identifiers
            short_root = f"{root_hex[:12]}...{root_hex[-4:]}" if len(root_hex) > 16 else root_hex
            short_custodian = custodian_id[:8] if custodian_id else "UNKNOWN"
            
            # Create comprehensive glyph data
            glyph_data = {
                "version": self.version,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "merkle_root": root_hex,
                "merkle_root_short": short_root,
                "state": state,
                "custodian_id": custodian_id,
                "custodian_short": short_custodian,
                "agent_name": agent_name,
                "visual_attributes": {
                    "color": config["color"],
                    "shape": selected_shape,
                    "icon": config["icon"],
                    "pattern": config["pattern"],
                    "pattern_seed": pattern_seed,
                    "rotation": rotation,
                    "scale": scale,
                    "opacity": config["opacity"],
                    "border": config["border"]
                },
                "derivation": {
                    "shape_seed": shape_seed,
                    "detail_seed": detail_seed,
                    "rotation_seed": rotation_seed,
                    "scale_seed": scale_seed,
                    "shape_index": shape_index
                }
            }
            
            # Cache the result
            self.glyph_cache[cache_key] = glyph_data
            
            return glyph_data
            
        except Exception as e:
            print(f"ERROR generating glyph: {e}")
            return None
    
    def generate_svg_template(self, glyph_data: Dict) -> str:
        """
        Generate an SVG template for the glyph.
        
        Args:
            glyph_data: Glyph data dictionary
            
        Returns:
            SVG string
        """
        if not glyph_data:
            return ""
        
        attrs = glyph_data["visual_attributes"]
        
        svg_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <!-- DBC HGL Glyph - {glyph_data['agent_name'] or glyph_data['merkle_root_short']} -->
    
    <!-- Background -->
    <rect width="200" height="200" fill="#f0f0f0" rx="10"/>
    
    <!-- Main Shape -->
    <g transform="translate(100, 100) scale({attrs['scale']}) rotate({attrs['rotation']})">
        <g fill="{attrs['color']}" fill-opacity="{attrs['opacity']}" stroke="{attrs['color']}" stroke-width="2">
            <!-- Shape placeholder - actual shape rendering would be more complex -->
            <circle cx="0" cy="0" r="70" opacity="0.7"/>
        </g>
        
        <!-- State Icon -->
        <text x="0" y="10" text-anchor="middle" font-family="Arial, sans-serif" 
              font-size="48" font-weight="bold" fill="white" stroke="black" stroke-width="1">
            {attrs['icon']}
        </text>
    </g>
    
    <!-- Border indicating state -->
    <rect width="200" height="200" fill="none" stroke="{attrs['color']}" 
          stroke-width="3" rx="10" stroke-dasharray="{ '5,5' if attrs['pattern'] == 'dashed' else 'none' }"/>
    
    <!-- Labels -->
    <text x="100" y="180" text-anchor="middle" font-family="Arial, sans-serif" 
          font-size="10" fill="#333">
        {glyph_data['merkle_root_short']}
    </text>
    <text x="100" y="190" text-anchor="middle" font-family="Arial, sans-serif" 
          font-size="10" fill="#666">
        State: {glyph_data['state']} | Custodian: {glyph_data['custodian_short']}
    </text>
</svg>'''
        
        return svg_template
    
    def print_glyph_info(self, glyph_data: Dict, format: str = "text"):
        """
        Print glyph information in specified format.
        
        Args:
            glyph_data: Glyph data dictionary
            format: Output format (text, json, minimal)
        """
        if not glyph_data:
            return
        
        if format == "json":
            print(json.dumps(glyph_data, indent=2))
        elif format == "minimal":
            attrs = glyph_data["visual_attributes"]
            print(f"📊 {glyph_data['agent_name'] or glyph_data['merkle_root_short']}")
            print(f"   State: {glyph_data['state']} {attrs['icon']}")
            print(f"   Shape: {attrs['shape']} (rot: {attrs['rotation']}°)")
            print(f"   Color: {attrs['color']}")
            print(f"   Custodian: {glyph_data['custodian_short']}")
        else:  # text format (default)
            print("\n" + "="*60)
            print("🔷 HELIX-TTD-DBC-SUITCASE HGL GLYPH")
            print("="*60)
            print(f"Version: {glyph_data['version']}")
            print(f"Timestamp: {glyph_data['timestamp']}")
            print(f"Agent: {glyph_data['agent_name'] or 'Unnamed Agent'}")
            print(f"DBC Root: {glyph_data['merkle_root_short']}")
            print(f"State: {glyph_data['state']}")
            print(f"Custodian: {glyph_data['custodian_id'] or 'Not specified'}")
            print("-"*60)
            print("VISUAL ATTRIBUTES:")
            attrs = glyph_data["visual_attributes"]
            print(f"  • Color: {attrs['color']}")
            print(f"  • Shape: {attrs['shape']}")
            print(f"  • Icon: {attrs['icon']}")
            print(f"  • Pattern: {attrs['pattern']}")
            print(f"  • Rotation: {attrs['rotation']}°")
            print(f"  • Scale: {attrs['scale']}")
            print(f"  • Opacity: {attrs['opacity']}")
            print("="*60 + "\n")


def main():
    """Command-line interface for enhanced glyph generation."""
    parser = argparse.ArgumentParser(
        description="Generate enhanced HGL glyphs for DBC agents",
        epilog="Example: python generate_enhanced_glyph.py 0x3A2B1F8C9D ACTIVE --custodian alice123"
    )
    
    parser.add_argument(
        "merkle_root",
        help="Merkle root of the DBC (hex string, with or without 0x prefix)"
    )
    
    parser.add_argument(
        "state",
        choices=["ACTIVE", "RESTRICTED", "REVOKED", "QUARANTINED", "SUSPENDED"],
        help="Current state of the agent"
    )
    
    parser.add_argument(
        "--custodian", "-c",
        default="",
        help="Custodian identifier"
    )
    
    parser.add_argument(
        "--name", "-n",
        default="",
        help="Agent name for display"
    )
    
    parser.add_argument(
        "--output", "-o",
        choices=["text", "json", "minimal", "svg"],
        default="text",
        help="Output format"
    )
    
    parser.add_argument(
        "--svg-file",
        help="Save SVG to specified file"
    )
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = EnhancedHGLGenerator()
    
    # Generate glyph data
    glyph_data = generator.generate_glyph_data(
        merkle_root=args.merkle_root,
        state=args.state,
        custodian_id=args.custodian,
        agent_name=args.name
    )
    
    if not glyph_data:
        sys.exit(1)
    
    # Output based on format
    if args.output == "svg":
        svg_content = generator.generate_svg_template(glyph_data)
        if args.svg_file:
            with open(args.svg_file, 'w') as f:
                f.write(svg_content)
            print(f"SVG saved to {args.svg_file}")
        else:
            print(svg_content)
    else:
        generator.print_glyph_info(glyph_data, format=args.output)


if __name__ == "__main__":
    main()
