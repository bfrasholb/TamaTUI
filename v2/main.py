#!/usr/bin/env python3

import curses
from classes import *
from render import Render
from helper import add_tuple
import time
import vlc
from gamesound import SnakeMusic

frames = 62
size = 12

def main(window: curses.window):
    food = Food(window.getmaxyx())
    snake = Snake(window.getmaxyx(), size, food)
    render = Render(window, snake, food)

    tracks = [
        (1, "./wavs/snake-soft.wav"),
        (2, "./wavs/snake-medium.wav"),
        (3, "./wavs/snake-ohshit.wav")
    ]
    background_music = SnakeMusic(tracks)
    time.sleep(2)
    while 1:
        background_music.stoptrack()
        background_music.playtrack(1)
        render.menu(snake)
        snake.respawn(render.game.getmaxyx(), size, food)
        loop_avg = []
        first_loop = 1
        loops = 0
        while snake.alive:
            snake.die()
            render.food(food)
            render.player(snake)
            render.score()

            ### Measure + Print FPS
            if not first_loop:
                end_time = time.time()
                loop_avg.append(end_time - start_time)
                start_time = time.time()
                total = 0
                for value in loop_avg:
                    total += value
                avg = total / len(loop_avg)
                fps = f"FPS: {int(1 / avg)}"
                render.console.addstr(
                    0,
                    render.console_yx[1] - len(fps),
                    fps,
                    curses.color_pair(5),
                )
            else:
                first_loop = 0
                start_time = time.time()

            render.refresh_pads(False)
            render.handle_input()
            time.sleep(1 / frames)
            if snake.alive == 0:
                render.game_over(snake)
            if loops == int(frames / (0.7 * snake.speed)):
                snake.move(food)
                loops = -1
            loops += 1

            if snake.multiplier >= 5:
                background_music.playtrack(2)
            if snake.multiplier >= 10:
                background_music.playtrack(3)


if __name__ == "__main__":
    curses.wrapper(main)  # Initialise and return the window to main()
