"""
Helper functions and utilities
"""

import json
import hashlib
import time
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def generate_node_id(node_type: str) -> str:
    """Generate a unique node ID"""
    timestamp = str(int(time.time() * 1000))
    return f"{node_type.lower()}_{timestamp}"

def validate_json(json_string: str) -> bool:
    """Validate if a string is valid JSON"""
    try:
        json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False

def sanitize_input(input_text: str, max_length: int = 10000) -> str:
    """Sanitize user input"""
    if not isinstance(input_text, str):
        input_text = str(input_text)
    
    # Truncate if too long
    if len(input_text) > max_length:
        input_text = input_text[:max_length]
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<script', '</script', 'javascript:', 'data:']
    for char in dangerous_chars:
        input_text = input_text.replace(char, '')
    
    return input_text.strip()

def format_timestamp(timestamp: Optional[float] = None) -> str:
    """Format timestamp for display"""
    if timestamp is None:
        timestamp = time.time()
    
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def calculate_execution_time(start_time: float) -> float:
    """Calculate execution time in seconds"""
    return round(time.time() - start_time, 3)

def hash_config(config: Dict[str, Any]) -> str:
    """Generate a hash for configuration comparison"""
    config_str = json.dumps(config, sort_keys=True)
    return hashlib.md5(config_str.encode()).hexdigest()

def deep_merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result

def validate_node_properties(node_type: str, properties: Dict[str, Any], templates: Dict) -> List[str]:
    """Validate node properties against template"""
    errors = []
    
    if node_type not in templates:
        errors.append(f"Unknown node type: {node_type}")
        return errors
    
    template_props = templates[node_type].get('properties', {})
    
    for prop_name, prop_value in properties.items():
        if prop_name not in template_props:
            errors.append(f"Unknown property '{prop_name}' for {node_type}")
            continue
        
        template_value = template_props[prop_name]
        
        # Validate against template constraints
        if isinstance(template_value, list) and prop_value not in template_value:
            errors.append(f"Invalid value '{prop_value}' for {prop_name}. Must be one of: {template_value}")
        
        elif isinstance(template_value, bool) and not isinstance(prop_value, bool):
            errors.append(f"Property '{prop_name}' must be boolean")
        
        elif isinstance(template_value, (int, float)) and not isinstance(prop_value, (int, float)):
            errors.append(f"Property '{prop_name}' must be numeric")
    
    return errors

def export_agent_config(canvas_data: Dict[str, Any], metadata: Optional[Dict] = None) -> Dict[str, Any]:
    """Export complete agent configuration"""
    config = {
        'version': '2.0',
        'exported_at': datetime.now().isoformat(),
        'canvas_data': canvas_data,
        'metadata': metadata or {}
    }
    
    return config

def import_agent_config(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Import and validate agent configuration"""
    required_fields = ['canvas_data']
    
    for field in required_fields:
        if field not in config_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate canvas data structure
    canvas_data = config_data['canvas_data']
    if not isinstance(canvas_data, dict):
        raise ValueError("Invalid canvas_data format")
    
    if 'nodes' not in canvas_data or 'connections' not in canvas_data:
        raise ValueError("Canvas data missing nodes or connections")
    
    return canvas_data

class PerformanceMonitor:
    """Monitor performance metrics"""
    
    def __init__(self):
        self.metrics = {}
    
    def start_timer(self, operation: str):
        """Start timing an operation"""
        self.metrics[operation] = {'start_time': time.time()}
    
    def end_timer(self, operation: str) -> float:
        """End timing and return duration"""
        if operation not in self.metrics:
            return 0.0
        
        duration = time.time() - self.metrics[operation]['start_time']
        self.metrics[operation]['duration'] = duration
        return duration
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all performance metrics"""
        return self.metrics
