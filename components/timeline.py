import streamlit as st
import textwrap
from data.mock_api import get_country_data

def render_timeline(country: str):
    """Renders a dynamic timeline based on the selected country."""
    
    country_data = get_country_data(country)
    timeline_events = country_data.get("timeline", [])
    
    # st.header and st.write are removed here because they are handled by the main dashboard UI now,
    # or we can style them better. Let's use a subtle subheader instead.
    st.markdown(f"<h3 style='margin-bottom: 0;'>Election Timeline: {country}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #888;'>System: {country_data.get('system', 'Unknown')}</p>", unsafe_allow_html=True)
    st.divider()

    if not timeline_events:
        st.warning("No timeline data available for this country.")
        return

    # CSS for the modern vertical timeline - Updated with Neon Purple SaaS theme
    st.markdown(textwrap.dedent("""
    <style>
    .timeline-container {
        position: relative;
        max-width: 800px;
        margin: 2rem auto;
        padding: 10px 0;
    }
    
    /* The central line */
    .timeline-container::after {
        content: '';
        position: absolute;
        width: 4px;
        background-color: rgba(255, 255, 255, 0.05);
        top: 0;
        bottom: 0;
        left: 150px;
        margin-left: -2px;
        border-radius: 2px;
    }

    .timeline-item {
        position: relative;
        display: flex;
        margin-bottom: 2.5rem;
        animation: slideUpFade 0.6s ease-out forwards;
        opacity: 0;
    }
    
    /* Staggered animation delays */
    .timeline-item:nth-child(1) { animation-delay: 0.1s; }
    .timeline-item:nth-child(2) { animation-delay: 0.2s; }
    .timeline-item:nth-child(3) { animation-delay: 0.3s; }
    .timeline-item:nth-child(4) { animation-delay: 0.4s; }
    .timeline-item:nth-child(5) { animation-delay: 0.5s; }
    .timeline-item:nth-child(6) { animation-delay: 0.6s; }

    .timeline-left {
        width: 150px;
        padding-right: 30px;
        text-align: right;
        padding-top: 18px;
    }
    
    .timeline-left-title {
        margin: 0;
        font-weight: 700;
        color: #8B5CF6; /* Neon Purple */
        font-size: 1.1rem;
    }
    
    .timeline-left-date {
        color: #888;
        font-size: 0.85rem;
        margin-top: 4px;
        display: block;
    }

    /* The dots */
    .timeline-marker {
        position: absolute;
        width: 22px;
        height: 22px;
        left: 139px; /* 150px - 11px */
        background-color: #0E1117; /* Dark theme bg to cutout line */
        border: 4px solid #8B5CF6;
        border-radius: 50%;
        z-index: 1;
        top: 20px;
        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
        transition: all 0.3s ease;
    }

    .timeline-content {
        flex: 1;
        padding: 24px;
        background: #1E1E2F; /* SaaS card bg */
        border-radius: 12px;
        margin-left: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2), 0 1px 3px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        border: 1px solid rgba(255,255,255,0.05);
        position: relative;
    }
    
    /* Interactive Hover Effects */
    .timeline-item:hover .timeline-content {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3), 0 3px 6px rgba(0,0,0,0.2);
        border-color: rgba(139, 92, 246, 0.4);
    }
    
    .timeline-item:hover .timeline-marker {
        background-color: #8B5CF6;
        box-shadow: 0 0 0 6px rgba(139, 92, 246, 0.2);
    }

    .timeline-content h4 {
        margin-top: 0;
        margin-bottom: 12px;
        font-size: 1.25rem;
        color: #FAFAFA;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .timeline-content p {
        margin-bottom: 0;
        color: #A0AEC0;
        line-height: 1.6;
        font-size: 0.95rem;
    }

    @keyframes slideUpFade {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Responsive Design for Mobile */
    @media screen and (max-width: 600px) {
        .timeline-container::after {
            left: 20px;
        }
        .timeline-item {
            flex-direction: column;
            margin-bottom: 2rem;
        }
        .timeline-left {
            width: 100%;
            text-align: left;
            padding-left: 50px;
            padding-top: 0;
            padding-bottom: 10px;
        }
        .timeline-marker {
            left: 9px;
            top: 2px;
        }
        .timeline-content {
            margin-left: 40px;
        }
    }
    </style>
    """), unsafe_allow_html=True)

    # Build the HTML structure
    html_content = '<div class="timeline-container">'
    
    # Simple icon mapping for visual flair
    icons = ["📝", "🗳️", "📣", "✅", "🎉", "⚖️"]
    
    for i, event in enumerate(timeline_events):
        icon = icons[i % len(icons)]
        html_content += textwrap.dedent(f"""
        <div class="timeline-item">
            <div class="timeline-left">
                <div class="timeline-left-title">Phase {i+1}</div>
                <span class="timeline-left-date">{event['date']}</span>
            </div>
            <div class="timeline-marker"></div>
            <div class="timeline-content">
                <h4><span>{icon}</span> {event['phase']}</h4>
                <p>{event['description']}</p>
            </div>
        </div>
        """)
        
    html_content += '</div>'
    
    # Render the complete HTML without leading spaces causing issues
    st.markdown(html_content, unsafe_allow_html=True)
