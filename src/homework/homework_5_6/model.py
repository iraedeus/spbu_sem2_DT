import copy
import math
import random
from abc import abstractmethod
from typing import Any, Optional

from src.homework.homework_5_6.observer import Observable


class Player:
    def __init__(self, id: int) -> None:
        self.id = id


class EasyBot(Player):
    def __init__(self, id: int) -> None:
        super().__init__(id)

    def turn(self, field: "Field") -> None:
        while True:
            random_x = random.randint(0, 2)
            random_y = random.randint(0, 2)
            if field.get(random_x, random_y) != 0:
                continue
            else:
                field.set(random_x, random_y, self.id)
                break


class HardBot(Player):
    def __init__(self, id: int) -> None:
        super().__init__(id)

    def turn(self, field: "Field") -> None:
        def get_indexes_of_possible_turns(field: list[list[int]]) -> list[tuple[int, int]]:
            possible_turns_indexes = []
            for r in range(3):
                for c in range(3):
                    if field[r][c] == 0:
                        possible_turns_indexes.append((r, c))
            return possible_turns_indexes

        opponent_id = 2 // self.id
        possible_turns = get_indexes_of_possible_turns(field.field_without_observers())

        for turn in possible_turns:
            if field.check_if_player_won(self.id):
                field.field[turn[0]][turn[1]].value = self.id
                return None

        for turn in possible_turns:
            if field.check_if_player_won(opponent_id):
                field.field[turn[0]][turn[1]].value = self.id
                return None

        best_turns = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2), (0, 1), (1, 0), (1, 2), (2, 1)]
        for turn in best_turns:
            if field.get(*turn) == 0:
                field.field[turn[0]][turn[1]].value = self.id
                return None


class Human(Player):
    def __init__(self, id: int) -> None:
        super().__init__(id)

    def turn(self, field: "Field", r: int, c: int) -> None:
        field.set(r, c, self.id)


class Field:
    def __init__(self) -> None:
        self._field: list[list[Observable]] = [
            [Observable(0), Observable(0), Observable(0)],
            [Observable(0), Observable(0), Observable(0)],
            [Observable(0), Observable(0), Observable(0)],
        ]

    @property
    def field(self) -> list[list[Observable]]:
        return self._field

    def field_without_observers(self) -> list[list[int]]:
        return [[self.get(r, c) for r in range(3)] for c in range(3)]

    def is_field_full(self) -> bool:
        return all([self.get(r, c) != 0 for r in range(3) for c in range(3)])

    def check_if_player_won(self, player_id: int) -> bool:
        for i in range(3):
            if (self.get(0, i) == self.get(1, i) == self.get(2, i) == player_id) or (
                self.get(i, 0) == self.get(i, 1) == self.get(i, 2) == player_id
            ):
                return True

        if (self.get(0, 0) == self.get(1, 1) == self.get(2, 2) == player_id) or (
            self.get(0, 2) == self.get(1, 1) == self.get(2, 0) == player_id
        ):
            return True
        else:
            return False

    def set(self, row: int, column: int, value: int) -> None:
        self.field[row][column].value = value

    def get(self, r: int, c: int) -> int:
        return self._field[r][c].value


class TicTacToeModel:
    def __init__(self) -> None:
        self.players: Optional[tuple[Player, Player]] = None
        self.current_player: Optional[Player] = None
        self.next_player: Optional[Player] = None
        self.field: Field = Field()
        self.session = Observable(0)

    def start_easy_bot_game(self, side: str) -> None:
        if side == "cross":
            self.players = (Human(1), EasyBot(2))
        else:
            self.players = (EasyBot(1), Human(2))
        self.current_player = self.players[0]
        self.next_player = self.players[1]

    def start_hard_bot_game(self, side: str) -> None:
        if side == "cross":
            self.players = (Human(1), HardBot(2))
        else:
            self.players = (HardBot(1), Human(2))
        self.current_player = self.players[0]
        self.next_player = self.players[1]

    def start_two_players(self) -> None:
        self.players = (Human(1), Human(2))
        self.current_player = self.players[0]
        self.next_player = self.players[1]

    def end_game(self) -> None:
        if self.next_player is not None:
            player_id = self.next_player.id
            is_current_player_won = self.field.check_if_player_won(player_id)
            is_field_full = self.field.is_field_full()
            new_model = TicTacToeModel()

            if is_current_player_won:
                self.session.value = player_id
                self.players = new_model.players
                self.current_player = new_model.current_player
                self.field = new_model.field
            elif is_field_full:
                self.session.value = 0

    def swap_players(self) -> None:
        self.next_player, self.current_player = self.current_player, self.next_player


if __name__ == "__main__":
    pass
