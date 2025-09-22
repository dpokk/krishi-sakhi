import os
from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher
from agents.weather_module import WeatherModule
from agents.agri_expert import AgriculturalExpert

from interfaces.user_interface import get_user_inputs, display_recommendations
from memory.memory_manager import MemoryManager

def main():
    print("\n🌾 Welcome to AI-Driven Farming Assistant 🌾\n")

    # Initialize memory
    memory = MemoryManager()

    # Dataset paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    farmer_dataset_path = os.path.join(base_dir, "dataset_farming", "farmer_advisor_dataset.csv")
    market_dataset_path = os.path.join(base_dir, "dataset_farming", "market_researcher_dataset.csv")

    # Instantiate agents
    farmer_advisor = FarmerAdvisor(farmer_dataset_path)
    market_researcher = MarketResearcher(market_dataset_path)
    weather_module = WeatherModule(location="India")
    agri_expert = AgriculturalExpert()

    # Get user input
    soil_data, crop = get_user_inputs()
    user_input = {"soil_data": soil_data, "crop": crop}

    memory.log_interaction("User", str(user_input), "Started analysis")

    # Flatten input for ML models
    flat_input = soil_data.copy()
    flat_input["current_crop"] = crop

    # Get recommendations from agents
    
    land_advice = farmer_advisor.get_recommendations(flat_input)
    market_advice = market_researcher.analyze({"crop": crop})
    weather_report = weather_module.get_real_time_weather()
    sustainability_advice = agri_expert.provide_guidance({"crop": crop, "soil": soil_data})

    # Combine and display results
    final_recommendations = {
        'Soil Advice': land_advice,
        'Market Trends': market_advice,
        'Weather Forecast': weather_report,
        'Sustainability Tips': sustainability_advice
    }

    memory.log_interaction("System", str(user_input), str(final_recommendations))

    display_recommendations(
    land_advice,                     # list from FarmerAdvisor
    [market_advice],                 # wrap market advice string
    sustainability_advice.split("\n")  # split multiline tips into list
)

    

if __name__ == '__main__':
    main()
