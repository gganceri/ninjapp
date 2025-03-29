from flask import request, jsonify, render_template
import openai
import os
from ninjaapp.projects import get_projects

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

  @app.route("/dashboard")
  def dashboard():
    projects = get_projects()
    return render_template("dashboard.html", projects=projects)
