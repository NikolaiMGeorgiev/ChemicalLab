from flask import Flask, request, jsonify
from  database import DB

db = DB()
app = Flask(__name__)

@app.route("/new_chat", methods=["POST"])
def add_chat():
    data = request.get_json()
    db.add_chat(None, data["vendor_id"])
    chat_data = db.get_pending_chat(data["vendor_id"])

    response = {
        "status": "OK",
        "chat_id": chat_data["id"]
    }

    return jsonify(response)

@app.route("/new_chat", methods=["GET"])
def get_chat():
    user_id = request.args.get("user_id")
    chat_data = db.join_pending_chat(user_id)
    if chat_data:
        return jsonify({
            "status": "OK",
            "chat_id": chat_data["id"],
            "vendor_id": chat_data["vendor_id"]
        })
    return jsonify({
        "status": "OK"
    })

@app.route("/start_chat", methods=["GET"])
def start_chat():
    chat_id = request.args.get("chat_id")
    print(chat_id)
    chat_data = db.get_chat(chat_id)
    if chat_data:
        return jsonify({
            "status": "OK",
            "user_id": chat_data["user_id"],
            "vendor_id": chat_data["vendor_id"]
        })
    return jsonify({
        "status": "OK"
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=12345, debug=True)
