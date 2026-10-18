from flask import Flask, render_template, jsonify, request
import json
from main import generate_language_pipeline

app = Flask(__name__, template_folder=".")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/questions", methods=["GET"])
def get_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data["questions"])

@app.route("/api/generate", methods=["POST"])
def generate_language():
    user_answers = request.json.get("answers", [])
    result = generate_language_pipeline(user_answers)
    return jsonify(result)

if __name__ == "__main__":
    print("Servidor iniciado en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)