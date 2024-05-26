from tkinter import Frame, Tk, ttk
from typing import Optional

from src.homework.homework_5_6.model import *
from src.homework.homework_5_6.view import *


class IViewModel:
    def __init__(self, model: TicTacToeModel) -> None:
        self._model = model

    def start(
        self, root: Tk, view_model: "ViewModel", data: dict[str, Any]
    ) -> MainMenuView | ChoiceView | MultiplayerMenuView | FieldView | GameResultView:
        return NotImplemented


class ViewModel:
    def __init__(self, root: Tk, model: TicTacToeModel) -> None:
        self._root = root
        self._model = model
        self.viewmodels = {
            "main": MainMenuViewModel(self._model),
            "choice": ChoiceViewModel(self._model),
            "multi": MultiplayerMenuViewModel(self._model),
            "field": FieldViewModel(self._model),
            "gameresult": GameResultViewModel(self._model),
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
        view.on_computer_btn.config(command=lambda: view_model.swap("field", {"bot": False, "multiplayer": False}))
        view.easy_bot_btn.config(command=lambda: view_model.swap("choice", {"challenge": False, "bot": True}))
        view.hard_bot_btn.config(command=lambda: view_model.swap("choice", {"challenge": True, "bot": True}))
        view.online_btn.config(command=lambda: view_model.swap("multi", {"bot": False, "multiplayer": True}))

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
                hard_human = (HardBot(1, self._model), Human(2))
                self._model.players = hard_human
                self._model.current_player = hard_human[0]
            elif side == "cross":
                human_hard = (Human(1), HardBot(2, self._model))
                self._model.players = human_hard
                self._model.current_player = human_hard[0]
        else:
            if side == "circle":
                easy_human = (EasyBot(1, self._model), Human(2))
                self._model.players = easy_human
                self._model.current_player = easy_human[0]
            elif side == "cross":
                human_easy = (Human(1), EasyBot(2, self._model))
                self._model.players = human_easy
                self._model.current_player = human_easy[0]

        view_model.swap("field", data)

    def _bind(self, view: ChoiceView, view_model: ViewModel, data: dict[str, Any]) -> None:
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

    def start(self, root: Tk, view_model: ViewModel, data: dict[str, Any]) -> MultiplayerMenuView:
        frame = MultiplayerMenuView(root)
        frame.grid(row=1, column=1)
        return frame


class FieldViewModel(IViewModel):
    def __init__(self, model: TicTacToeModel) -> None:
        super().__init__(model)

    def _bind_two_player(self, view: FieldView, view_model: ViewModel) -> None:
        if isinstance(self._model.players[0], Player):
            self._model.players = (Human(1), Human(2))
            self._model.current_player = self._model.players[0]

        def put_sign(view: FieldView, value: int, r: int, c: int) -> None:
            button = view.cells[r][c]

            if value == 1:
                button.config(text="\nX\n\n")
            if value == 2:
                button.config(text="\nO\n\n")

        session_observer = self._model.session
        session_observer.add_callback(lambda _: view_model.swap("gameresult", {}))

        buttons = view.cells
        for r in range(3):
            for c in range(3):
                button = buttons[r][c]
                observer = self._model.field[r][c]
                add_sign = lambda value, row=r, column=c: put_sign(view, value, row, column)
                observer.add_callback(add_sign)

                do_next_turn = lambda row=r, column=c: self._model.place(row, column)
                button.config(command=do_next_turn)

    def _bind_with_computer(self, view: FieldView, view_model: ViewModel) -> None:
        def put_sign(view: FieldView, value: int, r: int, c: int) -> None:
            button = view.cells[r][c]

            if value == 1:
                button.config(text="\nX\n\n")
            if value == 2:
                button.config(text="\nO\n\n")

        def bot_turn() -> None:
            if isinstance(self._model.current_player, EasyBot):
                easy_bot = self._model.current_player
                easy_bot.bot_turn()
            elif isinstance(self._model.current_player, HardBot):
                hard_bot = self._model.current_player
                hard_bot.bot_turn()

        def next_turn(r: int, c: int) -> None:
            if self._model.field[r][c].value == 0:
                self._model.place(r, c)
                bot_turn()

        session_observer = self._model.session
        session_observer.add_callback(lambda _: view_model.swap("gameresult", {}))

        buttons = view.cells
        for r in range(3):
            for c in range(3):
                button = buttons[r][c]
                observer = self._model.field[r][c]
                add_sign = lambda value, row=r, column=c: put_sign(view, value, row, column)
                observer.add_callback(add_sign)

                do_next_turn = lambda row=r, column=c: next_turn(row, column)
                button.config(command=do_next_turn)

        bot_turn()

    def _bind_multiplayer(self, view: FieldView, view_model: ViewModel) -> None:
        pass

    def start(self, root: Tk, view_model: ViewModel, data: dict[str, Any]) -> FieldView:
        frame = FieldView(root)
        frame.grid(row=1, column=1)
        if data["bot"]:
            self._bind_with_computer(frame, view_model)
        elif data["multiplayer"]:
            self._bind_multiplayer(frame, view_model)
        else:
            self._bind_two_player(frame, view_model)
        return frame


class GameResultViewModel(IViewModel):
    def __init__(self, model: TicTacToeModel) -> None:
        super().__init__(model)

    def _bind(self, view: GameResultView, vm: ViewModel) -> None:
        view.to_menu_btn.config(command=lambda: vm.swap("main", {}))

    def start(self, root: Tk, view_model: ViewModel, data: dict[str, Any]) -> GameResultView:
        def get_winner() -> str:
            if self._model.session.value == 0:
                return "Draw. No one wins"
            else:
                return f"Player {self._model.session.value} win"

        frame = GameResultView(root)
        self._bind(frame, view_model)
        frame.label.config(text=get_winner())
        frame.grid(row=1, column=1)
        return frame


if __name__ == "__main__":
    pass
