from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

# Cliente moderno de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta = None
    if request.method == "POST":
        pregunta = request.form.get("pregunta", "")
        if pregunta:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": pregunta}]
                )
                respuesta = response.choices[0].message.content.strip()
            except Exception as e:
                respuesta = f"Error: {str(e)}"
        else:
            respuesta = "No se recibió ninguna pregunta."

    return render_template("index.html", respuesta=respuesta)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
