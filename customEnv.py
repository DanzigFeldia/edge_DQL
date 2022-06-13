import socket

import gym
import numpy as np
from gym.spaces import Box, Discrete


class BlackJack(gym.Env):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(True)
        print("connecting")
        self.sock.connect((("127.0.0.1", 4050)))
        print("connected to {}".format(self.sock))
        self.action_space = Discrete(2)  # draw and stop
        self.observation_space = Box(low=0, high=255, shape=(12,))

        self.sock.send(b"name")
        received = self.sock.recv(1).decode()
        byte_size = int(received)
        print(byte_size)
        self.name = self.sock.recv(byte_size).decode()
        print(self.name)

        self.burnt = False

        self.cards = []
        self.waiting = False
        for _ in range(2):
            self.burnt = self.draw_a_card()


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
            if not self.burnt:
                self.waiting = False
            else:
                self.waiting = True
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

        #Formatting the state
        state = np.pad(self.cards, (0, 12 - len(self.cards)))

        # Returning the step information
        return state, reward, done, info

    def render(self, mode="human"):
        print("Player {} has those cards: {}".format(self.name, self.cards))

    def reset(self, *, seed=None, return_info=False, options=None, ):
        # print("reset")
        self.cards = []
        self.waiting = False
        self.burnt = False
        self.sock.send(b"rese")
        for _ in range(2):
            self.burnt = self.draw_a_card()
        return np.pad(self.cards, (0, 12 - len(self.cards)))

    def get_BJ_score(self):
        return sum(self.cards)

    def clean_up(self):
        self.sock.send(b"stop")

    def ping(self):
        self.sock.send(b"ping")
        data = self.sock.recv(4)
        print(data.decode())


def main(env):
    episodes = 10000  # 20 blackjack
    totalWin=0
    for episode in range(1, episodes + 1):

        done = False
        score = 0

        while not done:
            action = env.action_space.sample()
            n_state, reward, done, info = env.step(action)
            score += reward

        print('Episode:{} Score:{}'.format(episode, score))
        if score == 1:
            totalWin+=1
        env.reset()
    print(totalWin)

#Small script so we can test the envirronement. It just takes random action. We can keep track of the number of wins to compare with the trained agent.
if __name__ == "__main__":
    env = BlackJack()
    main(env)

