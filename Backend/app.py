from flask import Flask, request, jsonify, session
from flask_cors import CORS
from jarvis import process_input, greetings, languages, category, movie_recommendation, tell_weather
import random


app = Flask(__name__)
app.secret_key = "a_super_secret_key_12345"
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

weather_prompts = [
        "Sorry, I dont have permission to your location. Where do you live ?\n",
        "I can't access your location. Could you tell me where you're located?\n",
        "I don't have access to your location data. Mind sharing where you are?\n",
        "Where are you based? (I don’t have location permissions)\n",
        "I don’t have permission to see your location. Can you tell me your city or country?\n",
        "Since I can’t detect your location automatically, could you let me know where you are?\n",
    ]

@app.route("/api/start", methods=["GET"])
def start_chat():
    greeting = random.choice(greetings)
    return jsonify({"response": greeting})


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input_raw = data.get("message")

    if not user_input_raw:
        return jsonify({"error": "No Input Provided"}), 400
    
    user_input = user_input_raw.strip().lower()
    normalized_input = user_input.title()

    if user_input in ["movie", "movies"]:
        return jsonify({"response": "Sure!, Do you want any specific category or language?"})
    

    if normalized_input in languages or normalized_input in category:
        movie_result = movie_recommendation(normalized_input)
        return jsonify({"response": movie_result})
    
    if session.get("awaiting_weather_location"):
        session["awaiting_weather_location"] = False
        weather_result = tell_weather(user_input_raw)
        return jsonify({"response": weather_result})
    
    if "weather" in user_input:
        session["awaiting_weather_location"] = True
        return jsonify({"response": random.choice(weather_prompts)})

    
    response = process_input(user_input_raw)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True, port=5000)