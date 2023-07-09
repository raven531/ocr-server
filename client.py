import requests
import cv2

url = "http://192.168.88.101:8000/ocr"
# url = "http://172.17.0.2:8000/ocr"

content_type = "image/png"
headers = {"Content-Type": content_type}
img = cv2.imread("henry.png")
_, img_encoded = cv2.imencode('.png', img)
req = requests.post(url, headers=headers, data=img_encoded.tostring())
print(req.text)
