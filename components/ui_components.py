"""
UI components and styling for the Agent Builder
"""

import streamlit as st
from typing import Dict, Any
import json

class UIComponents:
    """Handles UI rendering and styling"""
    
    def get_custom_css(self) -> str:
        """Return enhanced custom CSS"""
        return """
        <style>
            /* Enhanced main styling */
            .main-header {
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 30px;
                font-size: 3rem;
                font-weight: 800;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }
            
            /* Enhanced sidebar styling */
            .sidebar-section {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 20px;
                margin-bottom: 25px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                backdrop-filter: blur(10px);
            }
            
            .sidebar-section h3 {
                margin-top: 0;
                font-weight: 700;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }
            
            /* Enhanced component cards */
            .component-card {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 15px;
                border-left: 5px solid #4CAF50;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }
            
            .component-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%);
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .component-card:hover {
                transform: translateY(-5px) scale(1.02);
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            }
            
            .component-card:hover::before {
                opacity: 1;
            }
            
            /* Enhanced JSON output */
            .json-output {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: #ffffff;
                padding: 25px;
                border-radius: 15px;
                border: 2px solid #4CAF50;
                font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                position: relative;
                overflow: hidden;
            }
            
            .json-output::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #4CAF50, #2196F3, #FF9800, #E91E63);
                animation: rainbow 3s linear infinite;
            }
            
            @keyframes rainbow {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
            
            /* Enhanced execution log */
            .execution-log {
                background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
                color: #00ff41;
                padding: 20px;
                border-radius: 15px;
                font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
                max-height: 500px;
                overflow-y: auto;
                border: 2px solid #00ff41;
                box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
                position: relative;
            }
            
            .execution-log::before {
                content: '> Terminal';
                position: absolute;
                top: -15px;
                left: 20px;
                background: #0f0f23;
                padding: 0 10px;
                color: #00ff41;
                font-size: 12px;
                font-weight: bold;
            }
            
            /* Enhanced status indicators */
            .status-indicator {
                display: inline-block;
                width: 14px;
                height: 14px;
                border-radius: 50%;
                margin-right: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.3);
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
                70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
                100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
            }
            
            .status-connected { 
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            }
            .status-disconnected { 
                background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
            }
            .status-warning { 
                background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
            }
            
            /* Enhanced agent stats */
            .agent-stats {
                background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
                color: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                margin: 15px 0;
                box-shadow: 0 8px 25px rgba(0, 114, 255, 0.3);
                position: relative;
                overflow: hidden;
            }
            
            .agent-stats::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
                transform: rotate(45deg);
                animation: shine 3s infinite;
            }
            
            @keyframes shine {
                0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
                100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
            }
            
            /* Enhanced tool results */
            .tool-result {
                background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
                border: 2px solid #4CAF50;
                color: #2e7d32;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
                position: relative;
            }
            
            .tool-result::before {
                content: '✓';
                position: absolute;
                top: -10px;
                right: 15px;
                background: #4CAF50;
                color: white;
                width: 20px;
                height: 20px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                font-weight: bold;
            }
            
            /* Enhanced error messages */
            .error-message {
                background: linear-gradient(135deg, #ffebee 0%, #fce4ec 100%);
                border: 2px solid #f44336;
                color: #c62828;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                box-shadow: 0 4px 15px rgba(244, 67, 54, 0.2);
                position: relative;
            }
            
            .error-message::before {
                content: '⚠';
                position: absolute;
                top: -10px;
                right: 15px;
                background: #f44336;
                color: white;
                width: 20px;
                height: 20px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                font-weight: bold;
            }
            
            /* Enhanced buttons */
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-weight: 600;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            }
            
            /* Enhanced metrics */
            .metric-container {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.3s ease;
            }
            
            .metric-container:hover {
                transform: translateY(-3px);
            }
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 10px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
            }
        </style>
        """
    
    def render_sidebar(self, config, session_state):
        """Render the enhanced sidebar"""
        # API Configuration Section
        st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.sidebar.markdown("### 🔐 OpenAI Configuration")
        
        api_key = st.sidebar.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to enable real agent execution"
        )
        
        if api_key:
            try:
                import openai
                openai.api_key = api_key
                client = openai.OpenAI(api_key=api_key)
                # Test the API key
                client.models.list()
                session_state.openai_client = client
                session_state.api_status = 'connected'
                st.sidebar.markdown(
                    '<span class="status-indicator status-connected"></span>API Connected',
                    unsafe_allow_html=True
                )
            except Exception as e:
                session_state.api_status = 'error'
                st.sidebar.markdown(
                    '<span class="status-indicator status-disconnected"></span>API Error',
                    unsafe_allow_html=True
                )
                st.sidebar.error(f"API Error: {str(e)[:50]}...")
        else:
            st.sidebar.markdown(
                '<span class="status-indicator status-disconnected"></span>API Not Connected',
                unsafe_allow_html=True
            )
        
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        
        # Component Library Section
        st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.sidebar.markdown("### 🧩 Component Library")
        
        components_config = config.get_component_templates()
        
        for comp_name, comp_info in components_config.items():
            with st.sidebar.container():
                st.sidebar.markdown(f"""
                <div class="component-card">
                    <strong>{comp_info['icon']} {comp_name}</strong><br>
                    <small>{comp_info['description']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        
        # Canvas Controls Section
        st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.sidebar.markdown("### ⚙️ Canvas Controls")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🗑️ Clear", use_container_width=True):
                session_state.canvas_data = {'nodes': [], 'connections': []}
                session_state.agent_flow = AgentFlow([], [], {})
                st.rerun()
        
        with col2:
            if st.button("💾 Save", use_container_width=True):
                # This will be handled in the management tab
                pass
        
        # Settings
        st.sidebar.markdown("#### Settings")
        session_state.auto_save_enabled = st.sidebar.checkbox("Auto Save", value=session_state.auto_save_enabled)
        session_state.theme = st.sidebar.selectbox("Theme", ["light", "dark"], index=0 if session_state.theme == "light" else 1)
        
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        
        # Execution Stats (if API connected)
        if session_state.openai_client:
            st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.sidebar.markdown("### 🚀 Quick Stats")
            
            stats = session_state.execution_stats
            st.sidebar.markdown(f"""
            <div class="agent-stats">
                <strong>Agent Statistics</strong><br>
                Runs: {stats.total_runs}<br>
                Success: {stats.successful_runs}<br>
                Failed: {stats.failed_runs}<br>
                Avg Time: {stats.avg_response_time:.2f}s
            </div>
            """, unsafe_allow_html=True)
            
            st.sidebar.markdown('</div>', unsafe_allow_html=True)
