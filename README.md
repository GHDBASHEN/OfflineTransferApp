# Offline PC Transfer

A lightweight, completely offline application to transfer text, links, documents, and photos between your PC and mobile phone in real-time.

## 1. How to Connect & Use

You do not need an active internet connection to use this app, but both devices must be on the same local network. The most reliable method is using your phone's built-in hotspot.

1. **Create the Network:** Turn off your mobile data (to prevent data usage), then turn on your phone's **Mobile Hotspot**.
2. **Connect the PC:** On your Windows PC, connect to your phone's Wi-Fi hotspot network.
3. **Launch the App:** Double-click the `OfflineTransfer.exe` application. 
4. **Scan to Connect:** A QR code will automatically pop up on your PC screen, and the transfer interface will open in your PC's web browser.
5. **Start Transferring:** Open your phone's camera and scan the QR code on your monitor. This opens the exact same interface on your phone. You can now send messages and files back and forth instantly!

*(Note: All transferred files are automatically saved in the `uploads` folder, and text messages are logged in the `files` folder located right next to the application.)*

---

## 2. Installation & Setup

Depending on how you want to run the application, choose one of the installation methods below.

### Option A: Using the Executable (For Standard Users)
1. Download the compiled `OfflineTransfer.exe` file.
2. Create a new folder on your Desktop (e.g., "Offline Transfer") and place the `.exe` file inside it. 
3. Double-click the file to run it. No further installation is required!

### Option B: Running from Source Code (For Developers)
1. Install **Python 3.11** or newer from python.org.
2. Download the project source files (ensure the `app.py` file and the `templates/index.html` folder structure are intact).
3. Open a terminal or command prompt inside the project folder.
4. Install the required dependencies by running:
   `pip install flask qrcode pillow`
5. Start the application by running:
   `python app.py`
