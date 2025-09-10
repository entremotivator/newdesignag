"""
Canvas management and rendering functionality
"""

import json
from typing import Dict, List, Any, Optional
import streamlit as st

class CanvasManager:
    """Manages the visual canvas and node interactions"""
    
    def __init__(self):
        self.grid_size = 30
        self.snap_threshold = 15
    
    def generate_canvas_html(self, canvas_data: Dict, config: Dict) -> str:
        """Generate the complete HTML/JS for the canvas"""
        # This method would generate the complete canvas HTML
        # The implementation is already provided in the main app
        pass
    
    def validate_node_position(self, x: float, y: float, snap_to_grid: bool = True) -> tuple:
        """Validate and adjust node position"""
        if snap_to_grid:
            x = round(x / self.grid_size) * self.grid_size
            y = round(y / self.grid_size) * self.grid_size
        
        # Ensure nodes stay within canvas bounds
        x = max(50, min(x, 950))
        y = max(50, min(y, 550))
        
        return x, y
    
    def validate_connection(self, from_node: str, to_node: str, connections: List[Dict]) -> bool:
        """Validate if a connection can be created"""
        # Prevent self-connections
        if from_node == to_node:
            return False
        
        # Check for existing connections
        existing = any(
            conn['from'] == from_node and conn['to'] == to_node
            for conn in connections
        )
        
        return not existing
    
    def calculate_bezier_path(self, start_pos: tuple, end_pos: tuple) -> str:
        """Calculate bezier curve path for connections"""
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Calculate control points
        dx = x2 - x1
        control_offset = min(abs(dx) * 0.5, 150)
        
        return f"M {x1} {y1} C {x1 + control_offset} {y1} {x2 - control_offset} {y2} {x2} {y2}"
    
    def export_canvas_data(self, canvas_data: Dict) -> str:
        """Export canvas data as JSON"""
        return json.dumps(canvas_data, indent=2)
    
    def import_canvas_data(self, json_data: str) -> Dict:
        """Import canvas data from JSON"""
        try:
            return json.loads(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {e}")
