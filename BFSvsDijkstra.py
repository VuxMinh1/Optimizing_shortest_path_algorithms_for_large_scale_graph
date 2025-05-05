import pygame
import sys
from queue import PriorityQueue, Queue

WIDTH = 600
ROWS = 30

pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("BFS vs Dijkstra Pathfinding")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

class Node:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.size = size
        self.color = WHITE
        self.neighbors = []
        self.g = float('inf')  # for Dijkstra

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE
        self.g = float('inf')

    def make_start(self):
        self.color = GREEN

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = BLUE

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = YELLOW

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < ROWS and 0 <= c < ROWS and not grid[r][c].is_barrier():
                self.neighbors.append(grid[r][c])

def make_grid():
    grid = []
    size = WIDTH // ROWS
    for i in range(ROWS):
        grid.append([Node(i, j, size) for j in range(ROWS)])
    return grid

def draw_grid(win):
    gap = WIDTH // ROWS
    for i in range(ROWS):
        pygame.draw.line(win, GREY, (0, i*gap), (WIDTH, i*gap))
        pygame.draw.line(win, GREY, (i*gap, 0), (i*gap, WIDTH))

def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win)
    pygame.display.update()

def get_clicked_pos(pos):
    gap = WIDTH // ROWS
    return pos[0] // gap, pos[1] // gap

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def bfs(draw, grid, start, end):
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {start}

    while not queue.empty():
        current = queue.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.put(neighbor)
                neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False

def dijkstra(draw, grid, start, end):
    count = 0
    pq = PriorityQueue()
    start.g = 0
    pq.put((0, count, start))
    came_from = {}

    while not pq.empty():
        _, _, current = pq.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g = current.g + 1
            if temp_g < neighbor.g:
                came_from[neighbor] = current
                neighbor.g = temp_g
                count += 1
                pq.put((neighbor.g, count, neighbor))
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False

def main(win):
    grid = make_grid()
    start = end = None
    running = True

    while running:
        draw(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:  # Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                for row in grid:
                    for node in row:
                        node.update_neighbors(grid)

                if event.key == pygame.K_b and start and end:
                    bfs(lambda: draw(win, grid), grid, start, end)

                if event.key == pygame.K_d and start and end:
                    dijkstra(lambda: draw(win, grid), grid, start, end)

                if event.key == pygame.K_c:
                    start = end = None
                    grid = make_grid()

main(WIN)
