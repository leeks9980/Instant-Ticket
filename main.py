import function as ft
import pyautogui
import time
import random

#로그인
ft.load_win()
time.sleep(0.5)
ft.move_mouse_curved_fast(0.56, 0.125, duration=random.gauss(1.5, 0.5))
pyautogui.click()
time.sleep(0.2)
ft.move_mouse_curved_fast(random.uniform(0.02, 0.13), 0.48, duration=random.gauss(1.5, 0.5))
pyautogui.click()

time.sleep(3)

#티켓 구매 링크 이동(한화 이글스 기준)
ft.move_mouse_curved_fast(0.28, 0.22, duration=0.5)
pyautogui.click()

ft.move_right_angle_ratio(0.36, 0.29, x_first=False)
pyautogui.click()

time.sleep(0.5)

ft.move_mouse_curved_fast(0.68, 0.9, duration=0.5)
pyautogui.click()

ft.move_mouse_curved_fast(0.547, 0.64, duration=0.5)
pyautogui.click()

time.sleep(2)

#보안 문자 캡처
save_path = r"D:\code\work_space\Instant Ticket\screenshot"
ft.screenshot_by_ratio(save_path, "CAPTCHA.png", 0.145, 0.32, 0.103, 0.067)

#보안 문자 입력
ft.move_mouse_curved_fast(0.18, 0.41, duration=0.5)
pyautogui.click()

A = ft.chptcha()
print(A)

pyautogui.write(A, interval=0.1)

ft.move_mouse_curved_fast(0.23, 0.48, duration=0.5)
pyautogui.click()