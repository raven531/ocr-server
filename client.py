import time

import requests
import cv2

# url = "http://192.168.88.101:8000/ocr"
url = "http://192.168.163.48:8000/ocr"

content_type = "image/png"
headers = {"Content-Type": content_type}
start = time.time()
img = cv2.imread("number.png")
_, img_encoded = cv2.imencode('.png', img)
req = requests.post(url, headers=headers, data=img_encoded.tostring())
print(req.text)
print(time.time()-start)