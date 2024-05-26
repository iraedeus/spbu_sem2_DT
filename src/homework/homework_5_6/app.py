from tkinter import Tk

from src.homework.homework_5_6.model import Player, TicTacToeModel
from src.homework.homework_5_6.viewmodel import ViewModel


class App:
    def __init__(self) -> None:
        self._root = self.setup_root()
        self._model = TicTacToeModel(Player(-1), Player(-1))
        self._viewmodel = ViewModel(self._root, self._model)

    def setup_root(self) -> Tk:
        root = Tk()
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)

        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)

        root.title("Tic Tac Toe")
        root.geometry("600x600+700+250")
        return root

    def start(self) -> None:
        self._viewmodel.start()
        self._root.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
