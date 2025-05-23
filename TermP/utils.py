# utils.py
# 수학/벡터 연산 관련 보조 함수 모듈

import numpy as np

def calculate_angle(a, b, c):
    """
    세 점 a, b, c가 주어지면 b를 정점으로 하는 ∠ABC를 계산.
    반환값: 각도(도 단위)
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ab = a - b
    cb = c - b
    # 내적 공식을 사용해 코사인 각도 계산
    cosine = np.dot(ab, cb) / (np.linalg.norm(ab) * np.linalg.norm(cb))
    cosine = np.clip(cosine, -1.0, 1.0)
    angle  = np.degrees(np.arccos(cosine))
    return angle
