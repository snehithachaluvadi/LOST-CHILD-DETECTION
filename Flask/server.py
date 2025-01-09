import os
from flask import Flask, render_template, request, jsonify
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from tinydb import TinyDB
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'Flask/known/'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Connect to TinyDB database
# We are using tinedb for ease of use, but in a real-world scenario, we would use a proper SQL database
# DB contents can be seen easily inside the JSON file
db = TinyDB('db.json')

# All valid usernames to their respective passwords
username_to_password_map = {
    "admin": "admin",
    "password": "password"
}

@app.route('/')
def home():
    return render_template('login.html')

# Route to tell if given credentials are valid
@app.route('/login/', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username in username_to_password_map and username_to_password_map.get(username) == password:
        return jsonify({"message": "Hello, {}!".format(username)}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Route to upload an image and store information about the child in the database
@app.route('/upload_image/', methods=['POST'])
def upload_image():
    # without an image file, we cannot proceed
    if 'file' not in request.files:
        return 'No file part', 400   
    # get the file
    file = request.files['file']
    if file.filename == '':
        # flask will automatically return this in JSON format along with the status code 400
        return 'No selected file', 400
    
    # if we have a valid file, proceed to save it and store the information in the database
    if file:
        filename = secure_filename(file.filename)
        # Save the image to the folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        name = request.form.get('name')
        age = request.form.get('age')
        guardian_name = request.form.get('guardian_name')
        guardian_phone = request.form.get('guardian_phone')
        db.insert(
            {
                'name': name,
                'age': age,
                'guardian_name': guardian_name,
                'guardian_phone': guardian_phone,
                'image_name': filename
            }
        )
        # flask will automatically return this in JSON format along with the status code 200
        return 'File uploaded and information stored', 200

if __name__ == '__main__':
    app.run(debug=True)
