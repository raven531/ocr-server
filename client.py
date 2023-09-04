import time

import requests
import cv2

url = "http://192.168.45.25:8000/ocr"
easyocr_url = "http://192.168.163.48:8000/easyocr"

content_type = "image/png"
headers = {"Content-Type": content_type}
img = cv2.imread("use.png")
_, img_encoded = cv2.imencode('.png', img)
start = time.time()
req = requests.post(easyocr_url, headers=headers, data=img_encoded.tostring())
print(req.text)
