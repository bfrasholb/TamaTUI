import curses
from player import Snake
import time
from helper import add_tuple
import json


def menu(game: curses.window, game_yx: tuple, leaderboard: curses.window, lb_yx: tuple, snake: object, tick_delay: int) -> None:
    menu_pos = (game_yx[0] // 2 - 5, game_yx[1] // 2 - 12)
    menu = [
        f"    Welcome to Snake!",
        #f"        Lines: {lb_y}",
        #f"      Columns: {lb_x}",
        f"            ",
        f"use the arrow keys to move",
        f"  press any key to start"
    ]

    for line in menu:
        game.addstr(*menu_pos, line)
        menu_pos = add_tuple(menu_pos, (1, 0))
    write_scores(leaderboard)

    # Draw and Wait for input
    refresh_pads(game, game_yx, leaderboard, lb_yx, snake, add_tuple(game_yx, lb_yx), True)
    game.nodelay(False)
    game.getch()
    game.nodelay(True)
#    game.timeout(tick_delay)
    game.clear()


def pause(window: curses.window, max_yx: tuple, leaderboard: curses.window, lb_yx: tuple, snake: object, tick_delay: int) -> None:
    #    window.clear()
    menu(window, max_yx, leaderboard, lb_yx, snake, tick_delay)

def game_over(game: curses.window, game_yx: int, leaderboard: curses.window, lb_yx: int, snake: object) -> None:
    menu_pos = (game_yx[0] // 2) - 2, (game_yx[1] // 2) - 5
    game.addstr(*menu_pos, "Enter Username:")
    cursor_pos = add_tuple(menu_pos, (1, 0))
    game.nodelay(False)

    user_string = ""

    while True:
        game.addstr(*cursor_pos, user_string + f" " * (18 - len(user_string)))
        game.noutrefresh(0, 0, *snake.yx, *add_tuple(lb_yx, game_yx))
        curses.doupdate()
        char = game.getkey()
        if char.isalpha() or char in ['KEY_BACKSPACE', '\n']:
            match char:
                case '\n':
                    break
                case 'KEY_BACKSPACE':
                    user_string = user_string[:-1]
                case _:
                    if len(user_string) < 18:
                        user_string += char

    game.nodelay(True)
    game.addstr(*menu_pos, f" " * 18)
    if user_string:
        save_score(user_string, snake.score)
    write_scores(leaderboard)

def save_score(username: str, score: int) -> None:
    try:
        with open("scores.json", "r") as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []

    scores.append({"username": username, "score": score})

    scores.sort(key=lambda x: x["score"], reverse=True)

    with open("scores.json", "w") as f:
        json.dump(scores, f, indent=4)

def write_scores(leaderboard: curses.window) -> None:
    try:
        with open("scores.json", "r") as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []
    leaderboard.addstr(1, 0, f"Leaderboard:")
    for i, player in enumerate(scores):
        leaderboard.addstr(3 + i, 0, f"{player['username']}: {player['score']}")
    curses.doupdate()


def handle_input(game: curses.window, game_yx: tuple, leaderboard: curses.window, lb_yx: tuple, snake: object, tick_delay: int, food: object) -> None:
    key = game.getch()

    match key:
        case 27:
            pause(game, game_yx, leaderboard, lb_yx, snake, tick_delay)
        case curses.KEY_UP:
            snake.turn('North')
        case curses.KEY_DOWN:
            snake.turn('South')
        case curses.KEY_RIGHT:
            snake.turn('East')
        case curses.KEY_LEFT:
            snake.turn('West')
        case curses.error:
            pass
        case _:
            pass


def score(game: curses.window, max_y: int, max_x: int, snake: object) -> None:
    scoreboard = f"Score: {int(snake.score)}"
    game.addstr(0, int(max_x - len(scoreboard)), scoreboard)


def player(game: curses.window, snake: object) -> None:
    # Render the body
    for index, point in enumerate(snake.points):
#        match index:
#            case 0:
#                game.addstr(*point, snake.get_head()[2][0], curses.color_pair(2))
#            case 1:
#                game.addstr(*point, snake.get_head()[2][1], curses.color_pair(2))
#            case 2:
#                game.addstr(*point, '█', curses.color_pair(3))
#            case _:
#                pass
        if index <= 1:
            game.addstr(*point, snake.get_head()[2][index], curses.color_pair(2))
        else:
            game.addstr(*point, snake.get_head()[2][2], curses.color_pair(3))

    for point in snake.tail:
        game.addstr(*point, ' ')

def food(game: curses.window, food: object) -> None:
    game.addstr(*food.yx, '', curses.color_pair(2))

def init_pads(window: curses.window, max_y: int, max_x: int, tick_delay: int) -> list[curses.window, tuple]:
    curses.curs_set(0) # disable cursor
    curses.start_color()  # allow color
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)  # create a green
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # create a red
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_YELLOW)

    # Pad Size Initialisation
    game_yx = (max_y - 1, (curses.COLS - 20))
    leaderboard_yx = (max_y - 1, max_x - game_yx[1])
    #initialise the pads
    leaderboard = curses.newpad(*leaderboard_yx)
    game = curses.newpad(*game_yx)

    # Set general curses settings for Game Pad
    game.keypad(True)
#    game.timeout(tick_delay)  # set tick speed
    game.clear()  # ensure blank canvas

    # Set general curses settings for leaderboard pad
    leaderboard.keypad(False)
#    leaderboard.timeout(False)
    leaderboard.clear()

    curses.doupdate()

    return [game, game_yx, leaderboard, leaderboard_yx]

def refresh_pads(game: curses.window, game_yx: tuple, leaderboard: curses.window, leaderboard_yx: tuple, snake: object, window_yx: tuple, all_pads: bool) -> None:
    if all_pads:
        leaderboard.noutrefresh(0, 0, 0, 0, *leaderboard_yx)
    game.noutrefresh(0, 0, *snake.yx, *window_yx)
    curses.doupdate()
