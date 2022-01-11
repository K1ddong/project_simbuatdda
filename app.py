"""
references:

1. 유튜버 '동빈나' (파이토치 모델 차용)
유튜브 : https://www.youtube.com/watch?v=Lu93Ah2h9XA
깃허브 : https://github.com/ndb796/CNN-based-Celebrity-Classification-AI-Service-Using-Transfer-Learning

2. 깃허브 'imfing' (플라스크 웹앱 기본 요소 (구성화면 및 기본 기능))
깃허브 : https://github.com/imfing/keras-flask-deploy-webapp

3. 모델 학습 데이터
네이버 검색 api 이미지 크롤링을 통한 데이터

"""


import io
from flask import Flask, jsonify, request, render_template
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import torch
from torchvision import transforms
import numpy as np
from util import base64_to_pil


# 파이토치 cpu 설정
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")  # device 객체

# pre_trained 모델 불러오기
model_path = "model\simbuatdda.pt"
model = torch.load(model_path, map_location=device)


# def imshow(input, title):
#     # torch.Tensor를 numpy 객체로 변환
#     input = input.numpy().transpose((1, 2, 0))
#     # 이미지 정규화 해제하기
#     mean = np.array([0.485, 0.456, 0.406])
#     std = np.array([0.229, 0.224, 0.225])
#     input = std * input + mean
#     input = np.clip(input, 0, 1)
#     # 이미지 출력
#     plt.imshow(input)
#     plt.title(title)
#     plt.show()


# 이미지 전처리
transforms_test = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


# 도라지 or 인삼
class_names = ["도라지", "인삼"]

# 이미지를 읽어 결과를 반환하는 함수
def get_prediction(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = transforms_test(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        _, preds = torch.max(outputs, 1)
        # imshow(image.cpu().data[0], title="predicted as : " + class_names[preds[0]])
    class_name = class_names[preds[0]]
    return render_template("result.html", data=class_name)
    # return class_names[preds[0]]


# 플라스크 앱 구성
app = Flask(__name__)


# 메인 화면
@app.route("/", methods=["GET"])
def index():
    # Main page
    return render_template("index.html")


# 이미지 분류후 결과
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # # 이미지 바이트 데이터 받아오기
        # file = request.files["file"]
        # file = request.files.get("imagefile", "")
        # image_bytes = file.read()

        # Get the image from post request
        img = base64_to_pil(request.json)
        # Save the image to ./uploads
        with io.BytesIO() as buf:
            img.save(buf, "jpeg")
            image_bytes = buf.getvalue()

        # 분류 결과 확인 및 클라이언트에게 결과 반환
        # class_name = get_prediction(image_bytes=image_bytes)
        class_name = get_prediction(image_bytes=image_bytes)
        # return jsonify({"class_name": class_name})
        # return render_template("result.html", data=class_name)
        # print("결과:", {"class_name": class_name})
        return jsonify(result=class_name, probability=None)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
