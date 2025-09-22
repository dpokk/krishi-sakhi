"""
Krishi Sakhi - Enhanced Farm Profiling Page
Interactive farm analysis with multilingual support and enhanced UI
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import time
import json
import math
from utils.geo_utils import (
    acres_to_radius, 
    generate_circle_polygon, 
    validate_kerala_coordinates
)
from utils.data_utils import get_mock_backend_response
from utils.language_utils import get_text, language_toggle, get_color_for_level

# Configure page
st.set_page_config(
    page_title="Farm Profile - Krishi Sakhi",
    page_icon="🌾",
    layout="wide"
)

def load_css():
    """Load custom CSS for enhanced UI"""
    try:
        with open('assets/styles.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found. Using default styling.")

def create_kerala_map():
    """Create an interactive colorful map centered on Kerala"""
    # Kerala's approximate center coordinates
    kerala_lat, kerala_lon = 10.8505, 76.2711
    
    # Create folium map with colorful satellite view
    m = folium.Map(
        location=[kerala_lat, kerala_lon],
        zoom_start=8,
        tiles=None  # We'll add custom tiles
    )
    
    # Add multiple tile layers for better visuals
    folium.TileLayer(
        'OpenStreetMap',
        name='Street Map',
        overlay=False,
        control=True
    ).add_to(m)
    
    folium.TileLayer(
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite View',
        overlay=False,
        control=True
    ).add_to(m)
    
    folium.TileLayer(
        'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Hybrid (Satellite + Roads)',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add a center marker for Kerala
    folium.Marker(
        [kerala_lat, kerala_lon],
        popup="<b>Kerala State Center</b><br>Click anywhere on the map to select your farm location",
        tooltip="Click on map to select farm location",
        icon=folium.Icon(color='green', icon='leaf', prefix='fa')
    ).add_to(m)
    
    return m

def display_step_indicator(step_num, step_text, is_completed=False, is_current=False):
    """Display enhanced step indicators"""
    status_class = "completed" if is_completed else ("current" if is_current else "pending")
    
    st.markdown(f"""
    <div class='step-indicator {status_class} fade-in'>
        <div class='step-number'>
            {step_num}
        </div>
        <div class='step-text'>
            {step_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_analysis_results(response_data, farm_lat, farm_lon, farm_area):
    """Display enhanced farm analysis results"""
    
    # Enhanced header with animation
    st.markdown(f"""
    <div class='main-header slide-up'>
        <h1 style='margin: 0; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>
            🌾 {get_text('farm_analysis')} 🌾
        </h1>
        <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;'>
            📍 Location: {farm_lat:.4f}, {farm_lon:.4f} | 🏞️ Area: {farm_area} {get_text('acres')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Main metrics row with enhanced styling
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card slide-up'>
            <div class='metric-value'>
                {response_data['soil_properties']['malayalam_texture'] if get_text('soil_type') == 'മണ്ണിന്റെ തരം' else response_data['soil_properties']['texture']}
            </div>
            <div class='metric-label'>
                🌱 {get_text('soil_type')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card slide-up'>
            <div class='metric-value'>
                {response_data['groundwater']['depth_meters']} {get_text('meters')}
            </div>
            <div class='metric-label'>
                💧 {get_text('groundwater')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        vegetation_text = (response_data['vegetation_index']['malayalam'] 
                          if get_text('vegetation_health') == 'സസ്യാവസ്ഥ' 
                          else response_data['vegetation_index']['remark'])
        st.markdown(f"""
        <div class='metric-card slide-up'>
            <div class='metric-value'>
                {vegetation_text}
            </div>
            <div class='metric-label'>
                🌿 {get_text('vegetation_health')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced nutrient levels section
    st.markdown("---")
    st.markdown(f"""
    <div class='welcome-card fade-in'>
        <h3 style='color: #2E8B57; text-align: center; margin-bottom: 2rem;'>
            🧪 {get_text('nutrient_levels')} 🧪
        </h3>
    """, unsafe_allow_html=True)

    # Nutrient display with progress bars
    nutrients = ['nitrogen', 'phosphorus', 'potassium']
    nutrient_levels = ['Low', 'Medium', 'High']
    
    for i, nutrient in enumerate(nutrients):
        level = nutrient_levels[i]
        level_text = get_text(level.lower())
        color = get_color_for_level(level)
        
        # Calculate progress percentage
        progress = {'Low': 30, 'Medium': 65, 'High': 95}[level]
        progress_class = f"progress-{level.lower()}"
        
        st.markdown(f"""
        <div style='margin: 1.5rem 0;'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                <span style='font-weight: 600; font-size: 1.1rem; color: #2c3e50;'>
                    {get_text(nutrient)} 
                </span>
                <span class='nutrient-{level.lower()}' style='font-size: 0.9rem;'>
                    {level_text}
                </span>
            </div>
            <div class='progress-container'>
                <div class='progress-bar {progress_class}' style='width: {progress}%;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Detailed soil properties with expandable section
    with st.expander(f"🔬 {get_text('detailed_soil')}", expanded=False):
        soil = response_data['soil_properties']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <strong>pH Level:</strong> {soil['ph']}<br>
                <strong>Organic Carbon:</strong> {soil['organic_carbon_percent']}{get_text('percent')}<br>
                <strong>CEC:</strong> {soil['cec']} cmol/kg
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <strong>Sand:</strong> {soil['sand_percent']}{get_text('percent')}<br>
                <strong>Silt:</strong> {soil['silt_percent']}{get_text('percent')}<br>
                <strong>Clay:</strong> {soil['clay_percent']}{get_text('percent')}
            </div>
            """, unsafe_allow_html=True)

    # Enhanced recommendations section
    st.markdown("---")
    
    st.markdown(f"""
    <div class='feature-list slide-up'>
        <h3 style='color: #2E8B57; text-align: center; margin-bottom: 2rem;'>
            💡 {get_text('recommendations')} 💡
        </h3>
    """, unsafe_allow_html=True)
    
    # Basic recommendations based on data
    basic_recommendations = [
        "Apply organic compost for better soil health",
        "Consider drip irrigation for water efficiency", 
        "Test soil pH levels regularly",
        "Use appropriate fertilizers based on soil analysis"
    ]
    
    for i, rec in enumerate(basic_recommendations, 1):
        st.markdown(f"""
        <div class='feature-item'>
            <div class='feature-icon'>{i}.</div>
            <div style='font-size: 1.1rem; line-height: 1.6;'>{rec}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    """Enhanced main function for farm profiling"""
    
    # Load custom CSS and language toggle
    load_css()
    language_toggle()
    
    # Initialize session state
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = None
    if 'farm_area' not in st.session_state:
        st.session_state.farm_area = 0.0
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False

    # Enhanced page header
    st.markdown(f"""
    <div class='main-header fade-in'>
        <h1 style='margin: 0;'>{get_text('farm_profile')}</h1>
        <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
            {get_text('welcome_description')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for input controls
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #2E8B57, #228B22); 
                    color: white; border-radius: 15px; margin-bottom: 2rem;'>
            <h3 style='margin: 0;'>🌾 Farm Setup</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 1: Location Selection
        display_step_indicator(1, get_text('step1'), 
                             is_completed=st.session_state.selected_location is not None,
                             is_current=st.session_state.selected_location is None)
        
        st.markdown(f"""
        <div style='background: rgba(46, 139, 87, 0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
            <p style='margin: 0; font-size: 0.9rem; color: #2c3e50;'>
                📍 {get_text('click_map')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 2: Area Input
        display_step_indicator(2, get_text('step2'), 
                             is_completed=st.session_state.farm_area > 0,
                             is_current=st.session_state.selected_location is not None and st.session_state.farm_area == 0)
        
        if st.session_state.selected_location:
            lat, lon = st.session_state.selected_location
            st.success(f"✅ Location: {lat:.4f}, {lon:.4f}")
            
            farm_area = st.number_input(
                get_text('enter_area'),
                min_value=0.1,
                max_value=1000.0,
                value=st.session_state.farm_area if st.session_state.farm_area > 0 else 1.0,
                step=0.1,
                format="%.1f",
                help="Enter your farm area in acres (1 acre = 4047 square meters)"
            )
            st.session_state.farm_area = farm_area
            
            # Show calculated metrics
            radius = acres_to_radius(farm_area)
            area_sqm = farm_area * 4047
            st.info(f"📏 Area: {area_sqm:.0f} m² | 🔄 Radius: {radius:.0f} m")
        
        # Step 3: Analysis
        display_step_indicator(3, get_text('step3'), 
                             is_completed=st.session_state.analysis_complete,
                             is_current=st.session_state.selected_location is not None and st.session_state.farm_area > 0)

    # Main content area
    if not st.session_state.analysis_complete:
        # Create and display map
        st.markdown(f"<div class='map-container'>", unsafe_allow_html=True)
        
        m = create_kerala_map()
        
        # Add existing location and enhanced visualization if available
        if st.session_state.selected_location:
            lat, lon = st.session_state.selected_location
            
            # Add main farm marker with custom icon
            folium.Marker(
                [lat, lon],
                popup=f"""<div style='font-family: Arial; font-size: 12px;'>
                         <b>🌾 Your Farm Location</b><br>
                         <b>Coordinates:</b> {lat:.4f}, {lon:.4f}<br>
                         <b>Area:</b> {st.session_state.farm_area} acres<br>
                         <i>Click 'Analyze' to get soil data</i>
                         </div>""",
                tooltip="🌾 Your Selected Farm Location",
                icon=folium.Icon(color='red', icon='home', prefix='fa')
            ).add_to(m)
            
            # Add circle representing farm area with enhanced styling
            if st.session_state.farm_area > 0:
                radius = acres_to_radius(st.session_state.farm_area)
                
                # Main area circle
                folium.Circle(
                    location=[lat, lon],
                    radius=radius,
                    popup=f"""<div style='font-family: Arial; font-size: 11px;'>
                             <b>Farm Area Boundary</b><br>
                             <b>Area:</b> {st.session_state.farm_area} acres<br>
                             <b>Radius:</b> {radius:.0f} meters<br>
                             <b>Perimeter:</b> {2 * 3.14159 * radius:.0f} meters
                             </div>""",
                    color='#FF6B35',  # Orange border
                    fillColor='#4CAF50',  # Green fill
                    fillOpacity=0.2,
                    weight=3,
                    dashArray='10, 5'  # Dashed border
                ).add_to(m)
                
                # Add boundary markers at cardinal directions
                directions = [
                    (0, 'North', '🧭'),
                    (90, 'East', '➡️'),
                    (180, 'South', '⬇️'),
                    (270, 'West', '⬅️')
                ]
                
                for angle, direction, emoji in directions:
                    # Calculate point on circle boundary
                    angle_rad = math.radians(angle)
                    # Approximate degrees per meter at this latitude
                    lat_offset = (radius * math.cos(angle_rad)) / 111320
                    lon_offset = (radius * math.sin(angle_rad)) / (111320 * math.cos(math.radians(lat)))
                    
                    boundary_lat = lat + lat_offset
                    boundary_lon = lon + lon_offset
                    
                    folium.CircleMarker(
                        [boundary_lat, boundary_lon],
                        radius=8,
                        popup=f"{emoji} {direction} Boundary",
                        tooltip=f"{direction}",
                        color='#FF6B35',
                        fillColor='#FFF',
                        fillOpacity=0.8,
                        weight=2
                    ).add_to(m)

        # Display map with enhanced interaction
        st.markdown("**📍 Click anywhere on the map to select your farm location**")
        map_data = st_folium(
            m, 
            width=800, 
            height=600, 
            returned_objects=["last_clicked", "last_object_clicked"],
            key="kerala_map"
        )
        
        # Handle map clicks with better validation
        clicked_location = None
        
        # Check for direct map clicks
        if map_data['last_clicked']:
            clicked_location = map_data['last_clicked']
        elif map_data['last_object_clicked']:
            clicked_location = map_data['last_object_clicked']
            
        if clicked_location:
            lat = clicked_location['lat']
            lon = clicked_location['lng']
            
            # Validate coordinates
            if validate_kerala_coordinates(lat, lon):
                st.session_state.selected_location = (lat, lon)
                st.success(f"✅ Farm location selected: {lat:.4f}, {lon:.4f}")
                st.rerun()
            else:
                st.warning("⚠️ Please select a location within Kerala state boundaries")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Analysis submission section
        if st.session_state.selected_location and st.session_state.farm_area > 0:
            st.markdown("---")
            st.markdown("### 📋 Ready for Analysis")
            
            # Show summary before analysis
            lat, lon = st.session_state.selected_location
            st.write(f"📍 **Location:** {lat:.4f}, {lon:.4f}")
            st.write(f"🌾 **Area:** {st.session_state.farm_area} acres")
            st.write(f"📏 **Coverage:** {st.session_state.farm_area * 4047:.0f} m²")
            
            # Analyze button with progress
            if st.button(
                f"🔍 {get_text('analyze_farm')}", 
                type="primary", 
                use_container_width=True,
                help="Click to start soil and vegetation analysis"
            ):
                # Enhanced loading with progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                stages = [
                    (0.2, "Analyzing satellite imagery..."),
                    (0.4, "Processing soil data..."),
                    (0.6, "Calculating vegetation indices..."),
                    (0.8, "Generating recommendations..."),
                    (1.0, "Analysis complete!")
                ]
                
                for progress, message in stages:
                    progress_bar.progress(progress)
                    status_text.text(message)
                    time.sleep(0.8)
                
                st.session_state.analysis_complete = True
                st.balloons()  # Celebration animation
                st.rerun()
        elif st.session_state.selected_location and st.session_state.farm_area <= 0:
            st.warning("⚠️ Please enter a valid farm area greater than 0 acres")
        elif st.session_state.farm_area > 0 and not st.session_state.selected_location:
            st.warning("⚠️ Please select a location on the map first")
    
    else:
        # Show analysis results
        lat, lon = st.session_state.selected_location
        farm_area = st.session_state.farm_area
        
        # Generate mock data payload
        radius = acres_to_radius(farm_area)
        boundary_polygon = generate_circle_polygon(lat, lon, radius)
        
        # Data sent to backend
        with st.expander(f"📤 {get_text('data_sent')}", expanded=False):
            payload = {
                "farmerId": "FARMER_123_DEMO",
                "farmLocation": {
                    "latitude": lat,
                    "longitude": lon
                },
                "farmAreaAcres": farm_area,
                "boundary": boundary_polygon
            }
            st.json(payload)
        
        # Get and display mock response
        response_data = get_mock_backend_response(lat, lon, farm_area)
        display_analysis_results(response_data, lat, lon, farm_area)
        
        # Reset button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 New Analysis", type="secondary", use_container_width=True):
                st.session_state.selected_location = None
                st.session_state.farm_area = 0.0
                st.session_state.analysis_complete = False
                st.rerun()

if __name__ == "__main__":
    main()
