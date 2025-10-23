// 🌾 Crop Knowledge Explorer Frontend Script (Render-ready)

// Global variables
let cropData = {};
let currentLanguage = 'en';
let currentCategory = '';

// Category mapping for validation and reassignment
const categoryMap = {
  "Papaya": "Fruits",
  "Banana": "Fruits",
  "Guava": "Fruits",
  "Pomegranate": "Fruits",
  "Brinjal": "Vegetables",
  "Bitter Gourd": "Vegetables",
  "Bottle Gourd": "Vegetables",
  "Pumpkin": "Vegetables",
  "Bhendi (Okra)": "Vegetables",
  "Carrot": "Vegetables",
  "Cabbage": "Vegetables",
  "Cauliflower": "Vegetables",
  "Beans": "Vegetables",
  "Beetroot": "Vegetables",
  "Broccoli": "Vegetables",
  "Moringa": "Vegetables",
  "Palak": "Greens",
  "Amaranthus": "Greens",
  "Lettuce": "Greens",
  "Spinach": "Greens",
  "Potato": "Tubers",
  "Sweet Potato": "Tubers",
  "Cassava": "Tubers",
  "Ashwagandha": "Herbal",
  "Aloe Vera": "Herbal",
  "Tulsi": "Herbal",
  "Curry Leaves": "Herbal",
  "Fenugreek": "Herbal",
  "Vetiver": "Herbal",
  "Coriander": "Herbal",
  "Vermicompost Unit": "Units",
  "Poultry Unit": "Units",
  "Goat Unit": "Units",
  "Dairy Unit": "Units",
  "Azolla Unit": "Units"
};

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
    try {
        await loadCropData();
        setupEventListeners();
        updateCategoryButtons();
    } catch (error) {
        console.error('❌ Error initializing app:', error);
        alert('Error loading the application. Please refresh the page.');
    } finally {
        hideLoading();
    }
});

// 🔍 Validate crop categorization using categoryMap
function validateCropCategorization() {
    console.log("🔍 Validating crop categorization...");
    
    const allCategories = ['Fruits', 'Vegetables', 'Greens', 'Tubers', 'Herbal', 'Units'];
    let validationErrors = [];
    
    // Check each category for correct crops
    allCategories.forEach(category => {
        const crops = cropData[category] || [];
        crops.forEach(crop => {
            const cropName = crop.English;
            if (cropName && categoryMap[cropName]) {
                const expectedCategory = categoryMap[cropName];
                if (expectedCategory !== category) {
                    validationErrors.push(`❌ ${cropName} is in ${category} but should be in ${expectedCategory}`);
                }
            }
        });
    });
    
    if (validationErrors.length === 0) {
        console.log("✅ All crops are in their correct categories!");
    } else {
        console.warn("⚠️ Category validation issues found:");
        validationErrors.forEach(error => console.warn(error));
    }
}

