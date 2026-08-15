import function as ft
import pyautogui
import time
import random
from datetime import datetime
import config

#접속 대기
def wait():
    while True:
        ft.screenshot_by_ratio(r".\work_space\Instant Ticket\waiting_img", "taget_img.png", 0.005, 0.07, 0.375, 0.53)
        print('대기 인원 확인')
        result = ft.is_same_image()
        print(result)
        if  10 >= result: 
            return "pass"

        time.sleep(0.5)

#보안 문자 해독
def CAPTCHA_solving():
    #보안 문자 캡처
    save_path = r".\work_space\Instant Ticket\screenshot"
    ft.screenshot_by_ratio(save_path, "CAPTCHA.png", 0.145, 0.32, 0.103, 0.067)

    #보안 문자 입력
    ft.move_mouse_curved_fast(0.18, 0.41, duration=0.6)
    pyautogui.click()
    A = ft.chptcha()
    pyautogui.write(A, interval=0.3)
    ft.move_mouse_curved_fast(0.23, 0.48, duration=0.8)
    pyautogui.click()

    time.sleep(0.5)
    
    ft.screenshot_by_ratio(r".\work_space\Instant Ticket\Decryption_successful_img", "taget_img.png", 0.005, 0.07, 0.375, 0.53)
    print('보안 문자 확인')
    result = ft.is_same_image(img_path1= r".\work_space\Instant Ticket\Decryption_successful_img\base_img.png", img_path2 = r".\work_space\Instant Ticket\Decryption_successful_img\taget_img.png")
    if  result >= 15:
        ft.move_mouse_curved_fast(0.18, 0.41, duration=0.6) 
        pyautogui.click()
        print("보안문자 입력")
        print(A)
        return "brake"

# 목표 시간 설정 (예: 2026년 8월 11일 오후 11시 0분 0초)
target_time = datetime(2026, 8, 12, 11, 0, 0)

print("작동중")
config.update_settings("기아", 6, 3, "중앙")
print(f"선택 팀: {config.team} / 경기: {config.Match_X},{config.Match_y} / 좌석: {config.Seat}")
while True:
    now = datetime.now()
    if now >= target_time:
        ft.Select_Match()
        wait()
        a = CAPTCHA_solving()
        if a != "brake":
            ft.Seat_Selection()
        break
    time.sleep(0.2)
