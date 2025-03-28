from flask import Flask, request, render_template_string
from flask_cors import CORS
import openai
import os

# Cargar API Key desde variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat con OpenAI</title>
    <style>
        body {
            font-family: "Segoe UI", sans-serif;
            background-color: #f4f4f7;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .chat-box {
            background: white;
            padding: 30px;
            border-radius: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            text-align: center;
            animation: fadeIn 1s ease-out;
        }
        h1 {
            margin-bottom: 20px;
        }
        input[type="text"] {
            padding: 10px;
            width: 300px;
            border: 2px solid #ccc;
            border-radius: 30px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        input[type="text"]:focus {
            border-color: #7a5cfa;
            outline: none;
        }
        button {
            padding: 10px 25px;
            background: #7a5cfa;
            border: none;
            color: white;
            font-size: 16px;
            margin-left: 10px;
            border-radius: 30px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        button:hover {
            background: #6847f5;
        }
        .response {
            margin-top: 20px;
            font-size: 16px;
            color: #333;
            animation: fadeInUp 0.5s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="chat-box">
        <h1>💬 Chat con OpenAI</h1>
        <form method="post">
            <input type="text" name="pregunta" placeholder="Escribe tu pregunta" required />
            <button type="submit">Enviar</button>
        </form>
        {% if respuesta %}
        <div class="response"><strong>Respuesta:</strong><br>{{ respuesta }}</div>
        {% elif error %}
        <div class="response" style="color: red;"><strong>Error:</strong><br>{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chat():
    respuesta = None
    error = None
    if request.method == "POST":
        pregunta = request.form["pregunta"]
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": pregunta}]
            )
            respuesta = completion.choices[0].message["content"]
        except Exception as e:
            error = str(e)
    return render_template_string(html, respuesta=respuesta, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
