# Krishi Sakhi (കൃഷി സഖി) - Enhanced AI-Powered Farming Assistant

## 🌾 Overview

**Krishi Sakhi** (Agricultural Friend) is an enhanced Python-based web application designed specifically for smallholder farmers in Kerala, India. The application provides hyper-localized, personalized agricultural advice by leveraging geospatial data and AI-powered analysis with a beautiful multilingual interface.

### 🆕 Latest Enhancements

#### 1. **Agricultural-Themed Background Design**
- **Blurred Agricultural Backgrounds**: Real farm images from Unsplash with blur effects for better readability
- **Semi-transparent Overlays**: Glass morphism design with backdrop filters
- **Responsive Visual Elements**: Adapts to different screen sizes and maintains visual appeal

#### 2. **Multilingual Support**
- **Language Toggle**: Easy switch between English (default) and Malayalam
- **Persistent Language Settings**: User's language choice is remembered across sessions  
- **Complete Translation**: All UI elements, labels, and messages are fully localized

#### 3. **Enhanced UI/UX**
- **Modern Card Design**: Glass morphism effects with agricultural color schemes
- **Interactive Animations**: Smooth transitions, hover effects, and loading animations
- **Progress Indicators**: Visual progress bars for nutrient levels and analysis steps
- **Step-by-Step Guidance**: Clear visual indicators for the farm profiling process

## 🚀 Key Features

### Core Functionality
✅ **Location-Based Analysis** | സ്ഥാന അടിസ്ഥാനത്തിലുള്ള വിശകലനം  
✅ **Soil Health Assessment** | മണ്ണിന്റെ ആരോഗ്യ വിലയിരുത്തൽ  
✅ **Vegetation Monitoring** | സസ്യ നിരീക്ഷണം  
✅ **Groundwater Information** | ഭൂഗർഭജല വിവരങ്ങൾ  
✅ **Multilingual Interface** | മൾട്ടിലിംഗ്വൽ ഇന്റർഫേസ്  
✅ **Interactive Maps** | ഇന്ററാക്ടീവ് മാപ്പുകൾ  

### Enhanced Visual Features
🎨 **Agricultural Background Imagery** - Blurred farm landscapes for immersive experience  
🌐 **Language Toggle Buttons** - Flag-based switcher (🇬🇧 English / 🇮🇳 മലയാളം)  
📊 **Animated Progress Bars** - Visual nutrient level indicators  
💨 **Smooth Animations** - Fade-in, slide-up effects throughout the interface  
🔄 **Loading Indicators** - Custom spinner with agricultural themes  

## 📁 Project Structure

`
krishi-sakhi/
│
├── README.md                    # Enhanced documentation
├── requirements.txt             # Python dependencies
├── app.py                      # Main application (Enhanced Welcome Page)
├── .streamlit/
│   └── config.toml             # Streamlit configuration with agricultural theme
├── pages/
│   └── 1_Farm_Profile.py       # Enhanced Farm profiling page
├── utils/
│   ├── __init__.py
│   ├── geo_utils.py           # Geographic calculations
│   ├── data_utils.py          # Data formatting & mock API
│   └── language_utils.py      # 🆕 Multilingual support utilities
└── assets/
    └── styles.css             # 🆕 Enhanced CSS with agricultural backgrounds
`

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10 or newer
- Internet connection (for background images and map tiles)

### Quick Start

1. **Navigate to project directory:**
   `ash
   cd V:\vishnu\random\hackathons\SIH\clo2\2front
   `

2. **Install dependencies:**
   `ash
   pip install -r requirements.txt
   `

3. **Launch the application:**
   `ash
   streamlit run app.py
   `

4. **Access the enhanced interface:**
   Open http://localhost:8501 in your browser

## 🌍 Multilingual Features

### Language Toggle
- **Default Language**: English (en)
- **Secondary Language**: Malayalam (ml) - മലയാളം
- **Toggle Location**: Sidebar with flag buttons (🇬🇧 / 🇮🇳)
- **Persistence**: Language choice saved in session state

### Supported Languages
`python
# Language codes and display names
'en': English - Complete interface translation
'ml': മലയാളം - Full Malayalam localization
`

## 🎨 Visual Design Elements

### Background Images
The application uses curated agricultural images from Unsplash:

1. **Main Background**: Farm landscape with rice fields
   - URL: photo-1574323347407-f5e1ad6d020b (Unsplash)
   - Effect: Blurred overlay with 95% opacity gradient

