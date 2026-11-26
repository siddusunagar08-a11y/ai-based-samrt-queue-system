# Run Instructions — AI-Based Smart Queue and Notification System

---

## ⚡ Quick Start: How to Run the Project

### 1. Open Terminal in the Project Directory
Make sure your terminal is inside the project folder:
```powershell
cd c:\Users\ADC\OneDrive\Desktop\Siddu
```

### 2. Start the Server
Run the application with Python:
```powershell
python run.py
```

When started, the terminal will display:
```text
=================================================================
  AI-Based Smart Queue System is RUNNING
  * Local PC URL:      http://127.0.0.1:5000
  * Mobile Wi-Fi URL:  http://192.168.x.x:5000
  (Make sure your phone is connected to the same Wi-Fi)
=================================================================
```

---

## 📱 How to Access from Your Mobile Phone (QR Code / Wi-Fi)

You do **NOT** need an FTP server. Here is how your phone connects to the web app:

1. **Connect your phone to the same Wi-Fi network** as this computer.
2. Open the website on your PC browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)
3. **Scan the QR Code**:
   - On the homepage: click **"Scan QR"** to open the mobile kiosk on your phone.
   - On the Token Confirmation page: scan the **"Scan with Phone Camera"** QR code.
   - The QR code now automatically uses your computer's Wi-Fi network address (e.g., `http://192.168.x.x:5000/...`), so your phone will open the page directly!
4. **Manual phone browser entry**: You can also type the Mobile Wi-Fi URL shown in your terminal (e.g., `http://192.168.1.10:5000`) into Chrome or Safari on your phone.

> **Windows Firewall Note**: If your phone cannot open the link, Windows Firewall might be blocking incoming port 5000. Allow Python when prompted, or run PowerShell as Administrator and run:
> ```powershell
> netsh advfirewall firewall add rule name="Flask Queue App" dir=in action=allow protocol=TCP localport=5000
> ```

---

## 🔑 Login & Verification Credentials

### 1. Admin Portal
- **URL**: [http://127.0.0.1:5000/admin/login](http://127.0.0.1:5000/admin/login)
- **Username**: `admin`
- **Password**: `admin123`

### 2. Customer Token Tracking (No Account Required)
- **URL**: [http://127.0.0.1:5000/track-token](http://127.0.0.1:5000/track-token)
- **Token Number**: Your token (e.g., `A-001`, `B-001`)
- **Verification Code**: You can enter **EITHER**:
  - The **Email Address** you entered when creating the token (e.g. `yourname@example.com`), **OR**
  - The **16-character Security Code** displayed on your token confirmation screen.

---

## ✉️ Email Notifications: Demo Mode vs. Real Inbox

### Why didn't you receive an email initially?
By default, the application runs with **`APP_DEMO_MODE=True`**. This is a safety feature so that the application runs anywhere without crashing or requiring email credentials. In Demo Mode, all acknowledgement, turn approaching, and counter call emails are safely recorded in the database audit log.
- You can inspect all generated emails at: [http://127.0.0.1:5000/admin/notifications](http://127.0.0.1:5000/admin/notifications)

### How to receive REAL emails in your actual personal Gmail inbox:
If you want emails to actually arrive in your real Gmail inbox, edit `.env`:

1. Open `.env` in this directory.
2. Update the mail settings to your Gmail account:
```ini
APP_DEMO_MODE=False
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-actual-email@gmail.com
MAIL_PASSWORD=your-16-character-google-app-password
MAIL_DEFAULT_SENDER="Smart Queue System <your-actual-email@gmail.com>"
```
3. **How to get a Gmail App Password**:
   - Go to your Google Account: [https://myaccount.google.com/security](https://myaccount.google.com/security)
   - Enable 2-Step Verification if not already enabled.
   - Search for **"App passwords"**.
   - Create a new App password named `Smart Queue`, copy the 16-letter password, and paste it into `MAIL_PASSWORD`.
4. Restart `python run.py`. Now, whenever a token is created or called, a real email will land directly in your inbox!

---

## 🧪 Run Automated Tests

To run the complete automated test suite (14 tests covering admin auth, queue logic, AI training, and notifications):
```powershell
python -m pytest
```

---

## 🛠️ Handy CLI Commands

- Re-initialize or reset database:
  ```powershell
  flask init-db
  ```
- Seed or reset the administrator account:
  ```powershell
  flask seed-admin --username admin --email admin@smartqueue.local --password admin123
  ```
- Train the Machine Learning model (`RandomForestRegressor`):
  ```powershell
  flask train-ml
  ```
