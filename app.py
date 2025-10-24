#!/usr/bin/env python3
"""
Crop Knowledge Explorer - Flask Web Application
===============================================

A multilingual Flask web application that displays crop data in multiple languages.

Local Development:
    pip install -r requirements.txt
    python app.py

Render Deployment:
    Build Command: pip install -r requirements.txt
    Start Command: gunicorn app:app

Author: Organixnatura
"""

import json
import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variable to store crop data
crop_data = {}

def clean_and_validate_crop_data(raw_data):
    """Clean and validate crop data, fix category assignments"""
    print("🧹 Starting data cleaning and validation...")
    
    # Define correct category mappings
    correct_categories = {
        "Fruits": ["Papaya", "Banana", "Guava", "Pomegranate"],
        "Vegetables": ["Brinjal", "Bitter Gourd", "Bottle Gourd", "Pumpkin", "Bhendi (Okra)", "Carrot", "Cabbage", "Cauliflower", "Beans", "Beetroot", "Broccoli", "Moringa"],
        "Greens": ["Palak", "Amaranthus", "Lettuce", "Spinach"],
        "Tubers": ["Potato", "Sweet Potato", "Cassava"],
        "Herbal": ["Ashwagandha", "Aloe Vera", "Tulsi", "Curry Leaves", "Fenugreek", "Vetiver", "Coriander"],
        "Units": ["Vermicompost Unit", "Poultry Unit", "Goat Unit", "Dairy Unit", "Azolla Unit"]
    }
    
    # Create reverse mapping for quick lookup
    crop_to_category = {}
    for category, crops in correct_categories.items():
        for crop in crops:
            crop_to_category[crop] = category
    
    cleaned_data = {category: [] for category in correct_categories.keys()}
    warnings = []
    
    # Process each category in raw data
    for category, crops in raw_data.items():
        if category not in correct_categories:
            print(f"⚠️ Removing unexpected category: {category}")
            continue
            
        for crop in crops:
            # Skip invalid entries
            if not crop.get('English') or crop.get('English') in ['nan', '', category]:
                continue
                
            crop_name = crop.get('English', '').strip()
            if not crop_name:
                continue
                
            # Check if crop is in correct category
            if crop_name in crop_to_category:
                correct_category = crop_to_category[crop_name]
                if correct_category != category:
                    warnings.append(f"⚠️ Moving {crop_name} from {category} to {correct_category}")
                    cleaned_data[correct_category].append(crop)
                else:
                    cleaned_data[category].append(crop)
            else:
                # Log unknown crops with console warning
                print(f"⚠️ Unknown crop: {crop_name} under {category}")
                warnings.append(f"⚠️ Unknown crop: {crop_name} under {category}")
                # Try to find a reasonable category for unrecognized crops
                if any(keyword in crop_name.lower() for keyword in ['unit', 'farm']):
                    cleaned_data['Units'].append(crop)
                else:
                    # Skip unknown crops that don't match any pattern
                    print(f"⚠️ Skipping unknown crop: {crop_name}")
                    continue
    
    # Print warnings
    for warning in warnings:
        print(warning)
    
    # Log final results
    print("✅ Final Categories:", list(cleaned_data.keys()))
    for category, crops in cleaned_data.items():
        print(f"📊 {category}: {len(crops)} crops")
        for crop in crops:
            print(f"  - {crop.get('English', 'Unknown')}")
    
    return cleaned_data

def load_crop_data():
    """Load crop data from JSON file with debug info"""
    global crop_data

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(base_dir, "crops_data.json")

        print(f"🔍 Looking for JSON at: {json_file}")
        print(f"📁 File exists: {os.path.exists(json_file)}")

        if not os.path.exists(json_file):
            print(f"⚠️ Warning: {json_file} not found! Using sample data.")
            return {}

        with open(json_file, "r", encoding="utf-8") as f:
            print("📖 Reading JSON file...")
            raw_data = json.load(f)
            print("✅ JSON file loaded successfully.")

        # Clean and validate the data
        data = clean_and_validate_crop_data(raw_data)
        
        total_items = sum(len(v) for v in data.values())
        print(f"📊 Loaded {total_items} total crop entries across {len(data)} categories.")

        crop_data = data
        return data

    except Exception as e:
        print(f"❌ Error loading crop data: {e}")
        return {}


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/data')
def get_data():
    """API endpoint to get crop data"""
    if not crop_data:
        print("🔄 Reloading crop data...")
        load_crop_data()
    return jsonify(crop_data)

@app.route('/categories')
def get_categories():
    """API endpoint to get available categories"""
    if not crop_data:
        load_crop_data()
    return jsonify({
        "categories": list(crop_data.keys()),
        "counts": {cat: len(items) for cat, items in crop_data.items()}
    })

