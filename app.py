# app.py (Updated with local image support)

import streamlit as st
from prompts import (
    generate_code,
    explain_code,
    explain_code_simple,
    debug_code,
    explain_concept
)
from llm import ask_llm
import base64
from pathlib import Path

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="AI Coding Assistant | Next-Gen Developer Suite",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Function to load local image as base64
# --------------------------------------------------
def get_image_base64(image_path):
    """Convert local image to base64 string for CSS background"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# --------------------------------------------------
# CUSTOM BACKGROUND IMAGE SETUP
# --------------------------------------------------
# METHOD 1: Use local image file
# Place your image in the same folder as app.py
# Supported formats: .jpg, .jpeg, .png, .webp

IMAGE_PATH = r"D:\CODING\project\ai_coding_bot\background.jpg"  # Change this to your image filename

# Try to load local image
image_base64 = get_image_base64(IMAGE_PATH)

if image_base64:
    # Use local image as background
    background_style = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                    url("data:image/jpg;base64,{image_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    </style>
    """
else:
    # Fallback gradient background if image not found
    background_style = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e, #0f3460);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    """

st.markdown(background_style, unsafe_allow_html=True)

# --------------------------------------------------
# Custom CSS - Premium Glassmorphism Design
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #0072ff, #00c6ff);
}

/* Floating Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(10, 10, 20, 0.8);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0, 255, 255, 0.2);
    box-shadow: 10px 0 30px rgba(0,0,0,0.3);
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

/* Sidebar Radio Buttons */
section[data-testid="stSidebar"] .stRadio > div {
    gap: 12px;
}

section[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.05);
    padding: 12px 16px;
    border-radius: 12px;
    transition: all 0.3s ease;
    border: 1px solid rgba(0, 255, 255, 0.1);
    margin: 4px 0;
    cursor: pointer;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(0, 198, 255, 0.15);
    border-color: rgba(0, 198, 255, 0.5);
    transform: translateX(5px);
    box-shadow: 0 4px 15px rgba(0,114,255,0.2);
}

/* Hero Header */
.hero-header {
    text-align: center;
    padding: 2rem 0;
    margin-bottom: 2rem;
    position: relative;
}

.glowing-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 50%, #00c6ff 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: shine 3s linear infinite;
    text-shadow: 0 0 30px rgba(0,198,255,0.3);
    margin-bottom: 0.5rem;
}

