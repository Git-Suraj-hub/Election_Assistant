import streamlit as st
import textwrap
from data.mock_api import get_supported_countries
from components.timeline import render_timeline
from components.simulator import render_simulator
from utils.chat import generate_llm_response

# App configuration
st.set_page_config(
    page_title="Election Intelligence Dashboard",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Global SaaS CSS ---
st.markdown(textwrap.dedent("""
<style>
    /* Dark Theme Backgrounds */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161824;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Glassmorphism Cards for Metrics */
    div[data-testid="metric-container"] {
        background-color: #1E1E2F;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        border-color: rgba(139, 92, 246, 0.4); /* Neon Purple Accent */
    }
    
    /* Top Header Styling */
    .dashboard-header {
        padding: 1.5rem 0 0.5rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .dashboard-title {
        font-weight: 800;
        font-size: 2.2rem;
        background: linear-gradient(90deg, #FFFFFF, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    .dashboard-subtitle {
        color: #888888;
        font-size: 1rem;
        margin-top: 5px;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E1E2F;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #A0AEC0;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #8B5CF6 !important;
        color: white !important;
        font-weight: 600;
    }
    
    /* Chat Message Styling */
    .stChatMessage {
        background-color: #1E1E2F;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.02);
        margin-bottom: 10px;
    }
    
    /* Button Styling */
    .stButton>button {
        border-radius: 8px;
        transition: all 0.2s;
    }
    .stButton>button[kind="primary"] {
        background-color: #8B5CF6;
        color: white;
        border: none;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #7C3AED;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
    }
</style>
"""), unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_country" not in st.session_state:
    st.session_state.current_country = "USA"
if "knowledge_level" not in st.session_state:
    st.session_state.knowledge_level = "Standard"

def reset_chat(api_key, app_mode):
    """Resets the chat history when settings change."""
    st.session_state.messages = []
    if api_key:
        welcome_msg = generate_llm_response(
            api_key,
            [{"role": "user", "content": "Hello! I just opened the app. Please introduce yourself briefly based on the current settings."}], 
            st.session_state.current_country, 
            st.session_state.knowledge_level,
            app_mode
        )
    else:
        welcome_msg = "Hello! 👋 I'm your Election Intelligence Assistant. Please enter your Gemini API Key in the sidebar to start chatting."
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# --- Sidebar Configuration ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1533/1533116.png", width=60) # Placeholder logo
    st.markdown("<h2 style='margin-top:0; padding-top:0;'>Assistant Config</h2>", unsafe_allow_html=True)
    
    api_key = st.text_input("Google Gemini API Key", type="password", help="Get your API key from Google AI Studio")
    if not api_key:
        st.warning("Please enter your API key to enable AI features.")
        
    st.divider()
    
    selected_country = st.selectbox(
        "🌍 Target Country", 
        get_supported_countries(),
        index=get_supported_countries().index(st.session_state.current_country)
    )
    
    knowledge_level = st.radio(
        "🧠 Knowledge Level",
        ["Beginner (Like I'm 10)", "Standard", "Advanced"],
        index=["Beginner (Like I'm 10)", "Standard", "Advanced"].index(st.session_state.knowledge_level),
        key="knowledge_level_radio"
    )

    # If settings change, reset chat and simulator state
    settings_changed = False
    if selected_country != st.session_state.current_country:
        st.session_state.current_country = selected_country
        settings_changed = True
    if knowledge_level != st.session_state.knowledge_level:
        st.session_state.knowledge_level = knowledge_level
        settings_changed = True
        
    if settings_changed:
        if "sim_step" in st.session_state:
             st.session_state.sim_step = 0
             st.session_state.sim_completed = False
             st.session_state.sim_selections = {}
        # We pass 'Chat Assistant' as the default mode for reset_chat context
        reset_chat(api_key, "Chat Assistant")

# --- Main Content Area ---

# Header
st.markdown(textwrap.dedent("""
<div class="dashboard-header">
    <h1 class="dashboard-title">Election Intelligence Platform</h1>
    <p class="dashboard-subtitle">Your interactive, AI-powered guide to democratic processes.</p>
</div>
"""), unsafe_allow_html=True)

# Top Metrics Bar
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Country", st.session_state.current_country)
with col2:
    st.metric("Knowledge Mode", st.session_state.knowledge_level.split()[0])
with col3:
    ai_status = "🟢 Connected" if api_key else "🔴 API Key Missing"
    st.metric("AI System Status", ai_status)

st.write("") # Spacing

# Dashboard Tabs
tab_chat, tab_sim, tab_time = st.tabs(["💬 AI Assistant", "🗳️ Voting Simulator", "📅 Election Timeline"])

with tab_chat:
    st.markdown("### Interactive Learning Session")
    
    # Initialize chat if empty
    if not st.session_state.messages:
        reset_chat(api_key, "Chat Assistant")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about the election process..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = generate_llm_response(
                    api_key, 
                    st.session_state.messages, 
                    st.session_state.current_country, 
                    st.session_state.knowledge_level,
                    "Chat Assistant"
                )
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with tab_sim:
    render_simulator(st.session_state.current_country)

with tab_time:
    render_timeline(st.session_state.current_country)
