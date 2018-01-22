#!/usr/bin/env python
import requests


def get_game_by_uuid(stupidchess_server, username, password, game_uuid):
    res = requests.get(f"{stupidchess_server}/api/game/{game_uuid}", auth=(username, password))
    res.raise_for_status()
    return res.json()




