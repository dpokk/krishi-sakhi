"""
Krishi Sakhi (കൃഷി സഖി) - AI-Powered Farming Assistant
Enhanced Main Application Entry Point (Welcome Page)

This is the landing page of the Krishi Sakhi application, designed for
smallholder farmers in Kerala to get personalized agricultural advice.
Features multilingual support and enhanced UI.
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

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "welcome"

def show_welcome_page():
    """Display the enhanced welcome page with language support"""
    
    # Load custom CSS
    load_css()
    
    # Language toggle in sidebar
    language_toggle()
    
    # Enhanced main header using Streamlit
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #2E8B57, #228B22); 
                border-radius: 15px; margin: 1rem 0; color: white;'>
    """, unsafe_allow_html=True)
    
    st.markdown(f"# {get_text('main_title')}")
    st.markdown(f"### {get_text('subtitle')}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Main content container
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Enhanced welcome card using Streamlit components
        with st.container():
            # Custom CSS for this section
            st.markdown("""
            <style>
            .welcome-container {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 249, 250, 0.95));
                padding: 2rem;
                border-radius: 15px;
                margin: 1rem 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                border-left: 4px solid #2E8B57;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f"## {get_text('welcome_title')}")
            st.write(get_text('welcome_description'))
        
        # Enhanced features section using simple Streamlit components
        st.markdown(f"### ✨ {get_text('key_features')} ✨")
        
        # Use success/info boxes for better visibility
        st.success(f"📍 {get_text('location_analysis')}")
        st.info(f"🌱 {get_text('soil_health')}")
        st.success(f"🌿 {get_text('vegetation_monitoring')}")
        st.info(f"💧 {get_text('groundwater_info')}")
        st.success(f"🌐 {get_text('multilingual')}")
        st.info(f"🗺️ {get_text('easy_maps')}")
        
        # Enhanced call-to-action button
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center the button with enhanced styling
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            if st.button(
                get_text('get_started'), 
                type="primary", 
                use_container_width=True,
                key="get_started_btn"
            ):
                # Show success message instead of navigation
                st.success("✅ Welcome! Please use the sidebar to navigate to 'Farm Profile' page.")
                st.info("👈 Look for the sidebar navigation on the left and click 'Farm Profile'")
    
    # Enhanced footer section
    st.markdown("---")
    st.markdown(f"""
    <div class='footer fade-in'>
        <h4 style='margin-bottom: 1rem; color: #fff;'>🌾 Krishi Sakhi 🌾</h4>
        <p style='margin: 0; font-size: 1.1rem;'>
            {get_text('powered_by')}
        </p>
        <p style='margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;'>
            {get_text('supporting')}
        </p>
        <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);'>
            <p style='margin: 0; font-size: 0.9rem; opacity: 0.8;'>
                🚀 Powered by Advanced Geospatial AI Technology
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def navigate_to_farm_profile():
    """Enhanced navigation to the farm profiling page"""
    load_css()
    language_toggle()
    
    # Enhanced loading animation
    st.markdown(f"""
    <div class='loading-container fade-in'>
        <div class='loading-spinner'></div>
        <h3 style='color: #2E8B57;'>{get_text('loading')}</h3>
        <p style='color: #666;'>Please wait while we prepare your farm analysis tools...</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show a temporary loading message and redirect instructions
    with st.spinner("Redirecting to Farm Profile..."):
        time.sleep(2)
    
    st.markdown(f"""
    <div class='welcome-card'>
        <h3 style='color: #2E8B57; text-align: center;'>🔄 {get_text('farm_profile')} Navigation</h3>
        
        <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    padding: 2rem; border-radius: 15px; margin: 1rem 0;'>
            <p style='font-size: 1.1rem; line-height: 1.6; margin-bottom: 1rem;'>
                <strong>To continue with your farm analysis:</strong>
            </p>
            <ul style='font-size: 1rem; line-height: 1.8; margin-left: 1rem;'>
                <li>Look for the sidebar navigation (← arrow on the left)</li>
                <li>Click on <strong>"Farm Profile"</strong></li>
                <li>Or refresh the page and use the navigation menu</li>
            </ul>
        </div>
        
        <div style='text-align: center; margin-top: 2rem;'>
            <button onclick='window.location.reload()' 
                    style='background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
                           color: white; border: none; padding: 1rem 2rem; 
                           border-radius: 10px; cursor: pointer; font-size: 1rem;
                           box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);'>
                🔄 Refresh Page
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Enhanced main application logic"""
    
    # Add some custom styling for the entire app
    st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # Handle navigation based on session state
    if st.session_state.page == "welcome":
        show_welcome_page()
    elif st.session_state.page == "farm_profile":
        navigate_to_farm_profile()
    else:
        # Fallback to welcome page
        st.session_state.page = "welcome"
        show_welcome_page()

if __name__ == "__main__":
    main()
