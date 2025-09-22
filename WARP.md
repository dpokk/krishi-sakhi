# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Krishi Sakhi** (കൃഷി സഖി - Agricultural Friend) is a Python-based Streamlit web application designed for smallholder farmers in Kerala, India. The application provides hyper-localized, personalized agricultural advice through geospatial data analysis and AI-powered recommendations with full English-Malayalam bilingual support.

## Core Development Commands

### Environment Setup
```powershell
# Install dependencies
pip install -r requirements.txt

# Run main application
streamlit run app.py

# Run simplified version (fallback)
streamlit run app_simple.py

# Run test application
streamlit run test_app.py

# Run specific tests for farm profiling
streamlit run pages/1_Farm_Profile.py
```

### Development Workflow
```powershell
# Start local development server (default port 8501)
streamlit run app.py

# Run on specific port
streamlit run app.py --server.port 8502

# Run with custom config
streamlit run app.py --server.headless true

# Debug mode with error details
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```

## High-Level Architecture

### Application Structure
The application follows a modular Streamlit multi-page architecture with utilities separation:

- **Entry Points**: Multiple app entry points (`app.py`, `app_simple.py`, `test_app.py`)
- **Page-Based Navigation**: Uses Streamlit's native page system (`pages/` directory)
- **Utility Modules**: Separated concerns for language, geospatial, and data processing
- **Asset Management**: CSS and styling in dedicated assets folder

### Key Architectural Patterns

#### 1. Multilingual Content Management
The application uses a centralized language dictionary system:
- **Language State**: Managed through Streamlit session state
- **Text Retrieval**: `get_text(key)` function for dynamic content
- **Language Toggle**: Persistent language switching with UI rerun
- **Fallback System**: Graceful degradation for missing translations

#### 2. Geospatial Processing Pipeline
Coordinate and area calculations follow a specific flow:
- **Input**: Acres → Radius conversion for circular farm representation
- **Polygon Generation**: Circle approximation using coordinate geometry
- **Validation**: Kerala-specific coordinate boundary checking
- **Display**: GeoJSON format for Folium map integration

#### 3. Mock Backend Integration Pattern
The application simulates real backend responses:
- **Deterministic Randomization**: Uses coordinate-based seeding
- **Realistic Data**: Mimics ISRO Bhuvan and SoilGrids responses
- **Formatting Layer**: Separates raw data from display formatting
- **Multi-source Simulation**: Combines soil, vegetation, and groundwater data

### Component Interaction Flow

1. **User Location Selection** → `pages/1_Farm_Profile.py`
2. **Geographic Processing** → `utils/geo_utils.py`
3. **Mock Analysis** → `utils/data_utils.py`
4. **Display Formatting** → Language-aware rendering
5. **UI Enhancement** → CSS styling and animations

## Key Technical Details

### Language System Architecture
- **File**: `utils/language_utils.py`
- **Languages**: English (`en`) and Malayalam (`ml`)
- **State Management**: Streamlit session state with automatic rerun
- **UI Integration**: Flag-based toggle buttons in sidebar

### Geospatial Calculations
- **File**: `utils/geo_utils.py`
- **Coordinate System**: WGS84 decimal degrees
- **Area Conversion**: Acres to circular radius using precise calculations
- **Boundary Validation**: Kerala state geographical boundaries
- **Map Integration**: Folium with multiple tile layers (Street, Satellite, Hybrid)

### Data Processing Pipeline
- **File**: `utils/data_utils.py`
- **Mock Backend**: Simulates agricultural data sources
- **Nutrient Analysis**: N-P-K levels with color coding
- **Soil Properties**: Texture, pH, composition analysis
- **Recommendation Engine**: Context-aware farming suggestions

### UI/UX Enhancement System
- **File**: `assets/styles.css`
- **Background Strategy**: Blurred agricultural imagery with overlay
- **Glass Morphism**: Backdrop filters for modern appearance
- **Responsive Design**: Mobile-friendly with breakpoints
- **Animation System**: CSS keyframes for smooth transitions

## Important Development Considerations

### State Management Patterns
- Always use `st.session_state` for persistent data across reruns
- Language changes trigger immediate `st.rerun()` for UI updates
- Form data validation happens before backend simulation calls

### Error Handling Strategy
- CSS file loading has graceful fallback to default styling
- Import errors in utility modules show user-friendly error messages
- Coordinate validation prevents invalid geographic operations
- Test app (`test_app.py`) verifies all module imports before main usage

### Performance Optimization
- CSS is loaded once per page using try-catch blocks
- Map tiles are cached by Folium for better performance
- Mock data uses coordinate-based seeding for consistent responses
- Large CSS animations are GPU-accelerated with transform properties

### Accessibility & Localization
- High contrast ratios maintained in CSS color schemes
- Malayalam text uses appropriate fonts and rendering
- Progress bars have semantic meaning with color coding
- Map interactions are keyboard accessible through Folium

## Configuration Files

### Streamlit Configuration (`.streamlit/config.toml`)
- **Theme**: Agricultural green color scheme (`#2E8B57`)
- **Server Settings**: Development-friendly CORS and error handling
- **Client Settings**: Caching enabled for better performance

### Dependencies (`requirements.txt`)
Core stack: Streamlit, Folium, Geopy, Pandas, NumPy
- **Streamlit**: ≥1.28.0 for latest features
- **Folium**: ≥0.14.0 for map rendering
- **Streamlit-Folium**: ≥0.15.0 for map integration
- **Geopy**: ≥2.3.0 for coordinate calculations

## Testing & Validation

### Test Application Usage
```powershell
streamlit run test_app.py
```
This validates:
- CSS loading functionality
- Language utilities import and operation
- Geospatial calculations accuracy
- Data utilities mock response generation

### Manual Testing Checklist
1. **Language Toggle**: Switch between English/Malayalam
2. **Map Interaction**: Click coordinates, verify Kerala bounds
3. **Area Input**: Test various acre values for radius calculation
4. **Analysis Display**: Verify nutrient levels and recommendations
5. **Responsive Design**: Test on different screen sizes

## Development Guidelines

### Code Style Patterns
- Use type hints in utility functions for better IDE support
- Malayalam text strings should include Unicode properly
- CSS classes follow BEM-like naming conventions
- Streamlit components prefer `use_container_width=True` for responsiveness

### Adding New Features
- **New Languages**: Add to `LANGUAGES` dict in `language_utils.py`
- **New Utilities**: Follow existing module patterns with comprehensive docstrings
- **UI Components**: Use CSS classes defined in `styles.css`
- **New Pages**: Follow `pages/1_Farm_Profile.py` structure and naming

### Debugging Common Issues
- **CSS Not Loading**: Check file path and use `test_app.py`
- **Language Not Switching**: Verify session state and rerun calls
- **Map Not Rendering**: Check Folium version and tile layer URLs
- **Coordinate Errors**: Validate inputs with `validate_kerala_coordinates()`

## Integration Points

### External Dependencies
- **Background Images**: Unsplash URLs for agricultural themes
- **Map Tiles**: OpenStreetMap, Esri, and Google tile services
- **Fonts**: Google Fonts Inter family for consistent typography

### Future Backend Integration
The mock system in `data_utils.py` is designed to be easily replaced with real API calls to:
- ISRO Bhuvan for satellite data
- ISRIC SoilGrids for soil information
- Local weather stations for environmental data

When integrating real APIs, replace `get_mock_backend_response()` while maintaining the same response structure for backward compatibility.