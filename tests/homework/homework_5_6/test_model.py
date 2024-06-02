from src.homework.homework_5_6.model import *


class TestEasyBot:
    model = TicTacToeModel()
    model.players = (HardBot(1), EasyBot(2))

    def test_game(self):
        first_player = self.model.players[0]
        second_player = self.model.players[1]
        for i in range(4):
            first_player.turn(self.model.field)
            if self.model.field.is_field_full():
                break
            second_player.turn(self.model.field)
            if self.model.field.is_field_full():
                break
        assert self.model.field.check_if_player_won(1)


class TestHardBot:
    model = TicTacToeModel()
    model.players = (HardBot(1), HardBot(2))

    def test_game(self):
        first_player = self.model.players[0]
        second_player = self.model.players[1]
        for i in range(4):
            first_player.turn(self.model.field)
            if i == 3:
                break
            second_player.turn(self.model.field)
        assert not self.model.field.check_if_player_won(1) and not self.model.field.check_if_player_won(2)
