from flask import request, jsonify
import openai
import os

def register_routes(app):

    @app.route("/api/chat", methods=["POST"])
    def chat_with_openai():
        try:
            data = request.get_json()
            user_input = data.get("message")

            openai.api_key = os.getenv("OPENAI_API_KEY")

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )

            reply = response["choices"][0]["message"]["content"]
            return jsonify({"response": reply})

        except Exception as e:
            return jsonify({"error": str(e)}), 500
