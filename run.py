import os
import socket
from app import create_app

app = create_app()

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    lan_ip = get_lan_ip()
    print("=" * 65)
    print("  AI-Based Smart Queue System is RUNNING")
    print(f"  * Local PC URL:      http://127.0.0.1:{port}")
    print(f"  * Mobile Wi-Fi URL:  http://{lan_ip}:{port}")
    print("  (Make sure your phone is connected to the same Wi-Fi)")
    print("=" * 65)
    # Bind to 0.0.0.0 so devices on local Wi-Fi / network can connect
    app.run(host='0.0.0.0', port=port, debug=True)
