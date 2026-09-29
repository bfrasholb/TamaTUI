import curses
from helper import add_tuple, add_tuple_wrap
import json
from time import sleep


class Render:
    def __init__(self, screen: curses.window, snake: object, food: object):
        # Renderer properties
        self.screen = screen
        self.max_yx = screen.getmaxyx()
        # Renderer Methods
        self.game, self.game_yx, self.lb, self.lb_yx, self.console, self.console_yx = self.init_pads(screen, snake, food)
        spawn_point = (self.game_yx[0] // 2, self.game_yx[1] // 2)
        self.snake = snake
        self.snake.points = [spawn_point, add_tuple((spawn_point[0] // 2, spawn_point[1] // 2), (0, 1))]
        self.last_key = -1

    ####################
    # Screens + Bounds #
    ####################

    @property
    def screen(self) -> curses.window:
        return self.__screen

    @screen.setter
    def screen(self, screen: curses.window) -> None:
        self.__screen = screen

    @property
    def max_yx(self) -> (int , int):
        return self.__max_yx

    @max_yx.setter
    def max_yx(self, bounds: (int, int)) -> None:
        self.__max_yx = bounds

    @property
    def game(self) -> curses.window:
        return self.__game

    @game.setter
    def game(self, window: curses.window) -> None:
        self.__game = window

    @property
    def game_yx(self) -> (int, int):
        return self.__game_yx

    @game_yx.setter
    def game_yx(self, bounds: (int, int)) -> None:
        self.__game_yx = bounds

    @property
    def lb(self) -> curses.window:
        return self.__lb

    @lb.setter
    def lb(self, window: curses.window) -> None:
        self.__lb = window

    @property
    def lb_yx(self) -> (int, int):
        return self.__lb_yx

    @lb_yx.setter
    def lb_yx(self, bounds: (int, int)) -> None:
        self.__lb_yx = bounds

    @property
    def console(self) -> curses.window:
        return self.__console

    @console.setter
    def console(self, window: curses.window) -> None:
        self.__console = window

    @property
    def console_yx(self) -> (int , int):
        return self.__console_yx

    @console_yx.setter
    def console_yx(self, bounds: (int, int)) -> None:
        self.__console_yx = bounds

    @property
    def snake(self) -> object:
        return self.__snake

    @snake.setter
    def snake(self, snake: object) -> None:
        self.__snake = snake

    @property
    def last_key(self) -> int:
        return self.__last_key

    @last_key.setter
    def last_key(self, key: int) -> None:
        self.__last_key = key

    #####################
    # Rendering Methods #
    #####################

    def init_pads(self, screen: curses.window, snake: object, food: object) -> [curses.window, (int, int)]:
        curses.start_color()  # allow color
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # create a red
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_RED)
        # Pad Size Initialisation
        lb_yx = (screen.getmaxyx())
        game_yx = (lb_yx[0] - 1, 2 * (lb_yx[0] - 1))
        console_yx = (lb_yx[0] - 2, lb_yx[1] - game_yx[1] - 27)

        #initialise the pads
        lb = curses.newpad(*lb_yx)
        console = curses.newpad(*console_yx)
        game = curses.newpad(*game_yx)

        # General Curses Settings
        curses.noecho() # Turn off key echoing
        curses.curs_set(0) # Set cursor visibility
        curses.cbreak() # Turn off buffered input

        # Set general curses settings for Game Pad
        game.keypad(True)
        game.clear()  # ensure blank canvas

        # Set general curses settings for leaderboard pad
        lb.keypad(False)
        lb.clear()

        curses.doupdate()

        return [game, game_yx, lb, lb_yx, console, console_yx]

    def refresh_pads(self, all_pads: bool) -> None:
        if all_pads:
            self.lb.noutrefresh(0, 0, 0, 0, *self.lb_yx)
        self.console.noutrefresh(0, 0, 1, (self.lb_yx[0] // 2) + self.game_yx[1] + 3, *self.max_yx)
        self.game.noutrefresh(0, 0, 1, ((self.lb_yx[0]) // 2), self.max_yx[0] - 2, self.max_yx[1])
        curses.doupdate()

    def menu(self, snake: object) -> None:
        menu_pos = (self.game_yx[0] // 2 - 5, self.game_yx[1] // 2 - 12)
        menu = [
            f"    Welcome to Snake!",
            #f"        Lines: {lb_y}",
            #f"      Columns: {lb_x}",
            f"            ",
            f"use the arrow keys to move",
            f"  press any key to start"
        ]

        for line in menu:
            self.game.addstr(*menu_pos, line, curses.color_pair(3))
            menu_pos = add_tuple(menu_pos, (1, 0))
        self.write_leaderboard()

        # Draw and Wait for input
        self.refresh_pads(True)
        self.game.nodelay(False)
        self.game.getch()
        self.game.nodelay(True)
        self.game.clear()
        self.console.clear()

    def player(self, snake: object) -> None:
        for point in snake.tail:
            self.game.addstr(point[0], 2 * point[1], '  ')
        if snake.orientation in ["East", "West"]:
            self.game.addstr(snake.points[0][0], 2 * snake.points[0][1], snake.get_head(), curses.color_pair(2))
        else:
            for index, point in enumerate(snake.points[:1]):
                self.game.addstr(point[0], 2 * point[1], snake.get_head()[index], curses.color_pair(2))
        for point in snake.points[1:]:
            self.game.addstr(point[0], 2 * point[1], '██', curses.color_pair(3))

    # def player(self, snake: object) -> None:
    #     for point in snake.tail:
    #         self.game.addstr(point[0], 2 * point[1], '  ', curses.color_pair(6))
    #     for point in snake.points:
    #         for i in range(0, 1):
    #             self.game.addstr(point[0] + i, 2 * point[1], '██', curses.color_pair(3))

    def food(self, food: object) -> None:
        self.game.addstr(food.yx[0], 2 * food.yx[1], '', curses.color_pair(2)) # 🐀

    def handle_input(self) -> None:
        key = self.game.getch()
        if key == -1:
            return

        while self.game.getch() == key:
            pass
        self.last_key = key

        match key:
            case 27:
                self.menu(self.snake)
            case curses.KEY_UP:
                self.snake.turn('North')
            case curses.KEY_DOWN:
                self.snake.turn('South')
            case curses.KEY_RIGHT:
                self.snake.turn('East')
            case curses.KEY_LEFT:
                self.snake.turn('West')
            case _:
                pass

    def game_over(self, snake: object) -> None:
        menu_pos = (self.game_yx[0] // 2) - 2, (self.game_yx[1] // 2) - 5
        self.game.addstr(*menu_pos, "Enter Username:")
        cursor_pos = add_tuple(menu_pos, (1, 0))
        self.game.nodelay(False)

        user_string = ""

        while True:
            self.game.addstr(*cursor_pos, user_string + f" " * (18 - len(user_string)))
            self.game.noutrefresh(0, 0, 1, ((self.lb_yx[0]) // 2), self.max_yx[0] - 2, self.max_yx[1])
            curses.doupdate()
            char = self.game.getkey()
            if char.isalpha() or char in ['KEY_BACKSPACE', '\n']:
                match char:
                    case '\n':
                        break
                    case 'KEY_BACKSPACE':
                        user_string = user_string[:-1]
                    case _:
                        if len(user_string) < 18:
                            user_string += char

        self.game.nodelay(True)
        self.game.clear()
        if user_string:
            self.save_score(user_string, snake.score)
        self.write_leaderboard()

    def save_score(self, username: str, score: int) -> None:
        try:
            with open("scores.json", "r") as f:
                scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []

        new_scores = [entry for entry in scores if entry['username'] != username]
        new_scores.append({"username": username, "score": score})
        new_scores.sort(key=lambda x: x["score"], reverse=True)
        with open("scores.json", "w") as f:
            json.dump(new_scores, f, indent=4)

    def write_leaderboard(self) -> None:
        # Fetch the leaderboard + Print Title
        self.lb.clear()
        try:
            with open("scores.json", "r") as f:
                scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []
        self.lb.addstr(1, 2, "Leaderboard:", curses.color_pair(5))

        for i, player in enumerate(scores):
            self.lb.addstr(3 + (2 * i), 3, f"{player['username']}:", curses.color_pair(3))
            self.lb.addstr(4 + (2 * i), 3, f"{player['score']}", curses.color_pair(3))
            i += 1

            # Render the border
        for i in range(0, self.lb_yx[1] - 1):
            self.lb.addstr(0, i, f'█', curses.color_pair(4))
            self.lb.addstr(self.lb_yx[0] - 1, i, '█', curses.color_pair(4))
        for i in range(0, self.lb_yx[0] - 1):
            self.lb.addstr(i, 0, '██', curses.color_pair(4))
            self.lb.addstr(i, self.lb_yx[1] - 2, '██', curses.color_pair(4))
            self.lb.addstr(i, ((self.lb_yx[0]) // 2) - 2, '██', curses.color_pair(4))
            self.lb.addstr(i, ((self.lb_yx[0]) // 2) + self.game_yx[1], '██', curses.color_pair(4))
        curses.doupdate()

    def score(self) -> None:
        # Print the player score aligned to the right of the game pad
        scoreboard = f"Score: {int(self.snake.score)}"
        self.console.addstr(0, 0, scoreboard, curses.color_pair(5))
        self.console.addstr(2, 0, f"Snake Multiplier:\n{self.snake.multiplier}\nSnake Orientation:\n{self.snake.orientation}\nSnake Points:\n{self.snake.points}\n", curses.color_pair(3))
