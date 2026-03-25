from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import sys

app = Flask(__name__)
CORS(app) # This allows your HTML files to talk to this Python server

# MongoDB Connection String
# - Connection string from your provided app.py
MONGO_URI = "mongodb+srv://thampankevin44_db_user:b4C7qYkhmwT_qg8@portfoliodb.8mmpapi.mongodb.net/jerseyDB?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Trigger a connection to check if URI is valid
    client.server_info() 
    db = client["jerseyDB"]
    orders = db["orders"]
    print("✅ Successfully connected to MongoDB Atlas")
except Exception as e:
    print(f"❌ Could not connect to MongoDB: {e}")
    sys.exit(1)

@app.route("/save-order", methods=["POST"])
def save_order():
    try:
        data = request.json
        print("📥 Received data:", data)

        if not data:
            return jsonify({"message": "No data received ❌"}), 400

        # This is where the 500 error is likely happening
        result = orders.insert_one({
            "items": data.get("items", []),
            "payment": data.get("payment", "")
        })

        print(f"✅ Saved to MongoDB: {result.inserted_id}")

        return jsonify({
            "message": "Order saved successfully ✅",
            "id": str(result.inserted_id)
        })

    except Exception as e:
        # This will print the EXACT reason for the 500 error in your terminal
        print("❌ DATABASE WRITE ERROR:", str(e)) 
        return jsonify({
            "message": "Database Error",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)