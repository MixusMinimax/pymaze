# pymaze
maze generator and viewer using pygame

### Demo (100x100)

![100x100 Demo](https://i.imgur.com/S7hsELS.gif)

```
usage: maze.py [-h] [-i FILE] [-o FILE] [-s SIZE [SIZE ...]] [-w] [-g] [-r REPETITIONS]

Generate and display mazes

optional arguments:
  -h, --help            show this help message and exit
  -i FILE, --input FILE
                        file that contains maze
  -o FILE, --output FILE
                        file to write maze to
  -s SIZE [SIZE ...], --size SIZE [SIZE ...]
                        size of the maze, width and then height
  -w, --window          draw maze with pygame
  -g, --generate        generate a random maze
  -r REPETITIONS, --repetitions REPETITIONS
                        repetitions per frame
```

### Info

* Uses Depth-First Search with randomized push order to populate the maze
* pymaze uses a custom binary format to store mazes: 4 bits for each cell, each bit defines if the cell is connected to the neigbor in that direction (north, east, south, west)
* If you choose to output the generated maze, and enable window mode, and happen to close the window during the maze's generation, pymaze will finish the maze in the background and writes to the file.
* If you close the window without having specified an output file, the generation will cancel as it's no longer needed.
* pygame is slow, so for big mazes simply don't include the `-w` flag. Another option is the `-r` flag, which defines how many steps to calculate per frame.

### Example Usages

#### Read from a file and display on screen:

```sh
python maze.py --window --input example1.maze
python maze.py -w -i example1.maze
python maze.py -wi example1.maze
```

#### Generate a 128x64 maze, and output it to a file:

```sh
python maze.py --generate --size 128 64 --output example2.maze
python maze.py -g -s 128 64 -o example2.maze
python maze.py -gs 128 64 -o example2.maze
```

#### Generate a 64x64 maze and view its generation:

```sh
python maze.py --window --generate --size 64 64
python maze.py -w -g -s 64 64
python maze.py -wgs 64 64
```

#### Generate a 256x256 maze, but to speed up the process, calculate 8 steps per frame:

```sh
python maze.py --window --generate --size 256 256 --repetitions 8
python maze.py -w -g -s 256 256 -r 8
python maze.py -wgs 256 256 -r 8
```