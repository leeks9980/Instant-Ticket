import pyautogui
import subprocess
import time
import matplotlib.pyplot as plt
import random
import math
import os 
import ssl
import easyocr
import torch
from PIL import Image
from torchvision import transforms

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

#창 로드
def  load_win():
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    url = "https://www.ticketlink.co.kr/sports"
    
    # 새 창으로 크롬 실행
    subprocess.Popen([chrome_path, "--new-window", url])
    
    # 2. 창이 열리고 화면에 뜰 때까지 잠시 대기 (컴퓨터 속도에 따라 1~2초 조절)
    time.sleep(1.5)
    
    # 3. 윈도우 키 + 위쪽 방향키를 눌러 현재 활성화된(새로 뜬) 창을 최대화
    pyautogui.hotkey('win', 'up')

#보안문자 해독
def chptcha(img_path=r"D:\code\work_space\Instant Ticket\screenshot\CAPTCHA.png"):
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