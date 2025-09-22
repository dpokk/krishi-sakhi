# agri_expert.py

class AgriculturalExpert:
    def __init__(self):
        # You can expand these rules or load from a knowledge base
        self.crop_guidelines = {
            "Wheat": [
                "Use raised bed planting to save water.",
                "Apply compost or green manure for organic health.",
                "Rotate with legumes to restore nitrogen in the soil."
            ],
            "Rice": [
                "Practice SRI (System of Rice Intensification) to boost yield.",
                "Alternate wetting and drying to conserve water.",
                "Avoid burning rice straw—convert it into biochar or mulch."
            ],
            "Maize": [
                "Use contour farming on sloped lands.",
                "Mulch to retain moisture and suppress weeds.",
                "Intercrop with beans to improve soil fertility."
            ]
        }

    def provide_guidance(self, user_input):
        crop = user_input.get("crop", "").capitalize()
        tips = self.crop_guidelines.get(crop, [
            "Adopt integrated pest management (IPM).",
            "Use drip irrigation to save water.",
            "Ensure soil testing every season."
        ])
        return "\n".join(tips)
