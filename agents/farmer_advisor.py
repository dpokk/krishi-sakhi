import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class FarmerAdvisor:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.model = None
        self.label_encoders = {}
        self.data = self._preprocess_data(self._load_data())
        self._train_model()

    def _load_data(self):
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")
        return pd.read_csv(self.dataset_path)

    def _preprocess_data(self, df):
        df = df.dropna()
        df.columns = df.columns.str.strip().str.lower()

        if 'recommended_crop' not in df.columns:
            raise ValueError("Dataset must contain a 'recommended_crop' column.")

        self.label_encoders = {}
        for col in df.select_dtypes(include=['object']).columns:
            if col != 'recommended_crop':
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col])

        self.label_encoders['recommended_crop'] = LabelEncoder()
        df['recommended_crop'] = self.label_encoders['recommended_crop'].fit_transform(df['recommended_crop'])

        return df

    def _train_model(self):
        features = self.data.drop('recommended_crop', axis=1)
        labels = self.data['recommended_crop']
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

    def get_recommendations(self, user_input):
        try:
            encoded_input = self._encode_input(user_input)
            df_input = pd.DataFrame([encoded_input])
            prediction_encoded = self.model.predict(df_input)[0]
            prediction = self.label_encoders['recommended_crop'].inverse_transform([prediction_encoded])[0]
            confidence = round(self.model.predict_proba(df_input)[0].max() * 100, 2)

            return {
                "prediction": prediction,
                "confidence": confidence,
                "input_used": user_input
            }
        except Exception as e:
            return {"error": str(e)}

    def _encode_input(self, input_dict):
        encoded = {}
        for key, value in input_dict.items():
            key = key.strip().lower()
            if key in self.label_encoders:
                encoder = self.label_encoders[key]
                if value in encoder.classes_:
                    encoded[key] = encoder.transform([value])[0]
                else:
                    encoded[key] = 0
            else:
                encoded[key] = value
        return encoded
