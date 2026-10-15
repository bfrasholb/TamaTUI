#!/usr/bin/env python3

import curses  # Import a Terminal Handling Library
import player
import time
import rendering
from time import sleep


TICK_DELAY = 128

def launch(window: curses.window) -> int:
    init = rendering.init_pads(window, *window.getmaxyx(), TICK_DELAY)
    run(*init, window.getmaxyx())


def run(game: curses.window, game_yx: tuple, leaderboard: curses.window, leaderboard_yx: tuple, window_yx: tuple) -> None:
    food = player.Food(game_yx)
#    loading = player.Snake(game_yx, food, 100)
    snake = player.Snake(game_yx, food, 10, leaderboard_yx, TICK_DELAY)

    while (1):
        game.clear()
        leaderboard.clear()
        tick_delay = TICK_DELAY
        rendering.menu(game, game_yx, leaderboard, leaderboard_yx, snake, tick_delay)
        snake.respawn(food, 10, leaderboard_yx, tick_delay)

        # Game Loop
        while (snake.alive):
            # Snake Checks if it died first, then moves
            snake.die(game, *game_yx)
            tick_delay = snake.move(food, tick_delay)
#            game.timeout(tick_delay)
            # Rendering Game Menus
            rendering.score(game, *game_yx, snake)
            # Render Objects
            rendering.food(game, food)
            rendering.player(game, snake)
            # Draw the screen from buffer
            rendering.refresh_pads(game, game_yx, leaderboard, leaderboard_yx, snake, window_yx, False)
            # Check Input
            rendering.handle_input(game, game_yx, leaderboard, leaderboard_yx, snake, tick_delay, food)
            sleep(tick_delay/1000)

        if snake.alive == 0:
            rendering.game_over(game, game_yx, leaderboard, leaderboard_yx, snake)

    return (1)


if __name__ == '__main__':
    curses.wrapper(launch)
