from flask import Flask, render_template, request, jsonify
import os
import time

app = Flask(__name__)

UPLOAD_FOLDER = '/home/hitech/MagicMirrornew/modules/MMM-FaceRecognition/testimage'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        if 'capturedPhoto' in request.files:
            file = request.files['capturedPhoto']
            if file:
                # Generate unique filename
                filename = f"{user_name}.png"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # If file exists, append timestamp
                if os.path.exists(filepath):
                    timestamp = int(time.time())
                    filename = f"{user_name}-{timestamp}.png"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                file.save(filepath)

                # Return success message as JSON
                return jsonify({'success': True, 'message': 'Photo saved successfully!'})

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
