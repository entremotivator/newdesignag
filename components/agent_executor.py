"""
Agent execution engine for running the created flows
"""

import asyncio
import time
from typing import Dict, List, Any, Optional
import openai
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AgentExecutor:
    """Executes agent flows with proper error handling and logging"""
    
    def __init__(self):
        self.execution_timeout = 300  # 5 minutes
    
    def execute_flow(
        self, 
        canvas_data: Dict, 
        input_data: str, 
        openai_client, 
        mode: str = "sequential",
        stream: bool = True
    ) -> Dict[str, Any]:
        """Execute the agent flow"""
        start_time = time.time()
        
        try:
            # Validate flow
            if not self._validate_flow(canvas_data):
                return {
                    'success': False,
                    'error': 'Invalid flow configuration',
                    'response_time': time.time() - start_time
                }
            
            # Execute based on mode
            if mode == "sequential":
                result = self._execute_sequential(canvas_data, input_data, openai_client, stream)
            elif mode == "parallel":
                result = self._execute_parallel(canvas_data, input_data, openai_client, stream)
            else:
                result = self._execute_conditional(canvas_data, input_data, openai_client, stream)
            
            response_time = time.time() - start_time
            
            return {
                'success': True,
                'output': result,
                'response_time': response_time,
                'intermediate_results': []
            }
        
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return {
                'success': False,
                'error': str(e),
                'response_time': time.time() - start_time
            }
    
    def _validate_flow(self, canvas_data: Dict) -> bool:
        """Validate the flow configuration"""
        nodes = canvas_data.get('nodes', [])
        connections = canvas_data.get('connections', [])
        
        if not nodes:
            return False
        
        # Check for input and output nodes
        has_input = any(node['type'] == 'input' for node in nodes)
        has_output = any(node['type'] == 'output' for node in nodes)
        
        return has_input and has_output
    
    def _execute_sequential(self, canvas_data: Dict, input_data: str, client, stream: bool) -> str:
        """Execute nodes sequentially"""
        nodes = canvas_data.get('nodes', [])
        connections = canvas_data.get('connections', [])
        
        # Build execution order
        execution_order = self._build_execution_order(nodes, connections)
        
        current_data = input_data
        
        for node_id in execution_order:
            node = next((n for n in nodes if n['id'] == node_id), None)
            if not node:
                continue
            
            current_data = self._execute_node(node, current_data, client)
        
        return current_data
    
    def _execute_parallel(self, canvas_data: Dict, input_data: str, client, stream: bool) -> str:
        """Execute compatible nodes in parallel"""
        # For now, fall back to sequential execution
        # In a full implementation, this would use asyncio for parallel execution
        return self._execute_sequential(canvas_data, input_data, client, stream)
    
    def _execute_conditional(self, canvas_data: Dict, input_data: str, client, stream: bool) -> str:
        """Execute with conditional routing"""
        # For now, fall back to sequential execution
        # In a full implementation, this would handle routing logic
        return self._execute_sequential(canvas_data, input_data, client, stream)
    
    def _build_execution_order(self, nodes: List[Dict], connections: List[Dict]) -> List[str]:
        """Build the execution order based on connections"""
        # Simple topological sort
        node_ids = [node['id'] for node in nodes]
        
        # Find input nodes (no incoming connections)
        incoming = {node_id: [] for node_id in node_ids}
        for conn in connections:
            incoming[conn['to']].append(conn['from'])
        
        # Start with input nodes
        queue = [node_id for node_id in node_ids if not incoming[node_id]]
        result = []
        
        while queue:
            current = queue.pop(0)
            result.append(current)
            
            # Find nodes that can now be executed
            for conn in connections:
                if conn['from'] == current:
                    target = conn['to']
                    incoming[target].remove(current)
                    if not incoming[target] and target not in queue and target not in result:
                        queue.append(target)
        
        return result
    
    def _execute_node(self, node: Dict, input_data: str, client) -> str:
        """Execute a single node"""
        node_type = node['type']
        properties = node.get('properties', {})
        
        try:
            if node_type == 'input':
                return input_data
            
            elif node_type == 'llm':
                return self._execute_llm_node(properties, input_data, client)
            
            elif node_type == 'prompt':
                return self._execute_prompt_node(properties, input_data)
            
            elif node_type == 'tool':
                return self._execute_tool_node(properties, input_data)
            
            elif node_type == 'memory':
                return self._execute_memory_node(properties, input_data)
            
            elif node_type == 'router':
                return self._execute_router_node(properties, input_data)
            
            elif node_type == 'parser':
                return self._execute_parser_node(properties, input_data)
            
            elif node_type == 'validator':
                return self._execute_validator_node(properties, input_data)
            
            elif node_type == 'webhook':
                return self._execute_webhook_node(properties, input_data)
            
            elif node_type == 'output':
                return self._execute_output_node(properties, input_data)
            
            else:
                logger.warning(f"Unknown node type: {node_type}")
                return input_data
        
        except Exception as e:
            logger.error(f"Error executing {node_type} node: {e}")
            return f"Error in {node_type}: {str(e)}"
    
    def _execute_llm_node(self, properties: Dict, input_data: str, client) -> str:
        """Execute LLM node"""
        try:
            model = properties.get('model', 'gpt-3.5-turbo')
            temperature = properties.get('temperature', 0.7)
            max_tokens = properties.get('max_tokens', 2000)
            system_prompt = properties.get('system_prompt', 'You are a helpful assistant.')
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_data}
            ]
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"LLM execution error: {e}")
            return f"LLM Error: {str(e)}"
    
    def _execute_prompt_node(self, properties: Dict, input_data: str) -> str:
        """Execute prompt template node"""
        template = properties.get('template', '{input}')
        variables = properties.get('variables', ['input'])
        
        # Simple template substitution
        result = template
        if 'input' in variables:
            result = result.replace('{input}', input_data)
        
        return result
    
    def _execute_tool_node(self, properties: Dict, input_data: str) -> str:
        """Execute tool node"""
        tool_type = properties.get('tool_type', 'calculator')
        
        if tool_type == 'calculator':
            try:
                # Simple calculator - evaluate safe expressions
                import re
                if re.match(r'^[\d\+\-\*\/$$$$\s\.]+$', input_data):
                    result = eval(input_data)
                    return str(result)
                else:
                    return "Invalid mathematical expression"
            except:
                return "Calculation error"
        
        elif tool_type == 'web_search':
            return f"Web search results for: {input_data} (simulated)"
        
        else:
            return f"Tool {tool_type} executed with input: {input_data}"
    
    def _execute_memory_node(self, properties: Dict, input_data: str) -> str:
        """Execute memory node"""
        memory_type = properties.get('memory_type', 'conversation_buffer')
        
        # Simple memory implementation
        return f"Memory ({memory_type}): {input_data}"
    
    def _execute_router_node(self, properties: Dict, input_data: str) -> str:
        """Execute router node"""
        routing_type = properties.get('routing_type', 'keyword')
        
        # Simple routing logic
        return input_data
    
    def _execute_parser_node(self, properties: Dict, input_data: str) -> str:
        """Execute parser node"""
        parser_type = properties.get('parser_type', 'json')
        
        if parser_type == 'json':
            try:
                import json
                # Try to parse as JSON
                parsed = json.loads(input_data)
                return json.dumps(parsed, indent=2)
            except:
                return input_data
        
        return input_data
    
    def _execute_validator_node(self, properties: Dict, input_data: str) -> str:
        """Execute validator node"""
        # Simple validation
        return input_data
    
    def _execute_webhook_node(self, properties: Dict, input_data: str) -> str:
        """Execute webhook node"""
        url = properties.get('url', '')
        
        if url:
            try:
                import requests
                response = requests.post(url, json={'data': input_data}, timeout=10)
                return response.text
            except:
                return f"Webhook error for URL: {url}"
        
        return input_data
    
    def _execute_output_node(self, properties: Dict, input_data: str) -> str:
        """Execute output node"""
        format_type = properties.get('format', 'text')
        template = properties.get('template', '{input}')
        
        if template and '{input}' in template:
            return template.replace('{input}', input_data)
        
        return input_data
