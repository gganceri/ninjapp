from flask import Flask, render_template_string, request
import openai
import os
from flask_cors import CORS

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Obtener clave de API desde variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

# HTML con animación y estilos embebidos
html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Chat con OpenAI</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #f3f4f6;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: white;
            padding: 40px;
            border-radius: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 700px;
            text-align: center;
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        h1 {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        input[type="text"] {
            padding: 12px;
            width: 70%;
            border: 1px solid #ccc;
            border-radius: 20px;
            outline: none;
            font-size: 16px;
        }
        button {
            background: #6c47ff;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 20px;
            margin-left: 10px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        button:hover {
            background: #4c2bdc;
        }
        .response {
            margin-top: 20px;
            font-size: 15px;
            color: #333;
            white-space: pre-wrap;
        }
        .error {
            color: red;
            margin-top: 20px;
        }
    </style>
</head>
<body>
<div class="card">
    <h1>💬 Chat con OpenAI</h1>
    <form method="post">
        <input type="text" name="pregunta" placeholder="Escribe tu pregunta">
        <button type="submit">Enviar</button>
    </form>
    {% if respuesta %}
        <div class="response">{{ respuesta }}</div>
    {% elif error %}
        <div class="error"><strong>Error:</strong> {{ error }}</div>
    {% endif %}
</div>
</body>
</html>
"""

# Ruta principal
@app.route("/", methods=["GET", "POST"])
def index():
    respuesta = ""
    error = ""

    if request.method == "POST":
        pregunta = request.form.get("pregunta")
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": pregunta}]
            )
            respuesta = completion.choices[0].message.content
        except Exception as e:
            error = str(e)

    return render_template_string(html_template, respuesta=respuesta, error=error)

# Iniciar servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
