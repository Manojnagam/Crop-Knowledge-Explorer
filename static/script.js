// Global variables
let cropData = {};
let currentLanguage = 'en';
let currentCategory = '';

// Language mappings for category labels
const categoryLabels = {
    "Fruits": "Fruits / பழங்கள் / పండ్లు / फल / ಹಣ್ಣುಗಳು",
    "Vegetables": "Vegetables / காய்கறிகள் / కూరగాయలు / सब्ज़ियाँ / ತರಕಾರಿಗಳು",
    "Greens": "Greens / கீரைகள் / ఆకుకూరలు / साग / ಸೊಪ್ಪುಗಳು",
    "Tubers": "Tubers / கிழங்குகள் / కందమూలాలు / कंद / ನೆಲಗಡ್ಡೆಗಳು",
    "Herbal": "Herbal / மூலிகைகள் / ఔషధ మొక్కలు / औषधीय पौधे / ಔಷಧಿ ಸಸ್ಯಗಳು",
    "Units": "Units / பிரிவுகள் / యూనిట్లు / इकाइयाँ / ಘಟಕಗಳು"
};

// Language codes mapping
const languageCodes = {
    'English': 'en',
    'தமிழ்': 'ta', 
    'తెలుగు': 'te',
    'हिन्दी': 'hi',
    'ಕನ್ನಡ': 'kn'
};

// Language-specific UI text
const uiTexts = {
    'en': {
        'selectCategory': 'Select a Category',
        'backToCategories': '← Back to Categories',
        'chooseLanguage': 'Choose Language',
        'crops': 'Crops',
        'noDataMessage': 'Crop names not available in this language yet. Please select English or Tamil to view crop data.',
        'noDataSubtitle': 'Please select English or Tamil to view crop data.'
    },
    'ta': {
        'selectCategory': 'ஒரு பிரிவைத் தேர்ந்தெடுக்கவும்',
        'backToCategories': '← பிரிவுகளுக்குத் திரும்பு',
        'chooseLanguage': 'மொழியைத் தேர்ந்தெடுக்கவும்',
        'crops': 'பயிர்கள்',
        'noDataMessage': 'இந்த மொழியில் பயிர் பெயர்கள் இன்னும் கிடைக்கவில்லை. பயிர் விவரங்களைப் பார்க்க ஆங்கிலம் அல்லது தமிழைத் தேர்ந்தெடுக்கவும்.',
        'noDataSubtitle': 'பயிர் விவரங்களைப் பார்க்க ஆங்கிலம் அல்லது தமிழைத் தேர்ந்தெடுக்கவும்.'
    },
    'te': {
        'selectCategory': 'వర్గాన్ని ఎంచుకోండి',
        'backToCategories': '← వర్గాలకు తిరిగి వెళ్ళు',
        'chooseLanguage': 'భాషను ఎంచుకోండి',
        'crops': 'పంటలు',
        'noDataMessage': 'ఈ భాషలో పంట పేర్లు ఇంకా అందుబాటులో లేవు. దయచేసి పంట వివరాలను చూడటానికి ఇంగ్లీష్ లేదా తమిళాన్ని ఎంచుకోండి.',
        'noDataSubtitle': 'దయచేసి పంట వివరాలను చూడటానికి ఇంగ్లీష్ లేదా తమిళాన్ని ఎంచుకోండి.'
    },
    'hi': {
        'selectCategory': 'श्रेणी चुनें',
        'backToCategories': '← श्रेणियों पर वापस जाएँ',
        'chooseLanguage': 'भाषा चुनें',
        'crops': 'फसलें',
        'noDataMessage': 'इस भाषा में फसल के नाम अभी उपलब्ध नहीं हैं। कृपया फसल विवरण देखने के लिए अंग्रेज़ी या तमिल चुनें।',
        'noDataSubtitle': 'कृपया फसल विवरण देखने के लिए अंग्रेज़ी या तमिल चुनें।'
    },
    'kn': {
        'selectCategory': 'ವರ್ಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        'backToCategories': '← ವರ್ಗಗಳಿಗೆ ಹಿಂದಿರುಗಿ',
        'chooseLanguage': 'ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        'crops': 'ಬೆಳೆಗಳು',
        'noDataMessage': 'ಈ ಭಾಷೆಯಲ್ಲಿ ಬೆಳೆ ಹೆಸರುಗಳು ಇನ್ನೂ ಲಭ್ಯವಿಲ್ಲ. ಬೆಳೆ ವಿವರಗಳನ್ನು ನೋಡಲು ಇಂಗ್ಲಿಷ್ ಅಥವಾ ತಮಿಳು ಆಯ್ಕೆಮಾಡಿ.',
        'noDataSubtitle': 'ಬೆಳೆ ವಿವರಗಳನ್ನು ನೋಡಲು ಇಂಗ್ಲಿಷ್ ಅಥವಾ ತಮಿಳು ಆಯ್ಕೆಮಾಡಿ.'
    }
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

async function initializeApp() {
    try {
        // Show loading
        showLoading();
        
        // Load crop data
        await loadCropData();
        
        // Setup event listeners
        setupEventListeners();
        
        // Initialize UI
        updateCategoryButtons();
        
        // Hide loading
        hideLoading();
        
    } catch (error) {
        console.error('Error initializing app:', error);
        hideLoading();
        alert('Error loading crop data. Please refresh the page.');
    }
}

async function loadCropData() {
    try {
        const response = await fetch('/data');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        cropData = await response.json();
        console.log('Loaded crop data:', cropData);
    } catch (error) {
        console.error('Error loading crop data:', error);
        throw error;
    }
}

function setupEventListeners() {
    // Language button event listeners
    const langButtons = document.querySelectorAll('.lang-btn');
    langButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const lang = this.getAttribute('data-lang');
            selectLanguage(lang);
        });
    });
    
    // Back button event listener
    const backBtn = document.getElementById('back-btn');
    if (backBtn) {
        backBtn.addEventListener('click', function() {
            showCategorySection();
        });
    }
}