@keyframes shine {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.subtitle {
    color: rgba(255,255,255,0.9);
    font-size: 1.1rem;
    text-align: center;
}

.glow-divider {
    width: 100px;
    height: 3px;
    background: linear-gradient(90deg, transparent, #00c6ff, #0072ff, transparent);
    margin: 20px auto;
    border-radius: 3px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 0.5; width: 100px; }
    50% { opacity: 1; width: 150px; }
}

/* Glass Cards */
.glass-card {
    background: rgba(20, 20, 40, 0.6);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(0, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, #00c6ff, #0072ff, #00c6ff);
    border-radius: 20px;
    opacity: 0;
    z-index: -1;
    transition: opacity 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 48px rgba(0,114,255,0.3);
}

.glass-card:hover::before {
    opacity: 0.3;
}

/* =========================
   INPUT FIELDS
========================= */

/* Text Areas */
.stTextArea textarea {
    background: rgba(10, 10, 20, 0.85) !important;
    border: 1px solid rgba(0, 255, 255, 0.2) !important;
    border-radius: 14px !important;
    color: white !important;
    padding: 14px !important;
    font-size: 15px !important;
}

/* Selectbox Main Container */
.stSelectbox > div > div {
    background: rgba(10, 10, 20, 0.85) !important;
    border: 1px solid rgba(0, 255, 255, 0.2) !important;
    border-radius: 14px !important;
    min-height: 50px !important;
}

/* Selected Text Inside Selectbox */
.stSelectbox div[data-baseweb="select"] > div {
    color: white !important;
    background: transparent !important;
}

/* Dropdown Text */
.stSelectbox div[data-baseweb="select"] span {
    color: white !important;
    font-weight: 500 !important;
}

/* Dropdown Menu */
div[data-baseweb="popover"] {
    background: rgba(15, 15, 30, 0.98) !important;
    backdrop-filter: blur(20px);
    border-radius: 12px !important;
    border: 1px solid rgba(0,255,255,0.2) !important;
}

/* Dropdown Options */
div[role="option"] {
    background: transparent !important;
    color: white !important;
    transition: all 0.2s ease;
}

/* Hover on Dropdown Options */
div[role="option"]:hover {
    background: rgba(0,198,255,0.15) !important;
    color: #00c6ff !important;
}

/* Input Focus Effects */
.stTextArea textarea:focus,
.stSelectbox > div > div:focus-within {
    border-color: #00c6ff !important;
    box-shadow: 0 0 20px rgba(0,198,255,0.35) !important;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #00c6ff !important;
    box-shadow: 0 0 15px rgba(0,198,255,0.3) !important;
    outline: none !important;
}

/* Labels */
.stSelectbox label, .stTextArea label, .stTextInput label {
    color: rgba(255,255,255,0.9) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    margin-bottom: 8px !important;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
    color: white;
    border: none;
    padding: 12px 28px;
    border-radius: 30px;
    font-weight: 600;
    font-size: 14px;
    transition: all 0.3s ease;
    width: 100%;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(0,114,255,0.5);
}

/* Chat Bubbles */
.user-bubble {
    background: linear-gradient(135deg, rgba(0,114,255,0.2), rgba(0,198,255,0.1));
    border: 1px solid rgba(0,114,255,0.3);
    border-radius: 20px 20px 5px 20px;
    padding: 15px 20px;
    margin: 10px 0;
    backdrop-filter: blur(10px);
    animation: slideInRight 0.3s ease;
}

.ai-bubble {
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(0,255,255,0.05));
    border: 1px solid rgba(0,255,255,0.2);
    border-radius: 20px 20px 20px 5px;
    padding: 15px 20px;
    margin: 10px 0;
    backdrop-filter: blur(10px);
    animation: slideInLeft 0.3s ease;
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(50px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-50px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Code Blocks */
pre {
    background: rgba(0,0,0,0.8) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    border: 1px solid rgba(0,255,255,0.2) !important;
    position: relative;
    overflow-x: auto;
}

code {
    font-family: 'Courier New', monospace !important;
    font-size: 13px !important;
    color: #00c6ff !important;
}

/* Feature Cards */
.feature-card {
    background: rgba(255,255,255,0.03);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
    border: 1px solid rgba(0,255,255,0.1);
}

.feature-card:hover {
    transform: translateY(-5px);
    background: rgba(0,198,255,0.1);
    border-color: rgba(0,198,255,0.3);
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Responsive Design */
@media (max-width: 768px) {
    .glowing-title {
        font-size: 2rem;
    }
    
    .glass-card {
        padding: 15px;
    }
    
    .user-bubble, .ai-bubble {
        padding: 10px 15px;
    }
}

.custom-subheader {
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Hero Header Section
# --------------------------------------------------
st.markdown("""
<div class="hero-header">
    <h1 class="glowing-title">🤖 AI Coding Assistant</h1>
    <p class="subtitle">Next-Generation AI-Powered Development Suite</p>
    <div class="glow-divider"></div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 3rem;">⚡</div>
        <h3 style="background: linear-gradient(135deg, #00c6ff, #0072ff); -webkit-background-clip: text; background-clip: text; color: transparent;">AI Tools</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    option = st.radio(
        "Select Tool",
        [
            "🚀 Generate Code",
            "📖 Explain Code",
            "🎯 Explain Simply",
            "🐛 Debug Code",
            "💡 Explain Concept"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Sidebar Info
    st.markdown("""
    <div style="background: rgba(0,198,255,0.1); border-radius: 15px; padding: 15px; margin-top: 20px;">
        <div style="text-align: center;">
            <div style="font-size: 1.2rem; font-weight: 600;">💡 Pro Tip</div>
            <div style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 10px;">
                You can regenerate responses or clear chat history anytime using the buttons below.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Remove emoji for logic
option_clean = option.replace("🚀 ", "").replace("📖 ", "").replace("🎯 ", "").replace("🐛 ", "").replace("💡 ", "")

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_language" not in st.session_state:
    st.session_state.current_language = "python"

if "current_option" not in st.session_state:
    st.session_state.current_option = None

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""

if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

prompt = ""

# --------------------------------------------------
# Main Content Area
# --------------------------------------------------
main_container = st.container()

with main_container:
    
    # --------------------------------------------------
    # Generate Code
    # --------------------------------------------------
    if option_clean == "Generate Code":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="custom-subheader">💻 Generate Production-Ready Code</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            language = st.selectbox(
                "📝 Programming Language",
                ["Python", "Java", "C", "C++", "JavaScript", "TypeScript", "Go", "Rust", "Ruby", "Swift"],
                help="Select your preferred programming language"
            )
        
        with col2:
            level = st.selectbox(
                "📊 Difficulty Level",
                ["Beginner", "Intermediate", "Advanced"],
                help="Choose the complexity level"
            )
        
        problem = st.text_area(
            "📌 Problem Statement",
            height=150,
            placeholder="Example: Write a function to find the factorial of a number...",
            help="Describe what you want the code to do"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if problem and problem.strip():
            prompt = generate_code(language, problem, level)
            st.session_state.current_option = "Generate Code"
            st.session_state.current_language = language.lower()
    
    # --------------------------------------------------
    # Explain Code
    # --------------------------------------------------
    elif option_clean == "Explain Code":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="custom-subheader">📖 Deep Code Explanation</p>', unsafe_allow_html=True)
        
        code = st.text_area(
            "📝 Code to Explain",
            height=250,
            placeholder="Paste your code here and I'll explain it in detail...",
            help="Paste any code snippet for detailed analysis"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if code and code.strip():
            prompt = explain_code(code)
            st.session_state.current_option = "Explain Code"
    
    # --------------------------------------------------
    # Explain Simply
    # --------------------------------------------------
    elif option_clean == "Explain Simply":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="custom-subheader">🎯 Simple Explanation (Beginner Friendly)</p>', unsafe_allow_html=True)
        
        code = st.text_area(
            "📝 Code to Simplify",
            height=250,
            placeholder="Paste code for a beginner-friendly explanation...",
            help="Get an easy-to-understand explanation of complex code"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if code and code.strip():
            prompt = explain_code_simple(code)
            st.session_state.current_option = "Explain Simply"
    
    # --------------------------------------------------
    # Debug Code
    # --------------------------------------------------
    elif option_clean == "Debug Code":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="custom-subheader">🐛 Intelligent Code Debugging</p>', unsafe_allow_html=True)
        
        code = st.text_area(
            "💻 Buggy Code",
            height=200,
            placeholder="Paste your code that needs debugging...",
            help="I'll find and fix bugs in your code"
        )
        
        error = st.text_area(
            "❌ Error Message (Optional)",
            height=100,
            placeholder="Paste any error messages you're getting...",
            help="Include error messages for better debugging"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if code and code.strip():
            prompt = debug_code(code, error if error else "No error message provided")
            st.session_state.current_option = "Debug Code"
    
    # --------------------------------------------------
    # Explain Concept
    # --------------------------------------------------
    elif option_clean == "Explain Concept":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="custom-subheader">💡 Learn Programming Concepts</p>', unsafe_allow_html=True)
        
        concept = st.text_area(
            "📚 Concept Name",
            height=150,
            placeholder="Example: Object-Oriented Programming, Recursion, Machine Learning...",
            help="Any programming concept you want to understand"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if concept and concept.strip():
            prompt = explain_concept(concept)
            st.session_state.current_option = "Explain Concept"
    
    # --------------------------------------------------
    # Action Buttons
    # --------------------------------------------------
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Generate Response", use_container_width=True):
            if not prompt:
                st.warning("⚠️ Please provide input before asking.")
            else:
                st.session_state.is_loading = True
                with st.spinner("🤖 AI is analyzing your request..."):
                    response = ask_llm(prompt)
                    st.session_state.last_prompt = prompt
                    st.session_state.messages.append({
                        "role": "user",
                        "content": prompt[:500] + "..." if len(prompt) > 500 else prompt
                    })
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                st.session_state.is_loading = False
                st.rerun()
    
    with col2:
        if st.button("🔄 Regenerate Response", use_container_width=True):
            if st.session_state.last_prompt:
                st.session_state.is_loading = True
                with st.spinner("🔄 Regenerating improved response..."):
                    response = ask_llm(st.session_state.last_prompt)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                st.session_state.is_loading = False
                st.rerun()
            else:
                st.warning("⚠️ No previous prompt to regenerate.")
    
    with col3:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.last_prompt = ""
            st.rerun()
    
    st.markdown("---")
    
    # --------------------------------------------------
    # Chat History Display
    # --------------------------------------------------
    if st.session_state.messages:
        st.markdown('<p class="custom-subheader" style="margin-bottom: 20px;">💬 Conversation History</p>', unsafe_allow_html=True)
        
        chat_container = st.container()
        
        with chat_container:
            for idx, msg in enumerate(st.session_state.messages):
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="user-bubble">
                        <strong>🧑 You</strong><br/>
                        {msg['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    if st.session_state.current_option == "Generate Code" and "```" in msg['content']:
                        code_content = msg['content']
                        st.markdown(f"""
                        <div class="ai-bubble">
                            <strong>🤖 AI Assistant</strong><br/>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(code_content, language=st.session_state.current_language)
                    else:
                        st.markdown(f"""
                        <div class="ai-bubble">
                            <strong>🤖 AI Assistant</strong><br/>
                            {msg['content']}
                        </div>
                        """, unsafe_allow_html=True)
                
                if idx < len(st.session_state.messages) - 1:
                    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
    
    else:
        # Welcome message when no chat history
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 3rem;">🚀</div>
            <h3 style="color: #00c6ff;">Welcome to AI Coding Assistant</h3>
            <p style="color: rgba(255,255,255,0.7);">Select a tool from the sidebar, provide the required input, and click "Generate Response" to get started!</p>
            <div style="display: flex; gap: 10px; justify-content: center; margin-top: 20px; flex-wrap: wrap;">
                <div class="feature-card">💻 Code Generation</div>
                <div class="feature-card">📖 Code Explanation</div>
                <div class="feature-card">🐛 Debugging</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.5); padding: 30px 0 20px 0; border-top: 1px solid rgba(0,255,255,0.1); margin-top: 30px;'>
    <small>
        🤖 AI Coding Assistant | Powered by Google Gemini AI | Real-time Intelligent Code Assistance
    </small>
    <br/>
    <small style='font-size: 0.7rem;'>
        Your 24/7 Programming Companion • Built with Streamlit
    </small>
</div>
""", unsafe_allow_html=True)