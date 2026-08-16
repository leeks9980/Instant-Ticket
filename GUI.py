import customtkinter as ctk
from datetime import datetime
import calendar
import threading
import time
import config
import main

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

DAYS = ["월", "화", "수", "목", "금", "토", "일"]

SEAT_OPTIONS = {
    "기아":  ["중앙", "응원석", "1루"],
    "한화":  ["중앙", "3루 응원", "3루", "1루 응원", "1루"],
}


# ─────────────────────────────────────────────────
# 실제 기능을 이 함수에 작성하세요.
# 오류 발생 시 예외를 raise 하면 오류 화면이 표시됩니다.
# ─────────────────────────────────────────────────
def run_process(team: str, seat: str, year: str,
                month: str, day: str, selected_cell: tuple | None):
    print(team,seat, year, month, day, selected_cell)

    row, col = selected_cell
    print(row, col)
    config.update_settings(team,col,row+1,seat,year,month,day)
    print('GUI 부분',config.team, config.Match_X, config.Match_y, config.seat, config.year, config.month, config.day )
    main.main_process()
    
    # 테스트용 오류: 아래 주석 해제 시 오류 화면으로 전환
    # raise ValueError("파일 처리 중 오류가 발생했습니다.")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("일정 관리")
        self.geometry("550x500")
        self.resizable(False, False)
        self.selected_cell = None
        self.cell_buttons: dict[tuple, ctk.CTkButton] = {}
        self._show_main()

    # ── 메인 화면 ─────────────────────────────────
    def _show_main(self):
        self._clear()
        self.configure(fg_color="#f5f5f5")

        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True)

        # 팀 선택 + 좌석 선택
        row1 = ctk.CTkFrame(main, fg_color="transparent")
        row1.pack(fill="x", padx=16, pady=(14, 4))

        ctk.CTkLabel(row1, text="팀 선택", width=60, anchor="w",
                     font=("맑은 고딕", 13, "bold")).pack(side="left")

        self.team_combo = ctk.CTkComboBox(
            row1,
            values=list(SEAT_OPTIONS.keys()),
            width=90, height=28, font=("맑은 고딕", 12),
            command=self._on_team_change,
            state="readonly",
        )
        self.team_combo.set("기아")
        self.team_combo.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(row1, text="좌석 선택", width=68, anchor="w",
                     font=("맑은 고딕", 13, "bold")).pack(side="left")

        self.seat_combo = ctk.CTkComboBox(
            row1,
            values=SEAT_OPTIONS["기아"],
            width=110, height=28, font=("맑은 고딕", 12),
            state="readonly",
        )
        self.seat_combo.set(SEAT_OPTIONS["기아"][0])
        self.seat_combo.pack(side="left")

        # 날짜
        row2 = ctk.CTkFrame(main, fg_color="transparent")
        row2.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(row2, text="날짜", width=60, anchor="w",
                     font=("맑은 고딕", 13, "bold")).pack(side="left")

        self.year_var = ctk.StringVar(value=str(datetime.today().year))

        ctk.CTkEntry(row2, textvariable=self.year_var,
                     width=54, height=28, font=("맑은 고딕", 12),
                     justify="center").pack(side="left")
        ctk.CTkLabel(row2, text="년",
                     font=("맑은 고딕", 12)).pack(side="left", padx=(3, 8))

        self.month_combo = ctk.CTkComboBox(
            row2, values=[f"{m}월" for m in range(1, 13)],
            width=76, height=28, font=("맑은 고딕", 12),
            command=self._on_month_change)
        self.month_combo.set(f"{datetime.today().month}월")
        self.month_combo.pack(side="left", padx=(0, 4))

        self.day_combo = ctk.CTkComboBox(
            row2, values=[], width=70, height=28,
            font=("맑은 고딕", 12))
        self.day_combo.pack(side="left")
        self._update_days()
        self.day_combo.set(f"{datetime.today().day}일")

        # 구분선
        ctk.CTkFrame(main, height=1, fg_color="#cccccc").pack(
            fill="x", padx=16, pady=8)

        # 격자
        grid_frame = ctk.CTkFrame(main, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=16)
        for c in range(7):
            grid_frame.columnconfigure(c, weight=1)
        for r in range(7):
            grid_frame.rowconfigure(r, weight=1)

        header_color = {5: "#2870c8", 6: "#c0392b"}
        for c, label in enumerate(DAYS):
            ctk.CTkLabel(
                grid_frame, text=label,
                font=("맑은 고딕", 11, "bold"),
                fg_color="#dce4f0",
                text_color=header_color.get(c, "#333333"),
                corner_radius=0
            ).grid(row=0, column=c, sticky="nsew", padx=1, pady=1)

        self.cell_buttons.clear()
        self.selected_cell = None
        for r in range(6):
            for c in range(7):
                btn = ctk.CTkButton(
                    grid_frame, text="",
                    fg_color="white", hover_color="#dce4f0",
                    border_width=1, border_color="#c0c0c0",
                    corner_radius=0,
                    command=lambda row=r, col=c: self._on_cell_click(row, col)
                )
                btn.grid(row=r + 1, column=c,
                         sticky="nsew", padx=1, pady=1)
                self.cell_buttons[(r, c)] = btn

        # 완료 버튼
        ctk.CTkButton(
            main, text="완료",
            height=34, font=("맑은 고딕", 13, "bold"),
            fg_color="#3d5fa0", hover_color="#2e4a80",
            command=self._on_complete
        ).pack(fill="x", padx=16, pady=(10, 14))

    # ── 실행 중 화면 ──────────────────────────────
    def _show_running(self):
        self._clear()
        self.configure(fg_color="#f5f5f5")

        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            center, text="실행중...",
            font=("맑은 고딕", 28, "bold"),
            text_color="#3d5fa0"
        ).pack()

        ctk.CTkLabel(
            center, text="잠시만 기다려 주세요",
            font=("맑은 고딕", 11),
            text_color="#888888"
        ).pack(pady=(6, 0))

    # ── 오류 화면 ─────────────────────────────────
    def _show_error(self, message: str):
        self._clear()
        self.configure(fg_color="#f5f5f5")

        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            center, text="오류 발생",
            font=("맑은 고딕", 24, "bold"),
            text_color="#c0392b"
        ).pack()

        ctk.CTkLabel(
            center, text=message,
            font=("맑은 고딕", 11),
            text_color="#555555",
            wraplength=400,
            justify="center"
        ).pack(pady=(8, 20))

        ctk.CTkButton(
            center, text="돌아가기",
            width=120, height=32,
            font=("맑은 고딕", 12),
            fg_color="#3d5fa0", hover_color="#2e4a80",
            command=self._show_main
        ).pack()

    # ── 이벤트 핸들러 ─────────────────────────────
    def _on_team_change(self, team: str):
        seats = SEAT_OPTIONS[team]
        self.seat_combo.configure(values=seats)
        self.seat_combo.set(seats[0])

    def _on_complete(self):
        team = self.team_combo.get()
        seat = self.seat_combo.get()
        year = self.year_var.get().strip()

        if not year.isdigit() or len(year) != 4:
            self._show_error("연도를 올바르게 입력해 주세요.\n(예: 2026)")
            return

        month = self.month_combo.get().replace("월", "")
        day = self.day_combo.get().replace("일", "")

        self._show_running()

        def task():
            try:
                run_process(team, seat, year, month, day, self.selected_cell)
            except Exception as e:
                # 에러 메시지를 미리 문자열로 추출하여 스코프 충돌 방지
                error_msg = str(e)
                print(f"[실제 발생한 에러]: {error_msg}")  # 콘솔에서도 바로 확인 가능
                self.after(0, lambda msg=error_msg: self._show_error(msg))

        threading.Thread(target=task, daemon=True).start()

    def _on_month_change(self, _=None):
        self._update_days()

    def _update_days(self):
        try:
            year = int(self.year_var.get())
        except ValueError:
            year = datetime.today().year
        try:
            month = int(self.month_combo.get().replace("월", ""))
        except ValueError:
            month = 1

        total = calendar.monthrange(year, month)[1]
        self.day_combo.configure(values=[f"{d}일" for d in range(1, total + 1)])

        try:
            if int(self.day_combo.get().replace("일", "")) > total:
                self.day_combo.set(f"{total}일")
        except ValueError:
            self.day_combo.set("1일")

    def _on_cell_click(self, row: int, col: int):
        key = (row, col)
        if self.selected_cell == key:
            self.cell_buttons[key].configure(fg_color="white")
            self.selected_cell = None
            return
        if self.selected_cell is not None:
            self.cell_buttons[self.selected_cell].configure(fg_color="white")
        self.cell_buttons[key].configure(fg_color="#3d5fa0")
        self.selected_cell = key

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    App().mainloop()