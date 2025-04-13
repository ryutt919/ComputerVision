import cv2 as cv

rtsp_url = "rtsp://210.99.70.120:1935/live/cctv002.stream"

# FFmpeg 백엔드 강제 적용 & UDP 프로토콜 추가
vd = cv.VideoCapture(f"{rtsp_url}?rtsp_transport=udp", cv.CAP_FFMPEG)
vd.set(cv.CAP_PROP_BUFFERSIZE, 1)  # 버퍼 크기 최소화

if not vd.isOpened():
    print("RTSP 스트림 연결 실패")
    exit()

# FPS 설정
fps = vd.get(cv.CAP_PROP_FPS)
if fps == 0:
    fps = 30
wait_msec = int(1 / fps * 1000)

# 첫 번째 프레임 읽기
valid, img = vd.read()
if not valid:
    print("RTSP 프레임 읽기 실패")
    vd.release()
    exit()

frame_size = (img.shape[1], img.shape[0])
fourcc = cv.VideoWriter_fourcc(*'MJPG')
save = cv.VideoWriter('webcam_rec.avi', fourcc, fps, frame_size)

is_recording = False
is_flipped = False  

while True:
    valid, img = vd.read()
    if not valid:
        print("프레임 읽기 실패 - 재연결 시도 중...")
        vd.release()
        vd = cv.VideoCapture(f"{rtsp_url}?rtsp_transport=udp", cv.CAP_FFMPEG)  # 재연결 시도
        vd.set(cv.CAP_PROP_BUFFERSIZE, 1)
        continue  # 다시 루프 실행

    if is_flipped:
        img = cv.flip(img, 1)  # 좌우 반전 적용

    if is_recording:
        save.write(img)  # 녹화 파일 저장
        cv.putText(img, "REC", (img.shape[1] - 100, 50), cv.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 0, 255), 2, cv.LINE_AA)

    # UI 표시
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(img, "R: Rec", (30, 30), font, 0.6, (0, 0, 0), 2, cv.LINE_AA)
    cv.putText(img, "R: Rec", (30, 30), font, 0.6, (0, 255, 0), 1, cv.LINE_AA)
    cv.putText(img, "F: Flip", (30, 60), font, 0.6, (0, 0, 0), 2, cv.LINE_AA)
    cv.putText(img, "F: Flip", (30, 60), font, 0.6, (0, 255, 0), 1, cv.LINE_AA)
    cv.putText(img, "ESC: Exit", (30, 90), font, 0.6, (0, 0, 0), 2, cv.LINE_AA)
    cv.putText(img, "ESC: Exit", (30, 90), font, 0.6, (0, 255, 0), 1, cv.LINE_AA)

    cv.imshow('video player', img)
    key = cv.waitKey(wait_msec)

    if key == 27:  # ESC 키를 누르면 종료
        break
    elif key == ord('r'):  # R키를 누르면 녹화 시작/종료
        is_recording = not is_recording
    elif key == ord('f'):  # F키를 누르면 좌우 반전
        is_flipped = not is_flipped

vd.release()
save.release()
cv.destroyAllWindows()