@app.route('/crop/<crop_name>')
def get_crop_details(crop_name):
    """API endpoint to get detailed information for a specific crop"""
    if not crop_data:
        load_crop_data()
    
    # Search for the crop across all categories
    for category, crops in crop_data.items():
        for crop in crops:
            # Check if the crop name matches (case-insensitive)
            if (crop.get('English', '').lower() == crop_name.lower() or 
                crop.get('Tamil', '').lower() == crop_name.lower()):
                
                # Get translations for all languages (try from data first, then fallback to translation)
                english_name = crop.get('English', '')
                
                # Get existing translations from data
                tamil_name = crop.get('Tamil', '')
                telugu_name = crop.get('Telugu', '')
                hindi_name = crop.get('Hindi', '')
                kannada_name = crop.get('Kannada', '')
                malayalam_name = crop.get('Malayalam', '')
                
                # If translations are missing or empty, get them from translation functions
                if not telugu_name or telugu_name.strip() == '':
                    telugu_name = get_telugu_translation(english_name)
                if not hindi_name or hindi_name.strip() == '':
                    hindi_name = get_hindi_translation(english_name)
                if not kannada_name or kannada_name.strip() == '':
                    kannada_name = get_kannada_translation(english_name)
                if not malayalam_name or malayalam_name.strip() == '':
                    malayalam_name = get_malayalam_translation(english_name)
                
                # Create detailed crop information
                crop_details = {
                    "name": english_name,
                    "tamil_name": tamil_name,
                    "category": category,
                    "languages": {
                        "English": english_name,
                        "Tamil": tamil_name,
                        "Telugu": telugu_name,
                        "Hindi": hindi_name,
                        "Kannada": kannada_name,
                        "Malayalam": malayalam_name
                    },
                    "botanical_name": crop.get('BOTANICAL NAME', 'Not available'),
                    "image_path": get_crop_image_path(english_name, category)
                }
                
                # Debug logging
                print(f"🌾 Crop: {english_name}")
                print(f"📁 Category: {category}")
                print(f"🖼️ Image path: {crop_details['image_path']}")
                print(f"🌍 Languages: {crop_details['languages']}")
                
                return jsonify(crop_details)
    
    # If crop not found
    return jsonify({"error": "Crop not found"}), 404

