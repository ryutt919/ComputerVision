# visualizer.py
# 관절 및 중심점 시각화 함수 모듈

import cv2 as cv
from config import COLORS, CONNECTIONS_BASIC

def draw_joints(frame, landmarks, joint_indices=()):
    """
    모든 관절(joint_indices)에 점을 찍어서 시각화.
    - 어깨(11,12)는 파란색 점으로 강조
    """
    for idx in joint_indices:
        if idx in landmarks:
            x, y = landmarks[idx]
            # 어깨 포인트는 파란색, 나머지는 config에 정의된 색상
            if idx in (11, 12):
                color = (255, 0, 0)  # 파란색 (BGR)
            else:
                color = COLORS.get(idx, (255, 255, 255))
            cv.circle(frame, (x, y), 3, color, -1)

def draw_connections(frame, landmarks, connections):
    """
    주어진 connections 리스트에 따라 선을 그음.
    - 모든 선은 배경 영향을 적게 받도록 흰 테두리 + 컬러 본선
    - 양 어깨(11↔12) 연결 선만 파란색, 나머지는 빨간색
    """
    for a, b in connections:
        if a in landmarks and b in landmarks:
            start = landmarks[a]
            end   = landmarks[b]
            # 흰 테두리
            cv.line(frame, start, end, (255, 255, 255), 4)
            # 본선 색상 결정
            if {a, b} == {11, 12}:
                main_color = (255, 0, 0)   # 파란색
            else:
                main_color = (0, 0, 255)   # 빨간색
            cv.line(frame, start, end, main_color, 2)

def draw_limbs(frame, landmarks, side):
    """
    왼팔 또는 오른팔 연결선 그리기.
    - 내부적으로 draw_connections를 사용하므로 테두리+본선 스타일 유지
    """
    if side == 'left':
        pairs = [(15, 13), (13, 11)]
    else:
        pairs = [(16, 14), (14, 12)]
    draw_connections(frame, landmarks, pairs)

def draw_torso(frame, shoulder_center, spine, head_center):
    """
    몸통 시각화: 
      1) 어깨 중점에 점을 찍고 
      2) 어깨 중점→척추, 어깨 중점→머리 중심을 draw_connections 스타일로 연결
    """
    torso_color = (128, 0, 128)  # 사용하지 않지만, 점색 필요시 사용 가능
    # 1) 어깨 중점 점찍기
    if shoulder_center:
        cv.circle(frame, shoulder_center, 6, (128, 0, 128), -1)

    # 2) 어깨 중점 → 척추
    if shoulder_center and spine:
        # 흰 테두리
        cv.line(frame, shoulder_center, spine, (255,255,255), 6)
        # 빨간 본선
        cv.line(frame, shoulder_center, spine, (0,0,255), 4)

    # 3) 어깨 중점 → 머리 중심
    if shoulder_center and head_center:
        # 흰 테두리
        cv.line(frame, shoulder_center, head_center, (255,255,255), 6)
        # 빨간 본선
        cv.line(frame, shoulder_center, head_center, (0,0,255), 4)
