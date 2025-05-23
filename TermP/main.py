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
from utils import is_facing_camera_3d


def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return

    # 영상 저장용 변수 초기화
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = None
    recording = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1) 관절 추정 (2D, 3D 모두)
        landmarks, landmarks_3d = get_pose_landmarks(frame)

        # 2) 관절 시각화 (점)
        draw_joints(frame, landmarks, JOINT_INDICES)

        # 3) 어\uuae68 연결 선 색상: 정면이면 파란, 아니면 청량
        facing_front = is_facing_camera_3d(landmarks_3d)
        shoulder_color = (255, 0, 0) if facing_front else (0, 255, 0)
        if 11 in landmarks and 12 in landmarks:
            start = landmarks[11]
            end = landmarks[12]
            cv.line(frame, start, end, (255, 255, 255), 4)  # 흑 테두리
            cv.line(frame, start, end, shoulder_color, 2)  # 본선

        # 4) 팔 연결 시각화
        if all(k in landmarks for k in [11, 13, 15]):
            draw_limbs(frame, landmarks, 'left')
        if all(k in landmarks for k in [12, 14, 16]):
            draw_limbs(frame, landmarks, 'right')

        # 5) 중심점 계산 및 몸통 시각화
        shoulder_center = get_shoulder_center(landmarks)
        spine = estimate_spine(landmarks)
        head_center = estimate_head_center_priority(landmarks)
        draw_torso(frame, shoulder_center, spine, head_center)

        # 6) 푸어쉬얼 평가 및 피드래크 출력
        feedback_msg = evaluate_pushup(landmarks)
        draw_feedback(frame, feedback_msg)

        # 7) 프레임 확대 및 반전
        frame = cv.resize(frame, None, fx=1.5, fy=1.5)
        frame = cv.flip(frame, 1)

        # 8) 노치 중이면 프레임 저장
        if recording:
            out.write(frame)

        # 9) 프레임 출력
        cv.imshow('Pose Trainer', frame)

        # 10) 키 입력 처리
        key = cv.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == ord('r'):
            recording = not recording
            if recording:
                print("노치 시작")
                height, width = frame.shape[:2]
                out = cv.VideoWriter('output.avi', fourcc, 20.0, (width, height))
            else:
                print("노치 중지")
                if out:
                    out.release()
                    out = None

    cap.release()
    if out:
        out.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
