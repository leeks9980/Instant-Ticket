import function as ft
import pyautogui
import time
import random
from datetime import datetime
import config

def main_process():
    print('메인 부분',config.team, config.Match_X, config.Match_y, config.seat, config.year, config.month, config.day )
    # 목표 시간 설정 (예: 2026년 8월 11일 오후 11시 0분 0초)
    target_time = datetime(config.year, config.month, config.day, 10, 59, 59)
    print("작동중")
    
    while True:
        now = datetime.now()
        if now >= target_time:
            ft.Select_Match()
            ft.wait()
            a = ft.CAPTCHA_solving()
            if a != "brake":
                ft.Seat_Selection()
            break
        time.sleep(0.2)
 