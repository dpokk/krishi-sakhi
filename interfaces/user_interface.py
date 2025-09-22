def get_user_inputs():
    print("\n🌾 Welcome to AI-Driven Farming Advisor 🌾")
    print("Please enter the following soil data:\n")

    soil_data = {
        "pH": float(input("Enter soil pH value (e.g. 6.5): ")),
        "N": float(input("Enter Nitrogen level (0-100): ")),
        "P": float(input("Enter Phosphorus level (0-100): ")),
        "K": float(input("Enter Potassium level (0-100): "))
    }

    current_crop = input("\nEnter the current crop (Wheat, Rice, Maize): ").strip().capitalize()

    return soil_data, current_crop


def display_recommendations(soil_recs, rotation_recs, sustainable_practices):
    print("\n🧾 Soil Recommendations:")
    for rec in soil_recs:
        print(" -", rec)

    print("\n🔄 Crop Rotation Suggestions:")
    for crop in rotation_recs:
        print(" -", crop)

    print("\n🌱 Sustainable Practices:")
    for practice in sustainable_practices:
        print(" -", practice)
