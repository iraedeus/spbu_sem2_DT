from tkinter import BOTH, END, LEFT, YES, ttk
from typing import Any


class MainMenuView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.easy_bot_btn = ttk.Button(self, text="Play with ez bot")
        self.easy_bot_btn.pack(expand=YES, fill=BOTH)
        self.hard_bot_btn = ttk.Button(self, text="Play with hard bot")
        self.hard_bot_btn.pack(expand=YES, fill=BOTH)
        self.on_computer_btn = ttk.Button(self, text="Play on one computer")
        self.on_computer_btn.pack(expand=YES, fill=BOTH)
        self.online_btn = ttk.Button(self, text="Multiplayer")
        self.online_btn.pack(expand=YES, fill=BOTH)


class MultiplayerMenuView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.ip_entry = ttk.Entry(self)
        self.ip_entry.insert(END, "Enter ip of server")
        self.ip_entry.pack()


class ChoiceView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.circle_btn = ttk.Button(self, text="Circle")
        self.circle_btn.pack(expand=YES, fill=BOTH)
        self.cross_btn = ttk.Button(self, text="Cross")
        self.cross_btn.pack(expand=YES, fill=BOTH)


class FieldView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.lines = []
        self.cells: list[list[ttk.Button]] = [[], [], []]

        for l in range(3):
            self.lines.append(ttk.Frame(self))
            self.lines[l].pack()
            for c in range(3):
                new_btn = ttk.Button(self.lines[l], text="\n\n\n")
                new_btn.pack(expand=YES, fill=BOTH, side=LEFT)
                self.cells[l].append(new_btn)

        self.config(height=300, width=300)


class GameResultView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.label = ttk.Label(self)
        self.label.pack()
        self.to_menu_btn = ttk.Button(self, text="Return to main menu")
        self.to_menu_btn.pack()

    pass


if __name__ == "__main__":
    pass
