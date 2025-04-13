import numpy as np
import cv2 as cv

# 비디오에서 체스보드 패턴을 선택한 이미지들을 추출하는 함수
def select_img_from_video(video_file, board_pattern, select_all=False, wait_msec=10, wnd_name='Camera Calibration', resize_scale=0.7):
    video = cv.VideoCapture(video_file)
    assert video.isOpened(), '비디오 인식 실패'

    img_select = []
    
    while True:
        valid, img = video.read()
        if not valid:
            break
        img = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
        img = cv.resize(img, None, fx=resize_scale, fy=resize_scale)

        if select_all:
            img_select.append(img)
        else:
            display = img.copy()
            cv.putText(display, f'NSelect: {len(img_select)},  Space : stop,  Enter : save,  ESC : exit',
                       (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
            cv.imshow(wnd_name, display)

            key = cv.waitKey(wait_msec)
            if key == ord(' '):
                complete, pts = cv.findChessboardCorners(img, board_pattern)
                cv.drawChessboardCorners(display, board_pattern, pts, complete)
                cv.imshow(wnd_name, display)
                key = cv.waitKey()
                if key == ord('\r'):
                    img_select.append(img)
            elif key == 27:
                break

    cv.destroyAllWindows()
    return img_select

# 체스보드 이미지들을 사용해 카메라 보정을 수행하는 함수
def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    assert len(img_points) > 0

    obj_pts = [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * board_cellsize] * len(img_points)

    return cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], K, dist_coeff, flags=calib_flags)

# 프로그램 실행 부분
if __name__ == '__main__':
    video_file = './data/myChess.mp4'
    board_pattern = (10, 7)
    board_cellsize = 0.022

    img_select = select_img_from_video(video_file, board_pattern)
    assert len(img_select) > 0, 'There is no selected images!'

    rms, K, dist_coeff, rvecs, tvecs = calib_camera_from_chessboard(img_select, board_pattern, board_cellsize)

    print('## Camera Calibration Results')
    print(f'* The number of selected images = {len(img_select)}')
    print(f'* RMS error = {rms}')
    print(f'* Camera matrix (K) = \n{K}')
    print(f'* Distortion coefficient (k1, k2, p1, p2, k3, ...) = {dist_coeff.flatten()}')