# analyzer.py
# 현재 자세가 기준 범위에 있는지 판단하고 메시지를 반환합니다.

from utils import calculate_angle

def evaluate_pushup(landmarks):
    # 왼쪽 어깨-팔꿈치-손목으로 이뤄진 팔의 각도 측정
    angle = calculate_angle(landmarks[11], landmarks[13], landmarks[15])
    
    # 기준 각도는 80~100도 사이 (팔이 수직에 가까워야 함)
    if 80 < angle < 100:
        return "정확한 자세입니다."
    else:
        return "팔을 더 곧게 펴세요."
