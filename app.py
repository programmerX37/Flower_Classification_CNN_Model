from flask import Flask, render_template, request, jsonify
from keras.models import load_model
import tensorflow as tf
import numpy as np
import os
from werkzeug.utils import secure_filename

# === Flask Setup ===
BASE_DIR = r"C:\Users\vsure\.vscode\AIML\Flower Recognization CNN Model\.ipynb_checkpoints"
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# === Load Model ===
model_path = os.path.join(BASE_DIR, 'Flower_Recog_Model.h5')
model = load_model(model_path)
flower_names = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

# === Helper Function to Classify ===
def classify_image(image_path):
    image = tf.keras.utils.load_img(image_path, target_size=(180, 180))
    img_array = tf.keras.utils.img_to_array(image)
    img_expanded = tf.expand_dims(img_array, 0)
    prediction = model.predict(img_expanded)
    result = tf.nn.softmax(prediction[0])
    label = flower_names[np.argmax(result)]
    confidence = np.max(result) * 100
    return label.capitalize(), confidence

# === Routes ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        label, confidence = classify_image(filepath)
        os.remove(filepath)  # Clean up
        return jsonify({
            'flower': label,
            'confidence': f'{confidence:.2f}%'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === Run App ===
if __name__ == '__main__':
    app.run(debug=True)
