import os
from flask import Flask, request
from flask_cors import CORS
import openai

# Cargar clave desde variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "<h2>💬 Chat con OpenAI</h2><form method='post' action='/chat'>" \
           "<input name='prompt' placeholder='Escribe tu pregunta' style='width:300px'>" \
           "<input type='submit' value='Enviar'></form>"

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.form.get("prompt", "")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response['choices'][0]['message']['content']
        return f"<h2>💬 Chat con OpenAI</h2><p><strong>Pregunta:</strong> {prompt}</p>" \
               f"<p><strong>Respuesta:</strong> {answer}</p><br><a href='/'>Volver</a>"
    except Exception as e:
        return f"<h2>⚠️ Error:</h2><pre>{e}</pre><br><a href='/'>Volver</a>"

if __name__ == "__main__":
    import sys
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
