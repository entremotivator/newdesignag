"""
Advanced LangChain Agent Builder with Fabric.js
A professional drag-and-drop interface for building AI agent workflows
"""

import streamlit as st
import json
import openai
from typing import Dict, List, Any, Optional, Union
import uuid
import re
import requests
import time
from datetime import datetime
import base64
import io
import pandas as pd
import numpy as np
from dataclasses import dataclass, asdict, field
from enum import Enum
import logging
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor
import hashlib

# Import our modular components
from components.ui_components import UIComponents
from components.canvas_manager import CanvasManager
from components.agent_executor import AgentExecutor
from components.data_models import *
from utils.config import Config
from utils.helpers import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentBuilderApp:
    """Main application class for the Agent Builder"""
    
    def __init__(self):
        self.config = Config()
        self.ui = UIComponents()
        self.canvas = CanvasManager()
        self.executor = AgentExecutor()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state with proper defaults and validation"""
        defaults = {
            'agent_flow': AgentFlow([], [], {}),
            'selected_node': None,
            'canvas_data': {'nodes': [], 'connections': []},
            'execution_log': [],
            'agent_running': False,
            'openai_client': None,
            'api_status': 'disconnected',
            'conversation_history': [],
            'current_agent_config': None,
            'saved_agents': {},
            'execution_stats': ExecutionStats(),
            'canvas_zoom': 1.0,
            'canvas_pan': {'x': 0, 'y': 0},
            'last_save_time': None,
            'auto_save_enabled': True,
            'theme': 'light',
            'grid_enabled': True,
            'snap_to_grid': True
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def run(self):
        """Main application entry point"""
        try:
            self._setup_page_config()
            self._render_custom_css()
            self._render_sidebar()
            self._render_main_content()
            self._handle_auto_save()
        except Exception as e:
            logger.error(f"Application error: {e}")
            st.error(f"An error occurred: {e}")
    
    def _setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Advanced LangChain Agent Builder",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/your-repo/agent-builder',
                'Report a bug': 'https://github.com/your-repo/agent-builder/issues',
                'About': "Advanced LangChain Agent Builder v2.0"
            }
        )
    
    def _render_custom_css(self):
        """Render enhanced custom CSS"""
        st.markdown(self.ui.get_custom_css(), unsafe_allow_html=True)
    
    def _render_sidebar(self):
        """Render the enhanced sidebar"""
        self.ui.render_sidebar(self.config, st.session_state)
    
    def _render_main_content(self):
        """Render the main application content"""
        st.markdown('<h1 class="main-header">🤖 Advanced LangChain Agent Builder</h1>', unsafe_allow_html=True)
        
        # Enhanced tabs with better organization
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎨 Visual Builder", 
            "⚙️ Configuration", 
            "🚀 Execution", 
            "📊 Analytics",
            "💾 Management"
        ])
        
        with tab1:
            self._render_visual_builder()
        
        with tab2:
            self._render_configuration()
        
        with tab3:
            self._render_execution()
        
        with tab4:
            self._render_analytics()
        
        with tab5:
            self._render_management()
    
    def _render_visual_builder(self):
        """Render the enhanced visual canvas"""
        st.markdown("### 🎨 Visual Canvas")
        
        # Canvas controls
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("🔍 Zoom In", use_container_width=True):
                st.session_state.canvas_zoom = min(st.session_state.canvas_zoom * 1.2, 3.0)
        
        with col2:
            if st.button("🔍 Zoom Out", use_container_width=True):
                st.session_state.canvas_zoom = max(st.session_state.canvas_zoom * 0.8, 0.3)
        
        with col3:
            if st.button("🎯 Reset View", use_container_width=True):
                st.session_state.canvas_zoom = 1.0
                st.session_state.canvas_pan = {'x': 0, 'y': 0}
        
        with col4:
            st.session_state.grid_enabled = st.checkbox("Grid", value=st.session_state.grid_enabled)
        
        with col5:
            st.session_state.snap_to_grid = st.checkbox("Snap", value=st.session_state.snap_to_grid)
        
        # Enhanced canvas with complete JavaScript
        canvas_html = self._generate_enhanced_canvas_html()
        st.components.v1.html(canvas_html, height=800, scrolling=False)
    
    def _generate_enhanced_canvas_html(self) -> str:
        """Generate complete enhanced HTML/JS for the canvas"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.0/fabric.min.js"></script>
            <style>
                body {{ margin: 0; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
                .canvas-container {{ 
                    border: 2px solid #ddd; 
                    border-radius: 15px; 
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    position: relative;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                }}
                .toolbar {{
                    display: flex;
                    gap: 10px;
                    margin-bottom: 15px;
                    padding: 15px;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    flex-wrap: wrap;
                }}
                .tool-btn {{
                    padding: 10px 15px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .tool-btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                }}
                .properties-panel {{
                    width: 320px;
                    background: white;
                    border: 1px solid #ddd;
                    border-radius: 15px;
                    padding: 20px;
                    max-height: 700px;
                    overflow-y: auto;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                }}
                .property-group {{
                    margin-bottom: 20px;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 8px;
                    border-left: 4px solid #007bff;
                }}
                .property-input {{
                    width: 100%;
                    padding: 8px 12px;
                    border: 1px solid #ddd;
                    border-radius: 6px;
                    margin-top: 5px;
                    transition: border-color 0.3s ease;
                }}
                .property-input:focus {{
                    outline: none;
                    border-color: #007bff;
                    box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
                }}
                .minimap {{
                    position: absolute;
                    top: 15px;
                    right: 15px;
                    width: 180px;
                    height: 120px;
                    border: 2px solid #333;
                    background: rgba(255,255,255,0.9);
                    border-radius: 8px;
                    backdrop-filter: blur(5px);
                }}
                .status-bar {{
                    position: absolute;
                    bottom: 15px;
                    left: 15px;
                    background: rgba(0,0,0,0.8);
                    color: white;
                    padding: 8px 15px;
                    border-radius: 20px;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="toolbar">
                <button class="tool-btn" style="background: #4CAF50; color: white;" onclick="addComponent('Input')">📝 Input</button>
                <button class="tool-btn" style="background: #2196F3; color: white;" onclick="addComponent('LLM')">🤖 LLM</button>
                <button class="tool-btn" style="background: #FF9800; color: white;" onclick="addComponent('Tool')">🔧 Tool</button>
                <button class="tool-btn" style="background: #607D8B; color: white;" onclick="addComponent('Memory')">🧠 Memory</button>
                <button class="tool-btn" style="background: #F44336; color: white;" onclick="addComponent('Router')">🔀 Router</button>
                <button class="tool-btn" style="background: #9C27B0; color: white;" onclick="addComponent('Prompt')">📋 Prompt</button>
                <button class="tool-btn" style="background: #795548; color: white;" onclick="addComponent('Parser')">🔍 Parser</button>
                <button class="tool-btn" style="background: #8BC34A; color: white;" onclick="addComponent('Output')">📤 Output</button>
                <button class="tool-btn" style="background: #FF5722; color: white;" onclick="toggleConnectionMode()">🔗 Connect</button>
                <button class="tool-btn" style="background: #9E9E9E; color: white;" onclick="clearCanvas()">🗑️ Clear</button>
            </div>
            
            <div style="display: flex; gap: 20px;">
                <div class="canvas-container" style="flex: 1;">
                    <canvas id="fabric-canvas" width="1000" height="600"></canvas>
                    <div class="minimap" id="minimap"></div>
                    <div class="status-bar" id="status-bar">Ready</div>
                </div>
                <div class="properties-panel" id="properties-panel">
                    <h3>🎛️ Node Properties</h3>
                    <div id="properties-content">
                        <p style="color: #666; text-align: center; margin-top: 50px;">
                            Select a node to edit its properties
                        </p>
                    </div>
                </div>
            </div>

            <script>
                // Enhanced Fabric.js canvas with professional features
                const canvas = new fabric.Canvas('fabric-canvas', {{
                    backgroundColor: '#f8f9fa',
                    selection: true,
                    preserveObjectStacking: true,
                    enableRetinaScaling: true
                }});

                // Component templates
                const componentTemplates = {json.dumps(self.config.get_component_templates())};

                // Enhanced state management
                let canvasState = {json.dumps(st.session_state.canvas_data)};
                let selectedNode = null;
                let connectionMode = false;
                let connectionStart = null;
                let nodeCounter = 1;
                let gridSnap = {20 if st.session_state.snap_to_grid else 1};
                let zoomLevel = {st.session_state.canvas_zoom};
                let gridEnabled = {str(st.session_state.grid_enabled).lower()};

                // Initialize canvas
                function initializeCanvas() {{
                    if (gridEnabled) {{
                        drawGrid();
                    }}
                    
                    // Load existing nodes and connections
                    loadCanvasState();
                    
                    // Setup event listeners
                    setupEventListeners();
                    
                    updateStatusBar('Canvas initialized');
                }}

                // Enhanced grid drawing
                function drawGrid() {{
                    const gridSize = 30;
                    const canvasWidth = canvas.width;
                    const canvasHeight = canvas.height;
                    
                    // Clear existing grid
                    canvas.getObjects().forEach(obj => {{
                        if (obj.isGrid) {{
                            canvas.remove(obj);
                        }}
                    }});
                    
                    // Vertical lines
                    for (let i = 0; i <= canvasWidth; i += gridSize) {{
                        const line = new fabric.Line([i, 0, i, canvasHeight], {{
                            stroke: '#e0e0e0',
                            strokeWidth: 0.5,
                            selectable: false,
                            evented: false,
                            excludeFromExport: true,
                            isGrid: true
                        }});
                        canvas.add(line);
                        canvas.sendToBack(line);
                    }}
                    
                    // Horizontal lines
                    for (let i = 0; i <= canvasHeight; i += gridSize) {{
                        const line = new fabric.Line([0, i, canvasWidth, i], {{
                            stroke: '#e0e0e0',
                            strokeWidth: 0.5,
                            selectable: false,
                            evented: false,
                            excludeFromExport: true,
                            isGrid: true
                        }});
                        canvas.add(line);
                        canvas.sendToBack(line);
                    }}
                }}

                // Enhanced node creation with better animations
                function createNode(type, x = null, y = null) {{
                    const nodeId = type.toLowerCase() + '_' + nodeCounter++;
                    const template = componentTemplates[type];
                    
                    if (!template) {{
                        console.error('Unknown component type:', type);
                        return null;
                    }}
                    
                    // Calculate position with smart placement
                    const posX = x || (Math.random() * 600 + 200);
                    const posY = y || (Math.random() * 400 + 100);
                    
                    // Snap to grid if enabled
                    const snapX = gridSnap > 1 ? Math.round(posX / gridSnap) * gridSnap : posX;
                    const snapY = gridSnap > 1 ? Math.round(posY / gridSnap) * gridSnap : posY;
                    
                    // Create enhanced gradient
                    const gradient = new fabric.Gradient({{
                        type: 'linear',
                        coords: {{ x1: 0, y1: 0, x2: 0, y2: 1 }},
                        colorStops: [
                            {{ offset: 0, color: template.color }},
                            {{ offset: 0.5, color: template.color }},
                            {{ offset: 1, color: fabric.Color.fromHex(template.color).darker(0.2).toHex() }}
                        ]
                    }});
                    
                    // Main rectangle with enhanced styling
                    const rect = new fabric.Rect({{
                        width: 160,
                        height: 100,
                        fill: gradient,
                        stroke: '#333',
                        strokeWidth: 2,
                        rx: 20,
                        ry: 20,
                        shadow: new fabric.Shadow({{
                            color: 'rgba(0,0,0,0.3)',
                            blur: 15,
                            offsetX: 3,
                            offsetY: 3
                        }})
                    }});
                    
                    // Enhanced icon with better positioning
                    const icon = new fabric.Text(template.icon, {{
                        fontSize: 28,
                        fontFamily: 'Arial',
                        fill: 'white',
                        textAlign: 'center',
                        top: -35,
                        left: 0,
                        originX: 'center',
                        originY: 'center',
                        shadow: new fabric.Shadow({{
                            color: 'rgba(0,0,0,0.5)',
                            blur: 2,
                            offsetX: 1,
                            offsetY: 1
                        }})
                    }});
                    
                    // Title with better typography
                    const title = new fabric.Text(type, {{
                        fontSize: 16,
                        fontWeight: 'bold',
                        fontFamily: 'Segoe UI, Arial',
                        fill: 'white',
                        textAlign: 'center',
                        top: -5,
                        left: 0,
                        originX: 'center',
                        originY: 'center',
                        shadow: new fabric.Shadow({{
                            color: 'rgba(0,0,0,0.5)',
                            blur: 2,
                            offsetX: 1,
                            offsetY: 1
                        }})
                    }});
                    
                    // Status indicator with animation
                    const statusIndicator = new fabric.Circle({{
                        radius: 8,
                        fill: '#4CAF50',
                        stroke: 'white',
                        strokeWidth: 2,
                        top: -45,
                        left: 70,
                        originX: 'center',
                        originY: 'center',
                        shadow: new fabric.Shadow({{
                            color: 'rgba(76, 175, 80, 0.5)',
                            blur: 5,
                            offsetX: 0,
                            offsetY: 0
                        }})
                    }});
                    
                    // Enhanced input/output ports
                    const inputPort = new fabric.Circle({{
                        radius: 10,
                        fill: '#fff',
                        stroke: '#333',
                        strokeWidth: 3,
                        top: 0,
                        left: -80,
                        originX: 'center',
                        originY: 'center',
                        portType: 'input',
                        shadow: new fabric.Shadow({{
                            color: 'rgba(0,0,0,0.3)',
                            blur: 5,
                            offsetX: 1,
                            offsetY: 1
                        }})
                    }});
                    
                    const outputPort = new fabric.Circle({{
                        radius: 10,
                        fill: '#fff',
                        stroke: '#333',
                        strokeWidth: 3,
                        top: 0,
                        left: 80,
                        originX: 'center',
                        originY: 'center',
                        portType: 'output',
                        shadow: new fabric.Shadow({{
                            color: 'rgba(0,0,0,0.3)',
                            blur: 5,
                            offsetX: 1,
                            offsetY: 1
                        }})
                    }});
                    
                    // Create enhanced group
                    const group = new fabric.Group([rect, icon, title, statusIndicator, inputPort, outputPort], {{
                        left: snapX,
                        top: snapY,
                        selectable: true,
                        hasControls: true,
                        hasBorders: true,
                        lockScalingX: true,
                        lockScalingY: true,
                        nodeId: nodeId,
                        nodeType: type,
                        borderColor: template.color,
                        cornerColor: template.color,
                        cornerStyle: 'circle',
                        cornerSize: 8,
                        transparentCorners: false
                    }});
                    
                    // Enhanced event listeners
                    setupNodeEvents(group, template);
                    
                    // Add to canvas with smooth animation
                    canvas.add(group);
                    
                    // Entrance animation
                    group.set({{ opacity: 0, scaleX: 0.1, scaleY: 0.1 }});
                    group.animate({{ opacity: 1, scaleX: 1, scaleY: 1 }}, {{
                        duration: 400,
                        easing: fabric.util.ease.easeOutBack,
                        onChange: canvas.renderAll.bind(canvas)
                    }});
                    
                    // Add to state
                    const nodeData = {{
                        id: nodeId,
                        type: type,
                        x: snapX,
                        y: snapY,
                        name: type + '_' + nodeId.split('_')[1],
                        properties: {{ ...template.properties }}
                    }};
                    
                    canvasState.nodes.push(nodeData);
                    updateStreamlitState();
                    updateStatusBar(`Added ${{type}} node`);
                    
                    return group;
                }}

                // Setup enhanced node event listeners
                function setupNodeEvents(group, template) {{
                    group.on('mousedown', function(e) {{
                        if (connectionMode) {{
                            handleConnectionMode(group);
                        }} else {{
                            selectNode(group);
                        }}
                    }});
                    
                    group.on('moving', function(e) {{
                        if (gridSnap > 1) {{
                            const snapX = Math.round(group.left / gridSnap) * gridSnap;
                            const snapY = Math.round(group.top / gridSnap) * gridSnap;
                            group.set({{ left: snapX, top: snapY }});
                        }}
                        updateConnections();
                        updateNodePosition(group);
                    }});
                    
                    group.on('mouseenter', function(e) {{
                        if (!connectionMode) {{
                            group.set({{
                                shadow: new fabric.Shadow({{
                                    color: 'rgba(0,0,0,0.5)',
                                    blur: 20,
                                    offsetX: 4,
                                    offsetY: 4
                                }})
                            }});
                            canvas.renderAll();
                        }}
                    }});
                    
                    group.on('mouseleave', function(e) {{
                        if (group !== selectedNode && !connectionMode) {{
                            group.set({{
                                shadow: new fabric.Shadow({{
                                    color: 'rgba(0,0,0,0.3)',
                                    blur: 15,
                                    offsetX: 3,
                                    offsetY: 3
                                }})
                            }});
                            canvas.renderAll();
                        }}
                    }});
                    
                    group.on('scaling', function(e) {{
                        // Prevent scaling to maintain consistent node sizes
                        group.set({{ scaleX: 1, scaleY: 1 }});
                    }});
                }}

                // Enhanced connection handling
                function handleConnectionMode(group) {{
                    if (!connectionStart) {{
                        connectionStart = group;
                        group.set({{ 
                            strokeWidth: 4, 
                            stroke: '#ff4444',
                            shadow: new fabric.Shadow({{
                                color: 'rgba(255, 68, 68, 0.5)',
                                blur: 10,
                                offsetX: 0,
                                offsetY: 0
                            }})
                        }});
                        canvas.renderAll();
                        updateStatusBar('Select target node to connect');
                    }} else if (connectionStart !== group) {{
                        if (canConnect(connectionStart, group)) {{
                            createConnection(connectionStart, group);
                            resetConnectionMode();
                            updateStatusBar('Connection created');
                        }} else {{
                            updateStatusBar('Invalid connection');
                        }}
                    }}
                }}

                // Validate connections
                function canConnect(startNode, endNode) {{
                    // Prevent self-connections
                    if (startNode === endNode) return false;
                    
                    // Check for existing connections
                    const existingConnection = canvasState.connections.find(conn => 
                        conn.from === startNode.nodeId && conn.to === endNode.nodeId
                    );
                    
                    return !existingConnection;
                }}

                // Enhanced connection creation with smooth bezier curves
                function createConnection(startNode, endNode) {{
                    const startPos = startNode.getCenterPoint();
                    const endPos = endNode.getCenterPoint();
                    
                    // Calculate control points for smooth bezier curve
                    const dx = endPos.x - startPos.x;
                    const dy = endPos.y - startPos.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    const controlOffset = Math.min(distance * 0.5, 150);
                    
                    const pathString = `M ${{startPos.x}} ${{startPos.y}} C ${{startPos.x + controlOffset}} ${{startPos.y}} ${{endPos.x - controlOffset}} ${{endPos.y}} ${{endPos.x}} ${{endPos.y}}`;
                    
                    const connectionId = 'conn_' + Date.now();
                    
                    // Create animated path
                    const path = new fabric.Path(pathString, {{
                        fill: '',
                        stroke: '#333',
                        strokeWidth: 4,
                        selectable: true,
                        evented: true,
                        shadow: new fabric.Shadow({{
                            color: 'rgba(0,0,0,0.3)',
                            blur: 8,
                            offsetX: 2,
                            offsetY: 2
                        }}),
                        connectionId: connectionId,
                        fromNode: startNode.nodeId,
                        toNode: endNode.nodeId,
                        strokeDashArray: [0, 0]
                    }});
                    
                    // Add connection events
                    path.on('mouseenter', function() {{
                        path.set({{ stroke: '#ff4444', strokeWidth: 6 }});
                        canvas.renderAll();
                    }});
                    
                    path.on('mouseleave', function() {{
                        path.set({{ stroke: '#333', strokeWidth: 4 }});
                        canvas.renderAll();
                    }});
                    
                    path.on('mousedown', function(e) {{
                        if (e.e.ctrlKey || e.e.metaKey) {{
                            deleteConnection(path);
                        }}
                    }});
                    
                    // Create arrow head
                    const angle = Math.atan2(dy, dx);
                    const arrowHead = new fabric.Triangle({{
                        left: endPos.x - 20 * Math.cos(angle),
                        top: endPos.y - 20 * Math.sin(angle),
                        width: 20,
                        height: 15,
                        fill: '#333',
                        selectable: false,
                        evented: false,
                        angle: (angle * 180 / Math.PI) + 90,
                        shadow: new fabric.Shadow({{
                            color: 'rgba(0,0,0,0.3)',
                            blur: 5,
                            offsetX: 1,
                            offsetY: 1
                        }}),
                        connectionId: connectionId
                    }});
                    
                    canvas.add(path);
                    canvas.add(arrowHead);
                    canvas.sendToBack(path);
                    
                    // Animate connection creation
                    animateConnectionCreation(path);
                    
                    // Add to state
                    canvasState.connections.push({{
                        id: connectionId,
                        from: startNode.nodeId,
                        to: endNode.nodeId,
                        fromPort: 'output',
                        toPort: 'input'
                    }});
                    
                    updateStreamlitState();
                }}

                // Animate connection creation
                function animateConnectionCreation(path) {{
                    let dashOffset = 0;
                    const animate = () => {{
                        dashOffset += 2;
                        path.set({{ strokeDashArray: [10, 5], strokeDashOffset: -dashOffset }});
                        canvas.renderAll();
                        
                        if (dashOffset < 100) {{
                            requestAnimationFrame(animate);
                        }} else {{
                            path.set({{ strokeDashArray: [0, 0], strokeDashOffset: 0 }});
                            canvas.renderAll();
                        }}
                    }};
                    animate();
                }}

                // Delete connection
                function deleteConnection(path) {{
                    const connectionId = path.connectionId;
                    
                    // Remove from canvas
                    canvas.getObjects().forEach(obj => {{
                        if (obj.connectionId === connectionId) {{
                            canvas.remove(obj);
                        }}
                    }});
                    
                    // Remove from state
                    canvasState.connections = canvasState.connections.filter(
                        conn => conn.id !== connectionId
                    );
                    
                    updateStreamlitState();
                    updateStatusBar('Connection deleted');
                }}

                // Update connections when nodes move
                function updateConnections() {{
                    canvasState.connections.forEach(conn => {{
                        const startNode = canvas.getObjects().find(obj => obj.nodeId === conn.from);
                        const endNode = canvas.getObjects().find(obj => obj.nodeId === conn.to);
                        
                        if (startNode && endNode) {{
                            const path = canvas.getObjects().find(obj => 
                                obj.connectionId === conn.id && obj.type === 'path'
                            );
                            const arrow = canvas.getObjects().find(obj => 
                                obj.connectionId === conn.id && obj.type === 'triangle'
                            );
                            
                            if (path && arrow) {{
                                const startPos = startNode.getCenterPoint();
                                const endPos = endNode.getCenterPoint();
                                
                                const dx = endPos.x - startPos.x;
                                const dy = endPos.y - startPos.y;
                                const distance = Math.sqrt(dx * dx + dy * dy);
                                const controlOffset = Math.min(distance * 0.5, 150);
                                
                                const pathString = `M ${{startPos.x}} ${{startPos.y}} C ${{startPos.x + controlOffset}} ${{startPos.y}} ${{endPos.x - controlOffset}} ${{endPos.y}} ${{endPos.x}} ${{endPos.y}}`;
                                
                                path.set({{ path: fabric.util.parsePath(pathString) }});
                                
                                const angle = Math.atan2(dy, dx);
                                arrow.set({{
                                    left: endPos.x - 20 * Math.cos(angle),
                                    top: endPos.y - 20 * Math.sin(angle),
                                    angle: (angle * 180 / Math.PI) + 90
                                }});
                            }}
                        }}
                    }});
                    canvas.renderAll();
                }}

                // Enhanced node selection
                function selectNode(group) {{
                    // Deselect previous node
                    if (selectedNode && selectedNode !== group) {{
                        selectedNode.set({{ 
                            strokeWidth: 2,
                            shadow: new fabric.Shadow({{
                                color: 'rgba(0,0,0,0.3)',
                                blur: 15,
                                offsetX: 3,
                                offsetY: 3
                            }})
                        }});
                    }}
                    
                    // Select new node
                    selectedNode = group;
                    group.set({{ 
                        strokeWidth: 4,
                        shadow: new fabric.Shadow({{
                            color: 'rgba(0,123,255,0.5)',
                            blur: 20,
                            offsetX: 0,
                            offsetY: 0
                        }})
                    }});
                    canvas.renderAll();
                    
                    // Update properties panel
                    updatePropertiesPanel(group);
                    updateStatusBar(`Selected ${{group.nodeType}} node`);
                }}

                // Enhanced properties panel
                function updatePropertiesPanel(group) {{
                    const nodeData = canvasState.nodes.find(n => n.id === group.nodeId);
                    if (!nodeData) return;
                    
                    const template = componentTemplates[group.nodeType];
                    const propertiesHtml = `
                        <div style="border-bottom: 2px solid #007bff; padding-bottom: 15px; margin-bottom: 20px;">
                            <h3 style="margin: 0; color: #007bff;">${{template.icon}} ${{group.nodeType}}</h3>
                            <small style="color: #666;">${{template.description}}</small>
                        </div>
                        
                        <div class="property-group">
                            <label style="font-weight: 600; color: #333;"><strong>Node Name:</strong></label>
                            <input type="text" class="property-input" value="${{nodeData.name}}" 
                                   onchange="updateNodeProperty('name', this.value)" 
                                   placeholder="Enter node name">
                        </div>
                        
                        <div class="property-group">
                            <label style="font-weight: 600; color: #333;"><strong>Position:</strong></label>
                            <div style="display: flex; gap: 10px; margin-top: 5px;">
                                <input type="number" class="property-input" value="${{Math.round(group.left)}}" 
                                       onchange="updateNodePosition('x', this.value)" placeholder="X" style="flex: 1;">
                                <input type="number" class="property-input" value="${{Math.round(group.top)}}" 
                                       onchange="updateNodePosition('y', this.value)" placeholder="Y" style="flex: 1;">
                            </div>
                        </div>
                        
                        ${{generatePropertyInputs(template.properties, nodeData.properties)}}
                        
                        <div style="margin-top: 30px; display: flex; gap: 10px;">
                            <button onclick="duplicateNode()" style="flex: 1; padding: 10px; background: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">
                                📋 Duplicate
                            </button>
                            <button onclick="deleteNode()" style="flex: 1; padding: 10px; background: #dc3545; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">
                                🗑️ Delete
                            </button>
                        </div>
                    `;
                    
                    document.getElementById('properties-content').innerHTML = propertiesHtml;
                }}

                // Generate enhanced property inputs
                function generatePropertyInputs(templateProps, currentProps) {{
                    let html = '';
                    
                    for (const [key, defaultValue] of Object.entries(templateProps)) {{
                        const currentValue = currentProps[key] !== undefined ? currentProps[key] : defaultValue;
                        const inputId = `prop_${{key}}`;
                        
                        html += `<div class="property-group">`;
                        html += `<label for="${{inputId}}" style="font-weight: 600; color: #333;"><strong>${{formatPropertyName(key)}}:</strong></label>`;
                        
                        if (Array.isArray(defaultValue)) {{
                            // Dropdown for array values
                            html += `<select id="${{inputId}}" class="property-input" onchange="updateNodeProperty('${{key}}', this.value)">`;
                            defaultValue.forEach(option => {{
                                const selected = option === currentValue ? 'selected' : '';
                                html += `<option value="${{option}}" ${{selected}}>${{option}}</option>`;
                            }});
                            html += `</select>`;
                        }} else if (typeof defaultValue === 'boolean') {{
                            // Checkbox for boolean values
                            const checked = currentValue ? 'checked' : '';
                            html += `<label style="display: flex; align-items: center; margin-top: 5px; cursor: pointer;">`;
                            html += `<input type="checkbox" id="${{inputId}}" ${{checked}} onchange="updateNodeProperty('${{key}}', this.checked)" style="margin-right: 8px;">`;
                            html += `<span>${{formatPropertyName(key)}}</span>`;
                            html += `</label>`;
                        }} else if (typeof defaultValue === 'number') {{
                            // Number input
                            html += `<input type="number" id="${{inputId}}" class="property-input" value="${{currentValue}}" 
                                     onchange="updateNodeProperty('${{key}}', parseFloat(this.value))" 
                                     step="0.1" placeholder="Enter number">`;
                        }} else if (key.includes('template') || key.includes('prompt') || key.includes('message')) {{
                            // Textarea for long text
                            html += `<textarea id="${{inputId}}" class="property-input" rows="4" 
                                     onchange="updateNodeProperty('${{key}}', this.value)" 
                                     placeholder="Enter ${{formatPropertyName(key).toLowerCase()}}">${{currentValue}}</textarea>`;
                        }} else {{
                            // Regular text input
                            html += `<input type="text" id="${{inputId}}" class="property-input" value="${{currentValue}}" 
                                     onchange="updateNodeProperty('${{key}}', this.value)" 
                                     placeholder="Enter ${{formatPropertyName(key).toLowerCase()}}">`;
                        }}
                        
                        html += `</div>`;
                    }}
                    
                    return html;
                }}

                // Format property names for display
                function formatPropertyName(name) {{
                    return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                }}

                // Update node properties
                function updateNodeProperty(key, value) {{
                    if (!selectedNode) return;
                    
                    const nodeData = canvasState.nodes.find(n => n.id === selectedNode.nodeId);
                    if (nodeData) {{
                        if (key === 'name') {{
                            nodeData.name = value;
                        }} else {{
                            nodeData.properties[key] = value;
                        }}
                        updateStreamlitState();
                        updateStatusBar(`Updated ${{formatPropertyName(key)}}`);
                    }}
                }}

                // Update node position
                function updateNodePosition(axis, value) {{
                    if (!selectedNode) return;
                    
                    const nodeData = canvasState.nodes.find(n => n.id === selectedNode.nodeId);
                    if (nodeData) {{
                        const numValue = parseFloat(value);
                        if (axis === 'x') {{
                            selectedNode.set({{ left: numValue }});
                            nodeData.x = numValue;
                        }} else if (axis === 'y') {{
                            selectedNode.set({{ top: numValue }});
                            nodeData.y = numValue;
                        }}
                        canvas.renderAll();
                        updateConnections();
                        updateStreamlitState();
                    }}
                }}

                // Duplicate selected node
                function duplicateNode() {{
                    if (!selectedNode) return;
                    
                    const newNode = createNode(
                        selectedNode.nodeType, 
                        selectedNode.left + 50, 
                        selectedNode.top + 50
                    );
                    
                    // Copy properties
                    const originalData = canvasState.nodes.find(n => n.id === selectedNode.nodeId);
                    const newData = canvasState.nodes.find(n => n.id === newNode.nodeId);
                    if (originalData && newData) {{
                        newData.properties = {{ ...originalData.properties }};
                        newData.name = originalData.name + '_copy';
                    }}
                    
                    selectNode(newNode);
                    updateStreamlitState();
                }}

                // Delete selected node
                function deleteNode() {{
                    if (!selectedNode) return;
                    
                    const nodeId = selectedNode.nodeId;
                    
                    // Remove connections
                    const connectionsToRemove = canvasState.connections.filter(
                        conn => conn.from === nodeId || conn.to === nodeId
                    );
                    
                    connectionsToRemove.forEach(conn => {{
                        canvas.getObjects().forEach(obj => {{
                            if (obj.connectionId === conn.id) {{
                                canvas.remove(obj);
                            }}
                        }});
                    }});
                    
                    // Remove node
                    canvas.remove(selectedNode);
                    
                    // Update state
                    canvasState.nodes = canvasState.nodes.filter(n => n.id !== nodeId);
                    canvasState.connections = canvasState.connections.filter(
                        conn => conn.from !== nodeId && conn.to !== nodeId
                    );
                    
                    selectedNode = null;
                    document.getElementById('properties-content').innerHTML = `
                        <p style="color: #666; text-align: center; margin-top: 50px;">
                            Select a node to edit its properties
                        </p>
                    `;
                    
                    updateStreamlitState();
                    updateStatusBar('Node deleted');
                }}

                // Toggle connection mode
                function toggleConnectionMode() {{
                    connectionMode = !connectionMode;
                    
                    if (connectionMode) {{
                        canvas.defaultCursor = 'crosshair';
                        updateStatusBar('Connection mode: Select source node');
                    }} else {{
                        resetConnectionMode();
                    }}
                }}

                // Reset connection mode
                function resetConnectionMode() {{
                    connectionMode = false;
                    canvas.defaultCursor = 'default';
                    
                    if (connectionStart) {{
                        connectionStart.set({{ 
                            strokeWidth: 2, 
                            stroke: '#333',
                            shadow: new fabric.Shadow({{
                                color: 'rgba(0,0,0,0.3)',
                                blur: 15,
                                offsetX: 3,
                                offsetY: 3
                            }})
                        }});
                        connectionStart = null;
                        canvas.renderAll();
                    }}
                    
                    updateStatusBar('Ready');
                }}

                // Clear canvas
                function clearCanvas() {{
                    if (confirm('Are you sure you want to clear the canvas? This action cannot be undone.')) {{
                        canvas.clear();
                        if (gridEnabled) {{
                            drawGrid();
                        }}
                        canvasState = {{ nodes: [], connections: [] }};
                        selectedNode = null;
                        nodeCounter = 1;
                        
                        document.getElementById('properties-content').innerHTML = `
                            <p style="color: #666; text-align: center; margin-top: 50px;">
                                Select a node to edit its properties
                            </p>
                        `;
                        
                        updateStreamlitState();
                        updateStatusBar('Canvas cleared');
                    }}
                }}

                // Load canvas state
                function loadCanvasState() {{
                    // Load existing nodes
                    canvasState.nodes.forEach(nodeData => {{
                        const group = createNodeFromData(nodeData);
                        if (group) {{
                            canvas.add(group);
                        }}
                    }});
                    
                    // Load existing connections
                    setTimeout(() => {{
                        canvasState.connections.forEach(connData => {{
                            const startNode = canvas.getObjects().find(obj => obj.nodeId === connData.from);
                            const endNode = canvas.getObjects().find(obj => obj.nodeId === connData.to);
                            
                            if (startNode && endNode) {{
                                createConnectionFromData(startNode, endNode, connData);
                            }}
                        }});
                    }}, 100);
                }}

                // Create node from data
                function createNodeFromData(nodeData) {{
                    const template = componentTemplates[nodeData.type];
                    if (!template) return null;
                    
                    // Similar to createNode but with existing data
                    // ... (implementation would be similar to createNode but using nodeData)
                    
                    return null; // Placeholder
                }}

                // Setup global event listeners
                function setupEventListeners() {{
                    // Keyboard shortcuts
                    document.addEventListener('keydown', function(e) {{
                        if (e.key === 'Delete' && selectedNode) {{
                            deleteNode();
                        }} else if (e.key === 'Escape') {{
                            resetConnectionMode();
                        }} else if (e.ctrlKey || e.metaKey) {{
                            if (e.key === 'd') {{
                                e.preventDefault();
                                duplicateNode();
                            }} else if (e.key === 'a') {{
                                e.preventDefault();
                                canvas.discardActiveObject();
                                const sel = new fabric.ActiveSelection(canvas.getObjects().filter(obj => obj.nodeId), {{
                                    canvas: canvas,
                                }});
                                canvas.setActiveObject(sel);
                                canvas.requestRenderAll();
                            }}
                        }}
                    }});
                    
                    // Canvas events
                    canvas.on('mouse:down', function(e) {{
                        if (!e.target && selectedNode) {{
                            selectedNode.set({{ strokeWidth: 2 }});
                            selectedNode = null;
                            document.getElementById('properties-content').innerHTML = `
                                <p style="color: #666; text-align: center; margin-top: 50px;">
                                    Select a node to edit its properties
                                </p>
                            `;
                            canvas.renderAll();
                        }}
                    }});
                    
                    // Mouse wheel zoom
                    canvas.on('mouse:wheel', function(opt) {{
                        const delta = opt.e.deltaY;
                        let zoom = canvas.getZoom();
                        zoom *= 0.999 ** delta;
                        if (zoom > 20) zoom = 20;
                        if (zoom < 0.01) zoom = 0.01;
                        canvas.zoomToPoint({{ x: opt.e.offsetX, y: opt.e.offsetY }}, zoom);
                        opt.e.preventDefault();
                        opt.e.stopPropagation();
                    }});
                }}

                // Update status bar
                function updateStatusBar(message) {{
                    const statusBar = document.getElementById('status-bar');
                    if (statusBar) {{
                        statusBar.textContent = message;
                        setTimeout(() => {{
                            statusBar.textContent = 'Ready';
                        }}, 3000);
                    }}
                }}

                // Update Streamlit state
                function updateStreamlitState() {{
                    // Send updated state to Streamlit
                    window.parent.postMessage({{
                        type: 'canvas_updated',
                        data: canvasState
                    }}, '*');
                }}

                // Add component function (called by toolbar buttons)
                function addComponent(type) {{
                    const node = createNode(type);
                    if (node) {{
                        selectNode(node);
                    }}
                }}

                // Initialize everything when page loads
                document.addEventListener('DOMContentLoaded', function() {{
                    initializeCanvas();
                }});

                // Initialize immediately if DOM is already loaded
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', initializeCanvas);
                }} else {{
                    initializeCanvas();
                }}
            </script>
        </body>
        </html>
        """
    
    def _render_configuration(self):
        """Render configuration panel"""
        st.markdown("### ⚙️ Agent Configuration")
        
        if st.session_state.canvas_data['nodes']:
            # Display current flow structure
            st.markdown("#### Current Flow Structure")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Nodes:**")
                for node in st.session_state.canvas_data['nodes']:
                    st.markdown(f"- {node['name']} ({node['type']})")
            
            with col2:
                st.markdown("**Connections:**")
                for conn in st.session_state.canvas_data['connections']:
                    from_node = next((n for n in st.session_state.canvas_data['nodes'] if n['id'] == conn['from']), None)
                    to_node = next((n for n in st.session_state.canvas_data['nodes'] if n['id'] == conn['to']), None)
                    if from_node and to_node:
                        st.markdown(f"- {from_node['name']} → {to_node['name']}")
            
            # Export configuration
            st.markdown("#### Export Configuration")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📋 Copy JSON", use_container_width=True):
                    config_json = json.dumps(st.session_state.canvas_data, indent=2)
                    st.code(config_json, language='json')
            
            with col2:
                if st.button("💾 Download", use_container_width=True):
                    config_json = json.dumps(st.session_state.canvas_data, indent=2)
                    st.download_button(
                        label="Download Configuration",
                        data=config_json,
                        file_name=f"agent_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            with col3:
                uploaded_file = st.file_uploader("📂 Import Config", type=['json'])
                if uploaded_file:
                    try:
                        config_data = json.load(uploaded_file)
                        st.session_state.canvas_data = config_data
                        st.success("Configuration imported successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error importing configuration: {e}")
        else:
            st.info("Create some nodes in the Visual Builder to see configuration options.")
    
    def _render_execution(self):
        """Render execution panel"""
        st.markdown("### 🚀 Agent Execution")
        
        if not st.session_state.openai_client:
            st.warning("Please configure your OpenAI API key in the sidebar to enable execution.")
            return
        
        if not st.session_state.canvas_data['nodes']:
            st.info("Create an agent flow in the Visual Builder to enable execution.")
            return
        
        # Execution controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            test_input = st.text_area(
                "Test Input",
                value="What is the capital of France?",
                height=100,
                help="Enter input to test your agent flow"
            )
        
        with col2:
            execution_mode = st.selectbox(
                "Execution Mode",
                ["Sequential", "Parallel", "Conditional"],
                help="Choose how to execute the agent flow"
            )
            
            stream_output = st.checkbox("Stream Output", value=True)
        
        with col3:
            if st.button("▶️ Execute Agent", type="primary", use_container_width=True):
                if test_input.strip():
                    self._execute_agent_flow(test_input, execution_mode, stream_output)
                else:
                    st.error("Please enter test input")
            
            if st.button("⏹️ Stop Execution", use_container_width=True):
                st.session_state.agent_running = False
        
        # Execution log
        if st.session_state.execution_log:
            st.markdown("#### Execution Log")
            
            log_container = st.container()
            with log_container:
                for i, log_entry in enumerate(reversed(st.session_state.execution_log[-10:])):
                    timestamp = log_entry.get('timestamp', 'Unknown')
                    level = log_entry.get('level', 'INFO')
                    message = log_entry.get('message', '')
                    
                    if level == 'ERROR':
                        st.error(f"[{timestamp}] {message}")
                    elif level == 'WARNING':
                        st.warning(f"[{timestamp}] {message}")
                    else:
                        st.info(f"[{timestamp}] {message}")
    
    def _render_analytics(self):
        """Render analytics panel"""
        st.markdown("### 📊 Analytics & Performance")
        
        stats = st.session_state.execution_stats
        
        # Performance metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Runs", stats.total_runs)
        
        with col2:
            success_rate = (stats.successful_runs / max(stats.total_runs, 1)) * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")
        
        with col3:
            st.metric("Failed Runs", stats.failed_runs)
        
        with col4:
            st.metric("Avg Response Time", f"{stats.avg_response_time:.2f}s")
        
        # Execution history chart
        if hasattr(stats, 'execution_history') and stats.execution_history:
            st.markdown("#### Execution History")
            
            df = pd.DataFrame(stats.execution_history)
            st.line_chart(df.set_index('timestamp')['response_time'])
        
        # Node usage statistics
        if st.session_state.canvas_data['nodes']:
            st.markdown("#### Node Usage Statistics")
            
            node_types = {}
            for node in st.session_state.canvas_data['nodes']:
                node_type = node['type']
                node_types[node_type] = node_types.get(node_type, 0) + 1
            
            df_nodes = pd.DataFrame(list(node_types.items()), columns=['Node Type', 'Count'])
            st.bar_chart(df_nodes.set_index('Node Type'))
    
    def _render_management(self):
        """Render management panel"""
        st.markdown("### 💾 Agent Management")
        
        # Save current agent
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Save Current Agent")
            agent_name = st.text_input("Agent Name", value="my_agent")
            agent_description = st.text_area("Description", height=100)
            
            if st.button("💾 Save Agent", use_container_width=True):
                if agent_name and st.session_state.canvas_data['nodes']:
                    agent_data = {
                        'name': agent_name,
                        'description': agent_description,
                        'canvas_data': st.session_state.canvas_data,
                        'created_at': datetime.now().isoformat(),
                        'version': '1.0'
                    }
                    st.session_state.saved_agents[agent_name] = agent_data
                    st.success(f"Agent '{agent_name}' saved successfully!")
                else:
                    st.error("Please enter a name and create some nodes first.")
        
        with col2:
            st.markdown("#### Load Saved Agent")
            if st.session_state.saved_agents:
                selected_agent = st.selectbox(
                    "Select Agent",
                    list(st.session_state.saved_agents.keys())
                )
                
                if selected_agent:
                    agent_data = st.session_state.saved_agents[selected_agent]
                    st.markdown(f"**Description:** {agent_data.get('description', 'No description')}")
                    st.markdown(f"**Created:** {agent_data.get('created_at', 'Unknown')}")
                    st.markdown(f"**Nodes:** {len(agent_data.get('canvas_data', {}).get('nodes', []))}")
                    
                    col_load, col_delete = st.columns(2)
                    
                    with col_load:
                        if st.button("📂 Load", use_container_width=True):
                            st.session_state.canvas_data = agent_data['canvas_data']
                            st.success(f"Agent '{selected_agent}' loaded!")
                            st.rerun()
                    
                    with col_delete:
                        if st.button("🗑️ Delete", use_container_width=True):
                            del st.session_state.saved_agents[selected_agent]
                            st.success(f"Agent '{selected_agent}' deleted!")
                            st.rerun()
            else:
                st.info("No saved agents found.")
        
        # Import/Export agents
        st.markdown("#### Import/Export Agents")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.saved_agents:
                agents_json = json.dumps(st.session_state.saved_agents, indent=2)
                st.download_button(
                    label="📥 Export All Agents",
                    data=agents_json,
                    file_name=f"agents_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        
        with col2:
            uploaded_agents = st.file_uploader("📤 Import Agents", type=['json'])
            if uploaded_agents:
                try:
                    imported_agents = json.load(uploaded_agents)
                    st.session_state.saved_agents.update(imported_agents)
                    st.success(f"Imported {len(imported_agents)} agents!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error importing agents: {e}")
    
    def _execute_agent_flow(self, test_input: str, mode: str, stream: bool):
        """Execute the agent flow"""
        try:
            st.session_state.agent_running = True
            
            # Add execution log entry
            log_entry = {
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'level': 'INFO',
                'message': f'Starting execution with input: {test_input[:50]}...'
            }
            st.session_state.execution_log.append(log_entry)
            
            # Execute using the AgentExecutor
            result = self.executor.execute_flow(
                st.session_state.canvas_data,
                test_input,
                st.session_state.openai_client,
                mode,
                stream
            )
            
            # Update statistics
            stats = st.session_state.execution_stats
            stats.total_runs += 1
            
            if result.get('success', False):
                stats.successful_runs += 1
                log_entry = {
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'level': 'INFO',
                    'message': f'Execution completed successfully'
                }
            else:
                stats.failed_runs += 1
                log_entry = {
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'level': 'ERROR',
                    'message': f'Execution failed: {result.get("error", "Unknown error")}'
                }
            
            st.session_state.execution_log.append(log_entry)
            
            # Update average response time
            response_time = result.get('response_time', 0)
            stats.avg_response_time = (
                (stats.avg_response_time * (stats.total_runs - 1) + response_time) / stats.total_runs
            )
            
            # Display result
            if result.get('success', False):
                st.success("Execution completed successfully!")
                st.markdown("**Result:**")
                st.markdown(result.get('output', 'No output'))
            else:
                st.error(f"Execution failed: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            logger.error(f"Execution error: {e}")
            st.error(f"Execution error: {e}")
        
        finally:
            st.session_state.agent_running = False
    
    def _handle_auto_save(self):
        """Handle auto-save functionality"""
        if st.session_state.auto_save_enabled:
            current_time = time.time()
            if (st.session_state.last_save_time is None or 
                current_time - st.session_state.last_save_time > 30):  # Auto-save every 30 seconds
                
                if st.session_state.canvas_data['nodes']:
                    # Auto-save logic here
                    st.session_state.last_save_time = current_time

# Run the application
if __name__ == "__main__":
    app = AgentBuilderApp()
    app.run()
