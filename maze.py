import math
import os
import random
import threading
import time

# Maze


class Node:

    def __init__(self, bin):
        self.north = bool(bin & 0b1000)
        self.east = bool(bin & 0b0100)
        self.south = bool(bin & 0b0010)
        self.west = bool(bin & 0b0001)

    def to_bin(self):
        return (
            (0b1000 if self.north else 0) |
            (0b0100 if self.east else 0) |
            (0b0010 if self.south else 0) |
            (0b0001 if self.west else 0)
        )

    def __str__(self):
        b = self.to_bin()
        return f'{b:04b}'


class Maze:

    def __init__(self, size):
        self.size = size
        self.field = [[0] * size[0]] * size[1]
        self.field = [[Node(0) for y in l] for l in self.field]
        self.changed = [[True] * size[0]] * size[1]
        self.changed = [[y for y in l] for l in self.field]

    def load(self, bin):
        for i, b in enumerate(bin):
            w = self.size[0]
            self.field[(i * 2) // w][(i * 2) % w] = Node((b >> 4) & 0b1111)
            if (i * 2 + 1) < (w * self.size[1]):
                self.field[(i * 2 + 1) // w][(i * 2 + 1) %
                                             w]=Node(b & 0b1111)

    def save(self):
        l=math.ceil(self.size[0] * self.size[1] / 2)
        w=self.size[0]
        bin=bytearray()
        for i in range(l):
            bin.append(
                (self.field[(i * 2) // w][(i * 2) % w].to_bin() << 4) |
                ((self.field[(i * 2 + 1) // w][(i * 2 + 1) %
                                               w].to_bin()) if (i * 2 + 1) < (self.size[0] * self.size[1]) else 0)
            )
        return bin

    def generate(self, start: Node):
        stack=[(start, None)]
        visited=[]
        previous=None

        while len(stack) > 0:
            next=stack.pop()
            if next[0] in visited:
                continue
            visited.append(next[0])
            self.changed[next[0][1]][next[0][0]]=True
            previous=next[1]
            if previous:
                self.changed[previous[1]][previous[0]]=True
                if previous[0] < next[0][0]:
                    self.get(previous).east=True
                    self.get(next[0]).west=True
                elif previous[0] > next[0][0]:
                    self.get(previous).west=True
                    self.get(next[0]).east=True
                elif previous[1] < next[0][1]:
                    self.get(previous).south=True
                    self.get(next[0]).north=True
                elif previous[1] > next[0][1]:
                    self.get(previous).north=True
                    self.get(next[0]).south=True
            neighbors=[
                ((next[0][0] - 1, next[0][1]), next[0]),
                ((next[0][0] + 1, next[0][1]), next[0]),
                ((next[0][0], next[0][1] - 1), next[0]),
                ((next[0][0], next[0][1] + 1), next[0])
            ]
            neighbors=[p for p in neighbors if self.in_bounds(
                p[0]) and p[0] not in visited]
            random.shuffle(neighbors)
            [stack.append(p) for p in neighbors]
            yield

    def in_bounds(self, pos):
        x=pos[0]
        y=pos[1]
        return x >= 0 and y >= 0 and x < self.size[0] and y < self.size[1]

    def get(self, pos):
        x=pos[0]
        y=pos[1]
        if not self.in_bounds(pos):
            raise AttributeError
        return self.field[y][x]

    def __str__(self):
        return '\n'.join([' '.join([f'{str(n)}' for n in l]) for l in self.field])


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error(f'The file {arg} does not exist!')
    else:
        return arg  # return path


def main():
    # Parse arguments
    import argparse
    parser=argparse.ArgumentParser(description='Generate and display mazes')
    parser.add_argument('-i', '--input', action='store',
                        help='file that contains maze', metavar='FILE',
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-o', '--output', action='store',
                        help='file to write maze to', metavar='FILE',
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-s', '--size', action='store',
                        help='size of the maze, width and then height',
                        type=int, nargs='+', default=[1, 1])
    parser.add_argument('-w', '--window', action='store_true',
                        help='draw maze with pygame',
                        default=False)
    parser.add_argument('-g', '--generate', action='store_true',
                        help='generate a random maze',
                        default=False)

    args=parser.parse_args()

    size=args.size
    maze=Maze(size)

    if args.input != None:
        with open(args.input, 'rb') as in_file:
            data=in_file.read()
            size=[data[0], data[1]]
            maze=Maze(size)
            maze.load(data[2:])

    # Display
    if args.window:
        from window import Window
        window=Window()
        window.open(size, (1500, 900))

    maze_generator=None
    if not args.input and args.generate:
        maze_generator=maze.generate((0, 0))

    running=True
    while running:
        if args.window:
            running=window.update(maze)

        if maze_generator:
            try:
                maze_generator.__next__()
            except StopIteration:
                maze_generator=None
        # time.sleep(.1)

        if not args.window and not maze_generator:
            running=False

    if args.output != None:
        with open(args.output, 'wb') as out_file:
            data=bytearray(maze.size) + maze.save()
            out_file.write(data)


if __name__ == '__main__':
    main()
