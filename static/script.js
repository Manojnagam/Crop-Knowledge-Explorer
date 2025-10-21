// 🌾 Crop Knowledge Explorer Frontend Script (Render-ready)

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

// Language-specific UI text
const uiTexts = {
    'en': {
        'selectCategory': 'Select a Category',
        'backToCategories': '← Back to Categories',
        'chooseLanguage': 'Choose Language',
        'noDataMessage': 'Crop names not available in this language yet. Please select English or Tamil to view crop data.',
        'noDataSubtitle': 'Please select English or Tamil to view crop data.'
    },
    'ta': {
        'selectCategory': 'ஒரு பிரிவைத் தேர்ந்தெடுக்கவும்',
        'backToCategories': '← பிரிவுகளுக்குத் திரும்பு',
        'chooseLanguage': 'மொழியைத் தேர்ந்தெடுக்கவும்',
        'noDataMessage': 'இந்த மொழியில் பயிர் பெயர்கள் இன்னும் கிடைக்கவில்லை. ஆங்கிலம் அல்லது தமிழைத் தேர்ந்தெடுக்கவும்.',
        'noDataSubtitle': 'பயிர் விவரங்களைப் பார்க்க ஆங்கிலம் அல்லது தமிழைத் தேர்ந்தெடுக்கவும்.'
    },
    'te': {
        'selectCategory': 'వర్గాన్ని ఎంచుకోండి',
        'backToCategories': '← వర్గాలకు తిరిగి వెళ్ళు',
        'chooseLanguage': 'భాషను ఎంచుకోండి',
        'noDataMessage': 'ఈ భాషలో పంట పేర్లు అందుబాటులో లేవు. ఇంగ్లీష్ లేదా తమిళాన్ని ఎంచుకోండి.',
        'noDataSubtitle': 'దయచేసి ఇంగ్లీష్ లేదా తమిళాన్ని ఎంచుకోండి.'
    },
    'hi': {
        'selectCategory': 'श्रेणी चुनें',
        'backToCategories': '← श्रेणियों पर वापस जाएँ',
        'chooseLanguage': 'भाषा चुनें',
        'noDataMessage': 'इस भाषा में फसल के नाम अभी उपलब्ध नहीं हैं। अंग्रेज़ी या तमिल चुनें।',
        'noDataSubtitle': 'कृपया अंग्रेज़ी या तमिल चुनें।'
    },
    'kn': {
        'selectCategory': 'ವರ್ಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        'backToCategories': '← ವರ್ಗಗಳಿಗೆ ಹಿಂದಿರುಗಿ',
        'chooseLanguage': 'ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        'noDataMessage': 'ಈ ಭಾಷೆಯಲ್ಲಿ ಬೆಳೆ ಹೆಸರುಗಳು ಲಭ್ಯವಿಲ್ಲ. ಇಂಗ್ಲಿಷ್ ಅಥವಾ ತಮಿಳು ಆಯ್ಕೆಮಾಡಿ.',
        'noDataSubtitle': 'ಇಂಗ್ಲಿಷ್ ಅಥವಾ ತಮಿಳು ಆಯ್ಕೆಮಾಡಿ.'
    }
};

// 🌱 Initialize app
document.addEventListener('DOMContentLoaded', async function() {
    showLoading();
    await loadCropData();
    setupEventListeners();
    updateCategoryButtons();
    hideLoading();
});

// 🌾 Load crop data from backend API
async function loadCropData() {
    try {
        const response = await fetch('/data');  // ✅ Fixed for Render
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        cropData = await response.json();
        console.log('✅ Crop data loaded:', cropData);
    } catch (error) {
        console.error('❌ Error loading crop data:', error);
        alert('Error loading crop data. Please refresh the page.');
    }
}

// 🌍 Event listeners for language buttons & back button
function setupEventListeners() {
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            selectLanguage(this.getAttribute('data-lang'));
        });
    });

    const backBtn = document.getElementById('back-btn');
    if (backBtn) backBtn.addEventListener('click', showCategorySection);
}

// 🌐 Handle language selection
function selectLanguage(lang) {
    currentLanguage = lang;
    document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-lang="${lang}"]`).classList.add('active');

    updateCategoryButtons();
    hideCropsSection();
}

// 🍀 Create category buttons dynamically
function updateCategoryButtons() {
    const container = document.getElementById('category-buttons');
    const title = document.getElementById('category-title');
    const currentText = uiTexts[currentLanguage] || uiTexts['en'];

    if (title) title.textContent = currentText.selectCategory;
    if (!container) return;

    container.innerHTML = '';
    Object.keys(cropData).forEach(category => {
        const btn = document.createElement('button');
        btn.className = 'category-btn';
        btn.textContent = getCategoryName(category, currentLanguage);
        btn.onclick = () => selectCategory(category);
        container.appendChild(btn);
    });
}

// 🏷️ Category name by language
function getCategoryName(category, lang) {
    const names = categoryLabels[category].split(' / ');
    const index = { 'en': 0, 'ta': 1, 'te': 2, 'hi': 3, 'kn': 4 };
    return names[index[lang]] || names[0];
}

// 🌸 Show crops in selected category
function selectCategory(category) {
    currentCategory = category;
    const crops = cropData[category] || [];
    const grid = document.getElementById('crops-grid');
    const title = document.getElementById('crops-title');
    const backBtn = document.getElementById('back-btn');
    const currentText = uiTexts[currentLanguage] || uiTexts['en'];

    if (title) title.textContent = getCategoryName(category, currentLanguage);
    if (backBtn) backBtn.textContent = currentText.backToCategories;
    grid.innerHTML = '';

    if (['te', 'hi', 'kn'].includes(currentLanguage)) {
        showLanguageMessage();
    } else {
        crops.forEach(crop => grid.appendChild(createCropCard(crop)));
    }

    showCropsSection();
}

// 🌾 Create individual crop card
function createCropCard(crop) {
    const card = document.createElement('div');
    card.className = 'crop-card';
    const cropName = (currentLanguage === 'ta')
        ? (crop.Tamil?.trim() || crop.English?.trim() || '-')
        : (crop.English?.trim() || '-');
    card.innerHTML = `<div class="crop-name">${cropName}</div>`;
    return card;
}

// 🌍 Show message for unsupported languages
function showLanguageMessage() {
    const grid = document.getElementById('crops-grid');
    const text = uiTexts[currentLanguage] || uiTexts['en'];
    grid.innerHTML = `
        <div class="language-message">
            <div class="message-icon">🌐</div>
            <div class="message-text">${text.noDataMessage}</div>
            <div class="message-subtitle">${text.noDataSubtitle}</div>
        </div>
    `;
}

// 🧭 Section control
function showCropsSection() {
    document.querySelector('.category-section').style.display = 'none';
    document.getElementById('crops-section').style.display = 'block';
}

function hideCropsSection() {
    document.querySelector('.category-section').style.display = 'block';
    document.getElementById('crops-section').style.display = 'none';
}

function showCategorySection() {
    hideCropsSection();
}

// 🌿 Loading overlay
function showLoading() {
    const el = document.getElementById('loading');
    if (el) el.classList.remove('hidden');
}

function hideLoading() {
    const el = document.getElementById('loading');
    if (el) el.classList.add('hidden');
}