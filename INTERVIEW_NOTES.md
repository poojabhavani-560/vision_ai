# VisionAI – Interview Notes

## What is your project?

VisionAI is a Flask-based AI image recognition system. Users upload an image and the application uses a pretrained MobileNetV2 model to predict the top three ImageNet categories with confidence scores. Results are stored in SQLite for history and dashboard statistics.

## What problem does it solve?

It provides a simple interface for turning an uploaded image into useful AI-based classification results without requiring the user to understand the underlying machine-learning process.

## Why did you choose MobileNetV2?

MobileNetV2 is a pretrained convolutional neural network designed to be relatively lightweight and efficient. It is a practical choice for a local student project because it provides strong image classification capability without requiring us to train a model from scratch.

## What is TensorFlow?

TensorFlow is a machine-learning framework used to build, train, and run machine-learning models.

## What is Flask?

Flask is a lightweight Python web framework. In VisionAI, Flask handles the web pages, file upload API, validation, prediction request, and database-related routes.

## What is OpenCV?

OpenCV is an open-source computer vision library. It is included in the project technology stack for image-processing capability and future computer-vision extensions.

## How does image prediction work?

The image is uploaded and validated, converted to RGB, resized to 224 × 224 pixels, preprocessed for MobileNetV2, and passed into the pretrained model. The model returns class probabilities, which are decoded into the top three labels.

## What is confidence score?

The confidence score is the model's probability value for a predicted class, expressed as a percentage. It indicates how strongly the model associates the image with that class; it is not a guarantee that the prediction is correct.

## How is prediction history stored?

SQLite stores the image name, primary prediction, confidence, and creation timestamp. Parameterized SQL queries are used for database operations.

## What happens when an invalid image is uploaded?

The application validates the file type and size in the browser and again on the server. It also verifies that the uploaded content can actually be read as an image. A friendly message is returned if validation fails.

## What challenges did you face?

The main challenges are handling image uploads safely, connecting a pretrained AI model to a web application, keeping the interface responsive during processing, and connecting real database data to dashboard statistics.

## What improvements can be added in the future?

Object detection, real-time camera recognition, multiple-image processing, authentication, cloud deployment, custom datasets, more advanced models, and AI-generated image descriptions can be added.

## 30-second explanation

"VisionAI is an AI image recognition web application built with Flask and TensorFlow. I use MobileNetV2 pretrained on ImageNet for real image classification. The user uploads an image, the backend validates and preprocesses it, the model returns the top three predictions, and the result is stored in SQLite. I also built a dashboard and history module using actual database data. I focused on making the project professional while keeping the code simple enough to explain."
