from flask import Flask, request, jsonify, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import certifi
from bson import ObjectId

import os

load_dotenv()
uri = os.getenv("MONGO_URI")


try:
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    client.admin.command('ping')
    print("✅ Pinged your deployment. Successfully connected to MongoDB!")
except Exception as e:
    print("❌ MongoDB connection error:", e)


db = client["testdb"] 
collection = db["flask-tutorial"]

app = Flask(__name__)


@app.route('/submit', methods=['POST'])
def submit():
    form_data = dict(request.json)
    collection.insert_one(form_data)
    return "Data submitted successfully"

@app.route('/view')
def view():
    data = list(collection.find({}, {'_id': 0}))  # remove _id directly
    return jsonify({'data': data})

@app.route('/api')
def api():
    name = request.values.get('name')
    age = request.values.get('age')

    if not age:
        return "Please provide age"
    age = int(age)
    if age > 18:
        return f"{name}, you can use the site, you are an adult!"
    else:
        return f"{name}, you are too young to use this site."

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    try:
        item_name = request.form.get('itemName')
        item_description = request.form.get('itemDescription')

        if not item_name or not item_description:
            return jsonify({"error": "Missing itemName or itemDescription"}), 400

        data = {"itemName": item_name, "itemDescription": item_description}
        result = collection.insert_one(data)

        # ✅ Convert the inserted ObjectId to string so JSON can handle it
        data["_id"] = str(result.inserted_id)

        return jsonify({
            "message": "To-Do item added successfully!",
            "data": data
        }), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500






if __name__ == '__main__':
    app.run(port=8000, debug=True, use_reloader=False)
