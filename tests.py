import unittest
from datetime import datetime
from user_management.user import User
from game_management.common import Game, Player
from game_management.AI import PlayerMove
from game_management.scores import Score


class TestPlayerMove(unittest.TestCase):
    """
    Unitary tests of the PlayerMove class in the game_management.AI module
    """
    def test_str(self):
        move = PlayerMove("O", 3, 8)
        self.assertEqual(move.__str__(), "turn_n: 3\tmove: 8\tresult: 0.0")

    def test_property_sign(self):
        self.assertEqual(PlayerMove("O", 3, 8).sign, "O")

    def test_property_turn_n(self):
        self.assertEqual(PlayerMove("O", 3, 8).turn_n, 3)

    def test_property_move(self):
        self.assertEqual(PlayerMove("O", 3, 8).move, 8)

    def test_property_result(self):
        self.assertEqual(PlayerMove("O", 3, 8).result, 0.0)


class TestGame(unittest.TestCase):
    """
    Unitary tests of the Game class in the game_management.common module
    """
    def test_property_round_nb(self):
        self.assertEqual(Game().round_nb, 0)

    def test_property_end(self):
        self.assertFalse(Game().end)

    def test_property_available_plays(self):
        self.assertEqual(Game().available_plays, [0, 1, 2, 3, 4, 5, 6, 7, 8])

    def test_make_move(self):
        game = Game()
        player_1 = Player("player_1", "O")
        player_2 = Player("player_2", "X")
        self.assertTrue(game.make_move("s", player_1))
        self.assertTrue(game.make_move(10, player_1))
        self.assertFalse(game.make_move(0, player_1))

        self.assertTrue(game.make_move(0, player_2))
        self.assertFalse(game.make_move(1, player_2))
        self.assertFalse(game.make_move(4, player_1))
        self.assertFalse(game.make_move(2, player_2))
        self.assertFalse(game.make_move(8, player_1))
        self.assertTrue(game.end)
        self.assertTrue(player_1.winner)


class TestScore(unittest.TestCase):
    """
    Unitary tests of the Score class in the game_management.scores module
    """
    def test_str(self):
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.assertEqual(Score("player_1", "X", 6, date).__str__(),
                         "{:40} {:25} {:10}".format("player_1", date, str(17)))

    def test_return_calculated(self):
        self.assertEqual(Score("player_1", "O", 5, "nothing").return_calculated_score(), 14)
        self.assertEqual(Score("player_1", "X", 7, "nothing").return_calculated_score(), 14)
        self.assertEqual(Score("player_1", "X", 6, "nothing").return_calculated_score(), 14)


class TestPlayer(unittest.TestCase):
    """
    Unitary tests of the Player class in the game_management.common module
    """
    def test_property_user_name(self):
        self.assertEqual(Player("player_1").user_name, "player_1")

    def test_property_sign(self):
        self.assertEqual(Player("player_1").sign, "")
        self.assertEqual(Player("player_1", "O").sign, "O")

        player_1 = Player("player_1", "X")
        player_1.sign = "O"
        self.assertEqual(player_1.sign, "O")

    def test_property_winner(self):
        player_1 = Player("player_1")
        self.assertFalse(player_1.winner)
        player_1.winner = True
        self.assertTrue(player_1.winner)


class TestUser(unittest.TestCase):
    """
    Unitary tests of the User class in the user_management.user module
    """
    def test_property_user_name(self):
        test_user_1 = User("user 123", "usertyuomn18643", "George", "Hanssen", "g.hanssen@example.com",
                           "Nothing to do . . . ", "True")
        test_user_2 = User("user 234", "ibsqigiad45433", "Logan", "Paul", "l.paul@example.com",
                           "New episode on youtube !!", "False")
        self.assertEqual(test_user_1.user_name, "user 123")
        self.assertEqual(test_user_2.user_name, "user 234")

    def test_property_name(self):
        test_user_1 = User("user 123", "usertyuomn18643", "George", "Hanssen", "g.hanssen@example.com",
                           "Nothing to do . . . ", "True")
        test_user_2 = User("user 234", "ibsqigiad45433", "Logan", "Paul", "l.paul@example.com",
                           "New episode on youtube !!", "False")
        self.assertEqual(test_user_1.name, "George")
        self.assertEqual(test_user_2.name, "Logan")

    def test_property_last_name(self):
        test_user_1 = User("user 123", "usertyuomn18643", "George", "Hanssen", "g.hanssen@example.com",
                           "Nothing to do . . . ", "True")
        test_user_2 = User("user 234", "ibsqigiad45433", "Logan", "Paul", "l.paul@example.com",
                           "New episode on youtube !!", "False")
        self.assertEqual(test_user_1.last_name, "Hanssen")
        self.assertEqual(test_user_2.last_name, "Paul")

    def test_property_email(self):
        test_user_1 = User("user 123", "usertyuomn18643", "George", "Hanssen", "g.hanssen@example.com",
                           "Nothing to do . . . ", "True")
        test_user_2 = User("user 234", "ibsqigiad45433", "Logan", "Paul", "l.paul@example.com",
                           "New episode on youtube !!", "False")
        self.assertEqual(test_user_1.email, "g.hanssen@example.com")
        self.assertEqual(test_user_2.email, "l.paul@example.com")

    def test_property_description(self):
        test_user_1 = User("user 123", "usertyuomn18643", "George", "Hanssen", "g.hanssen@example.com",
                           "Nothing to do . . . ", "True")
        test_user_2 = User("user 234", "ibsqigiad45433", "Logan", "Paul", "l.paul@example.com",
                           "New episode on youtube !!", "False")
        self.assertEqual(test_user_1.description, "Nothing to do . . . ")
        self.assertEqual(test_user_2.description, "New episode on youtube !!")

    def test_property_admin(self):
        test_user_1 = User("user 123", "usertyuomn18643", "George", "Hanssen", "g.hanssen@example.com",
                           "Nothing to do . . . ", "True")
        test_user_2 = User("user 234", "ibsqigiad45433", "Logan", "Paul", "l.paul@example.com",
                           "New episode on youtube !!", "False")
        self.assertTrue(test_user_1.admin)
        self.assertFalse(test_user_2.admin)

    def test_property_password(self):
        test_user_1 = User("user 123", "usertyuomn18643", "George", "Hanssen", "g.hanssen@example.com",
                           "Nothing to do . . . ", "True")
        test_user_2 = User("user 234", "ibsqigiad45433", "Logan", "Paul", "l.paul@example.com",
                           "New episode on youtube !!", "False")
        self.assertEqual(test_user_1.password, "Unable to fulfill request")
        self.assertEqual(test_user_2.password, "Unable to fulfill request")
