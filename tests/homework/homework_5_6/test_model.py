from src.homework.homework_5_6.model import *


class TestEasyBot:
    model = TicTacToeModel(HardBot(1), EasyBot(2))

    def test_game(self):
        first_player = self.model.players[0]
        second_player = self.model.players[1]
        for i in range(4):
            first_player.turn(self.model)
            if self.model.is_field_full(self.model.get_copy_of_field()):
                break
            second_player.turn(self.model)
            if self.model.is_field_full(self.model.get_copy_of_field()):
                break
        assert self.model.session.value == 1


class TestHardBot:
    model = TicTacToeModel(HardBot(1), HardBot(2))

    def test_game(self):
        first_player = self.model.players[0]
        second_player = self.model.players[1]
        for i in range(4):
            first_player.turn(self.model)
            if i == 3:
                break
            second_player.turn(self.model)
        assert self.model.session.value == 0
