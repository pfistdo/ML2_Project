from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
from PIL import Image
import numpy as np
import pandas as pd

app = Flask(
    __name__, static_folder="web", static_url_path="/", template_folder="web/templates"
)
app.config["UPLOAD_FOLDER"] = "web/uploads"  # folder to save uploaded images
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000  # 16MB


# Index page
@app.route("/")
def index():
    return render_template("index.html")


# Classify image
@app.route("/model/image", methods=["POST"])
def classify_dog():
    classes_labels = [
        "Afghan",
        "African Wild Dog",
        "Airedale",
        "American Hairless",
        "American Spaniel",
        "Basenji",
        "Basset",
        "Beagle",
        "Bearded Collie",
        "Bermaise",
        "Bichon Frise",
        "Blenheim",
        "Bloodhound",
        "Bluetick",
        "Border Collie",
        "Borzoi",
        "Boston Terrier",
        "Boxer",
        "Bull Mastiff",
        "Bull Terrier",
        "Bulldog",
        "Cairn",
        "Chihuahua",
        "Chinese Crested",
        "Chow",
        "Clumber",
        "Cockapoo",
        "Cocker",
        "Collie",
        "Corgi",
        "Coyote",
        "Dalmation",
        "Dhole",
        "Dingo",
        "Doberman",
        "Elk Hound",
        "French Bulldog",
        "German Sheperd",
        "Golden Retriever",
        "Great Dane",
        "Great Perenees",
        "Greyhound",
        "Groenendael",
        "Irish Spaniel",
        "Irish Wolfhound",
        "Japanese Spaniel",
        "Komondor",
        "Labradoodle",
        "Labrador",
        "Lhasa",
        "Malinois",
        "Maltese",
        "Mex Hairless",
        "Newfoundland",
        "Pekinese",
        "Pit Bull",
        "Pomeranian",
        "Poodle",
        "Pug",
        "Rhodesian",
        "Rottweiler",
        "Saint Bernard",
        "Schnauzer",
        "Scotch Terrier",
        "Shar_Pei",
        "Shiba Inu",
        "Shih-Tzu",
        "Siberian Husky",
        "Vizsla",
        "Yorkie",
    ]

    if request.method == "POST":
        image = Image.open(request.files["file"])

        # Load model
        dog_classifier = tf.keras.models.load_model('models\dog_classifier_mobile.h5')

        # Preprocess image
        img_array = tf.keras.utils.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0)

        predictions = dog_classifier.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        print(f"Predicted class is {classes_labels[np.argmax(score)]}")

        # Get breed info from csv
        breed_info = pd.read_csv('data/breed_data.csv', names=['Breed', 'Description', 'Fur Color', 'Height', 'Color of Eyes', 'Longevity', 'Character', 'Health issues'], skiprows=1)
        breed_info = breed_info[breed_info['Breed'] == classes_labels[np.argmax(score)]]
        breed_info = breed_info.to_dict('records')[0]
        return breed_info


# Upload image
@app.route("/upload", methods=["POST"])
def image_upload():
    if request.method == "POST":
        file = request.files["file"]
        file.save(
            os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
        )
        return "File uploaded successfully"


if __name__ == "__main__":
    app.run(debug=True)
    