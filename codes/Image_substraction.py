import cv2
import numpy as np

vid = cv2.VideoCapture('./data/PETS09-S2L1-raw.webm')
pre_frame = None

blur_ksize = (9,9)
blur_sigma = 3
diff_threshold = 40
bg_update_rate = 0.05
fg_update_rate = 0.001
zoom_level = 0.8

bg = cv2.imread('./data/extracted_bg.png')
bg = cv2.GaussianBlur(bg, blur_ksize, blur_sigma).astype(np.uint8)

box = lambda ksize: np.ones((ksize, ksize), dtype=np.uint8) #커널 생성기기
while True :
  valid, frame = vid.read()
  if not valid :
    break

  if pre_frame is None :
    pre_frame = frame.copy()
    continue
  frame_diff = cv2.absdiff(frame, pre_frame)
  pre_frame = frame.copy()

  frame_blur = cv2.GaussianBlur(frame, blur_ksize, blur_sigma)
  frame_diff_blur = frame_blur - bg

  frame_norm = np.linalg.norm(frame_diff_blur, axis=2)
  frame_bin = np.zeros_like(frame_norm, dtype=np.uint8)
  frame_bin[frame_norm>diff_threshold] = 255

  frame_mask = frame_bin.copy()
  frame_mask = cv2.erode(frame_mask, box(3)) # erode: 침식 (Erosion)
  frame_mask = cv2.dilate(frame_mask, box(5)) # dilate: 팽창 (Dilation)
  # 연속 두 번 dilate 하는 이유 :
  # 객체가 끊겨 보일 수 있는 경계 연결
  # 너무 얇은 윤곽선 연결
  # 커널 크기를 다르게 한 이유:
  # 5x5로 크게 뭉치고, 3x3으로 디테일한 연결
  fg = frame_mask == 255 # boolean 배열 생성성
  frame_mask = cv2.erode(frame_mask, box(3), iterations=2) 
  # iterations=2 → 2번 연속 : 객체 외곽을 자연스럽게 복원
  
  back = ~fg # fg의 반전
  bg[back]= (bg_update_rate*frame_blur[back]+(1-bg_update_rate)*bg[back])
  bg[fg] = (fg_update_rate*frame_blur[fg]+(1-fg_update_rate)*bg[fg])

  frame_fore = np.zeros_like(frame)
  frame_fore[fg] = frame[fg] # fg가 true인 인덱스만 가져오기

  merged_img = np.vstack((np.hstack((frame, frame_diff)), np.hstack((frame_fore, cv2.cvtColor(frame_mask, cv2.COLOR_GRAY2BGR)))))
  cv2.imshow('diff',merged_img)
  key = cv2.waitKey(int(1000/vid.get(cv2.CAP_PROP_FPS)))
  if key == 27 :
    break