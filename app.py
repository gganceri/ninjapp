from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

# Configura tu clave API desde la variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta = ""
    if request.method == "POST":
        pregunta = request.form["pregunta"]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": pregunta}
            ]
        )
        respuesta = response.choices[0].message["content"]

    return render_template("index.html", respuesta=respuesta)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
