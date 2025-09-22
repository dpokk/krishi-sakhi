"""
Language Utilities for Krishi Sakhi
Handles multilingual text management and language switching
"""

import streamlit as st

# Language dictionary with all text content
LANGUAGES = {
    'en': {
        'app_title': 'Krishi Sakhi | Your Digital Farming Assistant',
        'main_title': '🌾 Krishi Sakhi',
        'subtitle': 'Your Digital Farming Assistant',
        'welcome_title': 'Welcome to Krishi Sakhi! 🙏',
        'welcome_description': """Get personalized farming advice based on your exact location and land area. 
        Our AI-powered system analyzes soil properties, vegetation health, and groundwater 
        availability to provide you with actionable insights.""",
        'key_features': 'Key Features',
        'location_analysis': '**Location-Based Analysis**',
        'soil_health': '**Soil Health Assessment**',
        'vegetation_monitoring': '**Vegetation Monitoring**',
        'groundwater_info': '**Groundwater Information**',
        'multilingual': '**Multilingual Interface**',
        'easy_maps': '**Easy-to-Use Maps**',
        'get_started': '🌱 Get Started',
        'powered_by': 'Powered by Advanced Geospatial AI Technology',
        'supporting': 'Supporting Kerala\'s Farmers',
        'language_toggle': '🌐 Language',
        
        # Farm Profile Page
        'farm_profile': 'Farm Profile',
        'step1': 'Step 1: Mark Your Farm\'s Location',
        'step2': 'Step 2: Enter Your Land Area',
        'step3': 'Step 3: Analyze Your Farm',
        'click_map': 'Click on the map to mark your farm location',
        'enter_area': 'Enter your farm area in acres',
        'analyze_farm': '🔍 Analyze My Farm',
        'data_sent': 'Data Sent to Backend',
        'farm_analysis': 'Farm Analysis Report',
        'soil_type': 'Soil Type',
        'groundwater': 'Groundwater',
        'vegetation_health': 'Vegetation Health',
        'nutrient_levels': 'Nutrient Levels',
        'nitrogen': 'Nitrogen',
        'phosphorus': 'Phosphorus',
        'potassium': 'Potassium',
        'detailed_soil': 'Detailed Soil Properties',
        'recommendations': 'Recommendations',
        'low': 'Low',
        'medium': 'Medium',
        'high': 'High',
        'meters': 'meters',
        'percent': '%',
        'acres': 'acres',
        'loading': 'Analyzing your farm data...',
        'select_location': 'Please select a location on the map first',
        'enter_valid_area': 'Please enter a valid area greater than 0',
    },
    
    'ml': {
        'app_title': 'കൃഷി സഖി | നിങ്ങളുടെ ഡിജിറ്റൽ കൃഷി സഹായി',
        'main_title': '🌾 കൃഷി സഖി',
        'subtitle': 'നിങ്ങളുടെ ഡിജിറ്റൽ കൃഷി സഹായി',
        'welcome_title': 'കൃഷി സഖിയിലേക്ക് സ്വാഗതം! 🙏',
        'welcome_description': """നിങ്ങളുടെ കൃത്യമായ സ്ഥാനത്തും സ്ഥലത്തിന്റെ വിസ്തീർണ്ണത്തിന്റെ അടിസ്ഥാനത്തിലും 
        വ്യക്തിഗതമാക്കിയ കൃഷി ഉപദേശം നേടുക. ഞങ്ങളുടെ AI-പവർഡ് സിസ്റ്റം മണ്ണിന്റെ ഗുണങ്ങൾ, 
        സസ്യാരോഗ്യം, ഭൂഗർഭജല ലഭ്യത എന്നിവ വിശകലനം ചെയ്ത് നിങ്ങൾക്ക് 
        പ്രായോഗിക നിർദ്ദേശങ്ങൾ നൽകുന്നു.""",
        'key_features': 'പ്രധാന സവിശേഷതകൾ',
        'location_analysis': '**സ്ഥാന അടിസ്ഥാനത്തിലുള്ള വിശകലനം**',
        'soil_health': '**മണ്ണിന്റെ ആരോഗ്യ വിലയിരുത്തൽ**',
        'vegetation_monitoring': '**സസ്യ നിരീക്ഷണം**',
        'groundwater_info': '**ഭൂഗർഭജല വിവരങ്ങൾ**',
        'multilingual': '**മൾട്ടിലിംഗ്വൽ ഇന്റർഫേസ്**',
        'easy_maps': '**ഉപയോഗിക്കാൻ എളുപ്പമുള്ള മാപ്പുകൾ**',
        'get_started': '🌱 തുടങ്ങാം',
        'powered_by': 'വിപുലമായ ജിയോസ്പാഷ്യൽ AI സാങ്കേതികവിദ്യയാൽ പ്രവർത്തിക്കുന്നു',
        'supporting': 'കേരളത്തിലെ കർഷകരെ പിന്തുണയ്ക്കുന്നു',
        'language_toggle': '🌐 ഭാഷ',
        
        # Farm Profile Page
        'farm_profile': 'ഫാം പ്രൊഫൈൽ',
        'step1': 'ഘട്ടം 1: നിങ്ങളുടെ ഫാമിന്റെ സ്ഥാനം അടയാളപ്പെടുത്തുക',
        'step2': 'ഘട്ടം 2: നിങ്ങളുടെ സ്ഥലത്തിന്റെ വിസ്തീർണ്ണം നൽകുക',
        'step3': 'ഘട്ടം 3: നിങ്ങളുടെ ഫാം വിശകലനം ചെയ്യുക',
        'click_map': 'നിങ്ങളുടെ ഫാം സ്ഥാനം അടയാളപ്പെടുത്താൻ മാപ്പിൽ ക്ലിക്ക് ചെയ്യുക',
        'enter_area': 'നിങ്ങളുടെ ഫാം ഏരിയ ഏക്കറിൽ നൽകുക',
        'analyze_farm': '🔍 എന്റെ ഫാം വിശകലനം ചെയ്യുക',
        'data_sent': 'ബാക്കെൻഡിലേക്ക് അയച്ച ഡാറ്റ',
        'farm_analysis': 'ഫാം വിശകലന റിപ്പോർട്ട്',
        'soil_type': 'മണ്ണിന്റെ തരം',
        'groundwater': 'ഭൂഗർഭജലം',
        'vegetation_health': 'സസ്യാവസ്ഥ',
        'nutrient_levels': 'പ്രധാന പോഷകങ്ങൾ',
        'nitrogen': 'നൈട്രജൻ',
        'phosphorus': 'ഫോസ്ഫറസ്',
        'potassium': 'പൊട്ടാഷ്',
        'detailed_soil': 'മണ്ണിന്റെ വിശദാംശങ്ങൾ',
        'recommendations': 'ശിപാർശകൾ',
        'low': 'കുറവ്',
        'medium': 'ഇടത്തരം',
        'high': 'ഉയർന്നത്',
        'meters': 'മീറ്റർ',
        'percent': '%',
        'acres': 'ഏക്കർ',
        'loading': 'നിങ്ങളുടെ ഫാം ഡാറ്റ വിശകലനം ചെയ്യുന്നു...',
        'select_location': 'ദയവായി ആദ്യം മാപ്പിൽ ഒരു സ്ഥലം തിരഞ്ഞെടുക്കുക',
        'enter_valid_area': 'ദയവായി 0-ൽ കൂടുതൽ സാധുവായ ഏരിയ നൽകുക',
    }
}

