# Using DQN learning on a remote server-based multiplayer game.
This is an implementation of a trained agent playing a competitive multiplayer game. If you want to see how it was implemented, please follow the "tutorial.pdf" files.

Requirements
======
This uses Python 3.8.10 and the following libraries:
numpy:1.22.4
tensorflow:2.9.1
keras:2.9.0
gym:0.24.1
keras-rl2:1.0.5

Using Docker
======
You can make a docker container using the Dockerfile.
Alternatively, you may pull it from the hub using the following commands:

```
docker pull feldia/edge_dqn:v1
```
You can then create and enter a container from the docker image with the following commands:
```
docker run -it --rm --name=yourname -p ip:port:port/tcp edge_dqn:v1 /bin/bash
```
There, you may start the server and the main. You may need to change the ips in the source files.