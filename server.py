from flask import Flask, request, jsonify, render_template, Response
import ollama
import pprint
import json

from threading import Thread
import webview

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    llama_chat_history = None

    with open("chat_history.json", "r") as f:
        llama_chat_history = json.load(f)

    user_input = request.json.get("prompt")
    chat_id = request.json.get("id")

    llama_chat_history[chat_id]["history"].append({'role': 'user', 'content': user_input})

    reply = ""
    response_stream = ollama.chat(
        model='llama3.2',
        messages=llama_chat_history[chat_id]["history"],
        stream=True
    )
    for chunk in response_stream:
        reply += chunk['message']['content']
        
    llama_chat_history[chat_id]["history"].append({'role': 'assistant', 'content': reply})

    with open("chat_history.json", "w") as f:
        json.dump(llama_chat_history, f, indent=4)

    pprint.pprint(llama_chat_history[chat_id]["history"])

    return jsonify({"reply": reply})

@app.route("/history", methods=["GET"])
def history():
    llama_chat_history = None

    with open("chat_history.json", "r") as f:
        llama_chat_history = json.load(f)

    return jsonify(llama_chat_history)

@app.route("/edit_chat", methods=["POST"])
def edit_chat():
    name = request.json.get("name")
    remove_or_add = request.json.get("type")

    llama_chat_history = None

    with open("chat_history.json", "r") as f:
        llama_chat_history = json.load(f)

    if remove_or_add == "add":
        llama_chat_history.append({
            "name": name,
            "history": []
        })

    elif remove_or_add == "remove":
        for i, c in enumerate(llama_chat_history):
            if c["name"] == name:
                del llama_chat_history[i]

    with open("chat_history.json", "w") as f:
        json.dump(llama_chat_history, f, indent=4)

    return Response(status=200)

if __name__ == "__main__":
    # Thread(target=lambda: app.run(debug=True, use_reloader=False)).start()

    # print("Starting Webview...")
    # webview.create_window("Offline AI", "http://127.0.0.1:5000/")
    app.run(debug=True, use_reloader=False)