def get_language():
    """Get current language from session state"""
    if 'language' not in st.session_state:
        st.session_state.language = 'en'  # Default to English
    return st.session_state.language

def set_language(lang_code):
    """Set language in session state"""
    st.session_state.language = lang_code

def get_text(key):
    """Get text for current language"""
    lang = get_language()
    return LANGUAGES[lang].get(key, f"[{key}]")

def language_toggle():
    """Display language toggle button in sidebar"""
    current_lang = get_language()
    
    # Language toggle in sidebar
    with st.sidebar:
        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("ENG", help="English", key="lang_en", 
                        type="primary" if current_lang == 'en' else "secondary",
                        use_container_width=True):
                set_language('en')
                st.rerun()
        
        with col2:
            if st.button("മലയാളം", help="മലയാളം", key="lang_ml", 
                        type="primary" if current_lang == 'ml' else "secondary",
                        use_container_width=True):
                set_language('ml')
                st.rerun()
        
        st.markdown(f"**🌐 {get_text('language_toggle')}**")
        
def get_color_for_level(level):
    """Get color coding for nutrient levels"""
    colors = {
        'low': '#ff4444',    # Red
        'medium': '#ffaa00', # Orange  
        'high': '#44aa44'    # Green
    }
    return colors.get(level.lower(), '#666666')
