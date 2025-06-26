from flask import Flask, render_template, request
import cv2
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['qrfile']
        if file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            img = cv2.imread(filepath)
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(img)

            ssid = password = None
            if data.startswith("WIFI:"):
                parts = data.split(';')
                for part in parts:
                    if part.startswith("S:"):
                        ssid = part[2:]
                    elif part.startswith("P:"):
                        password = part[2:]

            return render_template('result.html', data=data, ssid=ssid, password=password)

    return render_template('index.html')

# ✅ Render.com support: use their PORT environment variable
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
