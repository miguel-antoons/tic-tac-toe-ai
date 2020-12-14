from game_management import common
from lan_management import server, client


def multi_play():
    """
    Runs the multiplayer mode
    :return: None
    """
    graphique = False
    choose = input("server or client : ")
    interface = input("interface yes or no : ")

    if interface == "no":
        common.game = common.Game(True)
        graphique = True
    if choose == "server":
        server.start(graphique)
    else:
        client.start(graphique)
