import pyautogui
import subprocess
import time
import random
import math
import os 
import ssl
import easyocr
import torch
from PIL import Image
from torchvision import transforms
import imagehash
import config

pyautogui.PAUSE = 0
parseq = torch.hub.load('baudm/parseq', 'parseq', pretrained=True).eval()

#마우스 제어(곡선)
def move_mouse_curved_fast(end_x, end_y, duration=0.1):
    start_x, start_y = pyautogui.position()

    # 화면 비율 계산
    screen_width, screen_height = pyautogui.size()
    target_x = screen_width * end_x
    target_y = screen_height * end_y
    
    # 제어점 생성
    cp_x = (start_x + target_x) / 2 + random.randint(-800, 800)
    cp_y = (start_y + target_y) / 2 + random.randint(-800, 800)

    # 시작 시간 기록 
    start_time = time.perf_counter()
    
    # 설정한 duration(시간)이 다 끝날 때까지 무한 반복
    while True:
        current_time = time.perf_counter()
        elapsed_time = current_time - start_time
        
        # 전체 목표 시간 중 현재 몇 % 진행되었는지 계산 (0.0 ~ 1.0)
        t = elapsed_time / duration
        
        # t가 1.0을 넘어가면(목표 시간 초과) 1.0으로 고정하고 반복문 종료 준비
        if t >= 1.0:
            t = 1.0
            
        # 2차 베지어 곡선 공식 (time.sleep 없이 진행률 t에 따라 위치 계산)
        current_x = int(((1 - t) ** 2) * start_x + 2 * (1 - t) * t * cp_x + (t ** 2) * target_x)
        current_y = int(((1 - t) ** 2) * start_y + 2 * (1 - t) * t * cp_y + (t ** 2) * target_y)

        # 0초로 설정하여 렉 없이 이동
        pyautogui.moveTo(current_x, current_y, duration=0)
        
        # 목표 지점에 도착했으면 무한 반복 탈출
        if t >= 1.0:
            break

#마우스 제어(직각)
def move_right_angle_ratio(end_x, end_y, speed_pixels_per_sec=1000, x_first=None):
    # 1. 현재(출발) 위치 가져오기
    start_x, start_y = pyautogui.position()
    
    # 화면 비율에 맞게 '실제 이동할 픽셀 좌표' 계산
    screen_width, screen_height = pyautogui.size()
    target_x = screen_width * end_x
    target_y = screen_height * end_y
    
    # 2. 어떤 축을 먼저 이동할지 결정
    if x_first is None:
        x_first = random.choice([True, False])
        
    # 3. 선택된 방향에 따라 '경유지(Corner)' 좌표 설정
    if x_first:
        # X축 먼저 이동 (가로 -> 세로)
        corner_x = target_x
        corner_y = start_y
        
    else:
        # Y축 먼저 이동 (세로 -> 가로)
        corner_x = start_x
        corner_y = target_y
    
    # 4. 각 구간의 실제 이동 거리 계산 (어느 방향이든 안전하게 거리 계산)
    dist_1 = math.hypot(corner_x - start_x, corner_y - start_y)   # 출발지 -> 경유지
    dist_2 = math.hypot(target_x - corner_x, target_y - corner_y) # 경유지 -> 도착지
    
    # 5. 거리에 비례하여 이동 시간(duration) 할당
    duration_1 = dist_1 / speed_pixels_per_sec
    duration_2 = dist_2 / speed_pixels_per_sec
    
    # 6. 직각 이동 실행
    pyautogui.moveTo(corner_x, corner_y, duration=duration_1) # 1단계 이동
    
    # [수정된 부분] 비율(end_x, y)이 아니라 픽셀(target_x, y)로 이동!
    pyautogui.moveTo(target_x, target_y, duration=duration_2) # 2단계 이동

