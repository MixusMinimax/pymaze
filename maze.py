import math
import os

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

    def load(self, bin):
        for i, b in enumerate(bin):
            w = self.size[0]
            self.field[(i * 2) // w][(i * 2) % w] = Node((b >> 4) & 0b1111)
            self.field[(i * 2 + 1) // w][(i * 2 + 1) % w] = Node(b & 0b1111)

    def save(self):
        l = math.ceil(self.size[0] * self.size[1] / 2)
        w = self.size[0]
        bin = bytearray()
        for i in range(l):
            bin.append(
                (self.field[(i * 2) // w][(i * 2) % w].to_bin() << 4) |
                self.field[(i * 2 + 1) // w][(i * 2 + 1) % w].to_bin()
            )
        return bin

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
    parser = argparse.ArgumentParser(description='Generate and display mazes')
    parser.add_argument('-i', '--input', action='store',
                        help='file that contains maze', metavar='FILE',
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-o', '--output', action='store',
                        help='file to write maze to', metavar='FILE',
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-s', '--size', action='store',
                        help='size of the maze, width and then height',
                        type=int, nargs='+', default=[1, 1])

    args = parser.parse_args()

    size = args.size
    maze = Maze(size)

    if args.input != None:
        with open(args.input, 'rb') as in_file:
            data = in_file.read()
            size = [data[0], data[1]]
            maze = Maze(size)
            maze.load(data[2:])
            print(maze)
    

    # Maze Generation

    if args.output != None:
        with open(args.output, 'wb') as out_file:
            data = bytearray(maze.size) + maze.save()
            out_file.write(data)


if __name__ == '__main__':
    main()
