from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# Configurar la API key desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form["question"]

    # Llamar a la API de ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )

    answer = response.choices[0].message["content"]
    return render_template("index.html", question=question, answer=answer)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
