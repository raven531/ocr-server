import codecs
import numpy as np
import torch
import cv2
from PIL import Image
from parseq.strhub.data.module import SceneTextDataModule
from flask import Flask, request
import ssl
#https://clay-atlas.com/us/blog/2021/09/26/python-en-urllib-error-ssl-certificate/
# this issue resolve is for IGS internal net cannot build docker image, suck!!
ssl._create_default_https_context = ssl._create_unverified_context

class OCRReader:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.parseq = torch.hub.load('baudm/parseq', 'parseq', pretrained=True).eval().to(self.device)
        self.img_transform = SceneTextDataModule.get_transform(self.parseq.hparams.img_size)

    def image_2_text(self, image):
        pil_img = Image.fromarray(image).convert('RGB')
        pil_img = self.img_transform(pil_img).unsqueeze(0).to(self.device)
        logits = self.parseq(pil_img)
        pred = logits.softmax(-1)

        label, conf = self.parseq.tokenizer.decode(pred)
        return label


reader = OCRReader()
app = Flask(__name__)


@app.route("/")
def main():
    return "welcome to use our ocr service!!!"


@app.route("/ocr", methods=['GET', 'POST'])
def service():
    data = request.data
    np_arr = np.fromstring(data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    ret = reader.image_2_text(img)
    try:
        return ret[0]
    except IndexError:
        return None


if __name__ == "__main__":
    app.run("0.0.0.0", port=8000)
