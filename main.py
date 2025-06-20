from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import hashlib
from blockchain import Blockchain

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Make sure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Create the blockchain instance
blockchain = Blockchain()

# Function to hash a file using SHA-256
def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

# Home route: Upload files and view the blockchain
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(filepath)
            file_hash = hash_file(filepath)
            blockchain.add_block(uploaded_file.filename, file_hash)
            return redirect(url_for('index'))
    return render_template('index.html', chain=blockchain.get_chain())

# Route to download uploaded files
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)


