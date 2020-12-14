from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


tableau = {"mouv": " "} #envoye classe game completé
tours = {"tours": 1}
clickeffectuer = {"fait": False}
person = []
board = []
id_change = []


class Grille(App):

    def build(self):
        """
        build the board
        :return: self.grille a list of widget
        """
        Config.set('graphics', 'width', '300')
        Config.set('graphics', 'height', '300')
        if person[0] == "X":
            self.title = 'client'
        else:
            self.title = 'server'
        self.grille = GridLayout(rows=3, cols=3)
        for i in range(9):
            case = Button(text=str(i))
            self.grille.add_widget(case)
            case.bind(on_press=self.click)
            board.append(case)
        return self.grille

    def click(self, event):
        """
        put a X or O onclick
        :param event: the button click
        :return: None
        """
        for i in range(9):
            if board[i].text == event.text:
                tableau["mouv"] = str(i)
                if person[0] == "X":
                    event.text = "X"
                else:
                    event.text = "O"
                clickeffectuer["fait"] = True

    def update(self):
        """
        update the board
        :return: None
        """
        if person[0] == "X":
            for i in board:
                if id_change[-1] == i.text:
                    i.text = "O"
        else:
            for i in board:
                if id_change[-1] == i.text:
                    i.text = "X"


def start(signe):
    """
    start the interface
    :param signe: the signe of the local player
    :return: none
    """
    person.append(signe)
    Grille().run()
