from flask import Flask, render_template, request, jsonify
import os
import socket
import qrcode
import threading
import webbrowser

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# This list stores our real-time chat history
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
    """Opens the PC browser and shows the QR code."""
    url = f"http://{ip_address}:5000"
    
    # 1. Automatically open the web interface on the PC
    webbrowser.open(f"http://127.0.0.1:5000")
    
    # 2. Generate and show the QR code for the phone
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
    """Receives a message and adds it to the history."""
    data = request.json
    text = data.get('message')
    
    if text:
        # Determine who sent it based on the IP address
        client_ip = request.remote_addr
        local_ip = get_local_ip()
        sender = "PC" if client_ip in ['127.0.0.1', local_ip] else "Mobile"
        
        chat_history.append({"sender": sender, "text": text})
    
    return jsonify({"status": "success"})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    """Sends the complete message history to the webpage."""
    return jsonify(chat_history)

@app.route('/upload_file', methods=['POST'])
def upload_file():
    """Handles file uploads."""
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            # Add a system message to the chat
            chat_history.append({"sender": "System", "text": f"File received: {file.filename}"})
    return jsonify({"status": "success"})

if __name__ == '__main__':
    local_ip = get_local_ip()
    threading.Timer(1.0, startup_tasks, args=[local_ip]).start()
    app.run(host='0.0.0.0', port=5000, debug=False)