#스크린샷
def screenshot_by_ratio(save_path, filename, start_x_ratio, start_y_ratio, width_ratio, height_ratio):
    # 1. 화면 비율 계산 (이전과 동일)
    screen_width, screen_height = pyautogui.size()
    start_x = int(screen_width * start_x_ratio)
    start_y = int(screen_height * start_y_ratio)
    capture_width = int(screen_width * width_ratio)
    capture_height = int(screen_height * height_ratio)
    
    # 2. 지정한 폴더가 컴퓨터에 없으면 자동으로 생성
    # exist_ok=True 옵션을 넣으면 이미 폴더가 있어도 에러가 나지 않습니다.
    os.makedirs(save_path, exist_ok=True)
    
    # 3. 폴더 경로와 파일 이름을 안전하게 합치기
    full_file_path = os.path.join(save_path, filename)
    
    # 4. 합쳐진 전체 경로(full_file_path)로 스크린샷 저장
    pyautogui.screenshot(full_file_path, region=(start_x, start_y, capture_width, capture_height))


#보안문자 해독
def chptcha(img_path=r".\work_space\Instant Ticket\screenshot\CAPTCHA.png"):
    img_transform = transforms.Compose([
        transforms.Resize((32, 128), transforms.InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize(0.5, 0.5) # 정규화
    ])
    
    # 3. 테스트할 이미지 불러오기 및 변환
    img = Image.open(img_path).convert('RGB')
    img_tensor = img_transform(img).unsqueeze(0) # 배치 차원 추가
    
    # 4. 이미지 텍스트 판독 (추론)
    with torch.inference_mode():
        logits = parseq(img_tensor)
        pred = logits.softmax(-1)
        label, certainty = parseq.tokenizer.decode(pred)
    
    return label[0]

#같은 화면 검사
def is_same_image(img_path1= r".\work_space\Instant Ticket\waiting_img\base_img.png", img_path2 = r".\Work_space\Instant Ticket\waiting_img\taget_img.png" , threshold=5):
    # 1. 두 이미지 불러오기
    img1 = Image.open(img_path1)
    img2 = Image.open(img_path2)
    
    # 2. 퍼셉추얼 해시 값 추출 (phash 기준)
    hash1 = imagehash.phash(img1)
    hash2 = imagehash.phash(img2)
    
    # 3. 해시 간의 거리(차이) 계산
    diff = hash1 - hash2
    print(f"이미지 차이 값: {diff}")
    
    # 4. 차이가 임계값(threshold) 이하이면 같은 이미지로 판단
    # 보통 5 이하이면 매우 유사하거나 같은 이미지로 판정함
    return diff

#경기 선택
def Select_Match():
    move_mouse_curved_fast(0.038, 0.034, duration=0.3)
    pyautogui.click()
    time.sleep(0.6)

    if config.team == '한화':
        move_mouse_curved_fast(0.71, 0.83, duration=0.3)
        pyautogui.click()

        move_mouse_curved_fast(0.038, 0.4, duration=0.3)
        pyautogui.click()
        pyautogui.keyUp('ctrl')
        pyautogui.scroll(-1400)
        time.sleep(0.2)

        move_mouse_curved_fast(0.31+(config.Match_X*0.06), 0.1+(config.Match_y*0.12), duration=0.2)   #기준 시작점
        time.sleep(0.1)
        pyautogui.click()

        move_mouse_curved_fast(0.547, 0.64, duration=0.3)
        pyautogui.click()
        time.sleep(1)

    elif config.team == '기아':
        move_mouse_curved_fast(0.038, 0.4, duration=0.3)
        pyautogui.click()
        pyautogui.keyUp('ctrl')
        pyautogui.scroll(-1600)
        time.sleep(0.2)

        move_mouse_curved_fast(0.71, 0.07, duration=0.3)
        pyautogui.click()
        
        move_mouse_curved_fast(0.30+(config.Match_X*0.065), 0.15+(config.Match_y*0.12), duration=0.2)   #기준 시작점
        time.sleep(0.1)
        pyautogui.click()

        move_mouse_curved_fast(0.55, 0.59, duration=0.3)
        pyautogui.click()
        time.sleep(1)

#좌석 지정
def Seat_Selection():
    print(config.team, config.seat)
    if config.team == '한화':
        #중앙 테이블
        if config.seat == "중앙":
            move_mouse_curved_fast(0.145, 0.5, duration=0.3)
            time.sleep(0.1)
            pyautogui.click()

        #3루 응원석
        elif config.seat == "3루 응원":
            move_mouse_curved_fast(0.108, 0.392, duration=0.3)
            time.sleep(0.1)
            pyautogui.click()

        #3루 지정석
        elif config.seat == "3루":
            move_mouse_curved_fast(0.12, 0.45, duration=0.3)
            time.sleep(0.1)
            pyautogui.click()

        #1루 응원석
        elif config.seat == "1루 응원":
            move_mouse_curved_fast(0.186, 0.4, duration=0.3)
            time.sleep(0.1)
            pyautogui.click()

        #1루 지정석
        elif config.seat == "1루":
            move_mouse_curved_fast(0.183, 0.45, duration=0.3)
            time.sleep(0.1)
            pyautogui.click()

        move_mouse_curved_fast(0.145, 0.38, duration=0.3)
        time.sleep(0.1)
        pyautogui.click()
        
        move_mouse_curved_fast(0.23, 0.15, duration=0.4)
        time.sleep(0.1)
        pyautogui.click()
        move_mouse_curved_fast(0.15, 0.5, duration=0.3)

    elif config.team == '기아':
        #중앙 테이블
        if config.seat == "중앙":
            move_mouse_curved_fast(0.145, 0.49, duration=0.3)
            time.sleep(0.1)
            pyautogui.click()

        elif config.seat == "응원석":
            move_mouse_curved_fast(0.10, 0.435, duration=0.3)
            time.sleep(0.1)
            pyautogui.click()

        elif config.seat == "1루":
            move_mouse_curved_fast(0.19, 0.435, duration=0.3)
            time.sleep(0.1)
            pyautogui.click()

            move_mouse_curved_fast(0.145, 0.41, duration=0.4)
            time.sleep(0.1)
            pyautogui.click()

            move_mouse_curved_fast(0.15, 0.5, duration=0.3)

#보안 문자 해독
def CAPTCHA_solving():
    #보안 문자 캡처
    save_path = r".\work_space\Instant Ticket\screenshot"
    screenshot_by_ratio(save_path, "CAPTCHA.png", 0.145, 0.32, 0.103, 0.067)

    #보안 문자 입력
    move_mouse_curved_fast(0.18, 0.41, duration=0.2)
    pyautogui.click()
    A = chptcha()
    pyautogui.write(A, interval=0.4)
    move_mouse_curved_fast(0.23, 0.48, duration=0.2)
    pyautogui.click()

    time.sleep(0.5)
    
    screenshot_by_ratio(r".\work_space\Instant Ticket\Decryption_successful_img", "taget_img.png", 0.005, 0.07, 0.375, 0.53)
    print('보안 문자 확인')
    result = is_same_image(img_path1= r".\work_space\Instant Ticket\Decryption_successful_img\base_img.png", img_path2 = r".\work_space\Instant Ticket\Decryption_successful_img\taget_img.png")
    if  result >= 15:
        move_mouse_curved_fast(0.18, 0.41, duration=0.2) 
        pyautogui.click()
        print("보안문자 입력")
        print(A)
        return "brake"

#접속 대기
def wait():
    while True:
        screenshot_by_ratio(r".\work_space\Instant Ticket\waiting_img", "taget_img.png", 0.005, 0.07, 0.375, 0.53)
        print('대기 인원 확인')
        result = is_same_image()
        print(result)
        if  10 >= result: 
            return "pass"

        time.sleep(0.5)
