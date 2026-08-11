import function as ft
import pyautogui
import time
import random
from datetime import datetime

# 목표 시간 설정 (예: 2026년 8월 11일 오후 11시 0분 0초)
target_time = datetime(2026, 8, 11, 11, 0, 0)

print(123)

while True:
    now = datetime.now()
    if now >= target_time:
        ft.move_mouse_curved_fast(0.038, 0.034, duration=0.5)
        pyautogui.click()

        time.sleep(2)

        ft.move_mouse_curved_fast(0.68, 0.9, duration=0.5)
        pyautogui.click()

        ft.move_mouse_curved_fast(0.547, 0.64, duration=0.5)
        pyautogui.click()

        time.sleep(2)
        #보안 문자 캡처
        save_path = r"C:\work_space\code\instant_ticket\screenshot"
        ft.screenshot_by_ratio(save_path, "CAPTCHA.png", 0.145, 0.32, 0.103, 0.067)


        
        #보안 문자 입력
        ft.move_mouse_curved_fast(0.18, 0.41, duration=0.5)
        pyautogui.click()

        A = ft.chptcha()
        print(A)

        pyautogui.write(A, interval=0.1)

        ft.move_mouse_curved_fast(0.23, 0.48, duration=0.5)
        pyautogui.click()

        ft.move_mouse_curved_fast(0.18, 0.41, duration=0.5)
        break
    time.sleep(0.2)

