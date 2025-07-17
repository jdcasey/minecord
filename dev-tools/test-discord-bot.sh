#!/bin/bash

podman run -ti --rm --name minecord \
  -v $HOME/.config/minecord.yaml:/home/minecord/.config/minecord.yaml:ro,z \
  -v $HOME/.config/minecord-admins.yaml:/home/minecord/.config/minecord-admins.yaml:z \
  minecord:local

