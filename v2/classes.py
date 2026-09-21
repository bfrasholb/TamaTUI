import curses
from helper import add_tuple, add_tuple_wrap
from random import randint


class Base:
    def __init__(self, bounds: tuple) -> None:
        self.yx = (curses.LINES // 2, curses.LINES // 2)
        self.max_yx = (bounds[0], bounds[0])

    @property
    def max_yx(self) -> tuple:
        return self.__max_yx

    @max_yx.setter
    def max_yx(self, bounds: (int, int)) -> None:
        self.__max_yx = bounds

    @property
    def yx(self) -> tuple:
        return self.__yx

    @yx.setter
    def yx(self, point) -> None:
        self.__yx = point

    def respawn(self) -> object:
        self.__init__()


class Food(Base):
    def __init__(self, bounds: tuple) -> None:
        super().__init__(bounds)
        self.yx = (randint(0, 34), randint(0, 34))

    def respawn(self, bounds: tuple) -> None:
        self.yx = (randint(0, bounds[0]), randint(0, bounds[1]))
        self.yx = add_tuple_wrap(self.yx, (0, 0), bounds)

class Snake(Base):
    def __init__(self, bounds: tuple, size: int, food: object) -> None:
        super().__init__(bounds)
        self.alive = 1
        self.multiplier = 1.0
        self.score = 0
        self.initial_size = size

        self.vectors = {'North': (-1, 0), 'South': (1, 0),
                        'East': (0, 1), 'West': (0, -1)}
        self.orientation = 'East'
        self.points = [self.yx]
        self.tail = []
        self.speed = 10

        self.build(food)

    ##############
    # Properties #
    ##############

    @property
    def alive(self) -> int:
        return self.__alive

    @alive.setter
    def alive(self, boolean: int) -> None:
        if boolean not in [0, 1]:
            raise ("Alive Boolean must be True or False")
        self.__alive = boolean

    @property
    def multiplier(self) -> float:
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, multiplier: float) -> None:
        self.__multiplier = multiplier

    @property
    def score(self) -> float:
        return self.__score

    @score.setter
    def score(self, score: float) -> None:
        self.__score = score

    @property
    def initial_size(self) -> int:
        return self.__initial_size

    @initial_size.setter
    def initial_size(self, initial_size: int) -> None:
        self.__initial_size = initial_size

    @property
    def speed(self) -> int:
        return self.__speed

    @speed.setter
    def speed(self, speed: int) -> None:
        self.__speed = speed

    ########################
    # Movements Properties #
    ########################

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
        self.__points = points

    @property
    def tail(self) -> list[tuple]:
        return self.__tail

    @tail.setter
    def tail(self, points: list(tuple)) -> None:
        self.__tail = points

    ###########
    # Methods #
    ###########

    def build(self, food: object) -> list:
        for _ in range(0, self.initial_size):
            self.move(food)

    def die(self) -> None:
        if set(self.points[1:]).intersection(self.points[:1]):
            self.alive = 0

    def get_new_head(self, direction: str) -> int:
        movement = self.vectors[direction]  # Get the movement vector
        current_head = self.points[0]  # Snake head remains single point based

        new_head = [add_tuple_wrap(current_head, movement, self.max_yx)]
        return new_head

    def move(self, food: object) -> int:
        """
        Vectorised orientation dependent movement
        Inserts the new_head at the front of the list, then trims the tail by 1
        """
        new_head = self.get_new_head(self.orientation)
        # Add the head
        self.points = new_head + self.points
        # If not building the snake, or eating the food, pop the tail
        if not len(self.points) < self.initial_size:
            if food.yx in new_head:
                food.respawn(self.max_yx)
                self.score += 1.0 * self.multiplier
                if not self.score % 5:  # Increases the multiplier by 1 per 5 foods eaten
                    self.multiplier += 1
                    self.speed += 5
            else:
                self.tail = self.points[-1:]
                self.points = self.points[:-1]

    def turn(self, direction: str) -> None:
        if set(self.points).intersection(set(self.get_new_head(direction))):
            return
        self.orientation = direction

    def respawn(self,  bounds: (int, int), size: int, food: object) -> None:
        self.__init__(bounds, size, food)

    def get_head(self):
        if self.orientation == 'North':
            return ['▕▏', '██'] # ▕▏▟▙▜▛
        if self.orientation == 'South':
            return ['▕▏', '██']
        if self.orientation == 'East':
            return '━━'
        if self.orientation == 'West':
            return '━━'
