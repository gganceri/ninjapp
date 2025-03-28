import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

# Lee la API KEY desde Railway
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Habilita CORS para todos los orígenes

@app.route("/")
def home():
    return "🧠 NinjaApp está corriendo con OpenAI."

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Falta el mensaje"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sos un asistente técnico de NinjaApp."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        ai_message = response["choices"][0]["message"]["content"].strip()
        return jsonify({"response": ai_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
