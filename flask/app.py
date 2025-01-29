from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder='.')

# Create upload folder
UPLOAD_FOLDER = 'testimages'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        if 'capturedPhoto' in request.files:
            file = request.files['capturedPhoto']
            if file:
                filename = f"{user_name}.png"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                return "Captured photo saved successfully"
    return render_template('templates/upload.html')

if __name__ == '__main__':
    app.run(port=5000)