# from flask import Flask, request,jsonify
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# from dotenv import load_dotenv # type: ignore
# import os

# # Load env variables
# load_dotenv()
# uri = os.getenv("MONGO_URI")

# # Connect to MongoDB
# client = MongoClient(uri, server_api=ServerApi('1'))
# db = client["testdb"]   # choose or create your DB
# collection =db['flask-tutorial']

# # Ping to check connection
# try:
#     client.admin.command('ping')
#     print("✅ Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(" MongoDB connection error:", e)

# app = Flask(__name__)

# # @app.route('/')
# # def home():
# #     day_of_week = datetime.today().strftime("%A")
# #     formatted_time = datetime.now().strftime("%H:%M:%S")
# #     return render_template('index.html', day=day_of_week, time=formatted_time)

# # @app.route('/time')
# # def time():
# #     formatted_time = datetime.now().strftime("%H:%M:%S")
# #     return formatted_time

# @app.route('/submit', methods=['POST'])
# def submit():
#     form_data = dict(request.json)
#     # Save into MongoDB collection
#     collection.insert_one(form_data)
#     return "Data submiteed successfully"

# @app.route('/view')
# def view():
#     data = collection.find()
#     data=list(data)
#     for item in data:
#         print(item)
#         del item['_id']

#     data={
#         'data':data
#     }
#     return  jsonify(data)

# @app.route('/api')
# def name():
#     name = request.values.get('name')
#     age = request.values.get('age')

#     if not age:
#         return "Please provide age"

#     age = int(age)
#     if age > 18:
#         return f"{name} you can use the site, you are adult !!"
#     else:
#         return f"{name} you are too young to use this site"

# if __name__ == '__main__':
#     app.run(port=8000,debug=True,use_reloader=False)




from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import certifi
import os

# Load env variables
load_dotenv()
uri = os.getenv("MONGO_URI")

# Connect to MongoDB
try:
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    client.admin.command('ping')
    print("✅ Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("❌ MongoDB connection error:", e)

db = client["testdb"]  # choose or create your DB
collection = db['flask-tutorial']

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

if __name__ == '__main__':
    app.run(port=8000, debug=True, use_reloader=False)
