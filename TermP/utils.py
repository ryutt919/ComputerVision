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

# 전역 변수 초기화
cos_sim_smoothed = 1.0

def is_facing_camera_3d(landmarks_3d, threshold=0.95, alpha=0.9):
    global cos_sim_smoothed
    if all(k in landmarks_3d for k in [11, 12]):
        ls = np.array(landmarks_3d[11])
        rs = np.array(landmarks_3d[12])
        shoulder_vec = rs - ls
        front_vec = np.cross(shoulder_vec, [0, -1, 0])
        front_vec /= np.linalg.norm(front_vec)
        camera_vec = np.array([0, 0, 1])
        cos_sim = np.dot(front_vec, camera_vec)

        # 스무딩 적용 (지수 이동 평균 방식)
        cos_sim_smoothed = alpha * cos_sim_smoothed + (1 - alpha) * cos_sim
        print("정면 유사도 (스무딩):", cos_sim_smoothed)
        return cos_sim_smoothed > threshold
    return False
