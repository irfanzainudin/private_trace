import cv2
import qrcode
from PIL import Image

def encode_qr(phone_number):
    img = qrcode.make(phone_number)
    img.save(f"./users/{phone_number}")
    return f"./users/{phone_number}"

def decode_qr(image):
    img = cv2.imread(image)
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    if bbox is not None:
        return data
    else:
        return None

