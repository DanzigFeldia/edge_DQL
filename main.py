from keras.layers import Dense, Activation, Flatten
from keras.models import Sequential
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import EpsGreedyQPolicy
from tensorflow.keras.optimizers import Adam

from customEnv import BlackJack

"""
Source:
https://www.section.io/engineering-education/building-a-reinforcement-learning-environment-using-openai-gym/
"""


def training():

    # Get the environment and extract the number of actions available
    env = BlackJack()
    nb_actions = env.action_space.n

    model = Sequential()
    # model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
    model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
    model.add(Dense(2))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))
    print(model.summary())

    policy = EpsGreedyQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,
                   target_model_update=1e-2,
                   policy=policy)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])

    # Okay, now it's time to learn something! We visualize the training here for show, but this slows down training quite a lot.
    #dqn.fit(env, nb_steps=5000, visualize=True, verbose=2)
    # We can save the weights for later uses
    #dqn.save_weights("weight.h5", overwrite=True)

    #If we already have weights
    dqn.load_weights("weight.h5")
    dqn.test(env, nb_episodes=10001, visualize=True)


if __name__ == "__main__":
    training()
