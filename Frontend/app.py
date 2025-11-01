from flask import Flask, render_template,request
from datetime import datetime
import requests 
BACKEND_URL='http://127.0.0.1:8000'

app = Flask(__name__)

@app.route('/')
def home():
    day_of_week = datetime.today().strftime("%A")
    formatted_time = datetime.now().strftime("%H:%M:%S")
    return render_template('index.html', day=day_of_week, time=formatted_time)

@app.route('/submit', methods=['POST'])
def submit():
    form_data=dict(request.form)
    requests.post(BACKEND_URL+'/submit',json=form_data)
    return "Data submitted successfuly"

@app.route('/get_data')
def get_data():
    response=requests.get(BACKEND_URL+'/view')
    return response.json()

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
