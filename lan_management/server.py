import socket
import pickle
from gui import interface
import threading
from game_management import common


tab = [False]


def handle_client(conn, addr, graphique, joueur):
    """
    handling of object
    :param conn: = server.accept()[0]
    :param addr: {tuple} of the id of the server and the port number
    :param graphique: {bool} True == console, False == interface
    :param joueur: {list} of current player
    :return: None
    """
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            if common.game.end:
                common.announce_winner(joueur[0], joueur[1])
                connected = False

            elif interface.tours["tours"] % 2 != 0:
                data = conn.recv(2048)
                reply = pickle.loads(data)  # data.decode("utf-8")
                interface.tableau["mouv"] = reply["mouv"]
                interface.id_change.append(reply["mouv"])
                if interface.tours["tours"] > 2:
                    common.game.make_move(interface.tableau["mouv"], joueur[1])
                    print("mouv :", interface.tableau["mouv"], joueur[1])
                print("reponse client", reply)
                interface.tours["tours"] += 1
                if not data:
                    print("disconnected not data")
                    connected = False
            else:
                if graphique:
                    interface.tours["tours"] += 1
                    console = input("choississer une case : ")
                    interface.tableau["mouv"] = console
                    common.game.make_move(interface.tableau["mouv"], joueur[0])
                    conn.send(pickle.dumps(interface.tableau))
                else:
                    if interface.clickeffectuer["fait"]:
                        print("tableau :", interface.tableau)
                        interface.tours["tours"] += 1
                        print("tableau envoyer: ", interface.tableau)

                        common.game.make_move(interface.tableau["mouv"], joueur[0])
                        print("mouv :", interface.tableau["mouv"], joueur[0])
                        interface.clickeffectuer["fait"] = False
                        conn.send(pickle.dumps(interface.tableau))

        except:
            print("disconnected execpt")
            connected = False
    print("disconnected after boucle")
    tab.append(True)
    conn.close()


def info():
    """
    info about the server
    :return: a socket object : server
    """
    port = 5050
    server_ip = socket.gethostbyname(socket.gethostname())
    print(f"[LISTENING] Server is listening on {server_ip}")
    addr = (server_ip, port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(addr)
    return server


def start(graphique):
    """
    start the game with the interface or the console
    :param graphique: {bool} True == console, False == interface
    :return: None
    """
    joueur = presentation()
    server = info()
    print("[STARTING] server is starting...")
    if not graphique:
        signe = "O"
        thread_interface = threading.Thread(target=interface.start, args=signe)
        thread_interface.start()
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, graphique, joueur))
        thread.start()
        print(f" ACTIVE CONNECTIONS :{threading.activeCount() - 1}")
        while True:
            if tab[-1]:
                break
        break


def presentation():
    """
    get the information about the player
    :return: {list} of current player
    """
    joueur = []
    nom_serveur = input("Enter the name of the first player : ")
    multi_player_1 = common.Player(nom_serveur, "O")
    nom_client = "client"
    multi_player_2 = common.Player(nom_client, "X")
    print(f"{multi_player_1.user_name} will represent the {multi_player_1.sign} plays and {multi_player_2.user_name} "
          f"will represent the {multi_player_2.sign} plays.\n")
    input("Press any key to continue...")
    print("Let's begin !")
    joueur.append(multi_player_1)
    joueur.append(multi_player_2)
    return joueur
