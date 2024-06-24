from flask import Flask, request, render_template
from google.cloud import storage
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        try:
            name = request.form["name"]
            age = request.form["age"]
            email = request.form["email"]
            phone = request.form["phone"]

            data = f"Name: {name}, Age: {age}, Email: {email}, Phone: {phone}\n"

            # Upload data to Google Cloud Storage
            upload_to_gcs(data)

            return "Form submitted successfully!"
        except Exception as e:
            return str(e), 500
    return render_template("form.html")

def upload_to_gcs(data):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    bucket_name = os.getenv("CLOUD_STORAGE_BUCKET")

    # Initialize a client
    storage_client = storage.Client(project=project_id)
    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    # Create a new blob and upload the file's content
    blob = bucket.blob("user_data.txt")
    blob.upload_from_string(data, content_type="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
