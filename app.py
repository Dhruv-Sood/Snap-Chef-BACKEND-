'''
from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("No API key set for Google Generative AI")

# Configure the generative AI model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/get_gemini_response', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400

    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # Process the uploaded image
    try:
        img = PIL.Image.open(filename)
        response = model.generate_content(["Only answer if you identify this image as food and tell me the recipe", img])
        return jsonify({'message': response.text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

'''

from flask import Flask, render_template


import os
from flask_cors import CORS
import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv
import io  # Added for handling image data
app = Flask(__name__)
# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("No API key set for Google Generative AI")

# Configure the generative AI model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/get_gemini_response', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400

    # Read image data from request
    image_data = file.read()

    # Process the uploaded image data
    try:
        img = PIL.Image.open(io.BytesIO(image_data))
        response = model.generate_content(["Only answer if you identify this image as food and tell me the recipe", img])
        return jsonify({'message': response.text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

