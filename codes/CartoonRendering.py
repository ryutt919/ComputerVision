import cv2
import numpy as np

def cartoonize_image(img_path, output_path=None):
    #  이미지 읽기
    img = cv2.imread(img_path)

    #  컬러 이미지를 부드럽게 만들기 (노이즈 제거)
    color = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

    #  그레이스케일로 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #  블러 적용 (노이즈 완화)
    gray_blur = cv2.medianBlur(gray, 7)


    #  에지 검출 (adaptive threshold 사용)
    edges = cv2.adaptiveThreshold(gray_blur, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, blockSize=13, C=3)
    
    # 후처리 (morphology)
    kernel = np.ones((2,2), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    #  컬러 이미지와 에지를 결합
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cartoon = cv2.bitwise_and(color, edges_colored)

    # 결과 보여주기
    cv2.imshow("img", img)
    cv2.imshow("Cartoon", cartoon)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 저장 옵션
    if output_path:
        cv2.imwrite(output_path, cartoon)

    return cartoon

cartoonize_image("truck.jpg", "cartoon_result.jpg")
