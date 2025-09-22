import pandas as pd
from sklearn.linear_model import LinearRegression

class MarketResearcher:
    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)
        self.model, self.columns = self._train_price_model()

    def _train_price_model(self):
        # Check if necessary columns exist
        if 'Product' not in self.df.columns or 'Market_Price_per_ton' not in self.df.columns:
            raise ValueError("Expected columns: 'Product', 'Market_Price_per_ton'")

        # Features (X) and Target (y)
        X = self.df[['Product']]
        y = self.df['Market_Price_per_ton']

        # One-hot encode the 'Product' column
        X_encoded = pd.get_dummies(X)

        # Train the model
        model = LinearRegression()
        model.fit(X_encoded, y)

        return model, X_encoded.columns

    def analyze(self, user_input):
        # Ensure 'product' is provided in user input
        crop = user_input.get('crop')
        if not crop:
            return "No crop provided for market analysis."

        # One-hot encode the input product
        input_df = pd.DataFrame({'Product': [crop]})
        input_encoded = pd.get_dummies(input_df)

        # Align columns with trained model
        input_encoded = input_encoded.reindex(columns=self.columns, fill_value=0)

        # Predict the price
        predicted_price = self.model.predict(input_encoded)[0]

        return f"Estimated market price for {crop} is ₹{predicted_price:.2f} per ton."
