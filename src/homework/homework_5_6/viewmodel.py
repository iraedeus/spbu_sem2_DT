from tkinter import Frame, Tk, ttk
from typing import Any, Optional

from src.homework.homework_5_6.model import *
from src.homework.homework_5_6.view import *


class IViewModel:
    def __init__(self, model: TicTacToeModel):
        self._model = model


class ViewModel:
    def __init__(self, root: Tk, model: TicTacToeModel) -> None:
        self._root = root
        self._model = model
        self.viewmodels = {
            "main": MainMenuViewModel(self._model),
            "choice": ChoiceViewModel(self._model),
            "multi": MultiplayerMenuViewModel(self._model),
            "field": FieldViewModel(self._model),
        }
        self.current_view: Optional[ttk.Frame] = None

    def swap(self, name: str, data: dict[str, Any]) -> None:
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = self.viewmodels[name].start(self._root, self, data)

    def start(self) -> None:
        self.swap("main", {})


class MainMenuViewModel(IViewModel):
    def __init__(self, model: TicTacToeModel) -> None:
        super().__init__(model)

    def _bind(self, view: MainMenuView, view_model: ViewModel) -> None:
        view.on_computer_btn.config(command=lambda: view_model.swap("field", {}))
        view.easy_bot_btn.config(command=lambda: view_model.swap("choice", {"challenge": False}))
        view.hard_bot_btn.config(command=lambda: view_model.swap("choice", {"challenge": True}))
        view.online_btn.config(command=lambda: view_model.swap("multi", {}))

    def start(self, root: Tk, view_model: ViewModel, data: dict[str, Any]) -> MainMenuView:
        frame = MainMenuView(root)
        frame.grid(row=1, column=1)
        self._bind(frame, view_model)
        return frame


class ChoiceViewModel(IViewModel):
    def __init__(self, model: TicTacToeModel) -> None:
        super().__init__(model)

    def choice(self, view_model: ViewModel, side: str, data: dict[str, Any]) -> None:
        if data["challenge"]:
            if side == "circle":
                players = [HardBot(1), Human(2)]
                self._model.players = players
                self._model.current_player = players[0]
            elif side == "cross":
                players = [Human(1), HardBot(2)]
                self._model.players = players
                self._model.current_player = players[0]
        else:
            if side == "circle":
                players = [EasyBot(1), Human(2)]
                self._model.players = players
                self._model.current_player = players[0]
            elif side == "cross":
                players = [Human(1), EasyBot(2)]
                self._model.players = players
                self._model.current_player = players[0]

        view_model.swap("field", {})

    def _bind(self, view: ChoiceView, view_model: ViewModel, data: dict[str, Any]):
        view.circle_btn.config(command=lambda: self.choice(view_model, "circle", data))
        view.cross_btn.config(command=lambda: self.choice(view_model, "cross", data))

    def start(self, root: Tk, view_model: ViewModel, data: dict[str, Any]) -> ChoiceView:
        frame = ChoiceView(root)
        frame.grid(row=1, column=1)
        self._bind(frame, view_model, data)
        return frame


class MultiplayerMenuViewModel(IViewModel):
    def __init__(self, model: TicTacToeModel) -> None:
        super().__init__(model)

    def start(self, root: Tk, view_model: ViewModel, data: dict[str, Any]):
        frame = MultiplayerMenuView(root)
        frame.grid(row=1, column=1)
        return frame


class FieldViewModel(IViewModel):
    def __init__(self, model: TicTacToeModel) -> None:
        super().__init__(model)

    def put_sign(self, view, r: int, c: int):
        value = self._model.field[r][c]
        button = view.cells[r][c]

        if value == 1:
            button.config(text="\nX\n\n")
        if value == 2:
            button.config(text="\nO\n\n")

    def _bind(self, view: FieldView):
        def put_sign(view, value: int, r: int, c: int):
            button = view.cells[r][c]

            if value == 1:
                button.config(text="\nX\n\n")
            if value == 2:
                button.config(text="\nO\n\n")

        buttons = view.cells
        for r in range(3):
            for c in range(3):
                button = buttons[r][c]
                observer = self._model.field[r][c]
                observer.add_callback(lambda value, row=r, column=c: put_sign(view, value, row, column))
                button.config(command=lambda row=r, column=c: self._model.place(row, column))

    def start(self, root: Tk, view_model: ViewModel, data: dict[str, Any]):
        frame = FieldView(root)
        frame.grid(row=1, column=1)
        self._bind(frame)
        return frame
