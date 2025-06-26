import cv2

img = cv2.imread('wifi_qr_code.jpg')
detector = cv2.QRCodeDetector()

data, bbox, _ = detector.detectAndDecode(img)

if data:
    print("✅ QR Code Decoded Data:")
    print(data)

    if data.startswith("WIFI:"):
        # শুরুতে 'WIFI:' সরিয়ে ফেলি
        wifi_data = data[5:].strip(';')
        fields = wifi_data.split(';')

        ssid = ''
        password = ''
        for field in fields:
            if field.startswith('S:'):
                ssid = field[2:]
            elif field.startswith('P:'):
                password = field[2:]

        print("\n📶 Wi-Fi Details:")
        print("SSID:", ssid if ssid else "N/A")
        print("Password:", password if password else "N/A")
else:
    print("🚫 QR Code detect করা যায়নি বা তাতে কোনো ডেটা নেই।")
