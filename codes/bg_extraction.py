import cv2
import numpy as np

vid =  cv2.VideoCapture('./data/PETS09-S2L1-raw.webm')
bg = None
frame_count = 0

while True:
  valid,frame = vid.read()
  if not valid :
    break
  frame_count += 1
  # cv2.imshow('vd', frame)
  # cv2.waitKey(1)

  if frame_count %100 ==0 :
    print(f'frame : {frame_count}')

  if bg is None :
    bg = np.zeros_like(frame, dtype=np.float64)
  bg += frame.astype(np.float64)
bg = bg/frame_count
bg = bg.astype(np.uint8)

cv2.imshow('bg_ex',bg)
cv2.imwrite('./data/extracted_bg.png', bg)
cv2.waitKey()