def get_telugu_translation(english_name):
    """Get Telugu translation for crop names"""
    telugu_translations = {
        "Papaya": "బొప్పాయి",
        "Banana": "అరటి",
        "Guava": "జామ",
        "Mango": "మామిడి",
        "Coconut": "కొబ్బరి",
        "Pineapple": "అనాస",
        "Orange": "నారింజ",
        "Lemon": "నిమ్మ",
        "Grape": "ద్రాక్ష",
        "Pomegranate": "దానిమ్మ",
        "Apple": "ఆపిల్",
        "Sweet Potato": "చిలకడదుంప",
        "Potato": "బంగాళదుంప",
        "Onion": "ఉల్లి",
        "Tomato": "టమాట",
        "Carrot": "క్యారెట్",
        "Beetroot": "బీట్ రూట్",
        "Radish": "ముల్లంగి",
        "Cabbage": "కోసుకూర",
        "Cauliflower": "కాలీఫ్లవర్",
        "Spinach": "పాలకూర",
        "Coriander": "కొత్తిమీర",
        "Mint": "పుదీన",
        "Curry Leaves": "కరివేపాకు",
        "Drumstick": "మునగ",
        "Brinjal": "వంకాయ",
        "Okra": "బెండకాయ",
        "Cucumber": "దోసకాయ",
        "Bottle Gourd": "సొరకాయ",
        "Ridge Gourd": "బీరకాయ",
        "Bitter Gourd": "కాకరకాయ",
        "Snake Gourd": "పొట్లకాయ",
        "Ash Gourd": "బుడిదకాయ",
        "Pumpkin": "గుమ్మడికాయ",
        "Green Chilli": "పచ్చిమిర్చి",
        "Red Chilli": "ఎర్రమిర్చి",
        "Ginger": "అల్లం",
        "Garlic": "వెల్లుల్లి",
        "Turmeric": "పసుపు",
        "Cardamom": "ఏలకులు",
        "Cinnamon": "దాల్చినచెక్క",
        "Clove": "లవంగం",
        "Pepper": "మిరియాలు",
        "Cumin": "జీలకర్ర",
        "Fennel": "సోంపు",
        "Fenugreek": "మెంతులు",
        "Mustard": "ఆవాలు",
        "Sesame": "నువ్వులు",
        "Groundnut": "వేరుశెనగ",
        "Sunflower": "పొద్దుతిరుగుడు",
        "Soybean": "సోయాబీన్",
        "Black Gram": "మినుములు",
        "Green Gram": "పెసలు",
        "Red Gram": "కంది",
        "Bengal Gram": "శనగలు",
        "Horse Gram": "ఉలవులు",
        "Cowpea": "బొబ్బర్లు",
        "Rice": "వరి",
        "Wheat": "గోధుమలు",
        "Maize": "మొక్కజొన్న",
        "Barley": "యవలు",
        "Millet": "సజ్జలు",
        "Sorghum": "జొన్నలు",
        "Ragi": "రాగులు",
        "Bajra": "సజ్జలు",
        "Jowar": "జొన్నలు",
        "Kodo": "కోడో",
        "Little Millet": "సామలు",
        "Foxtail Millet": "కొర్రలు",
        "Barnyard Millet": "ఊదలు",
        "Proso Millet": "వరిగలు",
        "Finger Millet": "రాగులు",
        "Pearl Millet": "సజ్జలు",
        "Teff": "టెఫ్",
        "Quinoa": "క్వినోవా",
        "Amaranth": "తోటకూర",
        "Buckwheat": "బక్వీట్",
        "Oats": "ఓట్స్",
        "Rye": "రై",
        "Triticale": "ట్రిటికేల్",
        "Spelt": "స్పెల్ట్",
        "Kamut": "కముత్",
        "Emmer": "ఎమ్మర్",
        "Einkorn": "ఐన్కోర్న్",
        "Freekeh": "ఫ్రీకె",
        "Bulgur": "బుల్గర్",
        "Couscous": "కౌస్కస్",
        "Farro": "ఫారో",
        "Wheat Berries": "గోధుమ బెర్రీలు",
        "Brown Rice": "గోధుమ రంగు వరి",
        "Wild Rice": "కాడు వరి",
        "Red Rice": "ఎరుపు వరి",
        "Black Rice": "నలుపు వరి",
        "Purple Rice": "ఊదా వరి",
        "Jasmine Rice": "జాస్మిన్ వరి",
        "Basmati Rice": "బాస్మతి వరి",
        "Arborio Rice": "ఆర్బోరియో వరి",
        "Sushi Rice": "సుషి వరి",
        "Sticky Rice": "అతుకుతున్న వరి",
        "Long Grain Rice": "పొడవైన వరి",
        "Short Grain Rice": "చిన్న వరి",
        "Medium Grain Rice": "మధ్యస్థ వరి",
        "Parboiled Rice": "ఉడికించిన వరి",
        "Converted Rice": "మార్చిన వరి",
        "Instant Rice": "తక్షణ వరి",
        "Precooked Rice": "ముందుగా వండిన వరి",
        "Frozen Rice": "గడ్డకట్టిన వరి",
        "Canned Rice": "క్యాన్ చేసిన వరి",
        "Rice Flour": "వరి పిండి",
        "Rice Bran": "వరి తవుడు",
        "Rice Husk": "వరి చోళం",
        "Rice Starch": "వరి స్టార్చ్",
        "Rice Syrup": "వరి సిరప్",
        "Rice Vinegar": "వరి వినెగర్",
        "Rice Wine": "వరి వైన్",
        "Rice Paper": "వరి కాగితం",
        "Rice Noodles": "వరి నూడిల్స్",
        "Rice Cakes": "వరి కేకులు",
        "Rice Pudding": "వరి పుడ్డింగ్",
        "Rice Milk": "వరి పాలు",
        "Rice Cream": "వరి క్రీమ్",
        "Rice Butter": "వరి వెన్న",
        "Rice Oil": "వరి నూనె",
        "Rice Protein": "వరి ప్రోటీన్",
        "Rice Fiber": "వరి ఫైబర్",
        "Rice Antioxidants": "వరి ఆంటీఆక్సిడెంట్స్",
        "Rice Vitamins": "వరి విటమిన్లు",
        "Rice Minerals": "వరి ఖనిజాలు",
        "Rice Amino Acids": "వరి అమైనో ఆసిడ్లు",
        "Rice Enzymes": "వరి ఎంజైమ్లు",
        "Rice Probiotics": "వరి ప్రోబయోటిక్స్",
        "Rice Prebiotics": "వరి ప్రీబయోటిక్స్",
        "Rice Postbiotics": "వరి పోస్ట్బయోటిక్స్",
        "Rice Synbiotics": "వరి సిన్బయోటిక్స్",
        "Rice Psychobiotics": "వరి సైకోబయోటిక్స్",
        "Rice Metabiotics": "వరి మెటాబయోటిక్స్",
        "Rice Parabiotics": "వరి పారాబయోటిక్స్",
        "Rice Eubiotics": "వరి యూబయోటిక్స్",
        "Rice Dysbiotics": "వరి డిస్బయోటిక్స్",
        "Rice Antibiotics": "వరి ఆంటీబయోటిక్స్"
    }
    
    return telugu_translations.get(english_name, english_name)

