from flask import Flask, render_template, request
from google.cloud import storage  # Import for Google Cloud Storage

app = Flask(__name__)

# Configure Google Cloud Storage (replace with your project details)
client = storage.Client()
bucket_name = "credit-card-details1"  # Replace with your bucket name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    age = request.form.get('age')

    # Input validation (example for name and age)
    if not name or name.isspace():
        return "Please enter a valid name."
    try:
        age = int(age)
        if age < 18:
            return "You must be 18 years or older to proceed."
    except ValueError:
        return "Invalid age. Please enter a number."

    # Data processing for non-sensitive data
    data = {"name": name, "age": age}

    # Store data in GCS bucket (assuming data is JSON-serializable)
    try:
        blob = client.bucket(bucket_name).blob(f"{name}-{age}.json")  # Generate unique filename
        blob.upload_from_string(json.dumps(data))  # Serialize data to JSON (replace with appropriate format)
        print(f"Data uploaded to GCS bucket: {bucket_name}")
    except Exception as e:
        print(f"Error uploading data to GCS: {e}")

    return render_template('success.html', name=name, age=age)

if __name__ == '__main__':
    app.run(debug=True)
