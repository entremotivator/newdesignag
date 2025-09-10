"""
Data models and structures for the Agent Builder
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import uuid
from datetime import datetime

class NodeType(Enum):
    """Enumeration of available node types"""
    INPUT = "input"
    LLM = "llm"
    TOOL = "tool"
    MEMORY = "memory"
    ROUTER = "router"
    OUTPUT = "output"
    PROMPT = "prompt"
    PARSER = "parser"
    VALIDATOR = "validator"
    WEBHOOK = "webhook"

@dataclass
class NodeConfig:
    """Configuration for a single node"""
    id: str
    type: str
    name: str
    x: float
    y: float
    properties: Dict[str, Any]
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())

@dataclass
class Connection:
    """Connection between two nodes"""
    id: str
    from_node: str
    to_node: str
    from_port: str
    to_port: str
    condition: Optional[str] = None
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())

@dataclass
class AgentFlow:
    """Complete agent flow configuration"""
    nodes: List[NodeConfig]
    connections: List[Connection]
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        if not self.metadata:
            self.metadata = {
                'created_at': datetime.now().isoformat(),
                'version': '1.0',
                'description': ''
            }

@dataclass
class ExecutionStats:
    """Statistics for agent execution"""
    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0
    avg_response_time: float = 0.0
    execution_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_execution(self, success: bool, response_time: float, error: Optional[str] = None):
        """Add an execution record"""
        self.total_runs += 1
        if success:
            self.successful_runs += 1
        else:
            self.failed_runs += 1
        
        # Update average response time
        self.avg_response_time = (
            (self.avg_response_time * (self.total_runs - 1) + response_time) / self.total_runs
        )
        
        # Add to history
        self.execution_history.append({
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'response_time': response_time,
            'error': error
        })
        
        # Keep only last 100 executions
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]

@dataclass
class ExecutionResult:
    """Result of agent execution"""
    success: bool
    output: Any
    response_time: float
    error: Optional[str] = None
    intermediate_results: List[Dict[str, Any]] = field(default_factory=list)
