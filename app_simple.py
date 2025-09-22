"""
Krishi Sakhi - Simple Version Without Complex HTML
Fixed version to avoid HTML rendering issues
"""

import streamlit as st
import time
from utils.language_utils import get_text, language_toggle

# Configure the Streamlit page
st.set_page_config(
    page_title="Krishi Sakhi | Your Digital Farming Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    """Load custom CSS for enhanced UI"""
    try:
        with open('assets/styles.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found. Using default styling.")

def show_welcome_page():
    """Display the enhanced welcome page with language support"""
    
    # Load custom CSS
    load_css()
    
    # Language toggle in sidebar
    language_toggle()
    
    # Simple header
    st.markdown(f"# 🌾 {get_text('main_title')}")
    st.markdown(f"### {get_text('subtitle')}")
    st.markdown("---")
    
    # Welcome section
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown(f"## {get_text('welcome_title')}")
        st.write(get_text('welcome_description'))
        
        st.markdown("---")
        
        # Key features using simple components
        st.markdown(f"### ✨ {get_text('key_features')} ✨")
        
        # Feature list with emojis and text
        features = [
            ("📍", get_text('location_analysis')),
            ("🌱", get_text('soil_health')),
            ("🌿", get_text('vegetation_monitoring')),
            ("💧", get_text('groundwater_info')),
            ("🌐", get_text('multilingual')),
            ("🗺️", get_text('easy_maps'))
        ]
        
        for emoji, feature_text in features:
            st.write(f"{emoji} **{feature_text}**")
        
        st.markdown("---")
        
        # Call to action button
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            if st.button(get_text('get_started'), type="primary", use_container_width=True):
                st.success("✅ Welcome! Please use the sidebar to navigate to 'Farm Profile' page.")
                st.info("👈 Look for the sidebar navigation on the left and click 'Farm Profile'")
    
    # Footer
    st.markdown("---")
    st.markdown(f"**🌾 Krishi Sakhi 🌾**")
    st.markdown(get_text('powered_by'))
    st.markdown(get_text('supporting'))

def main():
    """Main application logic"""
    
    # Hide Streamlit branding
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    show_welcome_page()

if __name__ == "__main__":
    main()
