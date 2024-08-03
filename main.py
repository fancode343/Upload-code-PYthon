from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)

# Set the maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Define the upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define a secret key for session management
app.secret_key = "your_secret_key"

# Generate a unique filename function
def generate_unique_filename(filename):
    extension = filename.rsplit(".", 1)[1]
    unique_id = str(uuid.uuid4().hex)
    return f"{unique_id}.{extension}"

# Define the upload route
@app.route("/upload", methods=["POST"])
def upload():
    # Get the uploaded file
    file = request.files["file"]

    if file.filename == "":
        flash("No selected file.")
        return redirect(url_for("index"))

    if file and file.filename:
        if file.content_length > MAX_FILE_SIZE:
            flash("File size exceeds the maximum allowed size.")
            return redirect(url_for("index"))

        filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], unique_filename))

        flash("File uploaded successfully.")
        return redirect(url_for("index"))

# Define the download route to serve uploaded files
@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    else:
        return "Not Found", 404

# Define a route to list all uploaded files
@app.route("/list")
def list_files():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("file_list.html", files=files)

@app.route("/filemanager")
def file_manager():
    path = request.args.get("path", os.getcwd())
    files = os.listdir(path)

    return render_template("filemanager.html", files=files, path=path)

# Define the index route
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
  
@app.route('/research-paper')
def research_paper():
    return render_template('researchpaper.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
