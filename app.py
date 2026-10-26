from flask import Flask, render_template, request, jsonify
import os
import socket
import qrcode
import threading
import webbrowser
import sys

# This helper function allows the .exe to find your templates folder
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__, template_folder=get_resource_path('templates'))

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

FILES_FOLDER = 'files'
os.makedirs(FILES_FOLDER, exist_ok=True)

chat_history = []

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def startup_tasks(ip_address):
    url = f"http://{ip_address}:5000"
    
    # Automatically open the web interface on the PC
    webbrowser.open(f"http://127.0.0.1:5000")
    
    # Generate and show the QR code for the phone
    print(f"\nServer running! Scan the QR code to connect your phone.")
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("connect_qr.png")
    img.show()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    text = data.get('message')
    
    if text:
        # Determine who sent it based on the IP address
        client_ip = request.remote_addr
        local_ip = get_local_ip()
        sender = "PC" if client_ip in ['127.0.0.1', local_ip] else "Mobile"
        
        # 1. Add to the live chat page
        chat_history.append({"sender": sender, "text": text})
        
        # 2. NEW: Save permanently to files/received_messages.txt
        message_filepath = os.path.join(FILES_FOLDER, 'received_messages.txt')
        with open(message_filepath, 'a', encoding='utf-8') as f:
            f.write(f"[{sender}]: {text}\n")
            
    return jsonify({"status": "success"})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(chat_history)

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Add a system notification to the chat
            chat_history.append({"sender": "System", "text": f"File received: {file.filename}"})
    return jsonify({"status": "success"})

if __name__ == '__main__':
    local_ip = get_local_ip()
    threading.Timer(1.0, startup_tasks, args=[local_ip]).start()
    app.run(host='0.0.0.0', port=5000, debug=False)