// 🌾 Load crop data from backend API
async function loadCropData() {
    try {
        console.log('🔄 Loading crop data from /data endpoint...');
        const response = await fetch('/data');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        cropData = data;
        console.log('✅ Crop data loaded successfully:', Object.keys(cropData));
        
        // Verify data structure
        if (!cropData || Object.keys(cropData).length === 0) {
            throw new Error('No crop data received from server');
        }
        
        // Debug logging for category counts
        const fruits = cropData.Fruits || [];
        const vegetables = cropData.Vegetables || [];
        const greens = cropData.Greens || [];
        const tubers = cropData.Tubers || [];
        const herbal = cropData.Herbal || [];
        const units = cropData.Units || [];
        
        console.table({
            Fruits: fruits.length,
            Vegetables: vegetables.length,
            Greens: greens.length,
            Tubers: tubers.length,
            Herbal: herbal.length,
            Units: units.length
        });
        console.log("✅ All categories cleaned and verified!");
        
        // Validate crop categorization using categoryMap
        validateCropCategorization();
        
        return cropData;
    } catch (error) {
        console.error('❌ Error loading crop data:', error);
        throw error; // Re-throw to be handled by caller
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
    
    // Setup modal event listeners
    setupModalEventListeners();
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
    
    // Get categories dynamically from the loaded data
    const categories = Object.keys(cropData);
    console.log('📂 Available categories:', categories);
    
    categories.forEach(category => {
        const btn = document.createElement('button');
        btn.className = 'category-btn';
        btn.textContent = getCategoryName(category, currentLanguage);
        btn.onclick = () => selectCategory(category);
        container.appendChild(btn);
    });
}

// 🏷️ Category name by language
function getCategoryName(category, lang) {
    // Check if category exists in our predefined labels
    if (categoryLabels[category]) {
        const names = categoryLabels[category].split(' / ');
        const index = { 'en': 0, 'ta': 1, 'te': 2, 'hi': 3, 'kn': 4 };
        return names[index[lang]] || names[0];
    }
    
    // For categories not in our predefined list, return the category name as-is
    // This ensures all categories from JSON data will be displayed
    return category;
}

// 🌸 Show crops in selected category
function selectCategory(category) {
    currentCategory = category;
    const allCrops = cropData[category] || [];
    
    // Filter out category header rows and invalid entries
    const validCrops = allCrops.filter(crop => {
        // Skip if English value equals the category name
        if (crop.English === category) {
            return false;
        }
        
        // Skip if Tamil is "nan" or blank
        if (crop.Tamil === 'nan' || crop.Tamil === '' || !crop.Tamil) {
            return false;
        }
        
        // Skip if English is empty or blank
        if (!crop.English || crop.English === '') {
            return false;
        }
        
        return true;
    });
    
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
        validCrops.forEach(crop => grid.appendChild(createCropCard(crop)));
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
    
    // Add click event to show crop details
    card.addEventListener('click', function() {
        showCropDetails(crop);
    });
    
    // Add cursor pointer to indicate clickable
    card.style.cursor = 'pointer';
    
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

// 🌱 Show crop details modal
async function showCropDetails(crop) {
    try {
        // Show loading in modal
        const modal = document.getElementById('crop-modal');
        const modalBody = modal.querySelector('.modal-body');
        modalBody.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading crop details...</p></div>';
        modal.style.display = 'block';
        
        // Get crop name for API call
        const cropName = crop.English?.trim() || crop.Tamil?.trim() || '';
        
        // Fetch detailed crop information
        const response = await fetch(`/crop/${encodeURIComponent(cropName)}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const cropDetails = await response.json();
        
        // Populate modal with crop details
        populateCropModal(cropDetails);
        
    } catch (error) {
        console.error('❌ Error loading crop details:', error);
        showCropDetailsError();
    }
}

// 🌐 Generate language grid with fixed 2x3 layout
function generateLanguageGrid(languages) {
    // Define the 6 languages in the required order
    const languageOrder = [
        'English', 'Tamil', 'Telugu',
        'Hindi', 'Kannada', 'Malayalam'
    ];
    
    // Debug logging for language data
    console.log('🌐 Generating language grid with data:', languages);
    
    // Helper function to get language value with case-insensitive matching
    function getLanguageValue(langKey) {
        // Try exact match first
        if (languages[langKey]) {
            const value = languages[langKey];
            const result = (value && value.trim() !== '' && value !== 'nan') ? value : '—';
            console.log(`  📝 ${langKey}: "${value}" → "${result}"`);
            return result;
        }
        
        // Try case-insensitive match
        const lowerKey = langKey.toLowerCase();
        for (const [key, value] of Object.entries(languages)) {
            if (key.toLowerCase() === lowerKey) {
                const result = (value && value.trim() !== '' && value !== 'nan') ? value : '—';
                console.log(`  📝 ${langKey} (matched ${key}): "${value}" → "${result}"`);
                return result;
            }
        }
        
        console.log(`  ❌ ${langKey}: not found → "—"`);
        return '—';
    }
    
    // Generate the 2x3 grid
    return languageOrder.map(lang => {
        const value = getLanguageValue(lang);
        return `
            <div class="language-item">
                <div class="language-name">${lang}</div>
                <div class="language-value">${value}</div>
            </div>
        `;
    }).join('');
}

// 🌾 Populate modal with crop details
function populateCropModal(cropDetails) {
    const modal = document.getElementById('crop-modal');
    const modalBody = modal.querySelector('.modal-body');
    const modalTitle = document.getElementById('modal-crop-name');
    
    // Set modal title
    modalTitle.textContent = cropDetails.name || 'Crop Details';
    
    // Debug logging
    console.log('🌾 Populating modal for crop:', cropDetails.name);
    console.log('🖼️ Image path:', cropDetails.image_path);
    console.log('🌍 Languages:', cropDetails.languages);
    console.log('🌐 Language data for', cropDetails.name, cropDetails);
    
    // Build image path using lowercase category and crop names
    const cropName = cropDetails.name || '';
    const category = cropDetails.category || '';
    
    // Convert category to lowercase for folder path
    const safeCategory = category.toLowerCase();
    
    // Convert crop name to lowercase and replace spaces, parentheses, and special chars with underscores
    const safeCrop = cropName.toLowerCase().replace(/[\s\(\)]+/g, "_");
    const firstLetter = safeCrop.charAt(0);
    const imagePath = `/static/images/${safeCategory}/${safeCrop}/${firstLetter}1.jpg`;
    
    console.log('🖼️ Trying image path:', imagePath);
    console.log('🔍 Full image URL will be:', window.location.origin + imagePath);
    
    // Create modal content with image at the top
    modalBody.innerHTML = `
        <div class="crop-image-section">
            <img src="${imagePath}" 
                 alt="${cropDetails.name || 'Crop'}" 
                 class="crop-image"
                 onerror="handleImageError(this)"
                 onload="handleImageLoad(this)">
            <div class="no-image-placeholder" style="display: none;">
                <div class="no-image-text">Image not available</div>
            </div>
        </div>
        
        <div class="crop-info-section">
            <h3>Names in Different Languages</h3>
            <div class="languages-grid" id="languages-info">
                ${generateLanguageGrid(cropDetails.languages || {})}
            </div>
        </div>
        
        <div class="crop-info-section">
            <h3>Botanical Name</h3>
            <div class="botanical-name">
                <div class="botanical-value">${cropDetails.botanical_name || 'Not available'}</div>
            </div>
        </div>
    `;
}

// 🖼️ Handle image load success
function handleImageLoad(img) {
    console.log('✅ Image loaded successfully:', img.src);
    console.log('✅ Final image path used:', img.src);
    const placeholder = img.nextElementSibling;
    if (placeholder) {
        placeholder.style.display = 'none';
    }
}

// 🖼️ Handle image load error
function handleImageError(img) {
    console.log('❌ Image failed to load:', img.src);
    console.log('⚠️ No image found for:', img.alt);
    
    // Try fallback with additional lowercase conversion
    const currentSrc = img.src;
    const fallbackPath = currentSrc.toLowerCase();
    
    if (currentSrc !== fallbackPath) {
        console.log('⚠️ Image not found, trying fallback:', fallbackPath);
        img.src = fallbackPath;
        return; // Let the image try to load the fallback
    }
    
    // If fallback also fails, show placeholder
    img.style.display = 'none';
    const placeholder = img.nextElementSibling;
    if (placeholder) {
        placeholder.style.display = 'block';
        placeholder.innerHTML = '<div class="no-image-text">Image not available</div>';
    }
}

// 🌿 Generate HTML for additional information with icons
function generateAdditionalInfoHTML(additionalInfo) {
    // Define icon mapping for different column types
    const iconMapping = {
        'BOTANICAL NAME': '🌿',
        'VALUE-ADDED PRODUCTS': '🏭',
        'AREA (ACRES)': '🌾',
        'INVESTMENT (₹)': '💰',
        'COST OF CULTIVATION (₹)': '🌱',
        'GROSS INCOME (₹)': '📈',
        'NET PROFIT (₹)': '💹',
        'Scientific Name': '🌿',
        'Family': '🌳',
        'Origin': '🌍',
        'Growing Season': '📅',
        'Nutritional Value': '🥗',
        'Uses': '🔧',
        'Cultivation Tips': '💡'
    };
    
    // Filter out language columns, empty values, and unwanted columns
    const languageColumns = ['English', 'Tamil', 'Telugu', 'Hindi', 'Kannada'];
    const unwantedColumns = ['Unnamed: 0', 'Unnamed'];
    
    const filteredInfo = Object.entries(additionalInfo).filter(([key, value]) => 
        !languageColumns.includes(key) && 
        !unwantedColumns.some(unwanted => key.includes(unwanted)) &&
        value && 
        value !== 'Not available' && 
        value !== 'nan' && 
        value !== '' &&
        value !== null &&
        value !== undefined
    );
    
    if (filteredInfo.length === 0) {
        return `
            <div class="no-additional-info">
                <div class="no-info-icon">📋</div>
                <div class="no-info-text">No additional information available for this crop.</div>
            </div>
        `;
    }
    
    return filteredInfo.map(([key, value]) => {
        const icon = iconMapping[key] || '📋';
        const formattedValue = formatValue(key, value);
        
        return `
            <div class="additional-item">
                <div class="additional-label">
                    <span class="info-icon">${icon}</span>
                    <strong>${key}:</strong>
                </div>
                <div class="additional-value">${formattedValue}</div>
            </div>
        `;
    }).join('');
}

// 💰 Format values based on column type
function formatValue(key, value) {
    // Handle null, undefined, or empty values
    if (!value || value === 'nan' || value === '') {
        return 'Not available';
    }
    
    // Format currency values
    if (key.includes('₹') || key.includes('INVESTMENT') || key.includes('COST') || key.includes('INCOME') || key.includes('PROFIT')) {
        const numValue = parseFloat(value);
        if (!isNaN(numValue)) {
            return `₹${numValue.toLocaleString('en-IN')}`;
        }
    }
    
    // Format area values
    if (key.includes('AREA')) {
        const numValue = parseFloat(value);
        if (!isNaN(numValue)) {
            return `${numValue} acres`;
        }
    }
    
    // Format botanical names (capitalize properly)
    if (key.includes('BOTANICAL') || key.includes('Scientific')) {
        return value.split(' ').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
        ).join(' ');
    }
    
    // Format value-added products (split by comma and format)
    if (key.includes('VALUE-ADDED') || key.includes('PRODUCTS')) {
        return value.split(',').map(item => item.trim()).join(', ');
    }
    
    return value;
}

// 🌍 Show error message in modal
function showCropDetailsError() {
    const modal = document.getElementById('crop-modal');
    const modalBody = modal.querySelector('.modal-body');
    const modalTitle = document.getElementById('modal-crop-name');
    
    modalTitle.textContent = 'Error';
    modalBody.innerHTML = `
        <div class="crop-info-section">
            <div style="text-align: center; padding: 40px;">
                <div style="font-size: 3rem; margin-bottom: 20px;">⚠️</div>
                <h3 style="color: #dc3545; margin-bottom: 15px;">Unable to load crop details</h3>
                <p style="color: #6c757d;">Please try again later or contact support if the problem persists.</p>
            </div>
        </div>
    `;
}

// 🌿 Modal control functions
function setupModalEventListeners() {
    const modal = document.getElementById('crop-modal');
    const closeBtn = document.getElementById('modal-close');
    const backBtn = document.getElementById('modal-back');
    
    // Close modal when clicking X
    if (closeBtn) {
        closeBtn.addEventListener('click', hideCropModal);
    }
    
    // Close modal when clicking back button
    if (backBtn) {
        backBtn.addEventListener('click', hideCropModal);
    }
    
    // Close modal when clicking outside
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                hideCropModal();
            }
        });
    }
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            hideCropModal();
        }
    });
}

function hideCropModal() {
    const modal = document.getElementById('crop-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}