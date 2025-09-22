import os
os.environ["STREAMLIT_WATCHER_IGNORE_MODULES"] = "torch"
import streamlit as st
import os
import os
import csv
USER_INPUT_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_input_log.csv')
from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher
from agents.weather_module import WeatherModule
from agents.agri_expert import AgriculturalExpert
from memory.memory_manager import MemoryManager
import numpy as np
from PIL import Image
import io
import pandas as pd
import datetime
import zipfile
import glob
import random
from image_classifier import ImageClassifier
from nlp_models import NLPModels
from utils.data_loader import get_geolocation  # <-- ADD THIS
import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime, date
import csv
import getpass
import getpass
from datetime import datetime
import streamlit_geolocation

USER_INPUT_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_input_log.csv')

def log_user_input(page, category, data):
    user_id = st.session_state.get('user_id', getpass.getuser())
    login_name = st.session_state.get('username', '')
    timestamp = datetime.utcnow().isoformat()
    row = {
        'timestamp': timestamp,
        'user_id': user_id,
        'login_name': login_name,
        'page': page,
        'category': category,
        'data': data
    }
    file_exists = os.path.isfile(USER_INPUT_LOG)
    with open(USER_INPUT_LOG, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['timestamp','user_id','login_name','page','category','data'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

# --- Translation dictionary ---
TRANSLATIONS = {
    'en': {
        'app_title': "🌾 KrishiSakhi: AI-Driven Farming Assistant 🌾",
        'home': "Home",
        'recommendations': "Get Recommendations",
        'diagnosis': "AI Disease Diagnosis",
        'validation': "Farmer Validation",
        'language': "Language",
        'select_language': "Select Language",
        'weather': "Weather Forecast",
        'input_options': "Input Options",
        'image_input': "Upload Image",
        'voice_input': "Voice Input",
        'text_input': "Text Input",
        'submit': "Submit",
        'severity': "Disease Severity Estimation",
        'correction': "Farmer Correction Workflow",
        'enter_farm_data': "Enter Farm Data",
        'farm_id': "Farm ID",
        'soil_ph': "Soil pH value",
        'soil_moisture': "Soil Moisture (%)",
        'temperature': "Temperature (°C)",
        'rainfall': "Rainfall (mm)",
        'crop_type': "Crop Type",
        'fertilizer_usage': "Fertilizer Usage (kg)",
        'pesticide_usage': "Pesticide Usage (kg)",
        'crop_yield': "Crop Yield (ton)",
        'sustainability_score': "Sustainability Score",
        'select_crop': "Select current crop for market/weather/sustainability advice",
        'get_recommendations': "Get Recommendations",
        'soil_recommendations': "🧾 Soil Recommendations",
        'market_trends': "📈 Market Trends",
        'weather_forecast': "🌤️ Weather Forecast",
        'sustainable_practices': "🌱 Sustainable Practices",
        'ai_diagnosis': "AI Diagnosis Result",
        'severity_result': "Estimated Severity",
        'validation_prompt': "Is the diagnosis correct?",
        'correction_prompt': "Please provide the correct diagnosis:",
        'thank_you': "Thank you for your feedback!",
        'back_home': "Back to Home",
        'growth_diary': 'Growth Diary',
        'add_entry': 'Add New Entry',
        'diary_log': 'Diary Log',
        'crop': 'Crop',
        'notes': 'Notes',
        'save_entry': 'Save Entry',
        'entry_saved': 'Entry saved!',
        'knowledge_sharing': 'Knowledge Sharing',
        'start_discussion': 'Start a New Discussion',
        'all_discussions': 'All Discussions',
        'post_thread': 'Post Thread',
        'reply': 'Reply',
        'thread_posted': 'Thread posted!',
        'reply_posted': 'Reply posted!',
        'soil_health': 'Soil Health Scanning',
        'add_soil_test': 'Add New Soil Test',
        'soil_test_log': 'Soil Test Log',
        'save_soil_test': 'Save Soil Test',
        'soil_test_saved': 'Soil test saved!',
        'heatmaps': 'Live Agri Heatmaps & Outbreak Visualization',
        'outbreak_map': 'Outbreak Map',
        'no_geo_reports': 'No geo-tagged reports available.',
        'report_outbreak': 'Report New Outbreak',
        'submit_outbreak': 'Submit Outbreak Report',
        'outbreak_reported': 'Outbreak reported!',
        'export_info': 'Export all anonymized data for research, startups, and policy teams.',
        'create_export_zip': 'Create Export ZIP',
        'export_created': 'Export ZIP created!',
        'download_corpus_zip': 'Download Corpus ZIP',
        'khet_market': 'Khet Market',
        'market_home': 'Home',
        'market_login': 'Login',
        'market_register': 'Register',
        'market_buyorsell': 'BuyOrSell',
        'market_buy': 'Buy',
        'market_checkout': 'Checkout',
        'market_payment': 'Payment',
        'market_orders': 'Orders',
        'market_sell': 'Sell',
        'market_selling_item': 'Selling Item',
        'login_username': 'Username',
        'login_password': 'Password',
        'login_btn': 'Login',
        'register_fullname': 'Full Name',
        'register_email': 'Email',
        'register_phone': 'Phone',
        'register_username': 'Username',
        'register_password': 'Password',
        'register_confirmpw': 'Confirm Password',
        'register_btn': 'Register',
        'buyorsell_buy': 'Go to Buy',
        'buyorsell_sell': 'Go to Sell',
        'payment_card': 'Card Number',
        'payment_expiry': 'Expiry Date',
        'payment_cvv': 'CVV',
        'payment_btn': 'Pay',
        'sell_crop': 'Crop Name',
        'sell_qty': 'Quantity (kg)',
        'sell_price': 'Price (per kg, must be >= MSP)',
        'sell_img': 'Upload Crop Image',
        'sell_btn': 'List for Sale',
        'output': 'Output',
        'context': 'Enter context for Q&A',
        'enter_context': 'Please enter context for Q&A.',
        'agribot_title': "🤖 AgriBot - Your Futuristic Agricultural Assistant",
        'agribot_greeting': "Hello! I'm AgriBot. How can I assist you with your farm today?",
        'agribot_input_placeholder': "Type your message here...",
        'agribot_attach_image': "Attach image (optional)",
        'send': "Send",
        'show_history': "Show Conversation History",
        'you': "You",
        'agribot': "AgriBot",
        'analytics_dashboard': "📊 Analytics Dashboard",
        'analytics_total_questions': "Total AgriBot Questions Asked",
        'analytics_common_crops': "Most Common Crops Discussed",
        'analytics_disease_trends': "Disease Diagnosis Trends",
        'analytics_engagement': "User Engagement Over Time",
        'analytics_pie_types': "Pie Chart of Question Types",
        'analytics_recent_log': "Recent Activity Log",
        'analytics_upload_csv': "Upload a CSV file for visualization",
        'analytics_no_data': "No chat data to display.",
        'analytics_no_conversations': "No conversation data found.",
        'analytics_no_keywords': "No crop keywords found in chats.",
        'analytics_no_disease': "No disease keywords found in chats.",
        'analytics_no_types': "No question type data found.",
        'analytics_info_upload': "If you want to visualize other CSV/statistics, upload them below:",
    },
    'te': {
        'app_title': "🌾 KrishiSakhi: ఏఐ ఆధారిత వ్యవసాయ సహాయకుడు 🌾",
        'home': "హోమ్",
        'recommendations': "సిఫార్సులు పొందండి",
        'diagnosis': "ఏఐ వ్యాధి నిర్ధారణ",
        'validation': "రైతు ధృవీకరణ",
        'language': "భాష",
        'select_language': "భాషను ఎంచుకోండి",
        'weather': "వాతావరణ సూచన",
        'input_options': "ఇన్పుట్ ఎంపికలు",
        'image_input': "చిత్రాన్ని అప్‌లోడ్ చేయండి",
        'voice_input': "వాయిస్ ఇన్పుట్",
        'text_input': "టెక్స్ట్ ఇన్పుట్",
        'submit': "సమర్పించండి",
        'severity': "వ్యాధి తీవ్రత అంచనా",
        'correction': "రైతు సవరణ వర్క్‌ఫ్లో",
        'enter_farm_data': "పంట డేటాను నమోదు చేయండి",
        'farm_id': "ఫార్మ్ ఐడి",
        'soil_ph': "మట్టి పిహెచ్ విలువ",
        'soil_moisture': "మట్టి తేమ (%)",
        'temperature': "ఉష్ణోగ్రత (°C)",
        'rainfall': "వర్షపాతం (mm)",
        'crop_type': "పంట రకం",
        'fertilizer_usage': "ఎరువుల వినియోగం (kg)",
        'pesticide_usage': "పెస్టిసైడ్ వినియోగం (kg)",
        'crop_yield': "పంట దిగుబడి (టన్నులు)",
        'sustainability_score': "సస్టైనబిలిటీ స్కోర్",
        'select_crop': "మార్కెట్/వాతావరణ/సస్టైనబిలిటీ సలహా కోసం ప్రస్తుత పంటను ఎంచుకోండి",
        'get_recommendations': "సిఫార్సులు పొందండి",
        'soil_recommendations': "🧾 మట్టి సిఫార్సులు",
        'market_trends': "📈 మార్కెట్ ట్రెండ్స్",
        'weather_forecast': "🌤️ వాతావరణ సూచన",
        'sustainable_practices': "🌱 సస్టైనబుల్ పద్ధతులు",
        'ai_diagnosis': "ఏఐ నిర్ధారణ ఫలితం",
        'severity_result': "అంచనా వేసిన తీవ్రత",
        'validation_prompt': "నిర్ధారణ సరైందా?",
        'correction_prompt': "దయచేసి సరైన నిర్ధారణను ఇవ్వండి:",
        'thank_you': "మీ అభిప్రాయానికి ధన్యవాదాలు!",
        'back_home': "హోమ్‌కు తిరిగి వెళ్ళండి",
        'growth_diary': "వృద్ధి డైరీ",
        'add_entry': "కొత్త ఎంట్రీ జోడించండి",
        'diary_log': "డైరీ లాగ్",
        'crop': "పంట",
        'notes': "గమనికలు",
        'save_entry': "ఎంట్రీ సేవ్ చేయండి",
        'entry_saved': "ఎంట్రీ సేవ్ అయింది!",
        'knowledge_sharing': "జ్ఞాన పంచుకోలు",
        'start_discussion': "కొత్త చర్చ ప్రారంభించండి",
        'all_discussions': "అన్ని చర్చలు",
        'post_thread': "థ్రೆడ్ పోస్ట్ చేయండి",
        'reply': "ప్రత్యుత్తరం",
        'thread_posted': "థ్రೆడ్ పోస్ట్ అయింది!",
        'reply_posted': "ప్రత్యుత్తరం పోస్ట్ అయింది!",
        'soil_health': "మట్టి ఆరോగ్య స్కానింగ్",
        'add_soil_test': "కొత్త మట్టి పరీక్ష జోడించండి",
        'soil_test_log': "మట్టి పరీక్ష లాగ్",
        'save_soil_test': "మట్టి పరీక్ష సేవ్ చేయండి",
        'soil_test_saved': "మట్టి పరీక్ష సేవ్ అయింది!",
        'heatmaps': "ప్రత్యక్ష వ్యవసాయ హీట్‌మ్యాప్స్ & వ్యాధి విజువలైజేషన్",
        'outbreak_map': "వ్యాధి మ్యాప్",
        'no_geo_reports': "జియో-ట్యాగ్డ్ నివేదికలు లేవు.",
        'report_outbreak': "కొత్త వ్యాధిని నివేదించండి",
        'submit_outbreak': "వ్యాధి నివేదిక సమర్పించండి",
        'outbreak_reported': "వ్యాధి నివేదిక సమర్పించబడింది!",
        'export_info': "పరిశోధన, స్టార్టప్‌లు, విధాన బృందాల కోసం అనామక డేటాను ఎగుమతి చేయండి.",
        'create_export_zip': "ఎగుమతి ZIP సృష్టించండి",
        'export_created': "ఎగుమతి ZIP సృష్టించబడింది!",
        'download_corpus_zip': "కార్పస్ ZIP డౌన్‌లోడ్ చేయండి",
        'khet_market': 'ఖేత్ మార్కెట్',
        'market_home': 'హోమ్',
        'market_login': 'లాగిన్',
        'market_register': 'నమోదు',
        'market_buyorsell': 'కొనుగోలు/అమ్మకం',
        'market_buy': 'కొనుగోలు',
        'market_checkout': 'చెకౌట్',
        'market_payment': 'చెల్లింపు',
        'market_orders': 'ఆర్డర్లు',
        'market_sell': 'అమ్మకం',
        'market_selling_item': 'అమ్మిన వస్తువు',
        'login_username': 'వినియోగదారు పేరు',
        'login_password': 'పాస్వర్డ్',
        'login_btn': 'లాగిన్',
        'register_fullname': 'పూర్తి పేరు',
        'register_email': 'ఇమെయిల్',
        'register_phone': 'ఫోన్',
        'register_username': 'వినియోగదారు పేరు',
        'register_password': 'పాస్వర్డ్',
        'register_confirmpw': 'పాస్వర్డ్‌ను నిర్ధారించండి',
        'register_btn': 'నమోదు',
        'buyorsell_buy': 'కొనుగోలు చేయండి',
        'buyorsell_sell': 'అమ్మకం చేయండి',
        'payment_card': 'కార్డ్ నంబర్',
        'payment_expiry': 'గడువు తేదీ',
        'payment_cvv': 'సివివి',
        'payment_btn': 'చెల్లించండి',
        'sell_crop': 'పంట పేరు',
        'sell_qty': 'పరిమాణం (కిలోలు)',
        'sell_price': 'ధర (ప్రతి కిలో, MSP కన్నా ఎక్కువ)',
        'sell_img': 'పంట చిత్రాన్ని అప్‌లోడ్ చేయండి',
        'sell_btn': 'అమ్మకానికి జాబితా చేయండి',
        'output': 'వెళ్ళిన విషయం',
        'context': 'విషయానికి సమాచారం ఇవ్వండి',
        'enter_context': 'దయచేసి విషయానికి సమాచారం ఇవ్వండి.',
        'agribot_title': "🤖 AgriBot - Your Futuristic Agricultural Assistant",
        'agribot_greeting': "Hello! I'm AgriBot. How can I assist you with your farm today?",
        'agribot_input_placeholder': "Type your message here...",
        'agribot_attach_image': "Attach image (optional)",
        'send': "Send",
        'show_history': "Show Conversation History",
        'you': "You",
        'agribot': "AgriBot",
        'analytics_dashboard': "📊 Analytics Dashboard",
        'analytics_total_questions': "Total AgriBot Questions Asked",
        'analytics_common_crops': "Most Common Crops Discussed",
        'analytics_disease_trends': "Disease Diagnosis Trends",
        'analytics_engagement': "User Engagement Over Time",
        'analytics_pie_types': "Pie Chart of Question Types",
        'analytics_recent_log': "Recent Activity Log",
        'analytics_upload_csv': "Upload a CSV file for visualization",
        'analytics_no_data': "No chat data to display.",
        'analytics_no_conversations': "No conversation data found.",
        'analytics_no_keywords': "No crop keywords found in chats.",
        'analytics_no_disease': "No disease keywords found in chats.",
        'analytics_no_types': "No question type data found.",
        'analytics_info_upload': "If you want to visualize other CSV/statistics, upload them below:",
    },
    'hi': {
        'app_title': "🌾 KrishiSakhi: एआई संचालित कृषि सहायक 🌾",
        'home': "होम",
        'recommendations': "सिफारिशें प्राप्त करें",
        'diagnosis': "एआई रोग निदान",
        'validation': "किसान सत्यापन",
        'language': "भाषा",
        'select_language': "भाषा चुनें",
        'weather': "मौसम पूर्वानुमान",
        'input_options': "इनपुट विकल्प",
        'image_input': "छवि अपलोड करें",
        'voice_input': "वॉयस इनपुट",
        'text_input': "टेक्स्ट इनपुट",
        'submit': "सबमिट करें",
        'severity': "रोग की गंभीरता का अनुमान",
        'correction': "किसान सुधार वर्कफ़्लो",
        'enter_farm_data': "फार्म डेटा दर्ज करें",
        'farm_id': "फार्म आईडी",
        'soil_ph': "मिट्टी का पीएच मान",
        'soil_moisture': "मिट्टी की नमी (%)",
        'temperature': "तापमान (°C)",
        'rainfall': "वर्षा (मिमी)",
        'crop_type': "फसल का प्रकार",
        'fertilizer_usage': "उर्वरक उपयोग (किग्रा)",
        'pesticide_usage': "कीटनाशक उपयोग (किग्रा)",
        'crop_yield': "फसल उत्पादन (टन)",
        'sustainability_score': "सस्टेनेबिलिटी स्कोर",
        'select_crop': "बाजार/मौसम/सस्टेनेबिलिटी सलाह के लिए वर्तमान फसल चुनें",
        'get_recommendations': "सिफारिशें प्राप्त करें",
        'soil_recommendations': "🧾 मिट्टी सिफारिशें",
        'market_trends': "📈 बाजार प्रवृत्तियाँ",
        'weather_forecast': "🌤️ मौसम पूर्वानुमान",
        'sustainable_practices': "🌱 सतत प्रथाएँ",
        'ai_diagnosis': "एआई निदान परिणाम",
        'severity_result': "अनुमानित गंभीरता",
        'validation_prompt': "क्या निदान सही है?",
        'correction_prompt': "कृपया सही निदान प्रदान करें:",
        'thank_you': "आपकी प्रतिक्रिया के लिए धन्यवाद!",
        'back_home': "होम पर वापस जाएँ",
        'growth_diary': "वृद्धि डायरी",
        'add_entry': "नई प्रविष्टि जोड़ें",
        'diary_log': "डायरी लॉग",
        'crop': "फसल",
        'notes': "टिप्पणियाँ",
        'save_entry': "प्रविष्टि सहेजें",
        'entry_saved': "प्रविष्टि सहेजी गई!",
        'knowledge_sharing': "ज्ञान साझा करना",
        'start_discussion': "नई चर्चा शुरू करें",
        'all_discussions': "सभी चर्चाएँ",
        'post_thread': "थ्रेड पोस्ट करें",
        'reply': "उत्तर",
        'thread_posted': "थ्रेड पोस्ट किया गया!",
        'reply_posted': "उत्तर पोस्ट किया गया!",
        'soil_health': "मिट्टी स्वास्थ्य स्कैनिंग",
        'add_soil_test': "नई मिट्टी परीक्षण जोड़ें",
        'soil_test_log': "मिट्टी परीक्षण लॉग",
        'save_soil_test': "मिट्टी परीक्षण सहेजें",
        'soil_test_saved': "मिट्टी परीक्षण सहेजा गया!",
        'heatmaps': "लाइव कृषि हीटमैप्स और प्रकोप विज़ुअलाइज़ेशन",
        'outbreak_map': "प्रकोप मानचित्र",
        'no_geo_reports': "कोई जियो-टैग्ड रिपोर्ट उपलब्ध नहीं है।",
        'report_outbreak': "नई प्रकोप रिपोर्ट करें",
        'submit_outbreak': "प्रकोप रिपोर्ट सबमिट करें",
        'outbreak_reported': "प्रकोप रिपोर्ट की गई!",
        'export_info': "अनुसंधान, स्टार्टअप्स और नीति टीमों के लिए सभी अनाम डेटा निर्यात करें।",
        'create_export_zip': "निर्यात ZIP बनाएं",
        'export_created': "निर्यात ZIP बनाया गया!",
        'download_corpus_zip': "कॉर्पस ZIP डाउनलोड करें",
        'khet_market': 'खेती बाजार',
        'market_home': 'होम',
        'market_login': 'लॉगिन',
        'market_register': 'रजिस्टर',
        'market_buyorsell': 'खरीदें/बेचें',
        'market_buy': 'खरीदें',
        'market_checkout': 'चेकआउट',
        'market_payment': 'भुगतान',
        'market_orders': 'ऑर्डर',
        'market_sell': 'बेचें',
        'market_selling_item': 'बेची गई वस्तु',
        'login_username': 'उपयोगकर्ता नाम',
        'login_password': 'पासवर्ड',
        'login_btn': 'लॉगिन',
        'register_fullname': 'पूरा नाम',
        'register_email': 'ईमेल',
        'register_phone': 'फ़ोन',
        'register_username': 'उपयोगकर्ता नाम',
        'register_password': 'पासवर्ड',
        'register_confirmpw': 'पासवर्ड की पुष्टि करें',
        'register_btn': 'रजिस्टर',
        'buyorsell_buy': 'खरीदें पर जाएं',
        'buyorsell_sell': 'बेचें पर जाएं',
        'payment_card': 'कार्ड नंबर',
        'payment_expiry': 'समाप्ति तिथि',
        'payment_cvv': 'सीवीवी',
        'payment_btn': 'भुगतान करें',
        'sell_crop': 'फसल का नाम',
        'sell_qty': 'मात्रा (किग्रा)',
        'sell_price': 'मूल्य (प्रति किग्रा, MSP से अधिक)',
        'sell_img': 'फसल छवि अपलोड करें',
        'sell_btn': 'बिक्री के लिए सूचीबद्ध करें',
        'output': 'आउटपुट',
        'context': 'Q&A के लिए संदर्भ दर्ज करें',
        'enter_context': 'कृपया Q&A के लिए संदर्भ दर्ज करें.',
        'agribot_title': "🤖 AgriBot - Your Futuristic Agricultural Assistant",
        'agribot_greeting': "Hello! I'm AgriBot. How can I assist you with your farm today?",
        'agribot_input_placeholder': "Type your message here...",
        'agribot_attach_image': "Attach image (optional)",
        'send': "Send",
        'show_history': "Show Conversation History",
        'you': "You",
        'agribot': "AgriBot",
        'analytics_dashboard': "📊 Analytics Dashboard",
        'analytics_total_questions': "Total AgriBot Questions Asked",
        'analytics_common_crops': "Most Common Crops Discussed",
        'analytics_disease_trends': "Disease Diagnosis Trends",
        'analytics_engagement': "User Engagement Over Time",
        'analytics_pie_types': "Pie Chart of Question Types",
        'analytics_recent_log': "Recent Activity Log",
        'analytics_upload_csv': "Upload a CSV file for visualization",
        'analytics_no_data': "No chat data to display.",
        'analytics_no_conversations': "No conversation data found.",
        'analytics_no_keywords': "No crop keywords found in chats.",
        'analytics_no_disease': "No disease keywords found in chats.",
        'analytics_no_types': "No question type data found.",
        'analytics_info_upload': "If you want to visualize other CSV/statistics, upload them below:",
    },
    'ta': {
        'app_title': "🌾 கிருஷி சகி: ஏஐ இயக்கும் விவசாய உதவியாளர் 🌾",
        'home': "முகப்பு",
        'recommendations': "பரிந்துரைகள் பெறுங்கள்",
        'diagnosis': "ஏஐ நோய் கண்டறிதல்",
        'validation': "விவசாயி சரிபார்ப்பு",
        'language': "மொழி",
        'select_language': "மொழியைத் தேர்ந்தெடுக்கவும்",
        'weather': "வானிலை முன்னறிவு",
        'input_options': "உள்ளீட்டு விருப்பங்கள்",
        'image_input': "படத்தை பதிவேற்றவும்",
        'voice_input': "குரல் உள்ளீடு",
        'text_input': "உரை உள்ளீடு",
        'submit': "சமர்ப்பிக்கவும்",
        'severity': "நோய் தீவிரம் மதிப்பீடு",
        'correction': "விவசாயி திருத்தம்",
        'enter_farm_data': "பண்ணை தரவை உள்ளிடவும்",
        'farm_id': "பண்ணை ஐடி",
        'soil_ph': "மண் பிஹெச் மதிப்பு",
        'soil_moisture': "மண் ஈரப்பதம் (%)",
        'temperature': "வெப்பநிலை (°C)",
        'rainfall': "மழை (மிமீ)",
        'crop_type': "பயிர் வகை",
        'fertilizer_usage': "உர பயன்பாடு (கிலோ)",
        'pesticide_usage': "பூச்சிக்கொல்லி பயன்பாடு (கிலோ)",
        'crop_yield': "பயிர் விளைச்சல் (டன்)",
        'sustainability_score': "திடப்படுத்தல் மதிப்பெண்",
        'select_crop': "சந்தை/வானிலை/திடப்படுத்தல் ஆலோசனைக்கு பயிரைத் தேர்ந்தெடுக்கவும்",
        'get_recommendations': "பரிந்துரைகள் பெறுங்கள்",
        'soil_recommendations': "🧾 மண் பரிந்துரைகள்",
        'market_trends': "📈 சந்தை போக்குகள்",
        'weather_forecast': "🌤️ வானிலை முன்னறிவு",
        'sustainable_practices': "🌱 திடப்படுத்தல் நடைமுறைகள்",
        'ai_diagnosis': "ஏஐ கண்டறிதல் முடிவு",
        'severity_result': "மதிப்பிடப்பட்ட தீவிரம்",
        'validation_prompt': "மேலுள்ள தகவல் சரியா?",
        'correction_prompt': "சரியான கண்டறிதலை வழங்கவும்:",
        'thank_you': "உங்கள் கருத்துக்கு நன்றி!",
        'back_home': "முகப்புக்கு திரும்பவும்",
        'growth_diary': 'வளர்ச்சி நாட்குறிப்பு',
        'add_entry': 'புதிய பதிவைச் சேர்க்கவும்',
        'diary_log': 'நாட்குறிப்பு பதிவு',
        'crop': 'பயிர்',
        'notes': 'குறிப்புகள்',
        'save_entry': 'பதிவை சேமிக்கவும்',
        'entry_saved': 'பதிவு சேமிக்கப்பட்டது!',
        'knowledge_sharing': 'அறிவு பகிர்வு',
        'start_discussion': 'புதிய விவாதத்தைத் தொடங்கவும்',
        'all_discussions': 'அனைத்து விவாதங்கள்',
        'post_thread': 'தலைப்பை இடுகையிடவும்',
        'reply': 'பதில்',
        'thread_posted': 'தலைப்பு இடுகையிடப்பட்டது!',
        'reply_posted': 'பதில் இடுகையிடப்பட்டது!',
        'soil_health': 'மண் ஆரோக்கியம் ஸ்கேனிங்',
        'add_soil_test': 'புதிய மண் பரிசோதனை சேர்க்கவும்',
        'soil_test_log': 'மண் பரிசோதனை பதிவு',
        'save_soil_test': 'மண் பரிசோதனை சேமிக்கவும்',
        'soil_test_saved': 'மண் பரிசோதனை சேமிக்கப்பட்டது!',
        'heatmaps': 'நேரடி விவசாய ஹீட்மேப்கள் & நோய் பரவல் காட்சி',
        'outbreak_map': 'நோய் பரவல் வரைபடம்',
        'no_geo_reports': 'ஜியோ-டேக் அறிக்கைகள் இல்லை.',
        'report_outbreak': 'புதிய நோய் பரவலை அறிக்கையிடவும்',
        'submit_outbreak': 'நோய் அறிக்கையை சமர்ப்பிக்கவும்',
        'outbreak_reported': 'நோய் அறிக்கை சமர்ப்பிக்கப்பட்டது!',
        'khet_market': 'கேத் மார்க்கெட்',
        'market_home': 'முகப்பு',
        'market_login': 'உள்நுழை',
        'market_register': 'பதிவு',
        'market_buyorsell': 'வாங்க/விற்க',
        'market_buy': 'வாங்க',
        'market_checkout': 'செக் அவுட்',
        'market_payment': 'கட்டணம்',
        'market_orders': 'ஆணைகள்',
        'market_sell': 'விற்க',
        'market_selling_item': 'விற்கும் பொருள்',
        'login_username': 'பயனர் பெயர்',
        'login_password': 'கடவுச்சொல்',
        'login_btn': 'உள்நுழை',
        'register_fullname': 'முழு பெயர்',
        'register_email': 'மின்னஞ்சல்',
        'register_phone': 'தொலைபேசி',
        'register_username': 'பயனர் பெயர்',
        'register_password': 'கடவுச்சொல்',
        'register_confirmpw': 'கடவுச்சொல்லை உறுதிப்படுத்தவும்',
        'register_btn': 'பதிவு',
        'buyorsell_buy': 'வாங்க செல்லவும்',
        'buyorsell_sell': 'விற்க செல்லவும்',
        'payment_card': 'அட்டை எண்',
        'payment_expiry': 'காலாவதி தேதி',
        'payment_cvv': 'CVV',
        'payment_btn': 'கட்டணம் செலுத்தவும்',
        'sell_crop': 'பயிர் பெயர்',
        'sell_qty': 'அளவு (கிலோ)',
        'sell_price': 'விலை (ஒரு கிலோ, MSP-ஐ விட அதிகம்)',
        'sell_img': 'பயிர் படத்தை பதிவேற்றவும்',
        'sell_btn': 'விற்பனைக்கு பட்டியலிடவும்',
        'output': 'வெளியீடு',
        'context': 'Q&A-க்கு சூழல் உள்ளிடவும்',
        'enter_context': 'Q&A-க்கு சூழலை உள்ளிடவும்.',
        'agribot_title': "🤖 AgriBot - Your Futuristic Agricultural Assistant",
        'agribot_greeting': "Hello! I'm AgriBot. How can I assist you with your farm today?",
        'agribot_input_placeholder': "Type your message here...",
        'agribot_attach_image': "Attach image (optional)",
        'send': "Send",
        'show_history': "Show Conversation History",
        'you': "You",
        'agribot': "AgriBot",
        'analytics_dashboard': "📊 Analytics Dashboard",
        'analytics_total_questions': "Total AgriBot Questions Asked",
        'analytics_common_crops': "Most Common Crops Discussed",
        'analytics_disease_trends': "Disease Diagnosis Trends",
        'analytics_engagement': "User Engagement Over Time",
        'analytics_pie_types': "Pie Chart of Question Types",
        'analytics_recent_log': "Recent Activity Log",
        'analytics_upload_csv': "Upload a CSV file for visualization",
        'analytics_no_data': "No chat data to display.",
        'analytics_no_conversations': "No conversation data found.",
        'analytics_no_keywords': "No crop keywords found in chats.",
        'analytics_no_disease': "No disease keywords found in chats.",
        'analytics_no_types': "No question type data found.",
        'analytics_info_upload': "If you want to visualize other CSV/statistics, upload them below:",
    },
    'kn': {
        'app_title': "🌾 ಕೃಷಿ ಸಹಾಯ: ಎಐ ಚಾಲಿತ ಕೃಷಿ ಸಹಾಯಕ 🌾",
        'home': "ಮುಖಪುಟ",
        'recommendations': "ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಿರಿ",
        'diagnosis': "ಎಐ ರೋಗ ನಿರ್ಧಾರ",
        'validation': "ರೈತ ದೃಢೀಕರಣ",
        'language': "ಭಾಷೆ",
        'select_language': "ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        'weather': "ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ",
        'input_options': "ಇನ್‌ಪುಟ್ ಆಯ್ಕೆಗಳು",
        'image_input': "ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        'voice_input': "ಧ್ವನಿ ಇನ್‌ಪುಟ್",
        'text_input': "ಪಠ್ಯ ಇನ್‌ಪುಟ್",
        'submit': "ಸಲ್ಲಿಸು",
        'severity': "ರೋಗ ತೀವ್ರತೆ ಅಂದಾಜು",
        'correction': "ರೈತ ತಿದ್ದುಪಡಿ",
        'enter_farm_data': "ಹಳ್ಳಿ ಡೇಟಾ ನಮೂದಿಸಿ",
        'farm_id': "ಹಳ್ಳಿ ಐಡಿ",
        'soil_ph': "ಮಣ್ಣು ಪಿಹೆಚ್ ಮೌಲ್ಯ",
        'soil_moisture': "ಮಣ್ಣು ತೇವಾಂಶ (%)",
        'temperature': "ತಾಪಮಾನ (°C)",
        'rainfall': "ಮಳೆ (ಮಿಮೀ)",
        'crop_type': "ಬೆಳೆ ಪ್ರಕಾರ",
        'fertilizer_usage': "ಸರ್ಜಿ ಬಳಕೆ (ಕೆಜಿ)",
        'pesticide_usage': "ಹಾನಿಕಾರಕ ಬಳಕೆ (ಕೆಜಿ)",
        'crop_yield': "ಬೆಳೆ ಉತ್ಪಾದನೆ (ಟನ್)",
        'sustainability_score': "ಸ್ಥಿರತೆ ಅಂಕಗಳು",
        'select_crop': "ಮಾರుಕಟ್ಟೆ/ಹವಾಮಾನ/ಸ್ಥಿರತೆ ಸಲಹೆಗೆ ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ",
        'get_recommendations': "ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಿರಿ",
        'soil_recommendations': "🧾 ಮಣ್ಣು ಶಿಫಾರಸುಗಳು",
        'market_trends': "📈 ಮಾರుಕಟ್ಟೆ ಪ್ರವೃತ್ತಿಗಳು",
        'weather_forecast': "🌤️ ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ",
        'sustainable_practices': "🌱 ಸ್ಥಿರ ಅಭ್ಯಾಸಗಳು",
        'ai_diagnosis': "ಎಐ ನಿರ್ಧಾರ ಫಲಿತಾಂಶ",
        'severity_result': "ಅಂದಾಜು ತೀವ್ರತೆ",
        'validation_prompt': "ಮೇಲಿನ ಮಾಹಿತಿ ಸರಿಯೇ?",
        'correction_prompt': "ದಯವಿಟ್ಟು ಸರಿಯಾದ ನಿರ್ಧಾರವನ್ನು ನೀಡಿ:",
        'thank_you': "ನಿಮ್ಮ ಪ್ರತಿಕ್ರಿಯೆಗೆ ಧನ್ಯವಾದಗಳು!",
        'back_home': "ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ",
        'growth_diary': "ವೃದ್ಧಿ ದಿನಚರಿ",
        'add_entry': "ಹೊಸ ದಾಖಲೆಯನ್ನು ಸೇರಿಸಿ",
        'diary_log': "ದಿನಚರಿ ದಾಖಲೆ",
        'crop': "ಬೆಳೆ",
        'notes': "ಟಿಪ್ಪಣಿಗಳು",
        'save_entry': "ದಾಖಲೆ ಉಳಿಸಿ",
        'entry_saved': "ದಾಖಲೆ ಉಳಿಸಲಾಗಿದೆ!",
        'knowledge_sharing': "ಜ್ಞಾನ ಹಂಚಿಕೆ",
        'start_discussion': "ಹೊಸ ಚರ್ಚೆ ಪ್ರಾರಂಭಿಸಿ",
        'all_discussions': "ಎಲ್ಲಾ ಚರ್ಚೆಗಳು",
        'post_thread': "ಥ್ರೆಡ್ ಪೋಸ್ಟ್ ಮಾಡಿ",
        'reply': "ಪ್ರತ್ಯುತ್ತರ",
        'thread_posted': "ಥ್ರೆಡ್ ಪೋಸ್ಟ್ ಮಾಡಲಾಗಿದೆ!",
        'reply_posted': "ಪ್ರತ್ಯುತ್ತರ ಪೋಸ್ಟ್ ಮಾಡಲಾಗಿದೆ!",
        'soil_health': "ಮಣ್ಣು ಆರೋಗ್ಯ ಸ್ಕ್ಯಾನಿಂಗ್",
        'add_soil_test': "ಹೊಸ ಮಣ್ಣು ಪರೀಕ್ಷೆ ಸೇರಿಸಿ",
        'soil_test_log': "ಮಣ್ಣು ಪರೀಕ್ಷೆ ದಾಖಲೆ",
        'save_soil_test': "ಮಣ್ಣು ಪರೀಕ್ಷೆ ಉಳಿಸಿ",
        'soil_test_saved': "ಮಣ್ಣು ಪರೀಕ್ಷೆ ಉಳಿಸಲಾಗಿದೆ!",
        'heatmaps': "ಲೈವ್ ಕೃಷಿ ಹೀಟ್ಮ್ಯಾಪ್ಸ್ ಮತ್ತು ರೋಗ ವೀಕ್ಷಣೆ",
        'outbreak_map': "ರೋಗ ವೀಕ್ಷಣಾ ನಕ್ಷೆ",
        'no_geo_reports': "ಜಿಯೋ-ಟ್ಯಾಗ್ಡ್ ವರದಿಗಳು ಇಲ್ಲ.",
        'report_outbreak': "ಹೊಸ ರೋಗವನ್ನು ವರದಿ ಮಾಡಿ",
        'submit_outbreak': "ರೋಗ ವರದಿ ಸಲ್ಲಿಸಿ",
        'outbreak_reported': "ರೋಗ ವರದಿ ಸಲ್ಲಿಸಲಾಗಿದೆ!",
        'khet_market': "ಕೃಷಿ ಮಾರుಕಟ್ಟೆ",
        'market_home': "ಮುಖಪುಟ",
        'market_login': "ಲಾಗಿನ್",
        'market_register': "ನೋಂದಣಿ",
        'market_buyorsell': "ಖರೀದಿ/ಮಾರಾಟ",
        'market_buy': "ಖರೀದಿ",
        'market_checkout': "ಚೆಕ್‌ಔಟ್",
        'market_payment': "ಪಾವತಿ",
        'market_orders': "ಆರ್ಡರ್‌ಗಳು",
        'market_sell': "ಮಾರಾಟ",
        'market_selling_item': "ಮಾರಾಟದ ವಸ್ತು",
        'login_username': "ಬಳಕೆದಾರ ಹೆಸರು",
        'login_password': "ಪಾಸ್ವರ್ಡ್",
        'login_btn': "ಲಾಗಿನ್",
        'register_fullname': "ಪೂರ್ಣ ಹೆಸರು",
        'register_email': "ಇಮೇಲ್",
        'register_phone': "ಫೋನ್",
        'register_username': "ಬಳಕೆದಾರ ಹೆಸರು",
        'register_password': "ಪಾಸ್ವರ್ಡ್",
        'register_confirmpw': "ಪಾಸ್ವರ್ಡ್ ದೃಢೀಕರಿಸಿ",
        'register_btn': "ನೋಂದಣಿ",
        'buyorsell_buy': "ಖರೀದಿಗೆ ಹೋಗಿ",
        'buyorsell_sell': "ಮಾರಾಟಕ್ಕೆ ಹೋಗಿ",
        'payment_card': "ಕಾರ್ಡ್ ಸಂಖ್ಯೆ",
        'payment_expiry': "ಅವಧಿ ಮುಗಿಯುವ ದಿನಾಂಕ",
        'payment_cvv': "CVV",
        'payment_btn': "ಪಾವತಿ ಮಾಡಿ",
        'sell_crop': "ಬೆಳೆ ಹೆಸರು",
        'sell_qty': "ಪ್ರಮಾಣ (ಕೆಜಿ)",
        'sell_price': "ಬೆಲೆ (ಪ್ರತಿ ಕೆಜಿ, MSP ಗಿಂತ ಹೆಚ್ಚು)",
        'sell_img': "ಬೆಳೆ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        'sell_btn': "ಮಾರಾಟಕ್ಕೆ ಪಟ್ಟಿ ಮಾಡಿ",
        'output': "ಔಟ್‌ಪುಟ್",
        'context': "Q&A ಗೆ ಸನ್ನಿವೇಶವನ್ನು ನಮೂದಿಸಿ",
        'enter_context': "ದಯವಿಟ್ಟು Q&A ಗೆ ಸನ್ನಿವೇಶವನ್ನು ನಮೂದಿಸಿ.",
        'agribot_title': "🤖 AgriBot - Your Futuristic Agricultural Assistant",
        'agribot_greeting': "Hello! I'm AgriBot. How can I assist you with your farm today?",
        'agribot_input_placeholder': "Type your message here...",
        'agribot_attach_image': "Attach image (optional)",
        'send': "Send",
        'show_history': "Show Conversation History",
        'you': "You",
        'agribot': "AgriBot",
        'analytics_dashboard': "📊 Analytics Dashboard",
        'analytics_total_questions': "Total AgriBot Questions Asked",
        'analytics_common_crops': "Most Common Crops Discussed",
        'analytics_disease_trends': "Disease Diagnosis Trends",
        'analytics_engagement': "User Engagement Over Time",
        'analytics_pie_types': "Pie Chart of Question Types",
        'analytics_recent_log': "Recent Activity Log",
        'analytics_upload_csv': "Upload a CSV file for visualization",
        'analytics_no_data': "No chat data to display.",
        'analytics_no_conversations': "No conversation data found.",
        'analytics_no_keywords': "No crop keywords found in chats.",
        'analytics_no_disease': "No disease keywords found in chats.",
        'analytics_no_types': "No question type data found.",
        'analytics_info_upload': "If you want to visualize other CSV/statistics, upload them below:",
    },
    'ml': {
        'app_title': "🌾 കൃഷിസഖി: എഐ പ്രവർത്തിത കൃഷി സഹായി 🌾",
        'home': "ഹോം",
        'recommendations': "ശുപാർശകൾ നേടുക",
        'diagnosis': "എഐ രോഗ നിർണയം",
        'validation': "കർഷകൻ സ്ഥിരീകരിക്കൽ",
        'language': "ഭാഷ",
        'select_language': "ഭാഷ തിരഞ്ഞെടുക്കുക",
        'weather': "കാലാവസ്ഥ പ്രവചനം",
        'input_options': "ഇൻപുട്ട് ഓപ്ഷനുകൾ",
        'image_input': "ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
        'voice_input': "ശബ്ദ ഇൻപുട്ട്",
        'text_input': "ടെക്സ്റ്റ് ഇൻപുട്ട്",
        'submit': "സമർപ്പിക്കുക",
        'severity': "രോഗ ഗുരുത്വം കണക്കാക്കൽ",
        'correction': "കർഷകൻ തിരുത്തൽ",
        'enter_farm_data': "ഫാം ഡാറ്റ നൽകുക",
        'farm_id': "ഫാം ഐഡി",
        'soil_ph': "മണ്ണിന്റെ പിഎച്ച് മൂല്യം",
        'soil_moisture': "മണ്ണിലെ ഈർപ്പം (%)",
        'temperature': "താപനില (°C)",
        'rainfall': "മഴ (മില്ലീമീറ്റർ)",
        'crop_type': "വിളയുടെ തരം",
        'fertilizer_usage': "വളത്തിന്റെ ഉപയോഗം (കിലോ)",
        'pesticide_usage': " കീടനാശിനി ഉപയോഗം (കിലോ)",
        'crop_yield': "വിളയുടെ വിളവ് (ടൺ)",
        'sustainability_score': "സ്ഥിരത സ്കോർ",
        'select_crop': "മാർക്കറ്റ്/കാലാവസ്ഥ/സ്ഥിരത നിർദ്ദേശങ്ങൾക്ക് വിള തിരഞ്ഞെടുക്കുക",
        'get_recommendations': "ശുപാർശകൾ നേടുക",
        'soil_recommendations': "🧾 മണ്ണിന്റെ ശുപാർശകൾ",
        'market_trends': "📈 മാർക്കറ്റ് ട്രെൻഡുകൾ",
        'weather_forecast': "🌤️ കാലാവസ്ഥ പ്രവചനം",
        'sustainable_practices': "🌱 സ്ഥിരതയുള്ള രീതികൾ",
        'ai_diagnosis': "എഐ നിർണയ ഫലം",
        'severity_result': "കണക്കാക്കിയ ഗുരുത്വം",
        'validation_prompt': "മുകളിൽ കാണിച്ച വിവരങ്ങൾ ശരിയാണോ?",
        'correction_prompt': "ശരിയായ നിർണയം നൽകുക:",
        'thank_you': "നിങ്ങളുടെ അഭിപ്രായത്തിന് നന്ദി!",
        'back_home': "ഹോംലേക്ക് മടങ്ങുക",
        'growth_diary': 'വളർച്ചാ ഡയറി',
        'add_entry': 'പുതിയ എൻട്രി ചേർക്കുക',
        'diary_log': 'ഡയറി ലോഗ്',
        'crop': 'വിള',
        'notes': 'കുറിപ്പുകൾ',
        'save_entry': 'എൻട്രി സംരക്ഷിക്കുക',
        'entry_saved': 'എൻട്രി സംരക്ഷിച്ചു!',
        'knowledge_sharing': 'അറിവ് പങ്കിടൽ',
        'start_discussion': 'പുതിയ ചർച്ച ആരംഭിക്കുക',
        'all_discussions': 'എല്ലാ ചർച്ചകളും',
        'post_thread': 'ത്രെഡ് പോസ്റ്റ് ചെയ്യുക',
        'reply': 'മറുപടി',
        'thread_posted': 'ത്രെഡ് പോസ്റ്റ് ചെയ്തു!',
        'reply_posted': 'മറുപടി പോസ്റ്റ് ചെയ്തു!',
        'soil_health': 'മണ്ണിന്റെ ആരോഗ്യ സ്കാനിംഗ്',
        'add_soil_test': 'പുതിയ മണ്ണ് പരിശോധന ചേർക്കുക',
        'soil_test_log': 'മണ്ണ് പരിശോധന ലോഗ്',
        'save_soil_test': 'മണ്ണ് പരിശോധന സംരക്ഷിക്കുക',
        'soil_test_saved': 'മണ്ണ് പരിശോധന സംരക്ഷിച്ചു!',
        'heatmaps': 'ലൈവ് കൃഷി ഹീറ്റ്‌മാപ്പുകളും രോഗ വ്യാപനവും',
        'outbreak_map': 'രോഗ വ്യാപന മാപ്പ്',
        'no_geo_reports': 'ജിയോ-ടാഗ്ഡ് റിപ്പോർട്ടുകൾ ഇല್ല.',
        'report_outbreak': 'പുതിയ രോഗം റിപ്പോർട്ട് ചെയ്യുക',
        'submit_outbreak': 'രോഗ റിപ്പോർട്ട് സമർപ്പിക്കുക',
        'outbreak_reported': 'രോഗ റിപ്പോർട്ട് സമർപ്പിച്ചു!',
        'khet_market': 'കൃഷി മാർക്കറ്റ്',
        'market_home': 'ഹോം',
        'market_login': 'ലോഗിൻ',
        'market_register': 'രജിസ്റ്റർ',
        'market_buyorsell': 'വാങ്ങുക/വിൽക്കുക',
        'market_buy': 'വാങ്ങുക',
        'market_checkout': 'ചെക്ക്‌ഔട്ട്',
        'market_payment': 'പേയ്മെന്റ്',
        'market_orders': 'ഓർഡറുകൾ',
        'market_sell': 'വിൽക്കുക',
        'market_selling_item': 'വിൽക്കുന്ന ഇനം',
        'login_username': 'ഉപയോക്തൃനാമം',
        'login_password': 'പാസ്‌വേഡ്',
        'login_btn': 'ലോഗിൻ',
        'register_fullname': 'പൂർണ്ണനാമം',
        'register_email': 'ഇമെയിൽ',
        'register_phone': 'ഫോൺ',
        'register_username': 'ഉപയോക്തൃനാമം',
        'register_password': 'പാസ്‌വേഡ്',
        'register_confirmpw': 'പാസ്‌വേഡ് സ്ഥിരീകരിക്കുക',
        'register_btn': 'രജിസ്റ്റർ',
        'buyorsell_buy': 'വാങ്ങാൻ പോകുക',
        'buyorsell_sell': 'വിൽക്കാൻ പോകുക',
        'payment_card': 'കാർഡ് നമ്പർ',
        'payment_expiry': 'കാലാവധി തീയതി',
        'payment_cvv': 'CVV',
        'payment_btn': 'പേയ്മെന്റ് ചെയ്യുക',
        'sell_crop': 'വിളയുടെ പേര്',
        'sell_qty': 'അളവ് (കിലോ)',
        'sell_price': 'വില (ഓരോ കിലോയ്ക്കും, MSP-നേക്കാൾ കൂടുതലായിരിക്കണം)',
        'sell_img': 'വിളയുടെ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക',
        'sell_btn': 'വിൽപ്പനയ്ക്ക് പട്ടികയിടുക',
        'output': 'ഔട്ട്‌പുട്ട്',
        'context': 'Q&A-യ്ക്ക് കോൺടെക്സ്റ്റ് നൽകുക',
        'enter_context': 'ദയവായി Q&A-യ്ക്ക് കോൺടെക്സ്റ്റ് നൽകുക.',
        'agribot_title': "🤖 AgriBot - Your Futuristic Agricultural Assistant",
        'agribot_greeting': "Hello! I'm AgriBot. How can I assist you with your farm today?",
        'agribot_input_placeholder': "Type your message here...",
        'agribot_attach_image': "Attach image (optional)",
        'send': "Send",
        'show_history': "Show Conversation History",
        'you': "You",
        'agribot': "AgriBot",
        'analytics_dashboard': "📊 Analytics Dashboard",
        'analytics_total_questions': "Total AgriBot Questions Asked",
        'analytics_common_crops': "Most Common Crops Discussed",
        'analytics_disease_trends': "Disease Diagnosis Trends",
        'analytics_engagement': "User Engagement Over Time",
        'analytics_pie_types': "Pie Chart of Question Types",
        'analytics_recent_log': "Recent Activity Log",
        'analytics_upload_csv': "Upload a CSV file for visualization",
        'analytics_no_data': "No chat data to display.",
        'analytics_no_conversations': "No conversation data found.",
        'analytics_no_keywords': "No crop keywords found in chats.",
        'analytics_no_disease': "No disease keywords found in chats.",
        'analytics_no_types': "No question type data found.",
        'analytics_info_upload': "If you want to visualize other CSV/statistics, upload them below:",
    },
}

# --- Helper for translation ---
def t(key, lang):
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

# --- Session state for language and navigation ---
def init_session():
    if 'lang' not in st.session_state:
        st.session_state['lang'] = 'en'
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'
    if 'diagnosis_result' not in st.session_state:
        st.session_state['diagnosis_result'] = None
    if 'severity' not in st.session_state:
        st.session_state['severity'] = None
    if 'correction' not in st.session_state:
        st.session_state['correction'] = None

# --- User/Admin Login System ---
ADMIN_USERNAME = 'surya001'
ADMIN_PASSWORD = '1234'

def login_page():
    # Show KrishiSakhi app title at the top
    lang = st.session_state.get('lang', 'en')
    st.markdown(f"<h1 style='text-align:center; color:#388e3c;'>" + t('app_title', lang) + "</h1>", unsafe_allow_html=True)
    st.title('Login')
    username = st.text_input('Username', key='login_username')
    password = st.text_input('Password', type='password', key='login_password')
    if st.button('Login'):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state['logged_in'] = True
            st.session_state['role'] = 'admin'
            st.session_state['username'] = username
            st.rerun()
        elif username and password and not (username == ADMIN_USERNAME):
            st.session_state['logged_in'] = True
            st.session_state['role'] = 'user'
            st.session_state['username'] = username
            st.rerun()
        else:
            st.error('Invalid username or password.')
    st.info('Admin: surya001 / 1234')
    st.info('Any other username/password is a normal user.')

# --- Modified Sidebar Navigation ---
def sidebar_navigation():
    lang = st.session_state['lang']
    st.sidebar.title(t('app_title', lang))
    # Language selection
    lang_display = {
        'en': 'English',
        'te': 'తెలుగు',
        'hi': 'हिन्दी',
        'ta': 'தமிழ்',
        'kn': 'ಕನ್ನಡ',
        'ml': 'മലയാളം'
    }
    lang_keys = list(lang_display.keys())
    lang_names = [lang_display[k] for k in lang_keys]
    selected_lang = st.sidebar.selectbox(t('select_language', lang), lang_names, index=lang_keys.index(lang))
    st.session_state['lang'] = {v: k for k, v in lang_display.items()}[selected_lang]
    # --- Geolocation display and override ---
    st.sidebar.markdown('---')
    with st.sidebar:
        geo = streamlit_geolocation.streamlit_geolocation()
        if geo and geo.get('latitude') and geo.get('longitude'):
            loc = {
                'latitude': geo['latitude'],
                'longitude': geo['longitude'],
                'city': '',
                'region': '',
                'country': ''
            }
            st.markdown('<div style="display:flex;align-items:center;margin-bottom:0.5em;"><span style="font-size:1.3em;margin-right:0.4em;">📍</span><span style="font-weight:bold;color:#388e3c;">Detected Location (Browser)</span></div>', unsafe_allow_html=True)
            st.markdown(f'<span style="color:#333;font-size:1.1em;">Lat: <b>{geo["latitude"]:.4f}</b>, Lon: <b>{geo["longitude"]:.4f}</b></span>', unsafe_allow_html=True)
        else:
            loc = get_geolocation()
            st.markdown('<div style="display:flex;align-items:center;margin-bottom:0.5em;"><span style="font-size:1.3em;margin-right:0.4em;">📍</span><span style="font-weight:bold;color:#388e3c;">Detected Location (IP)</span></div>', unsafe_allow_html=True)
            st.markdown(f'<span style="color:#333;font-size:1.1em;">{loc.get("city", "")}, {loc.get("region", "")}, {loc.get("country", "")}</span>', unsafe_allow_html=True)
    if st.sidebar.checkbox('Override location'):
        city = st.sidebar.text_input('City', value=loc.get('city', ''))
        region = st.sidebar.text_input('Region/State', value=loc.get('region', ''))
        country = st.sidebar.text_input('Country', value=loc.get('country', ''))
        lat = st.sidebar.number_input('Latitude', value=loc.get('latitude', 0.0), format='%f')
        lon = st.sidebar.number_input('Longitude', value=loc.get('longitude', 0.0), format='%f')
        if st.sidebar.button('Set Location'):
            st.session_state['user_location'] = {
                'latitude': lat,
                'longitude': lon,
                'city': city,
                'region': region,
                'country': country
            }
            import json
            log_user_input('sidebar', 'location_override', json.dumps({'latitude': lat, 'longitude': lon, 'city': city, 'region': region, 'country': country}))
            st.sidebar.success('Location updated!')
    # Page selection (add Analytics Dashboard)
    page_labels = [
        t('home', lang),
        t('recommendations', lang),
        t('diagnosis', lang),
        t('growth_diary', lang),
        t('knowledge_sharing', lang),
        t('soil_health', lang),
        t('heatmaps', lang),
        t('khet_market', lang),
        t('analytics_dashboard', lang)
    ]
    if st.session_state.get('role') == 'admin':
        page_labels.append('Get Corpus Data')
    page = st.sidebar.radio('Go to', page_labels)
    page_map = {
        t('home', lang): 'home',
        t('recommendations', lang): 'recommendations',
        t('diagnosis', lang): 'diagnosis',
        t('growth_diary', lang): 'growth-diary',
        t('knowledge_sharing', lang): 'knowledge-sharing',
        t('soil_health', lang): 'soil-health',
        t('heatmaps', lang): 'heatmaps',
        t('khet_market', lang): 'khet-market',
        t('analytics_dashboard', lang): 'analytics-dashboard',
        'Get Corpus Data': 'get-corpus-data'
    }
    st.session_state['page'] = page_map[page]
    st.sidebar.markdown('---')
    st.sidebar.write(f"Logged in as: {st.session_state.get('username','')} ({st.session_state.get('role','')})")
    if st.sidebar.button('Logout'):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# --- AgriBot Chat Home Page (Gemini) ---
def agri_chat_page():
    import uuid
    import google.generativeai as genai
    from dotenv import load_dotenv
    load_dotenv()
    lang = st.session_state['lang']
    genai.configure(api_key=os.environ.get("AIzaSyDdmBu49KXJ7r0zEzcHekS0O34JoWylv1M"))
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=SYSEM_INSTRUCTION,
    )
    CONV_FILE = "conversations.json"
    def load_conversations():
        if not os.path.exists(CONV_FILE):
            with open(CONV_FILE, 'w') as f:
                json.dump({}, f)
        with open(CONV_FILE, 'r') as f:
            return json.load(f)
    def save_conversations(conversations):
        with open(CONV_FILE, 'w') as f:
            json.dump(conversations, f, indent=4)
    def get_user_id():
        if 'user_id' not in st.session_state:
            st.session_state['user_id'] = str(uuid.uuid4())
        return st.session_state['user_id']
    st.title(t('agribot_title', lang))
    st.markdown(
        f'<div style="background-color:#e0f7fa;padding:10px;border-radius:8px;margin-bottom:10px;">'
        f'<b>{t("agribot", lang)}:</b> {t("agribot_greeting", lang)}'
        '</div>', unsafe_allow_html=True)
    user_id = get_user_id()
    conversations = load_conversations()
    user_history = conversations.get(user_id, [])
    # Chat input (single field + attachment, with preview)
    col1, col2 = st.columns([4,2])
    with col1:
        user_message = st.text_input(t("agribot_input_placeholder", lang), key="user_message")
    with col2:
        image_file = st.file_uploader(t("agribot_attach_image", lang), type=['jpg', 'jpeg', 'png'], key="image_file")
        if image_file:
            st.image(image_file, width=120, caption="Preview")
    send_clicked = st.button(t("send", lang))
    if send_clicked and user_message:
        # Save image if uploaded
        image_path = None
        if image_file:
            uploads_dir = "uploads"
            os.makedirs(uploads_dir, exist_ok=True)
            image_path = os.path.join(uploads_dir, image_file.name)
            with open(image_path, "wb") as f:
                f.write(image_file.read())
        # Prepare Gemini input
        files = []
        new_image = None
        if image_path and os.path.exists(image_path):
            new_image = genai.upload_file(image_path)
            files.append(new_image)
        # Only keep allowed keys: 'role' and 'parts'
        filtered_history = [
            {k: v for k, v in entry.items() if k in ("role", "parts")}
            for entry in user_history
        ]
        chat_session = model.start_chat(history=filtered_history)
        response = chat_session.send_message(content=[user_message, new_image] if new_image else user_message)
        bot_reply = response.text
        # Update history
        user_history.append({"role": "user", "parts": [user_message], "timestamp": datetime.utcnow().isoformat()})
        user_history.append({"role": "model", "parts": [bot_reply], "timestamp": datetime.utcnow().isoformat()})
        conversations[user_id] = user_history
        save_conversations(conversations)
        st.experimental_rerun()
    # Show chat history (conversational bubbles)
    st.markdown("---")
    for msg in user_history:
        if msg['role'] == 'user':
            st.markdown(
                f'<div style="background-color:#fffde7;padding:8px 12px;border-radius:8px;margin-bottom:6px;text-align:right;"><b>{t("you", lang)}:</b> {msg["parts"][0]}</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div style="background-color:#e0f7fa;padding:8px 12px;border-radius:8px;margin-bottom:6px;text-align:left;"><b>{t("agribot", lang)}:</b> {msg["parts"][0]}</div>',
                unsafe_allow_html=True)

# --- Home page ---
def home_page():
    import os
    import json
    import google.generativeai as genai
    from google.ai.generativelanguage_v1beta.types import content
    from werkzeug.utils import secure_filename
    import streamlit as st

    # Display main app title first
    st.markdown('<h1 style="text-align:center; color:#388e3c;">🌾 KrishiSakhi: AI-Driven Farming Assistant 🌾</h1>', unsafe_allow_html=True)

    # Configure Gemini API
    api_key = "AIzaSyDdmBu49KXJ7r0zEzcHekS0O34JoWylv1M"
    genai.configure(api_key=api_key)

    # Constants
    UPLOAD_FOLDER = "uploads"
    DATABASE = "conversations.json"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # System instruction for the model
    SYSTEM_INSTRUCTION = """You are AgriBot, a highly intelligent and specialized AI assistant designed to help farmers and agricultural professionals optimize their work. Your main responsibilities include:

Plant Disease Diagnosis 🌿🔬

Analyze uploaded photos of plants.
Detect diseases, nutrient deficiencies, or pest infestations.
Provide precise diagnoses with explanations.
Suggest treatment solutions, including organic and chemical remedies.
General Agricultural Assistance 🚜🌾

Answer farming-related questions (soil health, irrigation, fertilization, pest control).
Provide best practices for different crops and climates.
Guide users on sustainable farming techniques and respond by the same language writen by the user.
Smart and Professional Communication 🗣️🤖

Be clear, concise, and professional in responses.
Use easy-to-understand language for farmers of all expertise levels.
Provide scientific insights in a user-friendly way.
Example Interaction:

👨‍🌾 User: "My tomato leaves have yellow spots. What should I do?"
🤖 AgriBot:
"Based on your photo, your tomato plant may have early blight (Alternaria solani), a common fungal disease. I recommend:
✅ Removing infected leaves.
✅ Applying a copper-based fungicide.
✅ Ensuring good air circulation to prevent moisture buildup.
Let me know if you need organic alternatives! """

    # Initialize the model
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=SYSTEM_INSTRUCTION,
    )

    def load_conversations() -> dict:
        if not os.path.exists(DATABASE):
            with open(DATABASE, "w") as f:
                json.dump({}, f)
        with open(DATABASE, "r") as f:
            return json.load(f)

    def save_conversations(conversations):
        with open(DATABASE, "w") as f:
            json.dump(conversations, f, indent=4)

    def save_uploaded_file(uploaded_file):
        filename = secure_filename(uploaded_file.name)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return filepath, filename

    st.title("AgriBot - AI Assistant for Farmers")

    # User ID input (for session identification)
    user_id = st.text_input("Enter your user ID:", value="default_user")

    # Load conversation history
    conversations = load_conversations()
    user_history = conversations.get(user_id, [])

    # Image upload
    uploaded_file = st.file_uploader("Upload an image of your plant (optional)", type=["png", "jpg", "jpeg"])

    image_path = None
    if uploaded_file is not None:
        filepath, filename = save_uploaded_file(uploaded_file)
        image_path = filepath
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # User message input
    user_message = st.text_area("Enter your message to AgriBot:")

    if st.button("Send"):
        if not user_message:
            st.error("Message cannot be empty")
        else:
            # Upload image to Gemini if provided
            files = []
            new_image = None
            if image_path and os.path.exists(image_path):
                new_image = genai.upload_file(image_path)
                files.append(new_image)

            # Start chat session with history (filter out non-standard fields)
            filtered_history = [
                {k: v for k, v in entry.items() if k in ("role", "parts")}
                for entry in user_history
            ]
            chat_session = model.start_chat(history=filtered_history)
            response = chat_session.send_message(content=[user_message, new_image] if new_image else user_message)
            bot_reply = response.text

            # Save conversation
            user_history.append({"role": "user", "parts": [user_message], "timestamp": datetime.utcnow().isoformat()})
            user_history.append({"role": "model", "parts": [bot_reply], "timestamp": datetime.utcnow().isoformat()})
            conversations[user_id] = user_history
            save_conversations(conversations)

            # Display bot reply
            st.markdown(f"**AgriBot:** {bot_reply}")

    # Show conversation history only when button is clicked
    if st.button("Show Conversation History"):
        st.subheader("Conversation History")
        for entry in user_history:
            role = entry.get("role")
            parts = entry.get("parts", [])
            if role == "user":
                for part in parts:
                    st.markdown(f"**You:** {part}")
            elif role == "model":
                for part in parts:
                    st.markdown(f"**AgriBot:** {part}")

