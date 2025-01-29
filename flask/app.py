from flask import Flask, render_template, request
import os

# Initialize the Flask app
app = Flask(__name__)

# Create the folder to save images if it doesn't exist
UPLOAD_FOLDER = 'testimages'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user's name from the form
        user_name = request.form.get('user_name')

        if not user_name:
            return "Please provide a name."

        # Check if an image file is submitted
        if 'capturedPhoto' in request.files:
            file = request.files['capturedPhoto']
            if file:
                filename = f"{user_name}.png"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                return f"Captured photo saved as {filename} in {UPLOAD_FOLDER}"

    return render_template('upload.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
