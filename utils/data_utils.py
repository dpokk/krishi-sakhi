"""
Data utility functions for Krishi Sakhi application.

This module contains functions for:
- Formatting analysis data for display
- Generating mock backend responses
- Color coding for nutrient levels
"""

import random
from typing import Dict, Any, Tuple
import streamlit as st

def format_nutrient_level(level: str, malayalam: str) -> Tuple[str, str]:
    """
    Format nutrient level with appropriate color coding.
    
    Args:
        level (str): Nutrient level (Low, Medium, High)
        malayalam (str): Malayalam translation
        
    Returns:
        Tuple[str, str]: (color, formatted_text)
    """
    color_map = {
        'Low': '#FF4444',      # Red
        'Medium': '#FF8800',   # Orange  
        'High': '#00AA00'      # Green
    }
    
    color = color_map.get(level, '#666666')
    formatted_text = f"{level} | {malayalam}"
    
    return color, formatted_text

def get_mock_backend_response(lat: float, lng: float, acres: float) -> Dict[str, Any]:
    """
    Generate a mock backend response with realistic but varied data.
    
    This simulates what a real backend would return after analyzing
    geospatial data from sources like ISRO Bhuvan and ISRIC SoilGrids.
    
    Args:
        lat (float): Farm latitude
        lng (float): Farm longitude  
        acres (float): Farm area in acres
        
    Returns:
        Dict[str, Any]: Mock analysis data
    """
    
    # Add some randomization to make responses feel more realistic
    random.seed(int((lat + lng + acres) * 1000) % 1000)
    
    # Mock soil texture variations
    soil_textures = [
        {"type": "Sandy Loam", "malayalam": "മണൽ കലർന്ന പശിമരാശി മണ്ണ്"},
        {"type": "Clay Loam", "malayalam": "കളിമൺ കലർന്ന പശിമരാശി മണ്ണ്"},
        {"type": "Loamy Sand", "malayalam": "പശിമരാശി കലർന്ന മണൽമണ്ണ്"},
        {"type": "Silty Clay", "malayalam": "സിൽറ്റി കളിമണ്ണ്"},
    ]
    
    # Mock vegetation states
    vegetation_states = [
        {"ndvi": 0.78, "remark": "Healthy Vegetation", "malayalam": "ആരോഗ്യകരമായ സസ്യങ്ങൾ"},
        {"ndvi": 0.65, "remark": "Moderate Vegetation", "malayalam": "ഇടത്തരം സസ്യാവസ്ഥ"},
        {"ndvi": 0.85, "remark": "Excellent Vegetation", "malayalam": "മികച്ച സസ്യാവസ്ഥ"},
        {"ndvi": 0.55, "remark": "Sparse Vegetation", "malayalam": "കുറഞ്ഞ സസ്യാവസ്ഥ"},
    ]
    
    # Mock groundwater availability  
    groundwater_options = [
        {"depth": 15, "availability": "Good", "malayalam": "നല്ല ലഭ്യത"},
        {"depth": 25, "availability": "Moderate", "malayalam": "ഇടത്തരം ലഭ്യത"},
        {"depth": 8, "availability": "Excellent", "malayalam": "മികച്ച ലഭ്യത"},
        {"depth": 35, "availability": "Limited", "malayalam": "പരിമിതമായ ലഭ്യത"},
    ]
    
    # Select random options based on coordinates
    soil = random.choice(soil_textures)
    vegetation = random.choice(vegetation_states)  
    groundwater = random.choice(groundwater_options)
    
    # Generate nutrient levels with some logic
    nutrient_options = ["Low", "Medium", "High"]
    malayalam_nutrients = {
        "Low": "കുറവ്",
        "Medium": "ഇടത്തരം", 
        "High": "ഉയർന്നത്"
    }
    
    nitrogen = random.choice(nutrient_options)
    phosphorus = random.choice(nutrient_options)
    potassium = random.choice(nutrient_options)
    
    # Generate pH with realistic range
    ph = round(5.5 + random.random() * 2, 1)  # pH between 5.5 and 7.5
    
    # Generate soil composition percentages that add up to 100
    sand = random.randint(30, 70)
    clay = random.randint(10, 40)
    silt = 100 - sand - clay
    if silt < 0:
        silt = random.randint(10, 30)
        sand = 100 - clay - silt
    
    mock_response = {
        "land_cover": {
            "class": "Agricultural Land",
            "malayalam": "കൃഷിഭൂമി"
        },
        "vegetation_index": {
            "ndvi": vegetation["ndvi"],
            "remark": vegetation["remark"],
            "malayalam": vegetation["malayalam"]
        },
        "soil_properties": {
            "texture": soil["type"],
            "malayalam_texture": soil["malayalam"],
            "sand_percent": sand,
            "silt_percent": silt,
            "clay_percent": clay,
            "ph": ph,
            "organic_carbon_percent": round(0.8 + random.random() * 1.0, 1),
            "cec": round(15 + random.random() * 10, 1)
        },
        "nutrient_levels": {
            "nitrogen": nitrogen,
            "phosphorus": phosphorus, 
            "potassium": potassium,
            "malayalam_nitrogen": malayalam_nutrients[nitrogen],
            "malayalam_phosphorus": malayalam_nutrients[phosphorus],
            "malayalam_potassium": malayalam_nutrients[potassium]
        },
        "groundwater": {
            "depth_meters": groundwater["depth"],
            "availability": groundwater["availability"],
            "malayalam_availability": groundwater["malayalam"]
        },
        "analysis_metadata": {
            "farm_coordinates": {"lat": lat, "lng": lng},
            "farm_area_acres": acres,
            "analysis_timestamp": "2024-01-15T10:30:00Z",
            "data_sources": ["ISRO Bhuvan", "ISRIC SoilGrids", "Local Weather Stations"]
        }
    }
    
    return mock_response