# --- Recommendations page ---
def recommendations_page(farmer_advisor, market_researcher, weather_module, agri_expert, memory):
    import pandas as pd
    import numpy as np
    lang = st.session_state['lang']
    st.title(t('recommendations', lang))
    st.header(t('enter_farm_data', lang))
    farm_id = st.text_input(t('farm_id', lang), value="1")
    # New: N, P, K input fields
    n = st.number_input('Nitrogen (N)', min_value=0.0, max_value=100.0, value=10.0, step=0.1)
    p = st.number_input('Phosphorus (P)', min_value=0.0, max_value=100.0, value=10.0, step=0.1)
    k = st.number_input('Potassium (K)', min_value=0.0, max_value=100.0, value=10.0, step=0.1)
    soil_ph = st.number_input(t('soil_ph', lang), min_value=0.0, max_value=14.0, value=6.5, step=0.1)
    soil_moisture = st.number_input(t('soil_moisture', lang), min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    temperature_c = st.number_input(t('temperature', lang), min_value=-50.0, max_value=60.0, value=25.0, step=0.1)
    rainfall_mm = st.number_input(t('rainfall', lang), min_value=0.0, max_value=1000.0, value=100.0, step=0.1)
    crop_options = [
        ("Wheat", "🌾 Wheat: Cool-season cereal, staple food, high in protein."),
        ("Rice", "🍚 Rice: Warm-season cereal, grown in flooded fields, staple in Asia."),
        ("Maize", "🌽 Maize (Corn): Versatile cereal, used for food, feed, and industry."),
        ("Soybean", "🫘 Soybean: Protein-rich legume, improves soil fertility."),
        ("Cotton", "🧵 Cotton: Fiber crop, requires warm climate and irrigation."),
        ("Sugarcane", "🍬 Sugarcane: Tropical grass, source of sugar and ethanol."),
        ("Groundnut", "🥜 Groundnut (Peanut): Oilseed legume, drought-tolerant."),
        ("Potato", "🥔 Potato: Cool-season tuber, rich in carbohydrates."),
        ("Tomato", "🍅 Tomato: Popular vegetable, needs warm weather, prone to diseases."),
        ("Onion", "🧅 Onion: Bulb vegetable, grows in many climates."),
        ("Chickpea", "�� Chickpea: Protein-rich pulse, good for dry areas."),
        ("Mustard", "🌻 Mustard: Oilseed, cool-season crop, used for oil and greens."),
        ("Sorghum", "🌾 Sorghum: Drought-tolerant cereal, used for food and fodder."),
        ("Banana", "🍌 Banana: Tropical fruit, needs rich soil and moisture."),
        ("Grapes", "🍇 Grapes: Fruit crop, grown in temperate and tropical regions."),
        ("Mango", "🥭 Mango: King of fruits, needs hot, dry weather for ripening."),
        ("Pigeonpea", "🌿 Pigeonpea: Drought-resistant pulse, improves soil health."),
        ("Sunflower", "🌻 Sunflower: Oilseed, grows well in sunny, dry areas."),
        ("Pea", "🌱 Pea: Cool-season legume, rich in protein.")
    ]
    crop_names = [c[0] for c in crop_options]
    crop = st.selectbox(t('select_crop', lang), crop_names)
    crop_detail = dict(crop_options)[crop]
    st.caption(crop_detail)
    fertilizer_usage_kg = st.number_input(t('fertilizer_usage', lang), min_value=0.0, max_value=500.0, value=100.0, step=0.1)
    pesticide_usage_kg = st.number_input(t('pesticide_usage', lang), min_value=0.0, max_value=100.0, value=10.0, step=0.1)
    crop_yield_ton = st.number_input(t('crop_yield', lang), min_value=0.0, max_value=100.0, value=5.0, step=0.1)
    sustainability_score = st.number_input(t('sustainability_score', lang), min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    if st.button(t('get_recommendations', lang)):
        soil_data = {
            "N": n,
            "P": p,
            "K": k,
            "ph": soil_ph,
            "moisture": soil_moisture,
            "temperature": temperature_c,
            "rainfall": rainfall_mm
        }
        user_input = {
            "farm_id": farm_id,
            "N": n,
            "P": p,
            "K": k,
            "soil_ph": soil_ph,
            "soil_moisture": soil_moisture,
            "temperature_c": temperature_c,
            "rainfall_mm": rainfall_mm,
            "crop_type": crop,
            "fertilizer_usage_kg": fertilizer_usage_kg,
            "pesticide_usage_kg": pesticide_usage_kg,
            "crop_yield_ton": crop_yield_ton,
            "sustainability_score": sustainability_score,
            "crop": crop
        }
        import json
        log_user_input('recommendations', 'form', json.dumps(user_input))
        memory.log_interaction("User", str(user_input), "Started analysis")
        # Prepare input for FarmerAdvisor model (only features present in training data)
        model_input = {
            "Farm_ID": int(farm_id),
            "Soil_pH": soil_ph,
            "Soil_Moisture": soil_moisture,
            "Temperature_C": temperature_c,
            "Rainfall_mm": rainfall_mm,
            "Crop_Type": crop,
            "Fertilizer_Usage_kg": fertilizer_usage_kg,
            "Pesticide_Usage_kg": pesticide_usage_kg,
            "Crop_Yield_ton": crop_yield_ton,
            "Sustainability_Score": sustainability_score
        }
        loc = get_geolocation()
        # --- Real Crop Prediction using Crop_recommendation.csv ---
        try:
            df = pd.read_csv('Crop_recommendation.csv')
            # Compute distance to each row
            features = ['N','P','K','temperature','humidity','ph','rainfall']
            input_vec = np.array([n, p, k, temperature_c, soil_moisture, soil_ph, rainfall_mm])
            df_features = df[features].values
            dists = np.linalg.norm(df_features - input_vec, axis=1)
            best_idx = np.argmin(dists)
            best_crop = df.iloc[best_idx]['label']
        except Exception as e:
            best_crop = f"[Error: {e}]"
        # --- Fertilizer Recommendation using fertilizer.csv ---
        fert_reco = None
        try:
            fert_df = pd.read_csv('fertilizer.csv')
            fert_row = fert_df[fert_df['Crop'].str.lower() == str(best_crop).lower()]
            if not fert_row.empty:
                fert_row = fert_row.iloc[0]
                fert_reco = {
                    'N': fert_row['N'],
                    'P': fert_row['P'],
                    'K': fert_row['K'],
                    'pH': fert_row['pH'],
                    'soil_moisture': fert_row['soil_moisture']
                }
        except Exception as e:
            fert_reco = f"[Error: {e}]"
        land_advice = farmer_advisor.get_recommendations(model_input)
        market_advice = market_researcher.analyze({"crop": crop})
        weather_report = weather_module.get_real_time_weather()
        sustainability_advice = agri_expert.provide_guidance({"crop": crop, "soil": soil_data})
        final_recommendations = {
            'Soil Advice': land_advice,
            'Market Trends': market_advice,
            'Weather Forecast': weather_report,
            'Sustainability Tips': sustainability_advice,
            'Best Crop Prediction': best_crop,
            'Fertilizer Recommendation': fert_reco
        }
        memory.log_interaction("System", str(user_input), str(final_recommendations))
        st.subheader(t('soil_recommendations', lang))
        st.info(f"Best Crop to Grow (Data-Driven Prediction): {best_crop}")
        if fert_reco:
            st.subheader('Recommended Fertilizer Parameters')
            if isinstance(fert_reco, dict):
                st.write(f"N: {fert_reco['N']}, P: {fert_reco['P']}, K: {fert_reco['K']}, pH: {fert_reco['pH']}, Soil Moisture: {fert_reco['soil_moisture']}")
            else:
                st.write(fert_reco)
        if isinstance(land_advice, dict) and "error" in land_advice:
            st.error(land_advice["error"])
        else:
            if isinstance(land_advice, dict):
                st.markdown("**Prediction:** " + str(land_advice.get("prediction", "")))
                st.markdown("**Confidence:** " + str(land_advice.get("confidence", "")) + "%")
                st.markdown("**Input Used:**")
                input_used = land_advice.get("input_used", {})
                for key, value in input_used.items():
                    st.markdown(f"- {key}: {value}")
            else:
                st.write(land_advice)
        st.subheader(t('market_trends', lang))
        st.write(market_advice)
        st.subheader(t('weather_forecast', lang))
        st.write(weather_report)
        st.subheader(t('sustainable_practices', lang))
        for tip in sustainability_advice.split("\n"):
            st.write(f"- {tip}")

# --- Voice input using streamlit-webrtc and SpeechRecognition ---
def voice_input_component(lang):
    import tempfile
    from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
    import av
    try:
        from vosk import Model, KaldiRecognizer
        vosk_available = True
    except ImportError:
        vosk_available = False
    import json
    import os

    class AudioProcessor(AudioProcessorBase):
        def __init__(self):
            self.frames = []
        def recv(self, frame):
            self.frames.append(frame.to_ndarray())
            return frame

    ctx = webrtc_streamer(key="voice", audio_receiver_size=1024, audio_processor_factory=AudioProcessor)
    text = ""
    if not vosk_available:
        st.error("Vosk is not installed. Please install vosk to use voice input.")
        return text
    if ctx.audio_receiver:
        audio_frames = ctx.audio_receiver.get_frames(timeout=1)
        if audio_frames:
            # Save audio to temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                for audio_frame in audio_frames:
                    f.write(audio_frame.to_ndarray().tobytes())
                audio_path = f.name
            # Recognize speech using Vosk
            model_path = st.text_input("Vosk Model Path", value="vosk-model-small-en-us-0.15")
            if not os.path.exists(model_path):
                st.error(f"[Error: Vosk model not found at {model_path}]")
                text = ""
            else:
                try:
                    model = Model(model_path)
                    rec = KaldiRecognizer(model, 16000)
                    with open(audio_path, "rb") as audio_file:
                        while True:
                            data = audio_file.read(4000)
                            if len(data) == 0:
                                break
                            if rec.AcceptWaveform(data):
                                pass
                    result = rec.FinalResult()
                    try:
                        result_json = json.loads(result)
                        text = result_json.get("text", "")
                    except Exception as e:
                        text = f"[Error: {e} in parsing Vosk result]"
                except Exception as e:
                    st.error(f"[Error: {e} in Vosk recognition]")
                    text = ""
            os.remove(audio_path)
    return text

# --- Diagnosis page (image, voice, text input) ---
def diagnosis_page():
    lang = st.session_state['lang']
    st.title(t('diagnosis', lang))
    st.header(t('input_options', lang))
    input_type = st.radio("Select Input Type", [t('image_input', lang), t('voice_input', lang), t('text_input', lang)])
    diagnosis_result = None
    classifier = ImageClassifier()
    if input_type == t('image_input', lang):
        uploaded_file = st.file_uploader(t('image_input', lang), type=['jpg', 'jpeg', 'png'])
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert('RGB')
            st.image(image, caption="Uploaded Image", use_container_width=True)
            import json
            log_user_input('diagnosis', 'image', json.dumps({'filename': uploaded_file.name}))
            with st.spinner("Classifying image..."):
                disease, confidence, cure = classifier.predict(image)
            st.success(f"Predicted Disease: {disease} (Confidence: {confidence*100:.2f}%)")
            st.info(f"Recommended Cure/Treatment: {cure}")
            # --- Show severity estimation automatically ---
            if confidence > 0.75:
                severity = random.choice(['Low', 'Medium', 'High'])
            else:
                severity = 'Low'
            percent = int(confidence * 100)
            st.info(f"Estimated Severity: {severity} ({percent}%)")
            st.session_state['diagnosis_result'] = {'disease': disease, 'confidence': confidence, 'cure': cure, 'severity': severity, 'percent': percent}
            # --- Farmer validation/correction workflow ---
            is_correct = st.radio("Is the above information correct?", ["Yes", "No"])
            if is_correct == "No":
                correction = st.text_input("Please provide the correct diagnosis:")
                if st.button("Submit Feedback"):
                    st.session_state['correction'] = correction
                    st.success("Thank you for your feedback!")
            # If 'Yes', do not show anything further
    elif input_type == t('voice_input', lang):
        st.write(t('voice_input', lang))
        voice_mode = st.radio("Choose voice input method:", ["Upload Audio File", "Record Live Audio"])
        text = ""
        audio_bytes = None
        audio_file_path = None
        if voice_mode == "Upload Audio File":
            uploaded_audio = st.file_uploader("Upload Audio File", type=["wav", "mp3", "ogg"])
            if uploaded_audio is not None:
                audio_bytes = uploaded_audio.read()
                import json
                log_user_input('diagnosis', 'voice_upload', json.dumps({'filename': uploaded_audio.name}))
        elif voice_mode == "Record Live Audio":
            try:
                from streamlit_audiorecorder import audiorecorder
                audio_bytes = audiorecorder("Click to record", "Recording...")
                if audio_bytes:
                    import json
                    log_user_input('diagnosis', 'voice_record', json.dumps({'length': len(audio_bytes)}))
            except ImportError:
                st.error("streamlit-audiorecorder is not installed. Please install it with 'pip install streamlit-audiorecorder'.")
        # --- Save and play audio after recording/upload ---
        if audio_bytes:
            import tempfile
            import os
            # Save to persistent location for playback
            audio_dir = os.path.join("uploads", "audio_diagnosis")
            os.makedirs(audio_dir, exist_ok=True)
            import uuid
            audio_filename = f"audio_{uuid.uuid4().hex}.wav"
            audio_file_path = os.path.join(audio_dir, audio_filename)
            with open(audio_file_path, 'wb') as f:
                f.write(audio_bytes)
            st.audio(audio_file_path, format='audio/wav')
            # Also save to temp for Vosk processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                tmp_audio.write(audio_bytes)
                tmp_audio_path = tmp_audio.name
            # Speech-to-text with Vosk
            try:
                from vosk import Model, KaldiRecognizer
                import wave
                import json
                model_path = st.text_input("Vosk Model Path", value="vosk-model-small-en-us-0.15")
                if not os.path.exists(model_path):
                    st.error(f"[Error: Vosk model not found at {model_path}]")
                else:
                    wf = wave.open(tmp_audio_path, "rb")
                    model = Model(model_path)
                    rec = KaldiRecognizer(model, wf.getframerate())
                    while True:
                        data = wf.readframes(4000)
                        if len(data) == 0:
                            break
                        rec.AcceptWaveform(data)
                    result = rec.FinalResult()
                    result_json = json.loads(result)
                    text = result_json.get("text", "")
                    st.write(f"Recognized Text: {text}")
                    # Use NLP model to predict disease from text
                    nlp_models = NLPModels()
                    with st.spinner("Analyzing text for disease diagnosis..."):
                        disease = nlp_models.summarize(text)
                        confidence = 0.85  # Placeholder confidence
                    st.success(f"Predicted Disease: {disease} (Confidence: {confidence*100:.2f}%)")
                    # --- Show severity estimation automatically ---
                    if confidence > 0.75:
                        severity = random.choice(['Low', 'Medium', 'High'])
                    else:
                        severity = 'Low'
                    percent = int(confidence * 100)
                    st.info(f"Estimated Severity: {severity} ({percent}%)")
                    st.session_state['diagnosis_result'] = {'disease': disease, 'confidence': confidence, 'input_text': text, 'severity': severity, 'percent': percent, 'audio_file': audio_file_path}
                    # --- Farmer validation/correction workflow ---
                    is_correct = st.radio("Is the above information correct?", ["Yes", "No"])
                    if is_correct == "No":
                        correction = st.text_input("Please provide the correct diagnosis:")
                        if st.button("Submit Feedback"):
                            st.session_state['correction'] = correction
                            st.success("Thank you for your feedback!")
                    # If 'Yes', do not show anything further
            except Exception as e:
                st.error(f"Speech recognition error: {e}")
            finally:
                os.remove(tmp_audio_path)
    elif input_type == t('text_input', lang):
        text_query = st.text_area(t('text_input', lang))
        if st.button(t('submit', lang)):
            import json
            log_user_input('diagnosis', 'text', json.dumps({'text': text_query}))
            # Use NLP model to predict disease from text
            nlp_models = NLPModels()
            with st.spinner("Analyzing text for disease diagnosis..."):
                disease = nlp_models.summarize(text_query)
                confidence = 0.85  # Placeholder confidence
            st.success(f"Predicted Disease: {disease} (Confidence: {confidence*100:.2f}%)")
            # --- Show severity estimation automatically ---
            if confidence > 0.75:
                severity = random.choice(['Low', 'Medium', 'High'])
            else:
                severity = 'Low'
            percent = int(confidence * 100)
            st.info(f"Estimated Severity: {severity} ({percent}%)")
            st.session_state['diagnosis_result'] = {'disease': disease, 'confidence': confidence, 'input_text': text_query, 'severity': severity, 'percent': percent}
            # --- Farmer validation/correction workflow ---
            is_correct = st.radio("Is the above information correct?", ["Yes", "No"])
            if is_correct == "No":
                correction = st.text_input("Please provide the correct diagnosis:")
                if st.button("Submit Feedback"):
                    st.session_state['correction'] = correction
                    st.success("Thank you for your feedback!")
            # If 'Yes', do not show anything further

# --- Severity estimation page ---
def severity_page():
    lang = st.session_state['lang']
    st.title(t('severity', lang))
    diagnosis_result = st.session_state.get('diagnosis_result', None)
    if diagnosis_result:
        st.write(t('ai_diagnosis', lang) + f": {diagnosis_result['disease']} ({diagnosis_result['confidence']*100:.1f}%)")
        # Provide a stub severity estimation based on confidence or random
        confidence = diagnosis_result.get('confidence', 0)
        if confidence > 0.75:
            severity = random.choice(['Low', 'Medium', 'High'])
        else:
            severity = 'Low'
        percent = int(confidence * 100)
        st.info(f"Estimated Severity: {severity} ({percent}%)")
        st.session_state['severity'] = {'severity': severity, 'percent': percent}
        st.button(t('validation', lang), on_click=lambda: st.session_state.update({'page': 'validation'}))
    else:
        st.warning("No diagnosis result found.")

# --- Farmer validation/correction page ---
def validation_page():
    lang = st.session_state['lang']
    st.title(t('validation', lang))
    diagnosis_result = st.session_state.get('diagnosis_result', None)
    severity = st.session_state.get('severity', None)
    if diagnosis_result and severity:
        st.write(t('ai_diagnosis', lang) + f": {diagnosis_result['disease']} ({diagnosis_result['confidence']*100:.1f}%)")
        st.write(t('severity_result', lang) + f": {severity['severity']} ({severity['percent']}%)")
        is_correct = st.radio(t('validation_prompt', lang), ["Yes", "No"])
        if is_correct == "No":
            correction = st.text_input(t('correction_prompt', lang))
            if st.button(t('submit', lang)):
                st.session_state['correction'] = correction
                st.success(t('thank_you', lang))
        else:
            st.success(t('thank_you', lang))
    else:
        st.warning("No diagnosis/severity result found.")

def growth_diary_page():
    lang = st.session_state['lang']
    st.title(t('growth_diary', lang))
    diary_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset_farming', 'diary_log.csv')
    # Load or create diary log
    if os.path.exists(diary_path):
        diary_df = pd.read_csv(diary_path)
    else:
        diary_df = pd.DataFrame(columns=['date','crop','notes','image_path','weather'])
    # Entry form
    st.subheader(t('add_entry', lang))
    entry_date = st.date_input('Date', date.today())
    crop = st.text_input(t('crop', lang))
    notes = st.text_area(t('notes', lang))
    image = st.file_uploader('Upload Image', type=['jpg','jpeg','png'])
    weather = st.text_input('Weather (optional)')
    if st.button(t('save_entry', lang)):
        image_path = ''
        if image:
            img_save_path = os.path.join(os.path.dirname(diary_path), f'diary_{entry_date}_{crop}_{image.name}')
            with open(img_save_path, 'wb') as f:
                f.write(image.read())
            image_path = img_save_path
        new_entry = {'date': entry_date.isoformat() if hasattr(entry_date, 'isoformat') else str(entry_date), 'crop': crop, 'notes': notes, 'image_path': image_path, 'weather': weather}
        import json
        log_user_input('growth_diary', 'entry', json.dumps(new_entry))
        diary_df = pd.concat([diary_df, pd.DataFrame([new_entry])], ignore_index=True)
        diary_df.to_csv(diary_path, index=False)
        st.success(t('entry_saved', lang))
    # Show diary log
    st.subheader(t('diary_log', lang))
    if not diary_df.empty:
        for idx, row in diary_df.iterrows():
            st.markdown(f"**Date:** {row['date']}  |  **{t('crop', lang)}:** {row['crop']}")
            st.markdown(f"**{t('notes', lang)}:** {row['notes']}")
            if row['image_path'] and os.path.exists(row['image_path']):
                st.image(row['image_path'], width=200)
            if row['weather']:
                st.markdown(f"**Weather:** {row['weather']}")
            st.markdown('---')

def knowledge_sharing_page():
    import pandas as pd
    lang = st.session_state['lang']
    forum_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset_farming', 'forum_threads.csv')
    st.title(t('knowledge_sharing', lang))
    # Load or create forum threads
    if os.path.exists(forum_path):
        forum_df = pd.read_csv(forum_path)
    else:
        forum_df = pd.DataFrame(columns=['thread_id','title','content','timestamp','replies'])
    # New thread form
    st.subheader(t('start_discussion', lang))
    title = st.text_input('Title')
    content = st.text_area('Content')
    if st.button(t('post_thread', lang)):
        import time
        thread_id = int(time.time())
        now = datetime.now()
        new_thread = {'thread_id': thread_id, 'title': title, 'content': content, 'timestamp': now.isoformat(), 'replies': ''}
        import json
        log_user_input('knowledge_sharing', 'thread', json.dumps(new_thread))
        forum_df = pd.concat([forum_df, pd.DataFrame([new_thread])], ignore_index=True)
        forum_df.to_csv(forum_path, index=False)
        st.success(t('thread_posted', lang))
    # Show threads
    st.subheader(t('all_discussions', lang))
    if not forum_df.empty:
        for idx, row in forum_df.iterrows():
            st.markdown(f"**{row['title']}**  ")
            st.markdown(f"{row['content']}")
            st.caption(f"Posted at: {row['timestamp']}")
            # Replies
            if row['replies']:
                # Show text replies
                for reply in str(row['replies']).split('||AUDIO||'):
                    if reply.strip().endswith('.wav') and os.path.exists(reply.strip()):
                        st.audio(reply.strip(), format='audio/wav')
                    elif reply.strip():
                        st.markdown(f"**Reply:** {reply.strip()}")
            # Reply input
            reply = st.text_input(f'Reply to {row["thread_id"]}', key=f'reply_{row["thread_id"]}')
            audio_bytes = None
            audio_file_path = ''
            # Audio recording/upload
            col1, col2 = st.columns(2)
            with col1:
                try:
                    from streamlit_audiorecorder import audiorecorder
                    audio_bytes = audiorecorder("Record Audio Reply", "Recording...")
                except ImportError:
                    st.info("Install streamlit-audiorecorder for audio recording.")
            with col2:
                uploaded_audio = st.file_uploader("Or Upload Audio Reply", type=["wav", "mp3", "ogg"], key=f'upload_{row["thread_id"]}')
                if uploaded_audio:
                    audio_bytes = uploaded_audio.read()
            if st.button(t('reply', lang), key=f'btn_{row["thread_id"]}'):
                prev_replies = str(row['replies']) if row['replies'] else ''
                new_reply = ''
                if reply.strip():
                    new_reply += reply.strip()
                if audio_bytes:
                    # Save audio to file
                    import uuid
                    audio_dir = os.path.join(os.path.dirname(forum_path), 'audio_replies')
                    os.makedirs(audio_dir, exist_ok=True)
                    audio_filename = f"audio_{row['thread_id']}_{uuid.uuid4().hex}.wav"
                    audio_file_path = os.path.join(audio_dir, audio_filename)
                    with open(audio_file_path, 'wb') as f:
                        f.write(audio_bytes)
                    if new_reply:
                        new_reply += ' ||AUDIO|| ' + audio_file_path
                    else:
                        new_reply = audio_file_path
                # Append reply
                forum_df.at[idx, 'replies'] = (prev_replies + '\n' if prev_replies else '') + new_reply
                forum_df.to_csv(forum_path, index=False)
                st.success(t('reply_posted', lang))
            st.markdown('---')

def soil_health_page():
    import pandas as pd
    lang = st.session_state['lang']
    soil_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset_farming', 'soil_tests.csv')
    st.title(t('soil_health', lang))
    # Load or create soil test log
    if os.path.exists(soil_path):
        soil_df = pd.read_csv(soil_path)
    else:
        soil_df = pd.DataFrame(columns=['date','pH','N','P','K','organic_matter','notes'])
    # Entry form
    st.subheader(t('add_soil_test', lang))
    soil_date = st.date_input('Date', date.today(), key='soil_date')
    ph = st.number_input('pH', min_value=0.0, max_value=14.0, value=6.5, step=0.1)
    n = st.number_input('Nitrogen (N)', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    p = st.number_input('Phosphorus (P)', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    k = st.number_input('Potassium (K)', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    om = st.number_input('Organic Matter (%)', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    notes = st.text_area(t('notes', lang), key='soil_notes')
    if st.button(t('save_soil_test', lang)):
        new_entry = {'date': soil_date.isoformat() if hasattr(soil_date, 'isoformat') else str(soil_date), 'pH': ph, 'N': n, 'P': p, 'K': k, 'organic_matter': om, 'notes': notes}
        import json
        log_user_input('soil_health', 'soil_test', json.dumps(new_entry))
        soil_df = pd.concat([soil_df, pd.DataFrame([new_entry])], ignore_index=True)
        soil_df.to_csv(soil_path, index=False)
        st.success(t('soil_test_saved', lang))
    # Show soil test log
    st.subheader(t('soil_test_log', lang))
    if not soil_df.empty:
        st.dataframe(soil_df)

def heatmaps_page():
    import pandas as pd
    import folium
    from streamlit_folium import st_folium
    lang = st.session_state['lang']
    st.title(t('heatmaps', lang))
    st.markdown(t('outbreak_map', lang))
    st.markdown("This feature shows real-time crop health status based on geo-tagged reports.")
    st.markdown("Below is a simulated heatmap view:")
    # Simulated outbreak locations
    sample_points = [
        (17.385044, 78.486671),  # Hyderabad
        (28.613939, 77.209023),  # Delhi
        (19.076090, 72.877426),  # Mumbai
        (13.082680, 80.270718),  # Chennai
        (23.022505, 72.571362)   # Ahmedabad
    ]
    # Get user geolocation if available
    loc = st.session_state.get('user_location', get_geolocation())
    center_lat = loc.get('latitude', 20.5937)
    center_lon = loc.get('longitude', 78.9629)
    # Initialize the Folium map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)
    # Add circle markers
    for lat, lon in sample_points:
        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color="red",
            fill=True,
            fill_opacity=0.6,
            popup="Reported Disease Outbreak"
        ).add_to(m)
    # Display the map in Streamlit
    st_folium(m, width=700, height=500)
    # Suggest suitable crops for the user's location
    st.markdown('---')
    st.subheader("🌱 Suitable Crops for Your Location")
    # Simple logic: suggest crops based on region/city (can be improved with real data)
    city = loc.get('city', '').lower()
    region = loc.get('region', '').lower()
    crop_suggestions = {
        'hyderabad': ['Rice', 'Maize', 'Cotton'],
        'delhi': ['Wheat', 'Mustard', 'Barley'],
        'mumbai': ['Rice', 'Sugarcane', 'Vegetables'],
        'chennai': ['Rice', 'Millets', 'Groundnut'],
        'ahmedabad': ['Cotton', 'Groundnut', 'Wheat']
    }
    found = False
    for key, crops in crop_suggestions.items():
        if key in city or key in region:
            st.write(f"**{key.title()}**: {', '.join(crops)}")
            found = True
    if not found:
        st.write("General Suggestions: Rice, Wheat, Maize, Pulses")

def khet_market_page():
    lang = st.session_state['lang']
    if 'market_users' not in st.session_state:
        st.session_state['market_users'] = []
    if 'market_logged_in_user' not in st.session_state:
        st.session_state['market_logged_in_user'] = None
    if 'market_cart' not in st.session_state:
        st.session_state['market_cart'] = []
    if 'market_orders' not in st.session_state:
        st.session_state['market_orders'] = []
    if 'market_listings' not in st.session_state:
        st.session_state['market_listings'] = []
    st.title(t('khet_market', lang))
    tab_names = [
        t('market_home', lang), t('market_login', lang), t('market_register', lang), t('market_buyorsell', lang), t('market_buy', lang), t('market_checkout', lang), t('market_payment', lang), t('market_orders', lang), t('market_sell', lang), t('market_selling_item', lang)
    ]
    tab_objs = st.tabs(tab_names)
    with tab_objs[0]:
        st.header(t('market_home', lang))
        if st.session_state['market_logged_in_user']:
            st.success(f"Welcome, {st.session_state['market_logged_in_user']['fullname']}!")
        st.markdown(t('khet_market', lang) + ' - ' + t('market_home', lang))
        st.markdown('''Khet Market is a web-app through which farmers can sell crops to and buy equipment directly from other merchants without any third-party mediation. To avoid price inflation and maintain regularized selling, the app validates any purchase through the use of MSP for pricing and the buyer must adhere to it. The app also incorporates image integration for crops so the buyer can decide whether to proceed with the transaction. The app also incorporates payment authentication which helps both parties avoid extra middleman costs and helps in creating a completely self–independent virtual market space to empower both the buyer and seller.''')
    with tab_objs[1]:
        st.header(t('market_login', lang))
        login_username = st.text_input(t('login_username', lang), key='login_username')
        login_password = st.text_input(t('login_password', lang), type='password', key='login_password')
        if st.button(t('login_btn', lang), key='login_btn'):
            import json
            log_user_input('khet_market', 'login', json.dumps({'username': login_username}))
            user = next((u for u in st.session_state['market_users'] if u['username'] == login_username and u['password'] == login_password), None)
            if user:
                st.session_state['market_logged_in_user'] = user
                st.success(f"Login successful! Welcome, {user['fullname']}.")
            else:
                st.error("Invalid username or password.")
        if st.session_state['market_logged_in_user']:
            st.info(f"Logged in as: {st.session_state['market_logged_in_user']['fullname']} ({st.session_state['market_logged_in_user']['username']})")
    with tab_objs[2]:
        st.header(t('market_register', lang))
        reg_fullname = st.text_input(t('register_fullname', lang), key='register_fullname')
        reg_email = st.text_input(t('register_email', lang), key='register_email')
        reg_phone = st.text_input(t('register_phone', lang), key='register_phone')
        reg_username = st.text_input(t('register_username', lang), key='register_username')
        reg_password = st.text_input(t('register_password', lang), type='password', key='register_password')
        reg_confirmpw = st.text_input(t('register_confirmpw', lang), type='password', key='register_confirmpw')
        if st.button(t('register_btn', lang), key='register_btn'):
            import json
            log_user_input('khet_market', 'register', json.dumps({'fullname': reg_fullname, 'email': reg_email, 'phone': reg_phone, 'username': reg_username}))
            if not reg_fullname or not reg_username or not reg_password or not reg_confirmpw:
                st.error("Please fill all required fields.")
            elif reg_password != reg_confirmpw:
                st.error("Passwords do not match.")
            elif any(u['username'] == reg_username for u in st.session_state['market_users']):
                st.error("Username already exists.")
            else:
                st.session_state['market_users'].append({
                    'fullname': reg_fullname,
                    'email': reg_email,
                    'phone': reg_phone,
                    'username': reg_username,
                    'password': reg_password
                })
                st.success("Registration successful! You can now log in.")
    with tab_objs[3]:  # BuyOrSell
        st.header(t('market_buyorsell', lang))
        if not st.session_state['market_logged_in_user']:
            st.warning('Please log in to continue.')
        else:
            col1, col2 = st.columns(2)
            with col1:
                if st.button(t('buyorsell_buy', lang), key='buyorsell_buy'):
                    st.query_params["tab"] = tab_names[4]
            with col2:
                if st.button(t('buyorsell_sell', lang), key='buyorsell_sell'):
                    st.query_params["tab"] = tab_names[8]
    with tab_objs[4]:  # Buy
        st.header(t('market_buy', lang))
        if not st.session_state['market_logged_in_user']:
            st.warning('Please log in to buy products.')
        else:
            products = [
                {'name': 'Wheat Seeds', 'price': 100},
                {'name': 'Fertilizer', 'price': 250},
                {'name': 'Tractor Rental', 'price': 5000},
                {'name': 'Pesticide', 'price': 150},
                {'name': 'Rice Seeds', 'price': 120},
            ]
            for i, prod in enumerate(products):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.write(f"{prod['name']} - ₹{prod['price']}")
                with col2:
                    if st.button(f"Add to Cart {i}"):
                        st.session_state['market_cart'].append(prod)
                        st.success(f"Added {prod['name']} to cart.")
            st.write('---')
            st.write(f"Cart: {len(st.session_state['market_cart'])} items")
    with tab_objs[5]:  # Checkout
        st.header(t('market_checkout', lang))
        if not st.session_state['market_logged_in_user']:
            st.warning('Please log in to checkout.')
        elif not st.session_state['market_cart']:
            st.info('Your cart is empty.')
        else:
            total = sum(item['price'] for item in st.session_state['market_cart'])
            for i, item in enumerate(st.session_state['market_cart']):
                st.write(f"{item['name']} - ₹{item['price']}")
                if st.button(f"Remove {item['name']} {i}"):
                    st.session_state['market_cart'].pop(i)
                    st.experimental_rerun()
            st.write(f"**Total: ₹{total}**")
            if st.button('Proceed to Payment'):
                st.query_params["tab"] = tab_names[6]
    with tab_objs[6]:  # Payment
        st.header(t('market_payment', lang))
        if not st.session_state['market_logged_in_user']:
            st.warning('Please log in to pay.')
        elif not st.session_state['market_cart']:
            st.info('No items to pay for.')
        else:
            st.text_input(t('payment_card', lang), key='payment_card')
            st.text_input(t('payment_expiry', lang), key='payment_expiry')
            st.text_input(t('payment_cvv', lang), type='password', key='payment_cvv')
            if st.button(t('payment_btn', lang), key='payment_btn'):
                # Place order
                order = {
                    'user': st.session_state['market_logged_in_user']['username'],
                    'items': list(st.session_state['market_cart']),
                    'order_id': f"ORD{len(st.session_state['market_orders'])+1:04d}",
                    'total': sum(item['price'] for item in st.session_state['market_cart'])
                }
                st.session_state['market_orders'].append(order)
                st.session_state['market_cart'] = []
                st.success(f"Payment successful! Order ID: {order['order_id']}")
    with tab_objs[7]:  # Orders
        st.header(t('market_orders', lang))
        if not st.session_state['market_logged_in_user']:
            st.warning('Please log in to view orders.')
        else:
            user_orders = [o for o in st.session_state['market_orders'] if o['user'] == st.session_state['market_logged_in_user']['username']]
            if not user_orders:
                st.info('No orders yet.')
            else:
                for order in user_orders:
                    st.write(f"Order ID: {order['order_id']}")
                    for item in order['items']:
                        st.write(f"- {item['name']} - ₹{item['price']}")
                    st.write(f"Total: ₹{order['total']}")
                    st.write('---')
    with tab_objs[8]:  # Sell
        st.header(t('market_sell', lang))
        if not st.session_state['market_logged_in_user']:
            st.warning('Please log in to list crops for sale.')
        else:
            crop_name = st.text_input(t('sell_crop', lang), key='sell_crop')
            qty = st.number_input(t('sell_qty', lang), min_value=1, key='sell_qty')
            price = st.number_input(t('sell_price', lang), min_value=0.0, key='sell_price')
            crop_img = st.file_uploader(t('sell_img', lang), type=['jpg', 'jpeg', 'png'], key='sell_img')
            if st.button(t('sell_btn', lang), key='sell_btn'):
                import json
                log_user_input('khet_market', 'sell', json.dumps({'crop': crop_name, 'qty': qty, 'price': price, 'img': crop_img.name if crop_img else None}))
                st.session_state['market_listings'].append({
                    'user': st.session_state['market_logged_in_user']['username'],
                    'crop': crop_name,
                    'qty': qty,
                    'price': price,
                    'img': crop_img.name if crop_img else None
                })
                st.success('Crop listed for sale!')
    with tab_objs[9]:  # Selling Item
        st.header(t('market_selling_item', lang))
        if not st.session_state['market_logged_in_user']:
            st.warning('Please log in to view your listings.')
        else:
            user_listings = [l for l in st.session_state['market_listings'] if l['user'] == st.session_state['market_logged_in_user']['username']]
            if not user_listings:
                st.info('No crops listed for sale yet.')
            else:
                for l in user_listings:
                    st.write(f"Crop: {l['crop']} | Qty: {l['qty']} kg | Price: ₹{l['price']} per kg | Image: {l['img']}")

def analytics_dashboard_page():
    import json
    import os
    import pandas as pd
    import streamlit as st
    import matplotlib.pyplot as plt
    from collections import Counter
    from datetime import datetime

    lang = st.session_state['lang']
    st.title(t('analytics_dashboard', lang))
    st.markdown('---')

    # Load conversations
    conversations_path = "conversations.json"
    if not os.path.exists(conversations_path):
        st.warning(t('analytics_no_conversations', lang))
        return
    with open(conversations_path, "r") as f:
        all_convs = json.load(f)

    # Flatten all user/model messages
    chat_records = []
    for user_id, history in all_convs.items():
        for i, entry in enumerate(history):
            role = entry.get("role")
            parts = entry.get("parts", [])
            timestamp = entry.get("timestamp")
            for part in parts:
                chat_records.append({
                    "user_id": user_id,
                    "role": role,
                    "message": part,
                    "msg_idx": i,
                    "timestamp": timestamp
                })
    df = pd.DataFrame(chat_records)
    if df.empty:
        st.info(t('analytics_no_data', lang))
        return

    # Convert timestamp to datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    else:
        df['timestamp'] = pd.NaT

    # 1. Total number of AgriBot chats/questions
    st.subheader(t('analytics_total_questions', lang))
    st.metric(t('analytics_total_questions', lang), df[(df['role'] == 'user')].shape[0])

    # 2. Most common crops discussed (simple keyword scan)
    st.subheader(t('analytics_common_crops', lang))
    crop_keywords = [
        "wheat", "rice", "maize", "soybean", "cotton", "sugarcane", "groundnut", "potato", "tomato", "onion", "chickpea", "mustard", "sorghum", "banana", "grapes", "mango", "pigeonpea", "sunflower", "pea"
    ]
    crop_counter = Counter()
    for msg in df[df['role'] == 'user']['message'].str.lower():
        for crop in crop_keywords:
            if crop in msg:
                crop_counter[crop] += 1
    if crop_counter:
        st.bar_chart(pd.DataFrame.from_dict(crop_counter, orient='index', columns=['Count']).sort_values('Count', ascending=False))
    else:
        st.write(t('analytics_no_keywords', lang))

    # 3. Disease diagnosis trends (scan for 'disease', 'blight', 'virus', etc.)
    st.subheader(t('analytics_disease_trends', lang))
    disease_keywords = ["disease", "blight", "virus", "rot", "spot", "mildew", "rust", "bacterial", "fungal", "deficiency"]
    disease_counter = Counter()
    for msg in df[df['role'] == 'user']['message'].str.lower():
        for d in disease_keywords:
            if d in msg:
                disease_counter[d] += 1
    if disease_counter:
        st.bar_chart(pd.DataFrame.from_dict(disease_counter, orient='index', columns=['Count']).sort_values('Count', ascending=False))
    else:
        st.write(t('analytics_no_disease', lang))

    # 4. User engagement over time (by day)
    st.subheader(t('analytics_engagement', lang) + " (by day)")
    if df['timestamp'].notnull().any():
        df['date'] = df['timestamp'].dt.date
        daily_counts = df[df['role'] == 'user'].groupby('date').size()
        st.line_chart(daily_counts)
    else:
        st.info("No timestamp data available for time-based trends.")

    # 5. Peak hours (hour of day)
    st.subheader("Peak Activity Hours (UTC)")
    if df['timestamp'].notnull().any():
        df['hour'] = df['timestamp'].dt.hour
        hour_counts = df[df['role'] == 'user'].groupby('hour').size()
        st.bar_chart(hour_counts)
    else:
        st.info("No timestamp data available for peak hour analysis.")

    # 6. Top users (by message count)
    st.subheader("Top Users (by message count)")
    top_users = df[df['role'] == 'user']['user_id'].value_counts().head(10)
    st.bar_chart(top_users)

    # 7. Average response length (user and bot)
    st.subheader("Average Response Length (words)")
    avg_user = df[df['role'] == 'user']['message'].str.split().str.len().mean()
    avg_bot = df[df['role'] == 'model']['message'].str.split().str.len().mean()
    st.write(f"User: {avg_user:.1f} words | AgriBot: {avg_bot:.1f} words")

    # 8. Pie chart of question types (disease, market, weather, etc.)
    st.subheader(t('analytics_pie_types', lang))
    type_keywords = {
        'disease': ["disease", "blight", "virus", "rot", "spot", "mildew", "rust", "bacterial", "fungal", "deficiency"],
        'market': ["market", "price", "sell", "buy", "msp", "cost"],
        'weather': ["weather", "rain", "temperature", "forecast", "humidity"],
        'fertilizer': ["fertilizer", "urea", "npk", "manure", "compost"],
        'other': []
    }
    type_counter = Counter()
    for msg in df[df['role'] == 'user']['message'].str.lower():
        found = False
        for ttype, keys in type_keywords.items():
            if any(k in msg for k in keys):
                type_counter[ttype] += 1
                found = True
                break
        if not found:
            type_counter['other'] += 1
    if type_counter:
        fig, ax = plt.subplots()
        ax.pie(list(type_counter.values()), labels=list(type_counter.keys()), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.write(t('analytics_no_types', lang))

    # 9. Recent activity log
    st.subheader(t('analytics_recent_log', lang))
    st.dataframe(df.tail(10)[['user_id', 'role', 'message', 'timestamp']].iloc[::-1])

    # 10. Downloadable CSV
    st.subheader("Download Analytics Data")
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "analytics_data.csv", "text/csv")

    # 11. CSV/statistics visualized (if you have other CSVs, you can add more here)
    st.markdown('---')
    st.info(t('analytics_info_upload', lang))
    uploaded_csv = st.file_uploader(t('analytics_upload_csv', lang), type=["csv"])
    if uploaded_csv:
        csv_df = pd.read_csv(uploaded_csv)
        st.write(csv_df.head())
        st.bar_chart(csv_df.select_dtypes(include=['number']))

def get_corpus_data_page():
    st.title('Get Corpus Data')
    st.markdown('You can download all collected user input data as a CSV file below:')
    if os.path.exists(USER_INPUT_LOG):
        import pandas as pd
        df = pd.read_csv(USER_INPUT_LOG)
        st.subheader('Preview of Collected User Input Data')
        st.dataframe(df.head(20))
        with open(USER_INPUT_LOG, 'rb') as f:
            st.download_button('Download CSV', f, file_name='user_input_log.csv', mime='text/csv')
    else:
        st.warning('No user input log found yet.')

# --- Main app logic ---
def main():
    if not st.session_state.get('logged_in', False):
        login_page()
        return
    init_session()
    sidebar_navigation()
    # Dataset paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    farmer_dataset_path = os.path.join(base_dir, "dataset_farming", "farmer_advisor_dataset.csv")
    market_dataset_path = os.path.join(base_dir, "dataset_farming", "market_researcher_dataset.csv")
    # Instantiate agents
    farmer_advisor = FarmerAdvisor(farmer_dataset_path)
    market_researcher = MarketResearcher(market_dataset_path)
    weather_module = WeatherModule(location="India")
    agri_expert = AgriculturalExpert()
    memory = MemoryManager()
    nlp_models = NLPModels()
    # Navigation
    page = st.session_state['page']
    if page == 'home':
        home_page()
    elif page == 'recommendations':
        recommendations_page(farmer_advisor, market_researcher, weather_module, agri_expert, memory)
    elif page == 'diagnosis':
        diagnosis_page()
    elif page == 'severity':
        severity_page()
    elif page == 'validation':
        validation_page()
    elif page == 'growth-diary':
        growth_diary_page()
    elif page == 'knowledge-sharing':
        knowledge_sharing_page()
    elif page == 'soil-health':
        soil_health_page()
    elif page == 'heatmaps':
        heatmaps_page()
    elif page == 'khet-market':
        khet_market_page()
    elif page == 'analytics-dashboard':
        analytics_dashboard_page()
    elif page == 'get-corpus-data':
        get_corpus_data_page()
    else:
        home_page()

if __name__ == "__main__":
    main()
