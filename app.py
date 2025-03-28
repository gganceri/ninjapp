import os
import openai
from flask import Flask, render_template_string, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>NinjaApp ✨</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 2rem;
            border-radius: 2rem;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            max-width: 600px;
            width: 100%;
            text-align: center;
            animation: fadeIn 1.2s ease-in-out;
        }
        h1 {
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }
        input[type="text"] {
            width: 70%;
            padding: 0.7rem;
            border-radius: 1rem;
            border: 1px solid #ccc;
        }
        button {
            padding: 0.7rem 1.5rem;
            border: none;
            background: #4f46e5;
            color: white;
            font-weight: bold;
            border-radius: 1rem;
            margin-left: 1rem;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        button:hover {
            background: #3730a3;
        }
        .respuesta {
            margin-top: 2rem;
            font-size: 1rem;
            color: #333;
            animation: fadeIn 0.8s ease-in-out;
        }
        .thinking {
            font-style: italic;
            color: #999;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>💬 Chat con OpenAI</h1>
        <form method="post">
            <input type="text" name="pregunta" placeholder="Escribe tu pregunta" required>
            <button type="submit">Enviar</button>
        </form>
        {% if respuesta %}
            <div class="respuesta">🧠 {{ respuesta }}</div>
        {% endif %}
        {% if error %}
            <div class="respuesta">⚠️ Error: {{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    respuesta = None
    error = None
    if request.method == 'POST':
        pregunta = request.form['pregunta']
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": pregunta}]
            )
            respuesta = completion.choices[0].message['content']
        except Exception as e:
            error = str(e)
    return render_template_string(html_template, respuesta=respuesta, error=error)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
