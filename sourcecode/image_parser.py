import cv2
import numpy as np
from PIL import Image
import pytesseract
import glob
import os


# 이미지 사이즈 변경 함수
def downscale(img, x):
    if x > 1280:
        print("big size")
        return

    y = int(0.75 * x)
    img = cv2.resize(img, (x, y))
    return img


# 폴더안 png 파일 가져오기
files = glob.glob('*.png')

# hsv 범위 설정
lower_color = (43, 91, 91)
upper_color = (118, 192, 192)

for links in files:
    img = cv2.imread(links)
    # 추출 데이터 자르기
    cut_img = img[50:350, 400:900]
    img_hsv = cv2.cvtColor(cut_img, cv2.COLOR_BGR2HSV)
    img_mask = cv2.inRange(img_hsv, lower_color, upper_color)
    img_resize = downscale(img_mask, 150)
    # kernel = np.ones((3, 3), np.uint8)
    # 십자커널 사용
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    erosion = cv2.erode(img_resize, kernel, iterations=1)
    # image 한글 추출
    result = pytesseract.image_to_string(erosion, lang='kor')
    # 추출한 데이터 공백 제거
    result = result.replace(" ", "")
    result = result.strip()
    # 파일 이름 변경
    os.rename(os.path.join(links), os.path.join(result + ".png"))
    print(result)

cv2.imshow("image", erosion)
cv2.waitKey(0)
