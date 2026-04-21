import streamlit as st
import time
import textwrap
from data.mock_api import get_country_data

def init_simulator_state():
    if "sim_step" not in st.session_state:
        st.session_state.sim_step = 0
    if "sim_completed" not in st.session_state:
        st.session_state.sim_completed = False
    if "sim_selections" not in st.session_state:
        st.session_state.sim_selections = {}

def render_simulator(country: str):
    init_simulator_state()
    
    country_data = get_country_data(country)
    steps = country_data.get("simulator_steps", [])
    
    # Custom CSS for the simulator to match SaaS theme
    st.markdown(textwrap.dedent("""
    <style>
        /* Simulator Form Styling */
        div[data-testid="stForm"] {
            background-color: #1E1E2F;
            border-radius: 12px;
            padding: 30px;
            border: 1px solid rgba(255,255,255,0.05);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        
        /* Success Message Container */
        .simulator-success {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(139, 92, 246, 0.2));
            border-left: 4px solid #8B5CF6;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
    </style>
    """), unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='margin-bottom: 0;'>🗳️ Interactive Voting Simulator: {country}</h3>", unsafe_allow_html=True)
    st.divider()
    
    if not steps:
        st.warning("Simulator data not available for this country yet.")
        return

    # If completed, show success message
    if st.session_state.sim_completed:
        st.markdown(textwrap.dedent("""
        <div class="simulator-success">
            <h3 style="color: #8B5CF6; margin-top:0;">🎉 Simulation Complete!</h3>
            <p style="color: #A0AEC0;">You have successfully navigated the voting process.</p>
        </div>
        """), unsafe_allow_html=True)
        st.balloons()
        
        st.write("#### Your Selections:")
        for k, v in st.session_state.sim_selections.items():
            st.markdown(f"- **{k}**: <span style='color:#8B5CF6;'>{v}</span>", unsafe_allow_html=True)
            
        st.write("")
        if st.button("Restart Simulator", type="primary"):
            st.session_state.sim_step = 0
            st.session_state.sim_completed = False
            st.session_state.sim_selections = {}
            st.rerun()
        return

    # Progress bar and indicator
    progress = st.session_state.sim_step / len(steps)
    st.progress(progress, text=f"Progress: Step {st.session_state.sim_step + 1} of {len(steps)}")
    
    st.write("") # Spacing
    
    # Current step logic
    current_step = steps[st.session_state.sim_step]
    
    with st.form(key=f"sim_form_{st.session_state.sim_step}"):
        st.markdown(f"<h3 style='color:#FAFAFA; margin-bottom: 5px;'>{current_step['title']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#A0AEC0; font-size:1.05rem;'>{current_step['description']}</p>", unsafe_allow_html=True)
        
        st.write("") # Spacing
        
        # Handle different input types if defined in the mock data
        user_input = None
        if current_step.get("type") == "choice":
            user_input = st.radio("Make your selection:", current_step.get("options", []))
            
        st.write("") # Spacing
        
        # Navigation buttons
        col1, col2 = st.columns([1, 1])
        
        with col2:
            is_last_step = st.session_state.sim_step == len(steps) - 1
            submit_label = "Submit Final Ballot" if is_last_step else "Next Step →"
            submitted = st.form_submit_button(submit_label, type="primary", use_container_width=True)
            
        with col1:
            if st.session_state.sim_step > 0:
                go_back = st.form_submit_button("← Previous Step", use_container_width=True)
                if go_back:
                    st.session_state.sim_step -= 1
                    st.rerun()

        if submitted:
            # Save selections if needed
            if user_input:
                 st.session_state.sim_selections[current_step["title"]] = user_input
                 
            # Simulate a brief loading time for realism
            with st.spinner("Processing..."):
                time.sleep(0.5)
                
            if is_last_step:
                st.session_state.sim_completed = True
            else:
                st.session_state.sim_step += 1
            st.rerun()
