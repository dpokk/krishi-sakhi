import streamlit as st

# Simple test app to verify everything works
st.title("🌾 Krishi Sakhi - Test Page")

# Test CSS loading
try:
    with open('assets/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    st.success("✅ CSS loaded successfully")
except Exception as e:
    st.error(f"❌ CSS loading failed: {e}")

# Test language utilities
try:
    from utils.language_utils import get_text, get_language
    st.success(f"✅ Language utils imported. Current language: {get_language()}")
    st.write(f"Welcome text: {get_text('welcome_title')}")
except Exception as e:
    st.error(f"❌ Language utils failed: {e}")

# Test geo utilities
try:
    from utils.geo_utils import acres_to_radius
    radius = acres_to_radius(1.0)
    st.success(f"✅ Geo utils imported. 1 acre = {radius:.2f} meter radius")
except Exception as e:
    st.error(f"❌ Geo utils failed: {e}")

# Test data utilities
try:
    from utils.data_utils import get_mock_backend_response
    st.success("✅ Data utils imported successfully")
except Exception as e:
    st.error(f"❌ Data utils failed: {e}")

st.info("If all tests pass, your main app should work fine!")