def get_hindi_translation(english_name):
    """Get Hindi translation for crop names"""
    hindi_translations = {
        "Papaya": "पपीता",
        "Banana": "केला",
        "Guava": "अमरूद",
        "Mango": "आम",
        "Coconut": "नारियल",
        "Pineapple": "अनानास",
        "Orange": "संतरा",
        "Lemon": "नींबू",
        "Grape": "अंगूर",
        "Pomegranate": "अनार",
        "Apple": "सेब",
        "Sweet Potato": "शकरकंद",
        "Potato": "आलू",
        "Onion": "प्याज",
        "Tomato": "टमाटर",
        "Carrot": "गाजर",
        "Beetroot": "चुकंदर",
        "Radish": "मूली",
        "Cabbage": "पत्ता गोभी",
        "Cauliflower": "फूल गोभी",
        "Spinach": "पालक",
        "Coriander": "धनिया",
        "Mint": "पुदीना",
        "Curry Leaves": "करी पत्ता",
        "Drumstick": "सहजन",
        "Brinjal": "बैंगन",
        "Okra": "भिंडी",
        "Cucumber": "खीरा",
        "Bottle Gourd": "लौकी",
        "Ridge Gourd": "तोरी",
        "Bitter Gourd": "करेला",
        "Snake Gourd": "चिचिंडा",
        "Ash Gourd": "पेठा",
        "Pumpkin": "कद्दू",
        "Green Chilli": "हरी मिर्च",
        "Red Chilli": "लाल मिर्च",
        "Ginger": "अदरक",
        "Garlic": "लहसुन",
        "Turmeric": "हल्दी",
        "Cardamom": "इलायची",
        "Cinnamon": "दालचीनी",
        "Clove": "लौंग",
        "Pepper": "काली मिर्च",
        "Cumin": "जीरा",
        "Fennel": "सौंफ",
        "Fenugreek": "मेथी",
        "Mustard": "सरसों",
        "Sesame": "तिल",
        "Groundnut": "मूंगफली",
        "Sunflower": "सूरजमुखी",
        "Soybean": "सोयाबीन",
        "Black Gram": "उड़द",
        "Green Gram": "मूंग",
        "Red Gram": "अरहर",
        "Bengal Gram": "चना",
        "Horse Gram": "कुलथी",
        "Cowpea": "लोबिया",
        "Rice": "चावल",
        "Wheat": "गेहूं",
        "Maize": "मक्का",
        "Barley": "जौ",
        "Millet": "बाजरा",
        "Sorghum": "ज्वार",
        "Ragi": "रागी",
        "Bajra": "बाजरा",
        "Jowar": "ज्वार",
        "Kodo": "कोदो",
        "Little Millet": "कुटकी",
        "Foxtail Millet": "कंगनी",
        "Barnyard Millet": "सामा",
        "Proso Millet": "चीना",
        "Finger Millet": "रागी",
        "Pearl Millet": "बाजरा",
        "Teff": "टेफ",
        "Quinoa": "क्विनोआ",
        "Amaranth": "चौलाई",
        "Buckwheat": "कुट्टू",
        "Oats": "जई",
        "Rye": "राई",
        "Triticale": "ट्रिटिकेल",
        "Spelt": "स्पेल्ट",
        "Kamut": "कामुत",
        "Emmer": "एमर",
        "Einkorn": "आइनकॉर्न",
        "Freekeh": "फ्रीके",
        "Bulgur": "बुलगर",
        "Couscous": "कुसकुस",
        "Farro": "फारो",
        "Wheat Berries": "गेहूं के दाने",
        "Brown Rice": "भूरे चावल",
        "Wild Rice": "जंगली चावल",
        "Red Rice": "लाल चावल",
        "Black Rice": "काले चावल",
        "Purple Rice": "बैंगनी चावल",
        "Jasmine Rice": "जैस्मिन चावल",
        "Basmati Rice": "बासमती चावल",
        "Arborio Rice": "आर्बोरियो चावल",
        "Sushi Rice": "सुशी चावल",
        "Sticky Rice": "चिपचिपे चावल",
        "Long Grain Rice": "लंबे दाने वाले चावल",
        "Short Grain Rice": "छोटे दाने वाले चावल",
        "Medium Grain Rice": "मध्यम दाने वाले चावल",
        "Parboiled Rice": "उबले चावल",
        "Converted Rice": "परिवर्तित चावल",
        "Instant Rice": "तुरंत चावल",
        "Precooked Rice": "पहले से पके चावल",
        "Frozen Rice": "जमे हुए चावल",
        "Canned Rice": "डिब्बाबंद चावल",
        "Rice Flour": "चावल का आटा",
        "Rice Bran": "चावल की भूसी",
        "Rice Husk": "चावल का छिलका",
        "Rice Starch": "चावल का स्टार्च",
        "Rice Syrup": "चावल का सिरप",
        "Rice Vinegar": "चावल का सिरका",
        "Rice Wine": "चावल की शराब",
        "Rice Paper": "चावल का कागज",
        "Rice Noodles": "चावल की नूडल्स",
        "Rice Cakes": "चावल के केक",
        "Rice Pudding": "चावल की खीर",
        "Rice Milk": "चावल का दूध",
        "Rice Cream": "चावल की क्रीम",
        "Rice Butter": "चावल का मक्खन",
        "Rice Oil": "चावल का तेल",
        "Rice Protein": "चावल का प्रोटीन",
        "Rice Fiber": "चावल का फाइबर",
        "Rice Antioxidants": "चावल के एंटीऑक्सिडेंट",
        "Rice Vitamins": "चावल के विटामिन",
        "Rice Minerals": "चावल के खनिज",
        "Rice Amino Acids": "चावल के अमीनो एसिड",
        "Rice Enzymes": "चावल के एंजाइम",
        "Rice Probiotics": "चावल के प्रोबायोटिक्स",
        "Rice Prebiotics": "चावल के प्रीबायोटिक्स",
        "Rice Postbiotics": "चावल के पोस्टबायोटिक्स",
        "Rice Synbiotics": "चावल के सिनबायोटिक्स",
        "Rice Psychobiotics": "चावल के साइकोबायोटिक्स",
        "Rice Metabiotics": "चावल के मेटाबायोटिक्स",
        "Rice Parabiotics": "चावल के पैराबायोटिक्स",
        "Rice Eubiotics": "चावल के यूबायोटिक्स",
        "Rice Dysbiotics": "चावल के डिसबायोटिक्स",
        "Rice Antibiotics": "चावल के एंटीबायोटिक्स"
    }
    
    return hindi_translations.get(english_name, english_name)

