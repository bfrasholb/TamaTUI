import curses
from random import randint
import time
from helper import add_tuple


class Food:

    def __init__(self, game_yx: tuple) -> None:
        self.maxyx = game_yx
        self.yx = (randint(0, (game_yx[0] - 3)), (randint(0, game_yx[1] - 3)))

    #################
    # Game Mechanic #
    #################

    def respawn(self, game_yx: tuple) -> object:
        self.__init__(game_yx)

    ###############
    # Coordinates #
    ###############

    @property
    def maxyx(self) -> tuple:
        return self.__maxyx

    @maxyx.setter
    def maxyx(self, game_yx: tuple) -> None:
        self.__maxyx = game_yx

    @property
    def yx(self) -> tuple:
        return self.__yx

    @yx.setter
    def yx(self, coordinate: tuple) -> None:
        """
        Points must be within range of the Window
        """
        self.__yx = coordinate


class Snake:
    def __init__(self, game_yx: tuple, food: object, size: int, leaderboard_yx: tuple, tick_delay: int) -> None:
        self.maxyx = game_yx
        self.alive = 1
        self.yx = (0, leaderboard_yx[1])
        self.vectors = {'North': (-1, 0), 'South': (1, 0),
                        'East': (0, 1), 'West': (0, -1)}
        self.orientation = 'East'
        self.multiplier = 1.0
        self.score = 0
        self.points = [(game_yx[0] // 2, game_yx[1] // 2), add_tuple((game_yx[0] // 2, game_yx[1] // 2), (0, 1))]
        self.initial_size = size
        self.build(food, tick_delay)

    ##################
    # Game Mechanics #
    ##################
    @property
    def maxyx(self) -> tuple:
        return self.__maxyx

    @maxyx.setter
    def maxyx(self, game_yx: tuple) -> None:
        self.__maxyx = game_yx

    @property
    def alive(self) -> int:
        return self.__alive

    @alive.setter
    def alive(self, boolean: int) -> None:
        if boolean not in [0, 1]:
            raise ("Alive Boolean must be True or False")
        self.__alive = boolean

    @property
    def initial_size(self) -> int:
        return self.__initial_size

    @initial_size.setter
    def initial_size(self, initial_size: int) -> None:
        self.__initial_size = initial_size

    @property
    def score(self) -> float:
        return self.__score

    @score.setter
    def score(self, score: float) -> None:
        self.__score = score

    @property
    def multiplier(self) -> float:
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, multiplier: float) -> None:
        self.__multiplier = multiplier

    def respawn(self, food: object, initial_size: int, leaderboard_yx: tuple, tick_delay: int) -> None:
        self.__init__(self.maxyx, food, initial_size, leaderboard_yx, tick_delay)

    def die(self, game: curses.window, max_y: int, max_x: int) -> None:
        if set(self.points[1:]).intersection(self.points[:1]):
            self.alive = 0

    def build(self, food: object, tick_delay: int) -> list:
        for _ in range(0, self.initial_size):
            self.move(food, tick_delay)

    ############
    # Movement #
    ############

    @property
    def yx(self) -> tuple:
        return self.__yx

    @yx.setter
    def yx(self, coordinate: tuple) -> None:
        self.__yx = coordinate

    @property
    def vectors(self) -> dict:
        return self.__vectors

    @vectors.setter
    def vectors(self, vectors: dict) -> None:
        self.__vectors = vectors

    @property
    def orientation(self) -> str:
        return self.__orientation

    @orientation.setter
    def orientation(self, direction: str) -> None:
        """
        Default Orientation is North, Initial is South
        """
        if direction not in self.vectors.keys():
            self.__orientation = 'North'
        self.__orientation = direction

    @property
    def points(self) -> list:
        return self.__points

    @points.setter
    def points(self, points: list) -> None:
        """
        Receives a list of points not individual!
        Modulo ensures strict range of (0, x) which causes screen wrapping
        """
        self.__points = [
            (
                y % (self.maxyx[0] - 2),
                x % (self.maxyx[1] - 2)
            )
            for (y, x) in points
        ]

    @property
    def tail(self) -> list[tuple]:
        return self.__tail

    @tail.setter
    def tail(self, points: list(tuple)) -> None:
        self.__tail = points

    def move(self, food: object, tick_delay: int) -> int:
        movement = self.vectors[self.orientation]  # Get the movement vector
        current_head = self.points[0]  # Snake head remains single point based

        match self.orientation:
            case "North":
                dimension = self.vectors["East"]
            case "South":
                dimension = self.vectors["West"]
            case "East":
                dimension = self.vectors["North"]
            case "West":
                dimension = self.vectors["South"]

        new_head = [add_tuple(current_head, movement)]
        return self.exec_move(food, tick_delay, new_head)

    def exec_move(self, food: object, tick_delay: int, new_head: object) -> int:
        """
        Vectorised orientation dependent movement
        Inserts the new_head at the front of the list, then trims the tail by 1
        """
        # Add the head
        self.points = new_head + self.points
        # If no building the snake, or eating the food, pop the tail
        if not len(self.points) < self.initial_size:
            if food.yx in new_head:
                food.respawn(tuple(self.maxyx))
                self.score += 1.0 * self.multiplier
                if not self.score % 10:  # Increases the multiplier by 1 per 5 foods eaten
                    self.multiplier += 1
                    return int((tick_delay / 2))
            else:
                self.tail = self.points[-1:]
                self.points = self.points[:-1]
        return tick_delay

    def turn(self, direction: str) -> None:
        match direction:
            case 'North':
                if self.orientation == 'South':
                    return
            case 'South':
                if self.orientation == 'North':
                    return
            case 'East':
                if self.orientation == 'West':
                    return
            case 'West':
                if self.orientation == 'East':
                    return
        self.orientation = direction

    #############
    # Rendering #
    #############

    def get_head(self):

        if self.orientation == 'North':
            return [*self.points[0], ' V██']
        if self.orientation == 'South':
            return [*self.points[0], ' ^██']
        if self.orientation == 'East':
            return [*self.points[0], '<-█']
        if self.orientation == 'West':
            return [*self.points[0], '>-█']
