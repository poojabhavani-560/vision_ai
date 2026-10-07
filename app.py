import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError

from config import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE,
    SECRET_KEY,
    UPLOAD_FOLDER,
)

from database import (
    add_prediction,
    clear_predictions,
    delete_prediction,
    get_dashboard_stats,
    get_predictions,
    init_db,
)

from model import predict_image


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


# Make sure upload folder exists
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

# Initialize database
init_db()


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def allowed_file(filename):
    """
    Check whether the uploaded file has
    an allowed extension.
    """

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def validate_image(file):
    """
    Validate uploaded image.
    """

    if not file or not file.filename:
        return "Please select an image to continue."

    if not allowed_file(file.filename):
        return "Invalid file type. Please upload JPG, JPEG, or PNG."

    try:
        file.stream.seek(0)

        image = Image.open(file.stream)

        image.verify()

        file.stream.seek(0)

    except (UnidentifiedImageError, OSError):

        return (
            "Unable to read this image. "
            "Please try another image."
        )

    return None


# ==========================================
# HOME
# ==========================================

@app.route("/")
def index():

    return render_template(
        "index.html",
        recognition_mode=False
    )


# ==========================================
# RECOGNITION PAGE
# ==========================================

@app.route("/recognition")
def recognition():

    return render_template(
        "index.html",
        recognition_mode=True
    )


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    stats = get_dashboard_stats()

    return render_template(
        "dashboard.html",
        stats=stats
    )


# ==========================================
# HISTORY
# ==========================================

@app.route("/history")
def history():

    search = request.args.get(
        "search",
        ""
    ).strip()

    predictions = get_predictions(search)

    return render_template(
        "history.html",
        predictions=predictions,
        search=search
    )


# ==========================================
# ABOUT
# ==========================================

@app.route("/about")
def about():

    return render_template("about.html")


# ==========================================
# IMAGE PREDICTION API
# ==========================================

@app.post("/api/predict")
def api_predict():

    file = request.files.get("image")

    error = validate_image(file)

    if error:

        return jsonify({
            "success": False,
            "error": error
        }), 400


    filename = secure_filename(
        file.filename
    )

    if not filename:

        return jsonify({
            "success": False,
            "error": "Invalid file name."
        }), 400


    # Prevent accidental overwrite
    save_path = Path(UPLOAD_FOLDER) / filename

    counter = 1

    original_stem = save_path.stem
    original_suffix = save_path.suffix

    while save_path.exists():

        filename = (
            f"{original_stem}_{counter}"
            f"{original_suffix}"
        )

        save_path = (
            Path(UPLOAD_FOLDER) / filename
        )

        counter += 1


    try:

        # Save uploaded image
        file.save(save_path)


        # Run AI prediction
        results = predict_image(
            save_path
        )


        if not results:

            raise ValueError(
                "No prediction results returned."
            )


        # Primary prediction
        primary = results[0]


        # Save prediction in database
        prediction_id = add_prediction(
            filename,
            primary["label"],
            primary["confidence"]
        )


        return jsonify({

            "success": True,

            "prediction_id": prediction_id,

            "image_name": filename,

            "prediction": primary["label"],

            "confidence": primary["confidence"],

            "top_predictions": results

        })


    except Exception as error:

        print(
            "Prediction error:",
            error
        )


        if save_path.exists():

            try:
                save_path.unlink()

            except OSError:
                pass


        return jsonify({

            "success": False,

            "error":
                "Something went wrong while "
                "analyzing the image. Please try again."

        }), 500


# ==========================================
# DELETE HISTORY RECORD
# ==========================================

@app.post(
    "/api/history/<int:prediction_id>/delete"
)
def api_delete_prediction(
    prediction_id
):

    try:

        delete_prediction(
            prediction_id
        )

        return jsonify({
            "success": True
        })


    except Exception as error:

        print(
            "Delete error:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                "Unable to delete this record."

        }), 500


# ==========================================
# CLEAR HISTORY
# ==========================================

@app.post("/api/history/clear")
def api_clear_history():

    try:

        clear_predictions()

        return jsonify({
            "success": True
        })


    except Exception as error:

        print(
            "Clear history error:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                "Unable to clear prediction history."

        }), 500


# ==========================================
# DASHBOARD API
# ==========================================

@app.get("/api/dashboard")
def api_dashboard():

    try:

        stats = get_dashboard_stats()

        return jsonify(stats)


    except Exception as error:

        print(
            "Dashboard error:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                "Unable to load dashboard data."

        }), 500


# ==========================================
# 404 ERROR
# ==========================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "index.html",
        recognition_mode=False
    ), 404


# ==========================================
# FILE TOO LARGE
# ==========================================

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({

        "success": False,

        "error":
            "File size exceeds the 5 MB limit."

    }), 413


# ==========================================
# GENERAL ERROR
# ==========================================

@app.errorhandler(Exception)
def handle_unexpected_error(error):

    # Print the real error in terminal
    # so developers can identify problems.

    print(
        "\n=============================="
    )

    print(
        "APPLICATION ERROR:"
    )

    print(
        error
    )

    print(
        "==============================\n"
    )


    if request.path.startswith("/api/"):

        return jsonify({

            "success": False,

            "error":
                "Something went wrong. "
                "Please try again."

        }), 500


    return (
        "Something went wrong. "
        "Please try again."
    ), 500


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )