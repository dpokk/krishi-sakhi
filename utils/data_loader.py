import pandas as pd
import os
import requests
import streamlit as st

class DataLoader:
    def __init__(self, base_path='dataset_farming'):
        self.base_path = base_path

    def load_farmer_data(self):
        """
        Load and preprocess the farmer advisor dataset.
        """
        path = os.path.join(self.base_path, 'farmer_advisor_dataset.csv')
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} does not exist.")

        df = pd.read_csv(path)
        df.dropna(inplace=True)
        df.columns = df.columns.str.strip().str.lower()
        return df

    def load_market_data(self):
        """
        Load and preprocess the market researcher dataset.
        """
        path = os.path.join(self.base_path, 'market_researcher_dataset.csv')
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} does not exist.")

        df = pd.read_csv(path)
        df.dropna(inplace=True)
        df.columns = df.columns.str.strip().str.lower()
        return df

def get_geolocation():
    if 'user_location' in st.session_state:
        return st.session_state['user_location']
    try:
        resp = requests.get('https://ipinfo.io/json')
        data = resp.json()
        loc = data.get('loc', '0,0').split(',')
        city = data.get('city', '')
        region = data.get('region', '')
        country = data.get('country', '')
        st.session_state['user_location'] = {
            'latitude': float(loc[0]),
            'longitude': float(loc[1]),
            'city': city,
            'region': region,
            'country': country
        }
        return st.session_state['user_location']
    except Exception as e:
        st.session_state['user_location'] = {'latitude': 0, 'longitude': 0, 'city': '', 'region': '', 'country': ''}
        return st.session_state['user_location']