def format_analysis_data(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format the mock backend response for display in Streamlit.
    
    Args:
        response (Dict[str, Any]): Raw mock response data
        
    Returns:
        Dict[str, Any]: Formatted data with display-friendly structure
    """
    
    # Format soil composition as a readable string
    soil_props = response["soil_properties"]
    composition_text = f"മണൽ {soil_props['sand_percent']}% | സിൽറ്റ് {soil_props['silt_percent']}% | കളിമണ്ണ് {soil_props['clay_percent']}%"
    
    # Format pH with interpretation
    ph = soil_props["ph"]
    if ph < 6.0:
        ph_interpretation = "അമ്ലത്വം ഉയർന്നത്"  # Acidic
    elif ph > 7.5:
        ph_interpretation = "ക്ഷാരത്വം ഉയർന്നത്"  # Alkaline  
    else:
        ph_interpretation = "ന്യൂട്രലായി"  # Neutral
    
    # Format organic carbon interpretation
    oc = soil_props["organic_carbon_percent"]
    if oc < 0.5:
        oc_interpretation = "കുറവ്"  # Low
    elif oc > 1.5:
        oc_interpretation = "ഉയർന്നത്"  # High
    else:
        oc_interpretation = "ഇടത്തരം"  # Medium
    
    formatted_data = {
        "overview": {
            "soil_type": soil_props["malayalam_texture"],
            "vegetation_status": response["vegetation_index"]["malayalam"],
            "groundwater_status": f"{response['groundwater']['depth_meters']} മീറ്റർ - {response['groundwater']['malayalam_availability']}"
        },
        "nutrients": {
            "nitrogen": {
                "level": response["nutrient_levels"]["nitrogen"],
                "malayalam": response["nutrient_levels"]["malayalam_nitrogen"],
                "color": format_nutrient_level(response["nutrient_levels"]["nitrogen"], 
                                             response["nutrient_levels"]["malayalam_nitrogen"])[0]
            },
            "phosphorus": {
                "level": response["nutrient_levels"]["phosphorus"],
                "malayalam": response["nutrient_levels"]["malayalam_phosphorus"],
                "color": format_nutrient_level(response["nutrient_levels"]["phosphorus"], 
                                             response["nutrient_levels"]["malayalam_phosphorus"])[0]
            },
            "potassium": {
                "level": response["nutrient_levels"]["potassium"],
                "malayalam": response["nutrient_levels"]["malayalam_potassium"],
                "color": format_nutrient_level(response["nutrient_levels"]["potassium"], 
                                             response["nutrient_levels"]["malayalam_potassium"])[0]
            }
        },
        "detailed_soil": {
            "composition": composition_text,
            "ph_value": f"{ph} ({ph_interpretation})",
            "organic_carbon": f"{oc}% ({oc_interpretation})",
            "cec": f"{soil_props['cec']} cmol/kg"
        },
        "vegetation": {
            "ndvi_value": response["vegetation_index"]["ndvi"],
            "health_status": response["vegetation_index"]["malayalam"],
            "interpretation": get_vegetation_interpretation(response["vegetation_index"]["ndvi"])
        }
    }
    
    return formatted_data

def get_vegetation_interpretation(ndvi: float) -> str:
    """
    Get Malayalam interpretation of NDVI values.
    
    Args:
        ndvi (float): NDVI value (0-1)
        
    Returns:
        str: Malayalam interpretation
    """
    if ndvi < 0.3:
        return "സസ്യങ്ങൾ ഇല്ല അല്ലെങ്കിൽ വളരെ കുറവ്"
    elif ndvi < 0.5:
        return "പുൽത്തകിടി അല്ലെങ്കിൽ കുറഞ്ഞ സസ്യങ്ങൾ"
    elif ndvi < 0.7:
        return "ഇടത്തരം സസ്യാവസ്ഥ"
    elif ndvi < 0.8:
        return "നല്ല സസ്യാവസ്ഥ"
    else:
        return "മികച്ച സസ്യാവസ്ഥ - ഇടതൂർന്ന പച്ചപ്പ്"

def generate_recommendations(analysis_data: Dict[str, Any]) -> Dict[str, list]:
    """
    Generate farming recommendations based on analysis data.
    
    Args:
        analysis_data (Dict[str, Any]): Formatted analysis data
        
    Returns:
        Dict[str, list]: Recommendations in different categories
    """
    recommendations = {
        "soil_management": [],
        "nutrient_management": [],
        "water_management": [],
        "crop_suggestions": []
    }
    
    # Generate recommendations based on nutrient levels
    nutrients = analysis_data["nutrients"]
    
    if nutrients["nitrogen"]["level"] == "Low":
        recommendations["nutrient_management"].append({
            "text": "നൈട്രജൻ വളം (യൂറിയ അല്ലെങ്കിൽ അമോണിയം സൾഫേറ്റ്) പ്രയോഗിക്കുക",
            "priority": "high"
        })
    
    if nutrients["phosphorus"]["level"] == "Low":
        recommendations["nutrient_management"].append({
            "text": "ഫോസ്ഫറസ് വളം (സൂപ്പർ ഫോസ്ഫേറ്റ്) ചേർക്കുക",
            "priority": "medium"
        })
    
    if nutrients["potassium"]["level"] == "Low":
        recommendations["nutrient_management"].append({
            "text": "പൊട്ടാഷ് വളം (മ്യൂറിയേറ്റ് ഓഫ് പൊട്ടാഷ്) ഉപയോഗിക്കുക",
            "priority": "medium"
        })
    
    # Add soil management recommendations
    recommendations["soil_management"].extend([
        {"text": "മണ്ണിന്റെ ആരോഗ്യത്തിനായി ജൈവവളം (കമ്പോസ്റ്റ്) ചേർക്കുക", "priority": "high"},
        {"text": "മണ്ണിന്റെ pH നിയന്ത്രിക്കാൻ കുമ്മായം പ്രയോഗിക്കുക", "priority": "medium"}
    ])
    
    return recommendations

def format_nutrient_recommendations(response_data: Dict[str, Any]) -> list:
    """
    Format nutrient recommendations from backend response.
    
    Args:
        response_data (Dict[str, Any]): Backend response data
        
    Returns:
        list: List of recommendation strings
    """
    recommendations = []
    
    # Get nutrient levels
    nutrients = response_data.get('nutrient_levels', {})
    
    if nutrients.get('nitrogen') == 'Low':
        recommendations.append("Apply nitrogen fertilizer (Urea or Ammonium Sulfate) | നൈട്രജൻ വളം പ്രയോഗിക്കുക")
    
    if nutrients.get('phosphorus') == 'Low':
        recommendations.append("Add phosphorus fertilizer (Super Phosphate) | ഫോസ്ഫറസ് വളം ചേർക്കുക")
        
    if nutrients.get('potassium') == 'Low':
        recommendations.append("Use potash fertilizer (Muriate of Potash) | പൊട്ടാഷ് വളം ഉപയോഗിക്കുക")
    
    # Add general recommendations
    recommendations.extend([
        "Apply organic compost for soil health | മണ്ണിന്റെ ആരോഗ്യത്തിനായി ജൈവവളം ചേർക്കുക",
        "Consider soil testing every 6 months | 6 മാസം കൂടുമ്പോൾ മണ്ണ് പരിശോധന നടത്തുക",
        "Maintain proper irrigation schedule | ശരിയായ നീർസേചന ഷെഡ്യൂൾ പാലിക്കുക"
    ])
    
    return recommendations
