import streamlit as st
from data.mock_api import get_country_data

def render_timeline(country: str):
    """Renders a dynamic timeline based on the selected country."""
    
    country_data = get_country_data(country)
    timeline_events = country_data.get("timeline", [])
    
    st.header(f"📅 Election Timeline: {country}")
    st.write(f"**System:** {country_data.get('system', 'Unknown')}")
    st.divider()

    if not timeline_events:
        st.warning("No timeline data available for this country.")
        return

    # Using markdown and containers to create a visual timeline
    for i, event in enumerate(timeline_events):
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"### Phase {i+1}")
                st.markdown(f"**{event['date']}**")
            with col2:
                st.info(f"#### {event['phase']}\n{event['description']}")
            
        if i < len(timeline_events) - 1:
            # Draw a subtle line between events
            st.markdown("<div style='text-align: center; color: gray;'>|</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; color: gray;'>v</div>", unsafe_allow_html=True)
            st.write("") # spacing
