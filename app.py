import streamlit as st
from data.mock_api import get_supported_countries
from components.timeline import render_timeline
from components.simulator import render_simulator
from utils.chat import generate_llm_response

# App configuration
st.set_page_config(
    page_title="Election Intelligence Assistant",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_country" not in st.session_state:
    st.session_state.current_country = "USA"

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
    st.title("⚙️ Settings")
    
    api_key = st.text_input("Google Gemini API Key", type="password", help="Get your API key from Google AI Studio")
    if not api_key:
        st.warning("Please enter your API key to enable AI features.")
        
    selected_country = st.selectbox(
        "Select Country", 
        get_supported_countries(),
        index=get_supported_countries().index(st.session_state.current_country)
    )
    
    knowledge_level = st.radio(
        "Select Knowledge Level",
        ["Beginner (Like I'm 10)", "Standard", "Advanced"],
        index=1,
        key="knowledge_level"
    )
    
    st.divider()
    st.markdown("### Navigation")
    app_mode = st.radio("Choose a mode:", ["💬 Chat Assistant", "🗳️ Voting Simulator", "📅 Election Timeline"])

    # If country changes, reset chat and simulator state
    if selected_country != st.session_state.current_country:
        st.session_state.current_country = selected_country
        if "sim_step" in st.session_state:
             st.session_state.sim_step = 0
             st.session_state.sim_completed = False
             st.session_state.sim_selections = {}
        reset_chat(api_key, app_mode)
        
# --- Main Content Area ---

if app_mode == "💬 Chat Assistant":
    st.title("🤖 Election Intelligence Assistant")
    st.write(f"Currently helping you understand the **{st.session_state.current_country}** election process at a **{st.session_state.knowledge_level}** level.")
    
    # Initialize chat if empty
    if not st.session_state.messages:
        reset_chat(api_key, app_mode)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about the election process..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_llm_response(
                    api_key, 
                    st.session_state.messages, 
                    st.session_state.current_country, 
                    st.session_state.knowledge_level,
                    app_mode
                )
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

elif app_mode == "🗳️ Voting Simulator":
    render_simulator(st.session_state.current_country)
    st.divider()
    st.info("💡 Want to ask a question about this simulator step? Switch to the **Chat Assistant** tab, and I'll remember where you were!")

elif app_mode == "📅 Election Timeline":
    render_timeline(st.session_state.current_country)
    st.divider()
    st.info("💡 Have a question about these dates? Switch to the **Chat Assistant** tab!")
