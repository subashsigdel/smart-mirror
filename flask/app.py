from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import logging

# Initialize Flask app
app = Flask(__name__, template_folder='.')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configuration
UPLOAD_FOLDER = 'testimages'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


def get_safe_filename(username):
    """Generate a safe filename with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return secure_filename(f"{username}_{timestamp}.png")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            user_name = request.form.get('user_name')

            if not user_name:
                return jsonify({'error': 'Please provide a name', 'success': False}), 400

            if 'capturedPhoto' not in request.files:
                return jsonify({'error': 'No file uploaded', 'success': False}), 400

            file = request.files['capturedPhoto']

            if file.filename == '':
                return jsonify({'error': 'No selected file', 'success': False}), 400

            filename = get_safe_filename(user_name)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(filepath)
            logging.info(f"File uploaded successfully: {filename} by user: {user_name}")

            return jsonify({
                'success': True,
                'message': f"Photo saved successfully as {filename}",
                'filename': filename
            })

        except Exception as e:
            logging.error(f"Error during file upload: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'An error occurred while processing your request'
            }), 500

    return render_template('templates/upload.html')


if __name__ == '__main__':
    # For development with SSL
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')

    # For production without SSL (use only behind HTTPS proxy):
    # app.run(host='0.0.0.0', port=5000)