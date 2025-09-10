"""
Configuration management for the Agent Builder
"""

from typing import Dict, Any

class Config:
    """Configuration manager for the application"""
    
    def __init__(self):
        self.component_templates = self._initialize_component_templates()
    
    def _initialize_component_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize component templates with enhanced configurations"""
        return {
            "Input": {
                "color": "#4CAF50",
                "icon": "📝",
                "description": "User input capture with validation",
                "properties": {
                    "input_type": ["text", "file", "voice", "structured"],
                    "validation": "",
                    "placeholder": "Enter your message...",
                    "required": True,
                    "max_length": 1000,
                    "multiline": False
                }
            },
            "LLM": {
                "color": "#2196F3",
                "icon": "🤖",
                "description": "Language model processing with advanced controls",
                "properties": {
                    "model": ["gpt-4o", "gpt-4", "gpt-3.5-turbo", "gpt-4o-mini"],
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "system_prompt": "You are a helpful assistant.",
                    "stream": True,
                    "top_p": 1.0,
                    "frequency_penalty": 0.0,
                    "presence_penalty": 0.0,
                    "stop_sequences": []
                }
            },
            "Prompt": {
                "color": "#9C27B0",
                "icon": "📋",
                "description": "Advanced prompt template engine",
                "properties": {
                    "template": "Answer the question: {question}",
                    "variables": ["question"],
                    "template_type": ["simple", "chat", "few_shot", "chain_of_thought"],
                    "examples": [],
                    "format_instructions": ""
                }
            },
            "Tool": {
                "color": "#FF9800",
                "icon": "🔧",
                "description": "External tools and API integrations",
                "properties": {
                    "tool_type": ["web_search", "calculator", "file_reader", "api_call", "database", "python_code"],
                    "endpoint": "",
                    "method": "GET",
                    "headers": {},
                    "parameters": {},
                    "timeout": 30,
                    "retry_count": 3,
                    "auth_type": "none"
                }
            },
            "Memory": {
                "color": "#607D8B",
                "icon": "🧠",
                "description": "Conversation memory and context management",
                "properties": {
                    "memory_type": ["conversation_buffer", "conversation_summary", "vector_store", "entity_memory"],
                    "max_tokens": 1000,
                    "return_messages": True,
                    "summary_template": "Summarize the conversation so far.",
                    "k": 5,
                    "moving_summary_buffer": 2000
                }
            },
            "Router": {
                "color": "#F44336",
                "icon": "🔀",
                "description": "Intelligent decision routing logic",
                "properties": {
                    "routing_type": ["semantic", "keyword", "model_based", "rule_based"],
                    "conditions": {},
                    "default_route": "",
                    "confidence_threshold": 0.8,
                    "routes": []
                }
            },
            "Parser": {
                "color": "#795548",
                "icon": "🔍",
                "description": "Output parsing and structured formatting",
                "properties": {
                    "parser_type": ["json", "xml", "regex", "structured", "pydantic"],
                    "schema": {},
                    "format_template": "",
                    "error_handling": "strict",
                    "output_format": "dict"
                }
            },
            "Validator": {
                "color": "#E91E63",
                "icon": "✅",
                "description": "Input/output validation and quality control",
                "properties": {
                    "validation_rules": {},
                    "error_message": "Validation failed",
                    "strict_mode": True,
                    "auto_fix": False,
                    "validation_type": "schema"
                }
            },
            "Webhook": {
                "color": "#00BCD4",
                "icon": "🌐",
                "description": "External webhook and API integration",
                "properties": {
                    "url": "",
                    "method": "POST",
                    "headers": {},
                    "auth_type": ["none", "bearer", "basic", "api_key"],
                    "timeout": 30,
                    "retry_on_failure": True,
                    "expected_status": 200
                }
            },
            "Output": {
                "color": "#8BC34A",
                "icon": "📤",
                "description": "Final output formatting and delivery",
                "properties": {
                    "format": ["text", "json", "html", "markdown"],
                    "template": "",
                    "post_process": False,
                    "save_to_file": False,
                    "file_path": ""
                }
            }
        }
    
    def get_component_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get all component templates"""
        return self.component_templates
    
    def get_component_template(self, component_type: str) -> Dict[str, Any]:
        """Get a specific component template"""
        return self.component_templates.get(component_type, {})
    
    def get_default_properties(self, component_type: str) -> Dict[str, Any]:
        """Get default properties for a component type"""
        template = self.get_component_template(component_type)
        return template.get('properties', {})
