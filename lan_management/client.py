import socket
import pickle
from gui import interface
import threading
from game_management import common


def info():
    """
    info about the server
    :return: a socket object : client
    """
    port = 5050 # The port used by the server  (non-privileged ports are > 1023)
    server_ip = socket.gethostbyname(socket.gethostname()) # get ip address serveur
    addr = (server_ip, port) # address server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a socket object which specify address family and socket type. AF_NET = IPV4, SOCK_STREAM = TCP
    client.connect(addr)
    return client


def gestion_client(graphique, client, joueur):
    """
    handling of object
    :param graphique: {bool} True == console, False == interface
    :param client: socket object
    :param joueur: list of 2 player (player 1 and 2)
    :return: -
    """
    if interface.tours["tours"] == 1:
        print("tableau envoyer de départ:", interface.tableau)
        client.send(pickle.dumps(interface.tableau))
        common.game.make_move(interface.tableau["mouv"], joueur[0])
        reception = pickle.loads(client.recv(2048))  # self.client.recv(2048).decode()
        interface.tableau["mouv"] = reception["mouv"]
        interface.id_change.append(reception["mouv"])
        common.game.make_move(interface.tableau["mouv"], joueur[1])
        print("tableau recu", reception)
        interface.tours["tours"] += 1
        gestion_client(graphique, client, joueur)
    else:
        if graphique:
            console = input("choississer une case : ")
            interface.tableau["mouv"] = console
            client.send(pickle.dumps(interface.tableau))
            common.game.make_move(interface.tableau["mouv"], joueur[0])
            if common.game.end:
                common.announce_winner(joueur[0], joueur[1])
            else:
                reception = pickle.loads(client.recv(2048))  # self.client.recv(2048).decode()
                interface.tableau["mouv"] = reception["mouv"]
                interface.id_change.append(reception["mouv"])
                common.game.make_move(interface.tableau["mouv"], joueur[1])
                if common.game.end:
                    print("tableau recu", reception)
                    common.announce_winner(joueur[0], joueur[1])
                else:
                    print("tableau recu", reception)
                    gestion_client(graphique, client, joueur)
        else:

            while True:
                if interface.clickeffectuer["fait"]:
                    client.send(pickle.dumps(interface.tableau))
                    common.game.make_move(interface.tableau["mouv"], joueur[0])
                    if common.game.end:
                        common.announce_winner(joueur[0], joueur[1])
                        break
                    else:
                        reception = pickle.loads(client.recv(2048))  # self.client.recv(2048).decode()
                        interface.tableau["mouv"] = reception["mouv"]
                        interface.id_change.append(reception["mouv"])
                        common.game.make_move(interface.tableau["mouv"], joueur[1])
                        interface.clickeffectuer["fait"] = False
                        print("tableau recu", reception)
                        break
            if common.game.end:
                common.announce_winner(joueur[0], joueur[1])
            else:
                gestion_client(graphique, client, joueur)





def start(graphique):
    """
    start the game with the interface or the console
    :param graphique: {bool} True == console, False == interface
    :return: None
    """
    client = info()
    joueur = presentation()
    if not graphique:
        threading_client = threading.Thread(target=interface.start, args="X")
        threading_client.start()
    print("tableau client :", interface.tableau)
    gestion_client(graphique, client, joueur)


def presentation():
    """
    get the information about the player
    :return: list of current player
    """
    joueur = []
    nom_client = input("Enter the name of the first player : ")
    multi_player_1 = common.Player(nom_client, "X")
    nom_server = "server"
    multi_player_2 = common.Player(nom_server, "O")
    print(f"{multi_player_1.user_name} will represent the {multi_player_1.sign} plays and {multi_player_2.user_name} "
          f"will represent the {multi_player_2.sign} plays.\n")
    input("Press any key to continue...")
    print("Let's begin !")
    joueur.append(multi_player_1)
    joueur.append(multi_player_2)
    return joueur
