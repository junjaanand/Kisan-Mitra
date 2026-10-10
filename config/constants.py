"""Constants, reference data, and UI helpers for KisanMitra."""

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Jammu and Kashmir"
]

STATE_DISTRICTS = {
    "Maharashtra": ["Nashik", "Pune", "Ahmednagar", "Solapur", "Kolhapur", "Nagpur", "Amravati", "Aurangabad / Chhatrapati Sambhajinagar", "Jalgaon", "Satara"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala", "Bathinda", "Sangrur", "Firozpur", "Hoshiarpur"],
    "Haryana": ["Karnal", "Hisar", "Ambala", "Rohtak", "Sirsa", "Kurukshetra", "Panipat", "Sonipat"],
    "Madhya Pradesh": ["Indore", "Ujjain", "Bhopal", "Dewas", "Sehore", "Hoshangabad", "Chhindwara", "Gwalior"],
    "Uttar Pradesh": ["Varanasi", "Agra", "Meerut", "Bareilly", "Kanpur", "Aligarh", "Prayagraj", "Gorakhpur"],
    "Gujarat": ["Rajkot", "Surat", "Ahmedabad", "Vadodara", "Junagadh", "Mehsana", "Amreli", "Bhavnagar"],
    "Rajasthan": ["Kota", "Jaipur", "Sri Ganganagar", "Jodhpur", "Alwar", "Nagaur", "Bikaner", "Hanumangarh"],
    "Andhra Pradesh": ["Guntur", "Krishna", "Kurnool", "Godavari", "Visakhapatnam", "Anantapur", "Nellore"],
    "Karnataka": ["Belagavi", "Dharwad", "Shivamogga", "Ballari", "Mysuru", "Davangere", "Haveri", "Kolar"],
    "Tamil Nadu": ["Coimbatore", "Thanjavur", "Madurai", "Salem", "Erode", "Tiruchirappalli", "Dindigul"],
    "Bihar": ["Patna", "Muzaffarpur", "Bhagalpur", "Gaya", "Samastipur", "Begusarai", "Purnia"],
    "West Bengal": ["Burdwan", "Hooghly", "Nadia", "Murshidabad", "North 24 Parganas", "Malda"]
}

MAJOR_CROPS = [
    # Vegetables & Roots
    "Onion", "Tomato", "Potato", "Garlic", "Ginger", "Green Chilli",
    "Cauliflower", "Cabbage", "Brinjal / Eggplant", "Okra / Bhindi", "Peas / Matar",
    # Cereals & Millets
    "Wheat", "Paddy / Rice", "Maize / Corn", "Bajra (Pearl Millet)", "Jowar (Sorghum)", "Ragi (Finger Millet)",
    # Pulses & Legumes
    "Chana / Gram", "Tur / Arhar Dal", "Moong Dal", "Urad Dal", "Masoor Dal",
    # Oilseeds & Cash Crops
    "Soybean", "Mustard", "Groundnut", "Cotton", "Sugarcane", "Sunflower", "Jute", "Tobacco",
    # Spices & Plantation
    "Cumin / Jeera", "Turmeric / Haldi", "Black Pepper", "Cardamom", "Coriander / Dhaniya",
    "Tea", "Coffee", "Rubber", "Coconut", "Arecanut / Supari",
    # Fruits
    "Apple", "Mango", "Banana", "Pomegranate / Anar", "Grapes", "Citrus / Orange", "Papaya", "Guava"
]

CROP_ICONS = {
    "Onion": "🧅", "Tomato": "🍅", "Potato": "🥔", "Wheat": "🌾",
    "Paddy / Rice": "🍚", "Soybean": "🌱", "Cotton": "☁️", "Mustard": "🌼",
    "Chana / Gram": "🫘", "Maize / Corn": "🌽", "Tur / Arhar Dal": "🥣",
    "Green Chilli": "🌶️", "Sugarcane": "🎋", "Garlic": "🧄", "Ginger": "🫚",
    "Groundnut": "🥜", "Banana": "🍌", "Mango": "🥭", "Apple": "🍎",
    "Grapes": "🍇", "Pomegranate / Anar": "🫐", "Papaya": "🍈", "Citrus / Orange": "🍊",
    "Cumin / Jeera": "🌿", "Turmeric / Haldi": "🟡", "Cardamom": "🌱",
    "Tea": "🍵", "Coffee": "☕", "Coconut": "🥥", "Moong Dal": "🫘",
    "Urad Dal": "🫘", "Cauliflower": "🥦", "Cabbage": "🥬", "Brinjal / Eggplant": "🍆",
    "Okra / Bhindi": "🌱", "General": "🌿"
}

SEVERITY_COLORS = {
    "URGENT": "red",
    "IMPORTANT": "orange",
    "INFO": "blue"
}

RECOMMENDATION_COLORS = {
    "SELL NOW": "#2E7D32",       # Green
    "HOLD": "#D84315",           # Amber / Orange-Red
    "WATCH MARKET": "#1565C0"    # Blue
}

# 4 Realistic Demo Personas for 1-click test
DEMO_PERSONAS = {
    "Rajesh Patil (Nashik)": {
        "farmer_name": "Rajesh Patil",
        "state": "Maharashtra",
        "district": "Nashik",
        "crops": ["Onion", "Tomato"],
        "farm_size_acres": 2.5,
        "season": "Rabi (Winter / Spring)",
        "irrigation": "Canal / Borewell / Tubewell",
        "description": "Onion & Tomato cultivator looking for best selling window & mandi comparison."
    },
    "Sukhwinder Singh (Amritsar)": {
        "farmer_name": "Sukhwinder Singh",
        "state": "Punjab",
        "district": "Amritsar",
        "crops": ["Wheat", "Mustard"],
        "farm_size_acres": 5.0,
        "season": "Rabi (Winter / Spring)",
        "irrigation": "Canal / Borewell / Tubewell",
        "description": "Grain & oilseed grower tracking procurement rates and input fertilizer discounts."
    },
    "Lakshmi Devi (Guntur)": {
        "farmer_name": "Lakshmi Devi",
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "crops": ["Cotton", "Green Chilli"],
        "farm_size_acres": 3.0,
        "season": "Kharif (Monsoon / Summer)",
        "irrigation": "Drip / Sprinkler",
        "description": "Commercial cash crop farmer needing pest alerts and high-rate trading yards."
    },
    "Rameshwar Yadav (Indore)": {
        "farmer_name": "Rameshwar Yadav",
        "state": "Madhya Pradesh",
        "district": "Indore",
        "crops": ["Soybean", "Wheat"],
        "farm_size_acres": 4.0,
        "season": "Rabi (Winter / Spring)",
        "irrigation": "Canal / Borewell / Tubewell",
        "description": "Soybean & wheat grower looking for seasonal price peaks and warehouse storage."
    }
}
