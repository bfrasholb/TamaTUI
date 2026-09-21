#!/usr/bin/env python3

import curses
from classes import *
from render import Render
from helper import add_tuple
import time

frames = 62
framerate = 1 / frames # Aim for 60 fps, overshoot for stability

def main(window: curses.window):
    food = Food(window.getmaxyx())
    snake = Snake(window.getmaxyx(), 12, food)
    render = Render(window, snake, food)

    while (1):
        render.menu(snake)
        snake.respawn(render.game.getmaxyx(), 12, food)
        loop_avg = []
        first_loop = 1
        loops = 0
        while (snake.alive):
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
                render.console.addstr(0, render.console_yx[1] - len(fps), fps, curses.color_pair(5))
            else:
                first_loop = 0
                start_time = time.time()

            render.refresh_pads(False)
            render.handle_input()
            time.sleep(framerate)
            if snake.alive == 0:
                render.game_over(snake)
            if loops == int(frames / (0.7 * snake.speed)):
                snake.move(food)
                loops = -1
            loops += 1

if __name__ == '__main__':
    curses.wrapper(main) # Initialise and return the window to main()
