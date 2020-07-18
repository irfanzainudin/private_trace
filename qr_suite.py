import cv2
import qrcode

def encode_qr(phone_number):
    img = qrcode.make(phone_number)
    return img

def decode_qr(image):
    img = cv2.imread(image)
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    if bbox is not None:
        return data
    else:
        return None