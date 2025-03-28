from flask import Flask, request, render_template_string
from flask_cors import CORS
import openai
import os

# Configurar Flask y CORS
app = Flask(__name__)
CORS(app)

# Cargar la API key desde variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# HTML + CSS + JS en un solo bloque para visual simple
html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Chat con OpenAI</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f2f2f2;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: white;
            padding: 2rem;
            border-radius: 2rem;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
            width: 90%;
            max-width: 600px;
            text-align: center;
            animation: fadeIn 1s ease;
        }
        h1 {
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }
        input[type="text"] {
            width: 70%;
            padding: 0.6rem;
            border-radius: 1rem;
            border: 1px solid #ccc;
            font-size: 1rem;
        }
        button {
            padding: 0.6rem 1.2rem;
            background-color: #6c47ff;
            color: white;
            border: none;
            border-radius: 1rem;
            font-weight: bold;
            font-size: 1rem;
            cursor: pointer;
            margin-left: 1rem;
        }
        .respuesta {
            margin-top: 1.5rem;
            font-size: 1rem;
            color: #333;
        }
        .error {
            color: red;
            margin-top: 1.2rem;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>💬 Chat con OpenAI</h1>
        <form method="POST">
            <input type="text" name="pregunta" placeholder="Escribe tu pregunta" required>
            <button type="submit">Enviar</button>
        </form>
        {% if respuesta %}
            <div class="respuesta">{{ respuesta }}</div>
        {% elif error %}
            <div class="error"><strong>Error:</strong> {{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    respuesta = None
    error = None
    if request.method == "POST":
        pregunta = request.form.get("pregunta")
        if not openai.api_key:
            error = "No se ha definido la clave API. Verifica la variable OPENAI_API_KEY."
        else:
            try:
                respuesta_api = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Sos un experto en vidrios y láminas para ventanas."},
                        {"role": "user", "content": pregunta}
                    ]
                )
                respuesta = respuesta_api.choices[0].message.content
            except Exception as e:
                error = str(e)
    return render_template_string(html_template, respuesta=respuesta, error=error)

# Puerto para Railway
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
