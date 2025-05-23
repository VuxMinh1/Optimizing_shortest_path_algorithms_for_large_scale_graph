import pygame
import math
import random
from queue import PriorityQueue

pygame.init()

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* and Bellman-Ford Pathfinding Visualization")

ROWS = 30
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165 ,0)
PURPLE = (128, 0, 128)
TURQUOISE = (64, 224, 208)

FONT = pygame.font.SysFont("comicsans", 15)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.weight = random.randint(1, 10)  # Random weight between 1 and 10

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        if self.color != BLACK and self.color != WHITE:
            text = FONT.render(str(self.weight), 1, BLACK)
            win.blit(text, (self.x + self.width//4, self.y + self.width//4))

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            r, c = self.row + d[0], self.col + d[1]
            if 0 <= r < self.total_rows and 0 <= c < self.total_rows:
                neighbor = grid[r][c]
                if not neighbor.is_barrier():
                    self.neighbors.append(neighbor)

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm_a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + neighbor.weight
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def algorithm_bellman_ford(draw, grid, start, end):
    distance = {node: float("inf") for row in grid for node in row}
    distance[start] = 0
    came_from = {}
    
    nodes = [node for row in grid for node in row if not node.is_barrier()]

    for _ in range(len(nodes) - 1):
        for node in nodes:
            for neighbor in node.neighbors:
                if distance[node] + neighbor.weight < distance[neighbor]:
                    distance[neighbor] = distance[node] + neighbor.weight
                    came_from[neighbor] = node
                    neighbor.make_open()
                    draw()

    if end in came_from:
        reconstruct_path(came_from, end, draw)
        end.make_end()
        return True

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # Left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # Right
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm_a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_b and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm_bellman_ford(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_r:
                    for row in grid:
                        for node in row:
                            if not node.is_barrier():
                                node.weight = random.randint(1, 10)

    pygame.quit()

main(WIN, WIDTH)
