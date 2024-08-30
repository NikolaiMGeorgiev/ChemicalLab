from flask import Flask, request, jsonify
from  database import DB

db = DB()
app = Flask(__name__)

@app.route("/new_chat", methods=["POST"])
def add_chat():
    try:
        data = request.get_json()
        db.add_chat(None, data["vendor_id"])
        chat_data = db.get_pending_chat(data["vendor_id"])
        if chat_data:
            return jsonify({
                "status": "OK",
                "chat_id": chat_data["id"]
            })
        raise Exception
    except Exception as e:
        print(e)
        return jsonify({
            "status": "ERROR",
            "message": "Chat creation failed"
        })

@app.route("/new_chat", methods=["GET"])
def get_chat():
    try:
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
    except Exception as e:
        print(e)
        return jsonify({
            "status": "ERROR",
            "message": "Failed to join chat"
        })

@app.route("/start_chat", methods=["GET"])
def start_chat():
    try:
        chat_id = request.args.get("chat_id")
        chat_data = db.get_chat(chat_id)
        if chat_data:
            return jsonify({
                "status": "OK",
                "user_id": chat_data["user_id"],
                "vendor_id": chat_data["vendor_id"]
            })
        raise Exception
    except Exception as e:
        print(e)
        return jsonify({
            "status": "ERROR",
            "message": "No chat with this id"
        })

@app.route("/message", methods=["POST"])
def add_message():
    try:
        data = request.get_json()
        db.add_message(data["chat_id"], data["content"], data["sender"])
        return jsonify({
            "status": "OK",
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "ERROR",
            "message": "Failed to send message"
        })
    

@app.route("/message", methods=["GET"])
def get_message():
    try:
        chat_id = request.args.get("chat_id")
        sender = "user" if request.args.get("receiver") == "vendor" else "vendor"
        message_data = db.get_unreceived_message(chat_id, sender)
        if message_data:
            return jsonify({
                "status": "OK",
                "message": message_data["content"],
            })
        return jsonify({
            "status": "OK"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "ERROR",
            "message": "Failed to receive message"
        })

if __name__ == '__main__':
    app.run(host='localhost', port=12345, debug=True)
