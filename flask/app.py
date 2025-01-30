from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import time

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'testimages')
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
                    filename = f"{user_name}_{timestamp}.png"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                file.save(filepath)

                # Return success message as JSON
                return jsonify({'success': True, 'message': 'Photo saved successfully!'})

    return render_template('upload.html')

@app.route('/gallery')
def gallery():
    # Get list of all images in the upload folder
    images = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        breakpoint()
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            images.append(filename)
    return render_template('gallery.html', images=images)

@app.route('/delete/<filename>')
def delete_image(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'success': True, 'message': 'Image deleted successfully!'})
        return jsonify({'success': False, 'message': 'File not found!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(port=5000, debug=True)