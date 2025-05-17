import os
import keras
from keras.models import load_model
import streamlit as st 
import tensorflow as tf
import numpy as np

st.markdown('<h1 style="text-align:center; font-size:2.5em;">Flower Classification CNN Model</h1>', unsafe_allow_html=True)
flower_names = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

model = load_model(r'C:\Users\vsure\.vscode\AIML\Flower Recognization CNN Model\.ipynb_checkpoints\Flower_Recog_Model.h5')

def classify_images(image_path):
    input_image = tf.keras.utils.load_img(image_path, target_size=(180,180))
    input_image_array = tf.keras.utils.img_to_array(input_image)
    input_image_exp_dim = tf.expand_dims(input_image_array,0)

    predictions = model.predict(input_image_exp_dim)
    result = tf.nn.softmax(predictions[0])
    flower = flower_names[np.argmax(result)]
    confidence = np.max(result) * 100
    # Styled card output
    card_html = f'''
    <div style="background-color:#f8f9ff; border-radius:16px; padding:24px; width:340px; box-shadow:0 2px 8px rgba(0,0,0,0.05);">
        <div style="font-size:2em; margin-bottom:8px; color:#6c63ff;">&#9728;&#65039;</div>
        <div style="font-size:1.5em; font-weight:600; color:#222;">{flower.capitalize()}</div>
        <div style="color:#888; font-size:1.1em; margin-bottom:16px;">Confidence: {confidence:.2f}%</div>
        <a href="#" style="display:inline-block; background:#6c63ff; color:#fff; padding:8px 20px; border-radius:8px; text-decoration:none; font-weight:500;">View Details</a>
    </div>
    '''
    return card_html

uploaded_file = st.file_uploader('Upload an Image')
if uploaded_file is not None:
    with open(os.path.join(r'C:\Users\vsure\.vscode\AIML\Flower Recognization CNN Model\.ipynb_checkpoints\upload', uploaded_file.name), 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    st.image(uploaded_file, width = 200)
    st.markdown(classify_images(uploaded_file), unsafe_allow_html=True)