def get_kannada_translation(english_name):
    """Get Kannada translation for crop names"""
    kannada_translations = {
        "Papaya": "ಪರಂಗಿ",
        "Banana": "ಬಾಳೆ",
        "Guava": "ಸೀಬೆ",
        "Mango": "ಮಾವು",
        "Coconut": "ತೆಂಗು",
        "Pineapple": "ಅನಾನಸ್",
        "Orange": "ಕಿತ್ತಳೆ",
        "Lemon": "ನಿಂಬೆ",
        "Grape": "ದ್ರಾಕ್ಷಿ",
        "Pomegranate": "ದಾಳಿಂಬೆ",
        "Apple": "ಸೇಬು",
        "Sweet Potato": "ಸಿಹಿ ಬಟಾಟೆ",
        "Potato": "ಆಲೂಗಡ್ಡೆ",
        "Onion": "ಈರುಳ್ಳಿ",
        "Tomato": "ಟೊಮಾಟೊ",
        "Carrot": "ಗಜ್ಜರಿ",
        "Beetroot": "ಬೀಟ್ ರೂಟ್",
        "Radish": "ಮೂಲಂಗಿ",
        "Cabbage": "ಕೋಸು",
        "Cauliflower": "ಹೂಕೋಸು",
        "Spinach": "ಪಾಲಕ್",
        "Coriander": "ಕೊತ್ತಂಬರಿ",
        "Mint": "ಪುದೀನ",
        "Curry Leaves": "ಕರಿಬೇವು",
        "Drumstick": "ನುಗ್ಗೆ",
        "Brinjal": "ಬದನೆ",
        "Okra": "ಬೆಂಡೆ",
        "Cucumber": "ಸೌತೆ",
        "Bottle Gourd": "ಸೋರೆ",
        "Ridge Gourd": "ಹೀರೆ",
        "Bitter Gourd": "ಹಾಗಲಕಾಯಿ",
        "Snake Gourd": "ಪಡವಲ",
        "Ash Gourd": "ಬೂದಿ ಕುಂಬಳ",
        "Pumpkin": "ಕುಂಬಳ",
        "Green Chilli": "ಹಸಿರು ಮೆಣಸು",
        "Red Chilli": "ಕೆಂಪು ಮೆಣಸು",
        "Ginger": "ಶುಂಠಿ",
        "Garlic": "ಬೆಳ್ಳುಳ್ಳಿ",
        "Turmeric": "ಅರಿಶಿಣ",
        "Cardamom": "ಏಲಕ್ಕಿ",
        "Cinnamon": "ದಾಲ್ಚಿನ್ನಿ",
        "Clove": "ಲವಂಗ",
        "Pepper": "ಕರಿಮೆಣಸು",
        "Cumin": "ಜೀರಿಗೆ",
        "Fennel": "ಸೋಂಪು",
        "Fenugreek": "ಮೆಂತ್ಯ",
        "Mustard": "ಸಾಸಿವೆ",
        "Sesame": "ಎಳ್ಳು",
        "Groundnut": "ಕಡಲೆಕಾಯಿ",
        "Sunflower": "ಸೂರ್ಯಕಾಂತಿ",
        "Soybean": "ಸೋಯಾಬೀನ್",
        "Black Gram": "ಉದ್ದು",
        "Green Gram": "ಹೆಸರು",
        "Red Gram": "ತೊವೆ",
        "Bengal Gram": "ಕಡಲೆ",
        "Horse Gram": "ಹುರಳಿ",
        "Cowpea": "ಅವರೆ",
        "Rice": "ಅಕ್ಕಿ",
        "Wheat": "ಗೋಧಿ",
        "Maize": "ಮೆಕ್ಕೆಜೋಳ",
        "Barley": "ಬಾರ್ಲಿ",
        "Millet": "ರಾಗಿ",
        "Sorghum": "ಜೋಳ",
        "Ragi": "ರಾಗಿ",
        "Bajra": "ಸಜ್ಜೆ",
        "Jowar": "ಜೋಳ",
        "Kodo": "ಕೋಡೋ",
        "Little Millet": "ಸಾಮೆ",
        "Foxtail Millet": "ನವಣೆ",
        "Barnyard Millet": "ಊದಲು",
        "Proso Millet": "ಬರಗು",
        "Finger Millet": "ರಾಗಿ",
        "Pearl Millet": "ಸಜ್ಜೆ",
        "Teff": "ಟೆಫ್",
        "Quinoa": "ಕ್ವಿನೋವಾ",
        "Amaranth": "ರಾಜಗಿರಿ",
        "Buckwheat": "ಬಕ್ವೀಟ್",
        "Oats": "ಓಟ್ಸ್",
        "Rye": "ರೈ",
        "Triticale": "ಟ್ರಿಟಿಕೇಲ್",
        "Spelt": "ಸ್ಪೆಲ್ಟ್",
        "Kamut": "ಕಮುತ್",
        "Emmer": "ಎಮ್ಮರ್",
        "Einkorn": "ಐನ್ಕೋರ್ನ್",
        "Freekeh": "ಫ್ರೀಕೆ",
        "Bulgur": "ಬುಲ್ಗರ್",
        "Couscous": "ಕೌಸ್ಕಸ್",
        "Farro": "ಫಾರೋ",
        "Wheat Berries": "ಗೋಧಿ ಬೆರ್ರಿಗಳು",
        "Brown Rice": "ಕಂದು ಅಕ್ಕಿ",
        "Wild Rice": "ಕಾಡು ಅಕ್ಕಿ",
        "Red Rice": "ಕೆಂಪು ಅಕ್ಕಿ",
        "Black Rice": "ಕಪ್ಪು ಅಕ್ಕಿ",
        "Purple Rice": "ನೇರಳೆ ಅಕ್ಕಿ",
        "Jasmine Rice": "ಜಾಸ್ಮಿನ್ ಅಕ್ಕಿ",
        "Basmati Rice": "ಬಾಸ್ಮತಿ ಅಕ್ಕಿ",
        "Arborio Rice": "ಆರ್ಬೋರಿಯೋ ಅಕ್ಕಿ",
        "Sushi Rice": "ಸುಶಿ ಅಕ್ಕಿ",
        "Sticky Rice": "ಅಂಟುವ ಅಕ್ಕಿ",
        "Long Grain Rice": "ಉದ್ದನೆಯ ಅಕ್ಕಿ",
        "Short Grain Rice": "ಚಿಕ್ಕ ಅಕ್ಕಿ",
        "Medium Grain Rice": "ಮಧ್ಯಮ ಅಕ್ಕಿ",
        "Parboiled Rice": "ಬೇಯಿಸಿದ ಅಕ್ಕಿ",
        "Converted Rice": "ಮಾರ್ಪಡಿಸಿದ ಅಕ್ಕಿ",
        "Instant Rice": "ತಕ್ಷಣ ಅಕ್ಕಿ",
        "Precooked Rice": "ಮುಂಚೆ ಬೇಯಿಸಿದ ಅಕ್ಕಿ",
        "Frozen Rice": "ಘನೀಕೃತ ಅಕ್ಕಿ",
        "Canned Rice": "ಕ್ಯಾನ್ ಮಾಡಿದ ಅಕ್ಕಿ",
        "Rice Flour": "ಅಕ್ಕಿ ಹಿಟ್ಟು",
        "Rice Bran": "ಅಕ್ಕಿ ತವುಡು",
        "Rice Husk": "ಅಕ್ಕಿ ಚೋಳ",
        "Rice Starch": "ಅಕ್ಕಿ ಸ್ಟಾರ್ಚ್",
        "Rice Syrup": "ಅಕ್ಕಿ ಸಿರಪ್",
        "Rice Vinegar": "ಅಕ್ಕಿ ವಿನೆಗರ್",
        "Rice Wine": "ಅಕ್ಕಿ ವೈನ್",
        "Rice Paper": "ಅಕ್ಕಿ ಕಾಗದ",
        "Rice Noodles": "ಅಕ್ಕಿ ನೂಡಲ್ಸ್",
        "Rice Cakes": "ಅಕ್ಕಿ ಕೇಕ್ಗಳು",
        "Rice Pudding": "ಅಕ್ಕಿ ಪುಡ್ಡಿಂಗ್",
        "Rice Milk": "ಅಕ್ಕಿ ಹಾಲು",
        "Rice Cream": "ಅಕ್ಕಿ ಕ್ರೀಮ್",
        "Rice Butter": "ಅಕ್ಕಿ ಬೆಣ್ಣೆ",
        "Rice Oil": "ಅಕ್ಕಿ ಎಣ್ಣೆ",
        "Rice Protein": "ಅಕ್ಕಿ ಪ್ರೋಟೀನ್",
        "Rice Fiber": "ಅಕ್ಕಿ ಫೈಬರ್",
        "Rice Antioxidants": "ಅಕ್ಕಿ ಆಂಟಿಆಕ್ಸಿಡೆಂಟ್ಗಳು",
        "Rice Vitamins": "ಅಕ್ಕಿ ವಿಟಮಿನ್ಗಳು",
        "Rice Minerals": "ಅಕ್ಕಿ ಖನಿಜಗಳು",
        "Rice Amino Acids": "ಅಕ್ಕಿ ಅಮೈನೋ ಆಸಿಡ್ಗಳು",
        "Rice Enzymes": "ಅಕ್ಕಿ ಎಂಜೈಮ್ಗಳು",
        "Rice Probiotics": "ಅಕ್ಕಿ ಪ್ರೋಬಯೋಟಿಕ್ಸ್",
        "Rice Prebiotics": "ಅಕ್ಕಿ ಪ್ರೀಬಯೋಟಿಕ್ಸ್",
        "Rice Postbiotics": "ಅಕ್ಕಿ ಪೋಸ್ಟ್ಬಯೋಟಿಕ್ಸ್",
        "Rice Synbiotics": "ಅಕ್ಕಿ ಸಿನ್ಬಯೋಟಿಕ್ಸ್",
        "Rice Psychobiotics": "ಅಕ್ಕಿ ಸೈಕೋಬಯೋಟಿಕ್ಸ್",
        "Rice Metabiotics": "ಅಕ್ಕಿ ಮೆಟಾಬಯೋಟಿಕ್ಸ್",
        "Rice Parabiotics": "ಅಕ್ಕಿ ಪಾರಾಬಯೋಟಿಕ್ಸ್",
        "Rice Eubiotics": "ಅಕ್ಕಿ ಯೂಬಯೋಟಿಕ್ಸ್",
        "Rice Dysbiotics": "ಅಕ್ಕಿ ಡಿಸ್ಬಯೋಟಿಕ್ಸ್",
        "Rice Antibiotics": "ಅಕ್ಕಿ ಆಂಟಿಬಯೋಟಿಕ್ಸ್"
    }
    
    return kannada_translations.get(english_name, english_name)

