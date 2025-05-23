# main.py
# 전체 파이프라인 제어: 입력 → 추정 → 시각화 → 평가 → 피드백

import cv2 as cv
from config import JOINT_INDICES, CONNECTIONS_BASIC
from pose_estimator import (
    get_pose_landmarks,
    estimate_spine,
    estimate_head_center_priority,
    get_shoulder_center
)
from visualizer import (
    draw_joints,
    draw_connections,
    draw_limbs,
    draw_torso
)
from analyzer import evaluate_pushup
from feedback import draw_feedback

def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1) 관절 추정
        landmarks = get_pose_landmarks(frame)

        # 2) 기본 관절 시각화
        draw_joints(frame, landmarks, JOINT_INDICES)
        draw_connections(frame, landmarks, CONNECTIONS_BASIC)

        # 3) 왼/오른 팔 시각화
        draw_limbs(frame, landmarks, 'left')
        draw_limbs(frame, landmarks, 'right')

        # 4) 중심점 계산
        shoulder_center = get_shoulder_center(landmarks)
        spine           = estimate_spine(landmarks)
        head_center     = estimate_head_center_priority(landmarks)

        # 5) 몸통 및 머리 연결 시각화
        draw_torso(frame,
                   shoulder_center,
                   spine,
                   head_center)

        # 6) 푸시업 평가 및 피드백 출력
        feedback_msg = evaluate_pushup(landmarks)
        draw_feedback(frame, feedback_msg)

        # 7) 결과 표시 및 종료 조건
        frame = cv.resize(frame, None, fx=1.5, fy=1.5)
        frame = cv.flip(frame,1)
        cv.imshow('Pose Trainer', frame)
        if cv.waitKey(1) & 0xFF == 27:  # ESC 키
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
