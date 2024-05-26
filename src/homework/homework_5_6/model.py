import copy
import math
import random
from abc import abstractmethod
from typing import Any

from src.homework.homework_5_6.observer import Observable


class Player:
    def __init__(self, id: int) -> None:
        self.id = id

    def turn(self, model: "TicTacToeModel") -> None:
        pass


class EasyBot(Player):
    def __init__(self, id: int) -> None:
        super().__init__(id)

    def turn(self, model: "TicTacToeModel") -> None:
        field = model.field
        while True:
            random_x = random.randint(0, 2)
            random_y = random.randint(0, 2)
            if field[random_x][random_y].value != 0:
                continue
            else:
                model.place(random_x, random_y)
                break


class HardBot(Player):
    def __init__(self, id: int) -> None:
        super().__init__(id)

    def minimax(self, model: "TicTacToeModel", field: list[list[int]]) -> tuple:
        def get_indexes_of_possible_turns(field: list[list[int]]) -> list[list]:
            possible_turns_indexes = []
            for r in range(3):
                for c in range(3):
                    if field[r][c] == 0:
                        possible_turns_indexes.append([(r, c), 0])
            return possible_turns_indexes

        def get_subset_of_possible_turns(indexes: list[list[Any]], possible_turns: list[list[Any]]) -> list:
            output = []
            for turn in indexes:
                for i in range(len(possible_turns)):
                    if turn[0] == possible_turns[i][0]:
                        output.append(possible_turns[i])
            return output

        def recursion(current_possible_turns: list[list[Any]], current_field: list[list[int]]) -> None:
            for turn in current_possible_turns:
                r, c = turn[0][0], turn[0][1]
                new_field = copy.deepcopy(current_field)
                new_field[r][c] = model.current_player.id
                new_possible_turns_indexes = get_indexes_of_possible_turns(new_field)
                new_possible_turns = get_subset_of_possible_turns(new_possible_turns_indexes, current_possible_turns)

                if model.check_if_current_player_won(model.current_player.id, new_field):
                    turn[1] += 1
                    model.swap_players()
                    return None
                elif model.check_if_current_player_won(2 // model.current_player.id, new_field):
                    turn[1] -= 1
                    model.swap_players()
                    return None
                elif model.is_field_full(new_field):
                    turn[1] += 0
                    model.swap_players()
                    return None
                else:
                    recursion(new_possible_turns, new_field)

        def get_best(possible_turns: list[list[Any]]) -> tuple[int, int]:
            return max(possible_turns, key=lambda turn: turn[1])[0]

        possible_turns = get_indexes_of_possible_turns(field)
        recursion(possible_turns, field)

        return get_best(possible_turns)

    def turn(self, model: "TicTacToeModel") -> None:
        field = model.get_copy_of_field()
        current_player = model.current_player
        list_field = [[field[r][c] for c in range(3)] for r in range(3)]
        r, c = self.minimax(model, list_field)
        model.current_player = current_player
        model.place(r, c)


class Human(Player):
    def __init__(self, id: int) -> None:
        super().__init__(id)


class TicTacToeModel:
    def __init__(self, player_1: Player, player_2: Player) -> None:
        self.players: tuple[Player, Player] = (player_1, player_2)
        self.current_player: Player = player_1
        self.field: list[list[Observable]] = [
            [Observable(0), Observable(0), Observable(0)],
            [Observable(0), Observable(0), Observable(0)],
            [Observable(0), Observable(0), Observable(0)],
        ]
        self.session = Observable(0)

    def get_copy_of_field(self) -> list[list[int]]:
        field = self.field
        output: list[list[int]] = [[], [], []]
        for r in range(3):
            for c in range(3):
                output[r].append(field[r][c].value)
        return output

    def place(self, row: int, column: int) -> None:
        def place_cross(row: int, column: int) -> None:
            if self.field[row][column].value == 0:
                self.field[row][column].value = 1
                self.swap_players()

        def place_circle(row: int, column: int) -> None:
            if self.field[row][column].value == 0:
                self.field[row][column].value = 2
                self.swap_players()

        if self.current_player is not None and self.current_player.id == 1:
            place_cross(row, column)
        else:
            place_circle(row, column)

        if self.check_if_current_player_won(
            self.get_last_turn_player_id(), self.get_copy_of_field()
        ) or self.is_field_full(self.get_copy_of_field()):
            self.end_game()

    def is_field_full(self, field: list[list[int]]) -> bool:
        no_zero = True
        for r in range(3):
            for c in range(3):
                if field[r][c] != 0:
                    no_zero = no_zero and True
                else:
                    no_zero = False

        return no_zero

    def get_last_turn_player_id(self) -> int:
        if self.current_player is not None:
            if self.current_player.id == 2:
                return 1
            else:
                return 2
        else:
            return 0

    def end_game(self) -> None:
        player_id = self.get_last_turn_player_id()
        is_current_player_won = self.check_if_current_player_won(player_id, self.get_copy_of_field())
        is_field_full = self.is_field_full(self.get_copy_of_field())
        new_model = TicTacToeModel(Player(-1), Player(-1))
        self.players = new_model.players
        self.current_player = new_model.current_player
        self.field = new_model.field

        if is_current_player_won:
            self.session.value = player_id
        elif is_field_full:
            self.session.value = 0

    def check_if_current_player_won(self, player_id: int, field: list[list[int]]) -> bool:
        smh = 0
        for i in range(3):
            if (field[0][i] == field[1][i] == field[2][i] == player_id) or (
                field[i][0] == field[i][1] == field[i][2] == player_id
            ):
                return True

        if (field[0][0] == field[1][1] == field[2][2] == player_id) or (
            field[0][2] == field[1][1] == field[2][0] == player_id
        ):
            return True
        return False

    def swap_players(self) -> None:
        for player in self.players:
            if player != self.current_player:
                self.current_player = player
                return None


if __name__ == "__main__":
    pass
