from flask import Flask, render_template, request
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/decode', methods=['POST'])
def decode():
    if 'qr_image' not in request.files:
        return "No file uploaded", 400

    file = request.files['qr_image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    img = cv2.imread(filepath)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    ssid = password = None

    if data and data.startswith("WIFI:"):
        wifi_data = data[5:].strip(';')
        fields = wifi_data.split(';')
        for field in fields:
            if field.startswith('S:'):
                ssid = field[2:]
            elif field.startswith('P:'):
                password = field[2:]

    return render_template('result.html', ssid=ssid, password=password, raw=data)

if __name__ == '__main__':
    app.run(debug=True)