function selectLanguage(lang) {
    currentLanguage = lang;
    
    // Update active language button
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-lang="${lang}"]`).classList.add('active');
    
    // Update language title
    const languageTitle = document.getElementById('language-title');
    if (languageTitle) {
        const currentText = uiTexts[currentLanguage] || uiTexts['en'];
        languageTitle.textContent = currentText.chooseLanguage;
    }
    
    // Update category buttons
    updateCategoryButtons();
    
    // Hide crops section if showing
    hideCropsSection();
}

function updateCategoryButtons() {
    const categoryButtonsContainer = document.getElementById('category-buttons');
    if (!categoryButtonsContainer) return;
    
    // Update category title
    const categoryTitle = document.getElementById('category-title');
    if (categoryTitle) {
        const currentText = uiTexts[currentLanguage] || uiTexts['en'];
        categoryTitle.textContent = currentText.selectCategory;
    }
    
    // Clear existing buttons
    categoryButtonsContainer.innerHTML = '';
    
    // Create category buttons
    Object.keys(cropData).forEach(category => {
        const button = document.createElement('button');
        button.className = 'category-btn';
        button.textContent = getCategoryName(category, currentLanguage);
        button.addEventListener('click', function() {
            selectCategory(category);
        });
        categoryButtonsContainer.appendChild(button);
    });
}

function getCategoryName(category, lang) {
    const labels = categoryLabels[category].split(' / ');
    const langIndex = {'en': 0, 'ta': 1, 'te': 2, 'hi': 3, 'kn': 4};
    return labels[langIndex[lang]] || labels[0];
}

function selectCategory(category) {
    currentCategory = category;
    showCrops(category);
}

function showCrops(category) {
    const crops = cropData[category] || [];
    
    // Update crops title
    const cropsTitle = document.getElementById('crops-title');
    if (cropsTitle) {
        cropsTitle.textContent = getCategoryName(category, currentLanguage);
    }
    
    // Update back button text
    const backBtn = document.getElementById('back-btn');
    if (backBtn) {
        const currentText = uiTexts[currentLanguage] || uiTexts['en'];
        backBtn.textContent = currentText.backToCategories;
    }
    
    // Populate crops grid
    const cropsGrid = document.getElementById('crops-grid');
    if (!cropsGrid) return;
    
    cropsGrid.innerHTML = '';
    
    // Check if current language supports crop data
    if (currentLanguage === 'te' || currentLanguage === 'hi' || currentLanguage === 'kn') {
        showLanguageMessage();
    } else if (crops.length === 0) {
        const currentText = uiTexts[currentLanguage] || uiTexts['en'];
        cropsGrid.innerHTML = `<p style="text-align: center; color: #666; font-style: italic;">No crops found in this category.</p>`;
    } else {
        crops.forEach(crop => {
            const cropCard = createCropCard(crop);
            cropsGrid.appendChild(cropCard);
        });
    }
    
    // Show crops section
    showCropsSection();
}

function createCropCard(crop) {
    const card = document.createElement('div');
    card.className = 'crop-card';
    
    // Show only the selected language's crop name
    let cropName;
    if (currentLanguage === 'ta') {
        // For Tamil, show only Tamil name
        cropName = crop.Tamil?.trim() || crop.English?.trim() || '-';
    } else {
        // For English, show only English name
        cropName = crop.English?.trim() || '-';
    }
    
    card.innerHTML = `
        <div class="crop-name">${cropName}</div>
    `;
    
    return card;
}

function showLanguageMessage() {
    const cropsGrid = document.getElementById('crops-grid');
    if (!cropsGrid) return;
    
    const currentText = uiTexts[currentLanguage] || uiTexts['en'];
    
    cropsGrid.innerHTML = `
        <div class="language-message">
            <div class="message-icon">🌐</div>
            <div class="message-text">${currentText.noDataMessage}</div>
            <div class="message-subtitle">${currentText.noDataSubtitle}</div>
        </div>
    `;
}

function showCropsSection() {
    const categorySection = document.querySelector('.category-section');
    const cropsSection = document.getElementById('crops-section');
    
    if (categorySection) categorySection.style.display = 'none';
    if (cropsSection) cropsSection.style.display = 'block';
}

function hideCropsSection() {
    const categorySection = document.querySelector('.category-section');
    const cropsSection = document.getElementById('crops-section');
    
    if (categorySection) categorySection.style.display = 'block';
    if (cropsSection) cropsSection.style.display = 'none';
}

function showCategorySection() {
    hideCropsSection();
}

function showLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.classList.remove('hidden');
    }
}

function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.classList.add('hidden');
    }
}