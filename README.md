# 🌾 Crop Knowledge Explorer

A multilingual Flask web application that displays crop data in multiple languages (English, Tamil, Telugu, Hindi, Kannada).

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open your browser to: http://localhost:5000
```

### Render Deployment
1. **Build Command**: `pip install -r requirements.txt`
2. **Start Command**: `gunicorn app:app`
3. **Python Version**: 3.10+

## 📁 Project Structure
```
Organixnatura/
├── app.py                    # Flask backend
├── requirements.txt          # Python dependencies
├── crops_data.json          # Crop data (JSON format)
├── templates/
│   └── index.html           # Main frontend HTML
└── static/
    ├── style.css            # CSS styles
    └── script.js            # Frontend JavaScript
```

## 🌐 Features
- **Multilingual Support**: English, Tamil, Telugu, Hindi, Kannada
- **6 Categories**: Fruits, Vegetables, Greens, Tubers, Herbal, Units
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Language Switching**: Instant UI updates
- **Clean Data Display**: No duplicates or missing values

## 🛠️ Technology Stack
- **Backend**: Flask, Flask-CORS
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Data**: JSON format
- **Deployment**: Gunicorn, Render.com

## 📊 Data Structure
The application reads from `crops_data.json` with the following structure:
```json
{
  "Fruits": [
    {"English": "Papaya", "Tamil": "பப்பாளி"},
    {"English": "Banana", "Tamil": "வாழை"}
  ],
  "Vegetables": [...],
  "Greens": [...],
  "Tubers": [...],
  "Herbal": [...],
  "Units": [...]
}
```

## 🔧 API Endpoints
- `GET /` - Main web interface
- `GET /data` - JSON crop data
- `GET /categories` - Available categories and counts
- `GET /health` - Health check for deployment

## 📱 Usage
1. Select a language from the top buttons
2. Choose a category (Fruits, Vegetables, etc.)
3. View crops in the selected language
4. Use "Back to Categories" to return to category selection

## 🌍 Language Support
- **English**: Full crop names in English
- **Tamil**: Full crop names in Tamil
- **Telugu/Hindi/Kannada**: UI in selected language, with message for crop data

## 🚀 Deployment Instructions

### For Render.com:
1. **Create a GitHub repository** with this project
2. **Connect to Render**:
   - New → Web Service
   - Connect your GitHub repository
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: 3.10+
3. **Deploy** and get your live URL!

### For Local Testing:
```bash
# Clone the repository
git clone <your-repo-url>
cd Organixnatura

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

## 📝 License
This project is open source and available under the MIT License.

## 🤝 Contributing
Feel free to submit issues and enhancement requests!

---
**Built with ❤️ for agricultural knowledge sharing**