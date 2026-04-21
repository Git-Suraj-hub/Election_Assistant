import streamlit as st
import time
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
    
    st.header(f"🗳️ Interactive Voting Simulator: {country}")
    
    if not steps:
        st.warning("Simulator data not available for this country yet.")
        return

    # If completed, show success message
    if st.session_state.sim_completed:
        st.success("🎉 You have successfully completed the voting simulation!")
        st.balloons()
        st.write("### Your Selections:")
        for k, v in st.session_state.sim_selections.items():
            st.write(f"- **{k}**: {v}")
            
        if st.button("Restart Simulator"):
            st.session_state.sim_step = 0
            st.session_state.sim_completed = False
            st.session_state.sim_selections = {}
            st.rerun()
        return

    # Progress bar
    progress = st.session_state.sim_step / len(steps)
    st.progress(progress, text=f"Step {st.session_state.sim_step + 1} of {len(steps)}")
    
    # Current step logic
    current_step = steps[st.session_state.sim_step]
    
    with st.form(key=f"sim_form_{st.session_state.sim_step}"):
        st.subheader(current_step["title"])
        st.write(current_step["description"])
        
        # Handle different input types if defined in the mock data
        user_input = None
        if current_step.get("type") == "choice":
            user_input = st.radio("Make your selection:", current_step.get("options", []))
            
        # Navigation buttons
        col1, col2 = st.columns([1, 1])
        
        with col2:
            is_last_step = st.session_state.sim_step == len(steps) - 1
            submit_label = "Submit Ballot" if is_last_step else "Next Step"
            submitted = st.form_submit_button(submit_label, type="primary", use_container_width=True)
            
        with col1:
            if st.session_state.sim_step > 0:
                go_back = st.form_submit_button("Previous Step", use_container_width=True)
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
