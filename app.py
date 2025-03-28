from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# Cargar la API key desde una variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta = None
    if request.method == "POST":
        pregunta = request.form.get("pregunta", "")  # evitar error si no hay campo
        if pregunta:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": pregunta}
                    ]
                )
                respuesta = response.choices[0].message["content"].strip()
            except Exception as e:
                respuesta = f"Error: {str(e)}"
        else:
            respuesta = "No se recibió ninguna pregunta."

    return render_template("index.html", respuesta=respuesta)
    
if __name__ == "__main__":
    app.run(debug=True)
