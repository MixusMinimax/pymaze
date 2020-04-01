import pygame
import math

pygame.init()


class Window:

    def open(self, size, max_window_size):
        cellSizeX = max_window_size[0] // size[0]
        cellSizeY = max_window_size[1] // size[1]
        self.cell_size = min(cellSizeX, cellSizeY)
        del cellSizeX, cellSizeY
        self.size = size
        self.window_size = [size[0] * self.cell_size, size[1] * self.cell_size]
        self.wall_thickness = max(1, self.cell_size // 16)
        self.display = pygame.display.set_mode(self.window_size)

    def update(self, maze):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                pygame.quit()

        cs = self.cell_size
        wt = self.wall_thickness

        updated = 0

        for y in range(maze.size[1]):
            for x in range(maze.size[0]):
                if maze.changed[y][x]:
                    maze.changed[y][x] = False
                    updated += 1
                    rx = x * self.cell_size
                    ry = y * self.cell_size
                    node = maze.field[y][x]
                    if node.to_bin():
                        pygame.draw.rect(self.display, (230,)
                                        * 3, (rx, ry, cs, cs))
                    else:
                        pygame.draw.rect(
                            self.display, (100, 20, 100), (rx, ry, cs, cs))
                    c = (30, 20, 40)
                    if not node.north:
                        pygame.draw.rect(self.display, c, (rx, ry, cs, wt))
                    if not node.east:
                        pygame.draw.rect(
                            self.display, c, (rx + cs - wt, ry, wt, cs))
                    if not node.south:
                        pygame.draw.rect(
                            self.display, c, (rx, ry + cs - wt, cs, wt))
                    if not node.west:
                        pygame.draw.rect(self.display, c, (rx, ry, wt, cs))
                    pygame.draw.rect(self.display, c, (rx, ry, wt, wt))
                    pygame.draw.rect(self.display, c, (rx + cs - wt, ry, wt, wt))
                    pygame.draw.rect(
                        self.display, c, (rx + cs - wt, ry + cs - wt, wt, wt))
                    pygame.draw.rect(self.display, c, (rx, ry + cs - wt, wt, wt))

        if updated:
            print(f'Updated: {updated}')
        pygame.display.update()
        return True
