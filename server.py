from flask import Flask, render_template, request, jsonify
import json
from nutrition_counter import get_vals
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            result = get_vals(filepath)
            # Clean up the uploaded file
            os.remove(filepath)
            return jsonify(result)
        except Exception as e:
            # Clean up the uploaded file in case of error
            os.remove(filepath)
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400

if __name__ == "__main__":
    app.run(debug=True)