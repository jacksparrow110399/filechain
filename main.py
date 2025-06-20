from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import hashlib
import json
from blockchain import Blockchain

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CHAIN_FILE = 'chain.json'

# Save blockchain to file
def save_chain(blockchain):
    with open(CHAIN_FILE, 'w') as f:
        json.dump(blockchain.get_chain(), f, indent=4)

# Load blockchain from file
def load_chain():
    if os.path.exists(CHAIN_FILE):
        with open(CHAIN_FILE, 'r') as f:
            return json.load(f)
    return None

# Initialize blockchain and load saved data if available
blockchain = Blockchain()
saved_data = load_chain()
if saved_data:
    blockchain.load_chain(saved_data)

def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(filepath)
            file_hash = hash_file(filepath)
            blockchain.add_block(uploaded_file.filename, file_hash)
            save_chain(blockchain)  # save chain after adding block
            return redirect(url_for('index'))
    return render_template('index.html', chain=blockchain.get_chain())

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)






