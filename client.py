import time

import requests
import cv2

url = "http://192.168.163.48:8000/ocr"

content_type = "image/png"
headers = {"Content-Type": content_type}
img = cv2.imread("origin_crop_version.png")
_, img_encoded = cv2.imencode('.png', img)
req = requests.post(url, headers=headers, data=img_encoded.tostring())
print(req.text)