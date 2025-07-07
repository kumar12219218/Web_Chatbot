from flask import Flask, render_template, request, jsonify, session
from chatbot import create_conversation_chain
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret_key")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "No input provided."})

    history = session.get("chat_history", [])
    response, updated_history = create_conversation_chain(user_input, history)
    session["chat_history"] = updated_history

    return jsonify({"response": response})

@app.route("/clear")
def clear():
    session.clear()
    return "Chat history cleared."

if __name__ == "__main__":
    app.run(debug=True)
