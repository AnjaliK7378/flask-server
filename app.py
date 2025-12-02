from flask import Flask, request, jsonify
from flask_cors import CORS   # <-- YE LINE ADD KARNA ZAROORI HAI
import random

app = Flask(__name__)
CORS(app)   # <-- YE BHI ADD KARNA HAI (Android se call accept karega)

# MEGA DATABASE — Indian farmers jo real mein lagate hain
CROPS_DATABASE = [
    # KHARIF FIELD CROPS
    {"crop": "Rice (धान)", "type": "Cereal", "season": "Kharif", "N": "low", "P": "med", "K": "med", "ph": "5.5-7.5"},
    {"crop": "Maize (मक्का)", "type": "Cereal", "season": "Kharif", "N": "med", "P": "high", "K": "high"},
    {"crop": "Jowar (ज्वार)", "type": "Cereal", "season": "Kharif", "N": "low", "P": "low", "K": "med"},
    {"crop": "Bajra (बाजरा)", "type": "Cereal", "season": "Kharif", "N": "low", "P": "low"},
    {"crop": "Cotton (कपास)", "type": "Fiber", "season": "Kharif", "N": "med", "P": "high"},
    {"crop": "Soybean (सोयाबीन)", "type": "Oilseed", "season": "Kharif", "N": "low", "P": "high"},
    {"crop": "Groundnut (मूंगफली)", "type": "Oilseed", "season": "Kharif", "N": "med", "P": "high"},
    {"crop": "Tur/Arhar (अरहर)", "type": "Pulse", "season": "Kharif", "N": "low", "P": "med"},
    {"crop": "Urad (उड़द)", "type": "Pulse", "season": "Kharif", "N": "low"},
    {"crop": "Moong (मूंग)", "type": "Pulse", "season": "Kharif/Zaid", "N": "low"},
    # RABI CROPS
    {"crop": "Wheat (गेहूं)", "type": "Cereal", "season": "Rabi", "N": "high", "P": "med", "K": "med"},
    {"crop": "Gram (चना)", "type": "Pulse", "season": "Rabi", "N": "low"},
    {"crop": "Mustard (सरसों)", "type": "Oilseed", "season": "Rabi", "N": "med", "P": "high"},
    {"crop": "Barley (जौ)", "type": "Cereal", "season": "Rabi", "N": "med"},
    {"crop": "Potato (आलू)", "type": "Vegetable", "season": "Rabi", "N": "high", "K": "high"},
    # VEGETABLES
    {"crop": "Tomato (टमाटर)", "type": "Vegetable", "season": "All", "ph": "6.0-7.0", "N": "high"},
    {"crop": "Brinjal (बैंगन)", "type": "Vegetable", "season": "All", "N": "high"},
    {"crop": "Ladyfinger (भिंडी)", "type": "Vegetable", "season": "Kharif/Zaid", "N": "med"},
    {"crop": "Chilli (मिर्च)", "type": "Vegetable", "season": "All", "P": "high"},
    {"crop": "Onion (प्याज)", "type": "Vegetable", "season": "Rabi", "P": "high"},
    {"crop": "Cucumber (खीरा)", "type": "Vegetable", "season": "Zaid", "K": "high"},
    {"crop": "Bitter Gourd (करेला)", "type": "Vegetable", "season": "Zaid", "N": "med"},
    # FRUITS
    {"crop": "Mango (आम)", "type": "Fruit", "season": "Perennial", "K": "high", "ph": "6.0-7.5"},
    {"crop": "Banana (केला)", "type": "Fruit", "season": "Perennial", "K": "very_high"},
    {"crop": "Papaya (पपीता)", "type": "Fruit", "season": "Perennial", "N": "high"},
    {"crop": "Guava (अमरूद)", "type": "Fruit", "season": "Perennial"},
    {"crop": "Muskmelon (खरबूजा)", "type": "Fruit", "season": "Zaid", "K": "high"},
    {"crop": "Watermelon (तरबूज)", "type": "Fruit", "season": "Zaid", "K": "high"},
    {"crop": "Pomegranate (अनार)", "type": "Fruit", "season": "Perennial", "ph": "6.5-7.5"},
]

@app.route('/predict_crop', methods=['POST'])
def predict_crop():
    data = request.json
    N = float(data['N'])
    P = float(data['P'])
    K = float(data['K'])
    ph = float(data['ph'])
    season = data.get('season', 'Kharif')

    suitable = []
    for c in CROPS_DATABASE:
        match = True

        if 'season' in c and season not in c['season'] and c['season'] != "All" and c['season'] != "Perennial":
            match = False

        if 'N' in c:
            if (c['N'] == "low" and N > 60) or (c['N'] == "high" and N < 70) or (c['N'] == "very_high" and N < 100):
                match = False
        if 'P' in c and, c['P'] == "high" and P < 45:
            match = False
        if 'K' in c:
            if (c['K'] == "high" and K < 50) or (c['K'] == "very_high" and K < 90):
                match = False
        if 'ph' in c:
            try:
                min_ph, max_ph = map(float, c['ph'].split('-'))
                if not (min_ph <= ph <= max_ph):
                    match = False
            except:
                pass

        if match:
            suitable.append(c)

    random.shuffle(suitable)
    top5 = suitable[:5] or [{"crop": "Moong (मूंग)", "type": "Pulse"}]

    result = []
    for i, crop in enumerate(top5, 1):
        result.append({
            "rank": i,
            "crop": crop['crop'],
            "type": crop['type'],
            "reason": f"Best match for {season} season + current soil"
        })

    return jsonify({"recommendations": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
