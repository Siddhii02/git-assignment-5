from flask import Flask, render_template, request
from datetime import datetime
import requests

# ✅ Create Flask app FIRST
app = Flask(__name__)

# Backend server URL
BACKEND_URL = 'http://127.0.0.1:8000'


# -----------------------------
# Home Route (renders index.html)
# -----------------------------
@app.route('/')
def home():
    day_of_week = datetime.today().strftime("%A")
    formatted_time = datetime.now().strftime("%H:%M:%S")
    return render_template('index.html', day=day_of_week, time=formatted_time)


# -----------------------------
# Old submit route (kept from previous project)
# -----------------------------
@app.route('/submit', methods=['POST'])
def submit():
    form_data = dict(request.form)
    requests.post(f'{BACKEND_URL}/submit', json=form_data)
    return "Data submitted successfully"


# -----------------------------
# ✅ New route for To-Do form (Step 3)
# -----------------------------
@app.route('/submit_todo', methods=['POST'])
def submit_todo():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')
    item_id = request.form.get('itemId')
    item_uuid = request.form.get('itemUUID')  
    item_description = request.form.get('itemDescription')
    try:
        response = requests.post(
            f'{BACKEND_URL}/submittodoitem',
            data={'itemName': item_name, 'itemDescription': item_description,'itemId': item_id, 'itemUUID': item_uuid,'itemDescription': item_description }
        )

        if response.status_code == 200:
            return "✅ To-Do item submitted successfully!"
        else:
            return f"❌ Failed to submit To-Do item. Backend returned: {response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ Error communicating with backend: {str(e)}"


# -----------------------------
# Route to view data
# -----------------------------
@app.route('/get_data')
def get_data():
    response = requests.get(f'{BACKEND_URL}/view')
    return response.json()


# -----------------------------
# Run the app
# -----------------------------
if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False)
