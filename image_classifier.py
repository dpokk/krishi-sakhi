import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image
import os
import streamlit as st

class ImageClassifier:
    def __init__(self, device=None):
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        self.class_names = self._load_imagenet_classes()

    def _load_imagenet_classes(self):
        # Try to load PlantDoc class names from a file, else use a hardcoded list
        plantdoc_classes_path = os.path.join(os.path.dirname(__file__), 'dataset_farming', 'plantdoc_classes.txt')
        if os.path.exists(plantdoc_classes_path):
            with open(plantdoc_classes_path, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        # Fallback: minimal PlantDoc class list (add more as needed)
        return [
            "Apple___Apple_scab",
            "Apple___Black_rot",
            "Apple___Cedar_apple_rust",
            "Apple___healthy",
            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
            "Corn_(maize)___Common_rust_",
            "Corn_(maize)___Northern_Leaf_Blight",
            "Corn_(maize)___healthy",
            "Grape___Black_rot",
            "Grape___Esca_(Black_Measles)",
            "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
            "Grape___healthy",
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy",
            "Tomato___Bacterial_spot",
            "Tomato___Early_blight",
            "Tomato___Late_blight",
            "Tomato___Leaf_Mold",
            "Tomato___Septoria_leaf_spot",
            "Tomato___Spider_mites Two-spotted_spider_mite",
            "Tomato___Target_Spot",
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
            "Tomato___Tomato_mosaic_virus",
            "Tomato___healthy"
        ]

    def _get_disease_info(self, class_name):
        # Map PlantDoc class names to readable names and cures
        mapping = {
            "Apple___Apple_scab": ("Apple Scab", "Remove and destroy infected leaves. Apply fungicide as needed."),
            "Apple___Black_rot": ("Apple Black Rot", "Prune infected branches. Use fungicides and proper sanitation."),
            "Apple___Cedar_apple_rust": ("Cedar Apple Rust", "Remove nearby juniper hosts. Apply fungicide early in the season."),
            "Apple___healthy": ("Healthy Apple Leaf", "No disease detected. Maintain good orchard hygiene."),
            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": ("Corn Gray Leaf Spot", "Rotate crops. Use resistant hybrids. Apply fungicide if needed."),
            "Corn_(maize)___Common_rust_": ("Corn Common Rust", "Use resistant varieties. Apply fungicide if severe."),
            "Corn_(maize)___Northern_Leaf_Blight": ("Corn Northern Leaf Blight", "Plant resistant hybrids. Rotate crops. Apply fungicide if needed."),
            "Corn_(maize)___healthy": ("Healthy Corn Leaf", "No disease detected. Maintain good field hygiene."),
            "Grape___Black_rot": ("Grape Black Rot", "Remove mummified fruit. Apply fungicide at bloom."),
            "Grape___Esca_(Black_Measles)": ("Grape Esca (Black Measles)", "Prune infected wood. Remove and destroy affected vines."),
            "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": ("Grape Leaf Blight", "Remove infected leaves. Apply fungicide if needed."),
            "Grape___healthy": ("Healthy Grape Leaf", "No disease detected. Maintain good vineyard hygiene."),
            "Potato___Early_blight": ("Potato Early Blight", "Remove infected leaves. Apply fungicide. Practice crop rotation."),
            "Potato___Late_blight": ("Potato Late Blight", "Destroy infected plants. Apply fungicide. Avoid overhead irrigation."),
            "Potato___healthy": ("Healthy Potato Leaf", "No disease detected. Maintain good field hygiene."),
            "Tomato___Bacterial_spot": ("Tomato Bacterial Spot", "Use disease-free seed. Apply copper-based bactericides."),
            "Tomato___Early_blight": ("Tomato Early Blight", "Remove infected leaves. Apply fungicide. Rotate crops."),
            "Tomato___Late_blight": ("Tomato Late Blight", "Destroy infected plants. Apply fungicide. Avoid overhead irrigation."),
            "Tomato___Leaf_Mold": ("Tomato Leaf Mold", "Increase air circulation. Apply fungicide if needed."),
            "Tomato___Septoria_leaf_spot": ("Tomato Septoria Leaf Spot", "Remove infected leaves. Apply fungicide. Avoid overhead watering."),
            "Tomato___Spider_mites Two-spotted_spider_mite": ("Tomato Spider Mites", "Spray with miticide or insecticidal soap. Increase humidity."),
            "Tomato___Target_Spot": ("Tomato Target Spot", "Remove infected leaves. Apply fungicide if needed."),
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus": ("Tomato Yellow Leaf Curl Virus", "Control whiteflies. Remove infected plants. Use resistant varieties."),
            "Tomato___Tomato_mosaic_virus": ("Tomato Mosaic Virus", "Remove infected plants. Disinfect tools. Use resistant varieties."),
            "Tomato___healthy": ("Healthy Tomato Leaf", "No disease detected. Maintain good field hygiene.")
        }
        return mapping.get(
            class_name,
            (f"Possible plant disease detected ({class_name})",
             "General advice: Remove affected leaves, improve air circulation, avoid overhead watering, and consult a local agricultural expert for precise treatment. Consider using disease-resistant varieties and maintaining good field hygiene.")
        )

    @st.cache_resource
    def load_model(_self):
        model = resnet50(pretrained=True)
        model.eval()
        model.to(_self.device)
        return model

    def predict(self, image: Image.Image):
        if self.model is None:
            self.model = self.load_model()
        image = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            outputs = self.model(image)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, predicted_idx = torch.max(probabilities, 0)
            predicted_class = self.class_names[predicted_idx] if predicted_idx < len(self.class_names) else f"class_{predicted_idx.item()}"
            disease_name, cure = self._get_disease_info(predicted_class)
            return disease_name, confidence.item(), cure
