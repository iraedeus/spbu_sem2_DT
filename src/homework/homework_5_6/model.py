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
        self.session = Observable(0)

    def end_game(self) -> None:
        player_id = self.get_last_turn_player_id()
        is_full = self.is_field_full()
        new_model = TicTacToeModel(None, None)
        self.players = new_model.players
        self.current_player = new_model.current_player
        self.field = new_model.field
        if not is_full:
            self.session.value = player_id
        else:
            self.session.value = 0

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

        if self.check_if_current_player_won() or self.is_field_full():
            self.end_game()

    def is_field_full(self) -> bool:
        no_zero = True
        for r in range(3):
            for c in range(3):
                if self.field[r][c].value != 0:
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

    def check_if_current_player_won(self) -> bool:
        field = self.field
        player_id = self.get_last_turn_player_id()

        for i in range(3):
            if (field[0][i] == field[1][i] == field[2][i] == Observable(player_id)) or (
                field[i][0] == field[i][1] == field[i][2] == Observable(player_id)
            ):
                return True

        if (field[0][0] == field[1][1] == field[2][2] == Observable(player_id)) or (
            field[0][2] == field[1][1] == field[2][0] == Observable(player_id)
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
