# VisionAI – AI Image Recognition System

**See the World Through AI**

VisionAI is a professional, beginner-friendly internship project that combines Flask, TensorFlow/Keras, MobileNetV2, image processing, JavaScript, and SQLite into a complete AI image recognition workflow.

## Overview

Users can upload a JPG, JPEG, or PNG image, preview it instantly, send it to a Flask backend, and receive the top three real ImageNet predictions from MobileNetV2 with confidence scores. Successful predictions are stored in SQLite and used to power the history page and dashboard.

## Features

- Premium responsive AI SaaS interface
- Drag-and-drop image upload
- Instant image preview
- 5 MB upload limit
- JPG, JPEG, and PNG validation
- Real MobileNetV2 ImageNet inference
- Top 3 predictions
- Confidence score and animated confidence bar
- SQLite prediction history
- Search by image name or prediction
- Delete individual history records
- Clear history with confirmation
- Dashboard statistics from actual database data
- Chart.js activity/category charts
- Friendly error handling
- Beginner-friendly project structure
- Interview notes and future enhancements

## Technologies

- Python
- Flask
- TensorFlow / Keras
- MobileNetV2
- OpenCV
- Pillow
- NumPy
- SQLite
- HTML5
- CSS3
- JavaScript
- Chart.js (CDN)

## Project Structure

```text
VisionAI/
├── app.py
├── model.py
├── database.py
├── config.py
├── requirements.txt
├── README.md
├── INTERVIEW_NOTES.md
├── .gitignore
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── history.html
│   └── about.html
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── images/logo.png
├── uploads/.gitkeep
└── database/.gitkeep
```

## How It Works

1. The user selects an image.
2. Browser-side JavaScript validates type and size and shows a preview.
3. Flask validates the uploaded file again.
4. Pillow reads the image and converts it to RGB.
5. The image is resized to 224 × 224.
6. MobileNetV2 preprocessing prepares the image.
7. MobileNetV2 predicts ImageNet classes.
8. The application decodes the top three predictions.
9. The first prediction and confidence are stored in SQLite.
10. The frontend displays the result.

## Installation

### Windows

```bash
git clone YOUR_REPOSITORY_URL
cd VisionAI

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python app.py
```

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python app.py
```

Open:

```text
http://127.0.0.1:5000
```

### First Run

TensorFlow/Keras may automatically download the MobileNetV2 ImageNet weights the first time the model is initialized. An internet connection is therefore normally needed on the first model load.

## Important Notes

- Do not commit `venv`, database files, uploaded images, or model caches.
- The dashboard is based on real SQLite data.
- The sample prediction names in the specification are examples only; the actual result depends on the uploaded image.
- MobileNetV2 is an image classification model. It predicts image categories; it is not an object-detection model that draws bounding boxes.

## Future Enhancements

- Object detection
- Real-time camera recognition
- Multiple image uploads
- User authentication
- Cloud deployment
- Advanced deep-learning models
- Custom dataset classification
- AI-powered image descriptions

## Interview Value

This project demonstrates frontend development, Flask API design, file validation, image preprocessing, pretrained deep-learning inference, database CRUD operations, dashboard data aggregation, responsive UI design, and basic security practices.