2. **Header Sections**: Green crop fields
   - URL: photo-1500937386664-56d1dfef3854 (Unsplash)
   - Effect: Semi-transparent overlay with backdrop blur

3. **Footer Areas**: Agricultural equipment and farmland
   - URL: photo-1523741543316-beb7fc7023d8 (Unsplash)
   - Effect: Dark overlay for contrast with white text

### CSS Enhancements
`css
/* Example: Agricultural background with blur effect */
.stApp {
    background: linear-gradient(
        135deg, 
        rgba(245, 247, 250, 0.95) 0%, 
        rgba(195, 207, 226, 0.95) 100%
    ),
    url('https://images.unsplash.com/photo-1574323347407...');
    background-size: cover;
    background-attachment: fixed;
    backdrop-filter: blur(8px);
}
`

## 📊 Enhanced User Experience

### Interactive Elements
- **Animated Cards**: Hover effects with subtle shadows and transforms
- **Progress Bars**: Color-coded nutrient levels with shimmer animations
- **Step Indicators**: Visual progress through the analysis process
- **Loading Animations**: Custom spinners with agricultural branding

### Responsive Design
- **Desktop**: Full-width layout with sidebar navigation
- **Mobile**: Responsive columns and touch-friendly controls
- **Accessibility**: High contrast ratios and readable font sizes

## 🔧 Technical Implementation

### Language Management (utils/language_utils.py)
`python
def get_text(key):
    """Get text for current language"""
    lang = get_language()
    return LANGUAGES[lang].get(key, f"[{key}]")

def language_toggle():
    """Display language toggle in sidebar"""
    # Flag-based button implementation
`

### Enhanced Styling (ssets/styles.css)
- **CSS Variables**: Consistent color scheme
- **Backdrop Filters**: Modern blur effects
- **Keyframe Animations**: Smooth transitions
- **Media Queries**: Mobile-responsive breakpoints

## 🌾 Farm Analysis Features

### Enhanced Analysis Display
1. **Visual Metrics**: Large, colorful cards with agricultural icons
2. **Nutrient Progress Bars**: Animated indicators for N-P-K levels
3. **Expandable Sections**: Detailed soil properties in collapsible cards
4. **Recommendation Lists**: Step-by-step guidance with visual priorities

### Sample Output
`
🌾 Farm Analysis Report | ഫാം വിശകലന റിപ്പോർട്ട് 🌾

📍 Location: 10.8505, 76.2711 | 🏞️ Area: 2.5 acres

🌱 Soil Type: Sandy Loam | മണൽ കലർന്ന പശിമരാശി മണ്ണ്
💧 Groundwater: 15 meters | 15 മീറ്റർ  
🌿 Vegetation Health: Healthy | ആരോഗ്യകരമായ സസ്യങ്ങൾ
`

## 🚀 Future Enhancements

### Planned Features
1. **More Languages**: Tamil, Telugu, Hindi support
2. **Offline Mode**: PWA capabilities for rural connectivity
3. **Voice Interface**: Speech recognition in local languages
4. **AR Visualization**: Crop health overlay using device camera
5. **Community Features**: Farmer forums and knowledge sharing

## 🤝 Contributing

### Development Guidelines
1. **Language Files**: Add new languages to utils/language_utils.py
2. **CSS Styling**: Follow existing class naming conventions
3. **Image Assets**: Use high-quality, royalty-free agricultural images
4. **Accessibility**: Ensure WCAG 2.1 AA compliance
5. **Mobile Testing**: Test on various screen sizes

### Code Style
- **Python**: PEP 8 compliance with type hints
- **CSS**: BEM methodology for class names
- **JavaScript**: ES6+ features where applicable

## 📝 License & Attribution

### Image Credits
- Background images courtesy of [Unsplash](https://unsplash.com)
- Agricultural photography by various contributors
- All images used under Unsplash License

### Software License
This project is developed for educational and agricultural development purposes. Please ensure proper attribution when using or extending this codebase.

## 📞 Support & Contact

For technical issues or feature requests:
- Create an issue in the project repository
- Provide detailed description with screenshots
- Include language preference (English/Malayalam)

---

**🌾 Krishi Sakhi - Empowering Kerala's Farmers with AI-Driven Agricultural Intelligence 🌾**

*Developed with ❤️ for the farming community of Kerala*