def get_malayalam_translation(english_name):
    """Get Malayalam translation for crop names"""
    # Predefined Malayalam translations for common crops
    malayalam_translations = {
        "Papaya": "പപ്പായ",
        "Banana": "വാഴ",
        "Guava": "പേരയ്ക്ക",
        "Mango": "മാങ്ങ",
        "Coconut": "തേങ്ങ",
        "Pineapple": "കൈതച്ചക്ക",
        "Orange": "ഓറഞ്ച്",
        "Lemon": "നാരങ്ങ",
        "Grape": "മുന്തിരി",
        "Pomegranate": "മാതളനാരകം",
        "Apple": "ആപ്പിൾ",
        "Sweet Potato": "മധുരക്കിഴങ്ങ്",
        "Potato": "ഉരുളക്കിഴങ്ങ്",
        "Onion": "ഉള്ളി",
        "Tomato": "തക്കാളി",
        "Carrot": "കാരറ്റ്",
        "Beetroot": "ബീറ്റ് റൂട്ട്",
        "Radish": "മുള്ളങ്കി",
        "Cabbage": "കാബേജ്",
        "Cauliflower": "കോൾ ഫ്ലവർ",
        "Spinach": "ചീര",
        "Coriander": "മല്ലി",
        "Mint": "പുതിന",
        "Curry Leaves": "കറിവേപ്പില",
        "Drumstick": "മുരിങ്ങ",
        "Brinjal": "വഴുതന",
        "Okra": "വെണ്ട",
        "Cucumber": "വെള്ളരി",
        "Bottle Gourd": "ചുരയ്ക്ക",
        "Ridge Gourd": "പീച്ചിങ്ക",
        "Bitter Gourd": "പാവയ്ക്ക",
        "Snake Gourd": "പടവലങ്ങ",
        "Ash Gourd": "കുമ്പളങ്ങ",
        "Pumpkin": "മത്തങ്ങ",
        "Green Chilli": "പച്ചമുളക്",
        "Red Chilli": "ചുവന്നമുളക്",
        "Ginger": "ഇഞ്ചി",
        "Garlic": "വെളുത്തുള്ളി",
        "Turmeric": "മഞ്ഞൾ",
        "Cardamom": "ഏലം",
        "Cinnamon": "കറുവപ്പട്ട",
        "Clove": "കരയാമ്പൂ",
        "Pepper": "കുരുമുളക്",
        "Cumin": "ജീരകം",
        "Fennel": "പെരുംജീരകം",
        "Fenugreek": "ഉലുവ",
        "Mustard": "കടുക്",
        "Sesame": "എള്ള്",
        "Groundnut": "നിലക്കടല",
        "Sunflower": "സൂര്യകാന്തി",
        "Soybean": "സോയാബീൻ",
        "Black Gram": "ഉഴുന്ന്",
        "Green Gram": "മുതിര",
        "Red Gram": "തുവര",
        "Bengal Gram": "കടല",
        "Horse Gram": "കുതിരമുതിര",
        "Cowpea": "വാള",
        "Rice": "അരി",
        "Wheat": "ഗോതമ്പ്",
        "Maize": "ചോളം",
        "Barley": "ബാർലി",
        "Millet": "ചോളം",
        "Sorghum": "ചോളം",
        "Ragi": "രാഗി",
        "Bajra": "ബജ്ര",
        "Jowar": "ചോളം",
        "Kodo": "കോഡോ",
        "Little Millet": "ചിറ്റചോളം",
        "Foxtail Millet": "തിന",
        "Barnyard Millet": "കുതിരവാല്",
        "Proso Millet": "പ്രോസോ ചോളം",
        "Finger Millet": "രാഗി",
        "Pearl Millet": "ബജ്ര",
        "Sorghum": "ചോളം",
        "Teff": "ടെഫ്",
        "Quinoa": "ക്വിനോവ",
        "Amaranth": "ചീര",
        "Buckwheat": "ബക്ക് വീറ്റ്",
        "Oats": "ഓട്സ്",
        "Rye": "റൈ",
        "Triticale": "ട്രിറ്റിക്കേൽ",
        "Spelt": "സ്പെൽറ്റ്",
        "Kamut": "കാമുത്",
        "Emmer": "എമ്മർ",
        "Einkorn": "ഐൻകോൺ",
        "Freekeh": "ഫ്രീക്കെ",
        "Bulgur": "ബൾഗർ",
        "Couscous": "കൗസ്കസ്",
        "Farro": "ഫാറോ",
        "Wheat Berries": "ഗോതമ്പ് ബെറി",
        "Brown Rice": "തവിട്ട് അരി",
        "Wild Rice": "കാട്ട് അരി",
        "Red Rice": "ചുവന്ന അരി",
        "Black Rice": "കറുത്ത അരി",
        "Purple Rice": "ഊത അരി",
        "Jasmine Rice": "ജാസ്മിൻ അരി",
        "Basmati Rice": "ബാസ്മതി അരി",
        "Arborio Rice": "ആർബോറിയോ അരി",
        "Sushi Rice": "സുഷി അരി",
        "Sticky Rice": "അടുത്ത അരി",
        "Long Grain Rice": "നീളമുള്ള അരി",
        "Short Grain Rice": "ചെറിയ അരി",
        "Medium Grain Rice": "ഇടത്തരം അരി",
        "Parboiled Rice": "ഉണക്കിയ അരി",
        "Converted Rice": "മാറ്റിയ അരി",
        "Instant Rice": "തൽക്ഷണ അരി",
        "Precooked Rice": "മുൻകൂട്ടി വേവിച്ച അരി",
        "Frozen Rice": "ഉറച്ച അരി",
        "Canned Rice": "ക്യാനിൽ അരി",
        "Rice Flour": "അരി മാവ്",
        "Rice Bran": "അരി തവിട്",
        "Rice Husk": "അരി ചോളം",
        "Rice Starch": "അരി അന്നജം",
        "Rice Syrup": "അരി സിറപ്പ്",
        "Rice Vinegar": "അരി വിനാഗിരി",
        "Rice Wine": "അരി വൈൻ",
        "Rice Paper": "അരി പേപ്പർ",
        "Rice Noodles": "അരി നൂഡിൽസ്",
        "Rice Cakes": "അരി കേക്കുകൾ",
        "Rice Pudding": "അരി പുഡ്ഡിംഗ്",
        "Rice Milk": "അരി പാൽ",
        "Rice Cream": "അരി ക്രീം",
        "Rice Butter": "അരി വെണ്ണ",
        "Rice Oil": "അരി എണ്ണ",
        "Rice Protein": "അരി പ്രോട്ടീൻ",
        "Rice Fiber": "അരി നാര്",
        "Rice Antioxidants": "അരി ആന്റിഓക്സിഡന്റുകൾ",
        "Rice Vitamins": "അരി വിറ്റാമിനുകൾ",
        "Rice Minerals": "അരി ധാതുക്കൾ",
        "Rice Amino Acids": "അരി അമിനോ ആസിഡുകൾ",
        "Rice Enzymes": "അരി എൻസൈമുകൾ",
        "Rice Probiotics": "അരി പ്രോബയോട്ടിക്സ്",
        "Rice Prebiotics": "അരി പ്രീബയോട്ടിക്സ്",
        "Rice Postbiotics": "അരി പോസ്റ്റ്ബയോട്ടിക്സ്",
        "Rice Synbiotics": "അരി സിൻബയോട്ടിക്സ്",
        "Rice Psychobiotics": "അരി സൈക്കോബയോട്ടിക്സ്",
        "Rice Metabiotics": "അരി മെറ്റബയോട്ടിക്സ്",
        "Rice Parabiotics": "അരി പാരബയോട്ടിക്സ്",
        "Rice Eubiotics": "അരി യൂബയോട്ടിക്സ്",
        "Rice Dysbiotics": "അരി ഡിസ്ബയോട്ടിക്സ്",
        "Rice Antibiotics": "അരി ആന്റിബയോട്ടിക്സ്",
        "Rice Probiotics": "അരി പ്രോബയോട്ടിക്സ്",
        "Rice Prebiotics": "അരി പ്രീബയോട്ടിക്സ്",
        "Rice Postbiotics": "അരി പോസ്റ്റ്ബയോട്ടിക്സ്",
        "Rice Synbiotics": "അരി സിൻബയോട്ടിക്സ്",
        "Rice Psychobiotics": "അരി സൈക്കോബയോട്ടിക്സ്",
        "Rice Metabiotics": "അരി മെറ്റബയോട്ടിക്സ്",
        "Rice Parabiotics": "അരി പാരബയോട്ടിക്സ്",
        "Rice Eubiotics": "അരി യൂബയോട്ടിക്സ്",
        "Rice Dysbiotics": "അരി ഡിസ്ബയോട്ടിക്സ്",
        "Rice Antibiotics": "അരി ആന്റിബയോട്ടിക്സ്"
    }
    
    return malayalam_translations.get(english_name, english_name)

def get_crop_image_path(english_name, category):
    """Get image path in a Render-safe lowercase format."""
    import os

    # Convert category and crop names to lowercase, clean special chars
    safe_category = category.lower()
    safe_crop = (
        english_name.lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "_")
    )

    base_path = f"static/images/{safe_category}/{safe_crop}"
    first_letter = safe_crop[0] if safe_crop else "x"
    expected_filename = f"{first_letter}1.jpg"
    expected_path = f"/static/images/{safe_category}/{safe_crop}/{expected_filename}"

    # Try expected filename
    if os.path.exists(os.path.join(base_path, expected_filename)):
        return expected_path

    # Try any image inside folder
    if os.path.exists(base_path):
        for file in os.listdir(base_path):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                return f"/static/images/{safe_category}/{safe_crop}/{file}"

    return None

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy", "message": "Crop Knowledge Explorer is running"})

if __name__ == '__main__':
    print("🚀 Loading Crop Knowledge Explorer...")
    crop_data = load_crop_data()

    if crop_data:
        print("✅ Data loaded successfully! Starting Flask server...")
        print("🌍 Open http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("❌ Failed to load data. Please check your crops_data.json file.")