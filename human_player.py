import socket

import numpy as np


class BlackJack():

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(1)
        print("connecting")
        self.sock.connect((("localhost", 4050)))
        print("connected to {}".format(self.sock))

        self.sock.send(b"name")
        byte_size = int(self.sock.recv(1).decode())
        print(byte_size)
        self.name = self.sock.recv(byte_size).decode()
        print(self.name)

        self.burnt = False

        self.cards = []
        self.waiting = False
        for _ in range(2):
            # draw 2 pog
            # print("init")
            self.burnt = self.draw_a_card()
            # time.sleep(0.1)
        # print(f"{self.name} is starting with {self.cards}")

    def draw_a_card(self):
        # print("draw")
        if not self.waiting:
            self.sock.send(b"draw")
            answer = self.sock.recv(1).decode()
            byte_size = int(answer)
            card = int(self.sock.recv(byte_size).decode())
            self.cards.append(card)
            # print(f"{self.name} drew a {card}")
            burning = self.get_BJ_score() > 21
            if burning:
                self.waiting = True
                # print("{} burnt".format(self.name))
            return burning

    def step(self, action):
        done = False
        reward = 0
        if action == 1 and not self.waiting:  # we wait
            # print("starting to wait")
            self.waiting = True
        if action == 0 and not self.waiting:  # draw a card
            # print("drawing a card")
            #    print("drawing, cards: {}".format(self.cards))
            self.burnt = self.draw_a_card()
            reward = 0
            if not self.burnt:
                done = False
            else:
                done = True
        if self.waiting:  # we stop
            # print("waiting")
            self.sock.send(b"wait")
            # ack = self.sock.recv(3)
            answer = self.sock.recv(1)
            print(answer)
            while answer == b"c":
                # print("waiting still")
                self.sock.send(b"wait")
                answer = self.sock.recv(1)
            if answer == b"w":
                print("{} won with {}".format(self.name, self.get_BJ_score()))
                reward = 1
                done = True
            elif answer == b"l":
                print("{} lost wih {}".format(self.name, self.get_BJ_score()))
                reward = -1
                done = True
            else:
                print(answer.decode())
                raise Exception()

        # Setting the placeholder for info
        info = {}

        # Returning the step information
        # to_return = np.array(self.cards)
        # to_return.resize(22, )
        return np.pad(self.cards, (0, 22 - len(self.cards))), reward, done, info

    def render(self, mode="human"):
        print("Player {} has those cards: {}".format(self.name, self.cards))

    def reset(self, *, seed=None, return_info=False, options=None, ):
        # print("reset")
        self.cards = []
        self.waiting = False
        self.burnt = False
        self.sock.send(b"rese")
        # ack = self.sock.recv(3)
        # print(ack)
        for _ in range(2):
            # draw 2 pog
            #    print("reset")
            self.burnt = self.draw_a_card()
            # time.sleep(0.1)
        # to_return = np.array(self.cards)
        # to_return.resize(22,)
        return np.pad(self.cards, (0, 22 - len(self.cards)))

    def get_BJ_score(self):
        return sum(self.cards)

    def clean_up(self):
        self.sock.send(b"stop")

    def ping(self):
        self.sock.send(b"ping")
        data = self.sock.recv(4)
        print(data.decode())


if __name__ == "__main__":
    playing = True
    env = BlackJack()
    while playing:
        cards = env.reset()
        waiting = False
        done = False
        reward = 0
        while not done:
            if not waiting:
                print("Your cards are {}".format([card for card in cards if card != 0]))
                choice = input("0 if you want to draw a card or 1 if you want to stop here")
                if choice == '0' or choice == '1':
                    cards, reward, done, info = env.step(int(choice))
                    if choice == '1':
                        waiting = True
                else:
                    print("You need to input 0 or 1")
            else:
                n_state, reward, done, info = env.step(1)
        if reward == 1:
            print("You've won")
        else:
            print("You've lost")

        choice = input("Want to replay y/N ?")
        if choice != "y":
            playing = False
