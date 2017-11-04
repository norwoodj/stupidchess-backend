#!/usr/local/bin/python
import click

from jconfigure import configure
from com.johnmalcolmnorwood.stupidchess import LOGGER
from .api_utils import get_game_by_uuid
from .game_print_utils import print_scoreboard, print_board, print_captures


@click.command()
@click.option("--stupidchess", "-s", help="Stupidchess server to call (Default: stupidchess.johnmalcolmnorwood.com)", default="http://stupidchess.johnmalcolmnorwood.com")
@click.option("--username", "-u", default="veintitres")
@click.option("--password", "-p", default="password")
@click.argument("game_uuid")
def main(stupidchess, username, password, game_uuid):
    configure()
    LOGGER.info(f"Retrieving info on Game {game_uuid} from stupidchess server {stupidchess}")

    game = get_game_by_uuid(stupidchess, username, password, game_uuid)
    print_scoreboard(game)
    print_board(game)
    print_captures(game)


if __name__ == "__main__":
    main()
