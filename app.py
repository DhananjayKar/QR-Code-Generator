from flask import Flask, render_template, request, send_file, url_for, jsonify
import qrcode
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
QR_FOLDER = 'qrcodes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['QR_FOLDER'] = QR_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Limit file size to 10MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    text = request.form.get('text', '').strip()
    file = request.files.get('file')

    print(f"Received Text: {text}")  # Debugging
    print(f"Received File: {file.filename if file else 'No file'}")  # Debugging

    if not text and not file:
        return jsonify({"error": "No input provided"}), 400

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr_data = []

    if text:
        qr_data.append(f"Text: {text}")

    if file:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            file_url = url_for('uploaded_file', filename=filename, _external=True)
            qr_data.append(f"File: {file_url}")
        else:
            return jsonify({"error": "Invalid file type"}), 400

    qr.add_data("\n".join(qr_data))
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    qr_filename = f"qr_{uuid.uuid4().hex}.png"
    qr_path = os.path.join(QR_FOLDER, qr_filename)
    img.save(qr_path)

    return send_file(qr_path, mimetype='image/png')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)