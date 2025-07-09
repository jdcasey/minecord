#!/bin/bash

podman run -ti --rm -p 25565:25565/tcp -p 25565:25565/udp -v ~/minecraft-world:/usr/local/mineserv/world:z mineserv:latest

