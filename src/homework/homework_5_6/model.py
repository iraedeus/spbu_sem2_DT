from typing import Optional

from src.homework.homework_5_6.observer import Observable


class Player:
    def __init__(self, id: int) -> None:
        self.id = id


class EasyBot(Player):
    def __init__(self, id: int) -> None:
        super().__init__(id)


class HardBot(Player):
    def __init__(self, id: int) -> None:
        super().__init__(id)


class Human(Player):
    def __init__(self, id: int) -> None:
        super().__init__(id)


class TicTacToeModel:
    def __init__(self, player_1: Optional[Player], player_2: Optional[Player]) -> None:
        self.players = (player_1, player_2)
        self.current_player = player_1
        self.field: list[list[Observable]] = [
            [Observable(0), Observable(0), Observable(0)],
            [Observable(0), Observable(0), Observable(0)],
            [Observable(0), Observable(0), Observable(0)],
        ]

    def place(self, row: int, column: int):
        def place_cross(row: int, column: int) -> None:
            if self.field[row][column].value == 0:
                self.field[row][column].value = 1
                self.swap_players()

        def place_circle(row: int, column: int) -> None:
            if self.field[row][column].value == 0:
                self.field[row][column].value = 2
                self.swap_players()

        if self.current_player.id == 1:
            place_cross(row, column)
        else:
            place_circle(row, column)

    def swap_players(self) -> None:
        for player in self.players:
            if player != self.current_player:
                self.current_player = player
                return None
