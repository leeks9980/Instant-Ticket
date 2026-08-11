import function as ft
import pyautogui
import time
import random
from datetime import datetime

#경기 선택
def Select_Match():
    ft.move_mouse_curved_fast(0.038, 0.034, duration=0.5)
    pyautogui.click()
    time.sleep(1)
    ft.move_mouse_curved_fast(0.68, 0.9, duration=0.5)
    pyautogui.click()
    ft.move_mouse_curved_fast(0.547, 0.64, duration=0.5)
    pyautogui.click()
    time.sleep(1)

#접속 대기
def wait():
    while True:
        ft.screenshot_by_ratio(r"D:\code\work_space\Instant Ticket\waiting_img", "taget_img.png", 0.005, 0.07, 0.375, 0.53)
        result = ft.is_same_image()
        if  result <= 10: 

            return "pass"

        time.sleep(0.5)

#보안 문자 해독
def CAPTCHA_solving():
    #보안 문자 캡처
    save_path = r"C:\work_space\code\instant_ticket\screenshot"
    ft.screenshot_by_ratio(save_path, "CAPTCHA.png", 0.145, 0.32, 0.103, 0.067)

    #보안 문자 입력
    ft.move_mouse_curved_fast(0.18, 0.41, duration=0.5)
    pyautogui.click()
    A = ft.chptcha()
    print(A)
    pyautogui.write(A, interval=0.1)
    ft.move_mouse_curved_fast(0.23, 0.48, duration=0.8)
    pyautogui.click()

    time.sleep(0.5)
    
    ft.screenshot_by_ratio(r"D:\code\work_space\Instant Ticket\Decryption_successful_img", "taget_img.png", 0.005, 0.07, 0.375, 0.53)
    result = ft.is_same_image(img_path1= r"D:\code\work_space\Instant Ticket\Decryption_successful_img\base_img.png", img_path2 = r"D:\code\work_space\Instant Ticket\Decryption_successful_img\taget_img.png")
    if  result >= 10:
        ft.move_mouse_curved_fast(0.18, 0.41, duration=0.5) 
        pyautogui.click()
        print("보안문자 입력")
        return "brake"

#좌석 지정
def Seat_Selection():
    ft.move_mouse_curved_fast(0.145, 0.5, duration=0.5)
    pyautogui.click()

    ft.move_mouse_curved_fast(0.145, 0.38, duration=0.5)
    pyautogui.click()

    ft.move_mouse_curved_fast(0.23, 0.15, duration=0.5)
    time.sleep(0.1)
    pyautogui.click()

    ft.move_mouse_curved_fast(0.15, 0.5, duration=0.5)

# 목표 시간 설정 (예: 2026년 8월 11일 오후 11시 0분 0초)
target_time = datetime(2026, 8, 11, 11, 0, 0)

print(123)

while True:
    now = datetime.now()
    if now >= target_time:
        Select_Match()
        wait()
        a = CAPTCHA_solving()
        if a != "brake":
            Seat_Selection()
    time.sleep(0.2)
