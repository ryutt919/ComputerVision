import numpy as np
import cv2 as cv

# 주어진 비디오 파일과 보정 파라미터
video_file = './data/myChess.mp4'
K = np.array([[603.51030778, 0, 674.89585317],
              [0, 603.45260428, 381.01122663],
              [0, 0, 1]])  # 보정된 카메라 내부 행렬

dist_coeff = np.array([0.03412314, -0.16458017,
                        0.0032529, 0.00097189,
                        0.17881176])  # 왜곡 계수들

# 비디오 열기
video = cv.VideoCapture(video_file)
assert video.isOpened(), 'Cannot read the given input, ' + video_file

# 왜곡 보정 여부 토글 변수
show_rectify = True
map1, map2 = None, None  # 리맵핑을 위한 맵 초기화
resize_scale = 0.7

while True:
    # 비디오에서 프레임 읽기
    valid, raw_img = video.read()
    if not valid:
        video.set(cv.CAP_PROP_POS_FRAMES, 0)  # 끝에 도달하면 처음으로 되감기
        continue

    # 회전 및 리사이즈 적용
    raw_img = cv.rotate(raw_img, cv.ROTATE_90_COUNTERCLOCKWISE)
    raw_img = cv.resize(raw_img, None, fx=resize_scale, fy=resize_scale)

    # 현재 프레임 기준 원본 저장
    original_img = raw_img.copy()

    # 보정 적용 여부에 따라 이미지 보정
    info = "Original"
    if show_rectify:
        if map1 is None or map2 is None:
            map1, map2 = cv.initUndistortRectifyMap(K, dist_coeff, None, None,
                                                    (original_img.shape[1], original_img.shape[0]), cv.CV_32FC1)
        img = cv.remap(original_img, map1, map2, interpolation=cv.INTER_LINEAR)
        info = "Rectified"
    else:
        img = original_img.copy()

    # 이미지에 현재 상태 텍스트만 출력
    cv.putText(img, f'{info} | Space : stop | Tab : toggle | ESC : exit',
               (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    # 이미지 출력
    cv.imshow("Geometric Distortion Correction", img)
    key = cv.waitKey(10)

    if key == ord(' '):  # Space: 일시정지
        display_show_rectify = show_rectify  # pause 중 toggle 반영용
        display_img = img.copy()
        while True:
            display_copy = display_img.copy()
            info_display = "Rectified" if display_show_rectify else "Original"
            cv.imshow("Geometric Distortion Correction", display_copy)

            key = cv.waitKey(0)
            if key == ord(' '):  # 다시 Space 입력 시 재생
                show_rectify = display_show_rectify  # toggle 반영
                break
            elif key == 27:  # ESC 입력 시 종료
                video.release()
                cv.destroyAllWindows()
                exit()
            elif key == ord('\t'):  # Tab 입력 시 보정 여부 토글
                display_show_rectify = not display_show_rectify
                if display_show_rectify:
                    if map1 is None or map2 is None:
                        map1, map2 = cv.initUndistortRectifyMap(K, dist_coeff, None, None,
                                                                (original_img.shape[1], original_img.shape[0]), cv.CV_32FC1)
                    display_img = cv.remap(original_img, map1, map2, interpolation=cv.INTER_LINEAR)
                else:
                    display_img = original_img.copy()
    elif key == 27:  # ESC: 종료
        break
    elif key == ord('\t'):  # Tab: 보정 여부 토글
        show_rectify = not show_rectify

video.release()
cv.destroyAllWindows()
