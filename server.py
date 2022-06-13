import random
import socket
import threading

from names import names

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0", 4050))
sock.setblocking(True)
sock.listen(5)

NBR_PLAYERS_NEEDED = 2



resolving_game = False


class Player:
    def __init__(self, cnn, addr, id):
        self.cards = 0
        self.name = "undefined"
        self.waiting = False

        self.rcards = []
        self.cnn = cnn
        self.addr = addr

        self.id = id

    '''def __repr__(self):
        return self.cards'''


players = {}

nbr_players = 0


def running():
    global nbr_players, players, resolving_game
    print("Main starting")
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    while True:
        if len(players) != 0:
            copy_of_players = players.copy()

            for key, player in copy_of_players.items():

                print(copy_of_players.items())
                print(f"Turn of {player.name}")
                cnn = player.cnn
                addr = player.addr
                waiting = True
                while nbr_players < NBR_PLAYERS_NEEDED:
                    if waiting:
                        print("waiting")
                        waiting = False

                try:
                    data2 = cnn.recv(4)
                    data = data2.decode()
                    print(data)
                    if data == "draw":
                        card = random.choice(cards)
                        cnn.send(str(len(str(card).encode())).encode())
                        cnn.send(str(card).encode())
                        players[key].cards += card
                        players[key].rcards.append(card)
                        if players[key].cards > 21:
                            players[key].cards = -1
                            players[key].waiting = True
                            all_players_waiting = [i.name for i in copy_of_players.values() if not i.waiting]
                            if len(all_players_waiting) == 0:
                                game_completed = True

                    elif data == "name":
                        name = random.choice(names)
                        name_b = name.encode()

                        cnn.send(str(len(name_b)).encode())

                        cnn.send(name_b)
                        players[key].name = name
                    elif data == "wait":
                        # cnn.send(b"ack")
                        players[key].waiting = True
                        copy_of_players[key].waiting = True
                        all_players_waiting = [i.name for i in copy_of_players.values() if not i.waiting]
                        if len(all_players_waiting) == 0:

                            winner = max(copy_of_players, key=lambda x: players[x].cards)

                            if player.id == winner:
                                print("{} won with a score of {} and the cards {}".format(player.name,
                                                                                          player.cards,
                                                                                          player.rcards))
                                player.cnn.send(b"w")
                            else:
                                print("{} lost with a score of {} and the cards {}".format(player.name,
                                                                                           player.cards,
                                                                                           player.rcards))
                                player.cnn.send(b"l")
                        else:
                            player.cnn.send(b"c")
                    elif data == "stop":
                        players = {k: v for k, v in copy_of_players.items() if v != player}

                        nbr_players -= 1
                    elif data == "rese":
                        players[player.id].rcards = []
                        players[player.id].cards = 0
                        players[player.id].waiting = False
                        copy_of_players[player.id].rcards = []
                        copy_of_players[player.id].cards = 0
                        copy_of_players[player.id].waiting = False
                        # print(player.name + " is resetting")
                        # cnn.send(b"ACK")
                    elif data == "ping":
                        print("pong")
                        cnn.send("1234".encode())
                    else:
                        raise Exception()
                    # render()

                except:
                    return



def render():
    for player in players.values():
        print("Player {}: {}, {}".format(player.name, player.cards, player.rcards))
    print("==================================================================")


def connection():
    global players, nbr_players, NBR_PLAYERS_NEEDED
    print("Connection starting")

    while 1:
        cnn2, addr2 = sock.accept()
        print(f"New player from address : {addr2}")
        new_player = Player(cnn2, addr2, nbr_players % NBR_PLAYERS_NEEDED)
        players[nbr_players % NBR_PLAYERS_NEEDED] = new_player
        nbr_players += 1


if __name__ == "__main__":
    print("==================================================================")
    threading.Thread(target=running).start()
    threading.Thread(target=connection).start()
