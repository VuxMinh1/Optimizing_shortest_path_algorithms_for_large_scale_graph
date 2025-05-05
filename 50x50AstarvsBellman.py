import pygame
import sys
import random
import heapq
from collections import deque

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 50, 50
CELL_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
BLUE = (0, 120, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* vs Bellman-Ford Pathfinding")
clock = pygame.time.Clock()

# Grid setup
grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
weights = [[1 for _ in range(COLS)] for _ in range(ROWS)]
start = (0, 0)
end = (ROWS - 1, COLS - 1)
mode = "A*"
animate = False
path_to_draw = []

# Draw functions
def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE
            if (i, j) == start:
                color = GREEN
            elif (i, j) == end:
                color = RED
            elif grid[i][j] == 0:
                color = BLACK
            elif weights[i][j] > 1:
                intensity = 255 - min(weights[i][j] * 20, 255)
                color = (intensity, intensity, 255)
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for node in path_to_draw:
        if node != start and node != end:
            pygame.draw.rect(screen, PURPLE, (node[1] * CELL_SIZE, node[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for i in range(ROWS):
        pygame.draw.line(screen, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
    for j in range(COLS):
        pygame.draw.line(screen, GREY, (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT))

def reconstruct_path(came_from, current):
    global path_to_draw
    path = []
    while current in came_from:
        current = came_from[current]
        if current != start:
            path.append(current)

    if animate:
        for node in reversed(path):
            pygame.draw.rect(screen, PURPLE, (node[1] * CELL_SIZE, node[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.update()
            clock.tick(60)

    path_to_draw = path

# Movement directions
moves = [(-1,0), (1,0), (0,-1), (0,1)]

# A* Algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar():
    open_set = [(0 + heuristic(start, end), 0, start)]
    came_from = {}
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        if current == end:
            reconstruct_path(came_from, current)
            return
        if current in visited:
            continue
        visited.add(current)

        for dx, dy in moves:
            ni, nj = current[0] + dx, current[1] + dy
            if 0 <= ni < ROWS and 0 <= nj < COLS and grid[ni][nj] == 1:
                neighbor = (ni, nj)
                temp_g = g_score[current] + weights[ni][nj]
                if neighbor not in g_score or temp_g < g_score[neighbor]:
                    g_score[neighbor] = temp_g
                    f_score = temp_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, temp_g, neighbor))
                    came_from[neighbor] = current
                    if animate:
                        pygame.draw.rect(screen, BLUE, (nj * CELL_SIZE, ni * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        pygame.display.update()
                        clock.tick(60)

# Bellman-Ford Algorithm
def bellman_ford():
    distance = {start: 0}
    came_from = {}
    for _ in range(ROWS * COLS - 1):
        for i in range(ROWS):
            for j in range(COLS):
                if grid[i][j] == 0:
                    continue
                for dx, dy in moves:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < ROWS and 0 <= nj < COLS and grid[ni][nj] == 1:
                        current = (i, j)
                        neighbor = (ni, nj)
                        weight = weights[ni][nj]
                        if current in distance:
                            new_dist = distance[current] + weight
                            if neighbor not in distance or new_dist < distance[neighbor]:
                                distance[neighbor] = new_dist
                                came_from[neighbor] = current
                                if animate:
                                    pygame.draw.rect(screen, YELLOW, (nj * CELL_SIZE, ni * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                                    pygame.display.update()
                                    clock.tick(60)
    if end in came_from:
        reconstruct_path(came_from, end)

def randomize_map():
    global start, end, path_to_draw
    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < 0.2:
                grid[i][j] = 0
                weights[i][j] = float('inf')
            else:
                grid[i][j] = 1
                weights[i][j] = random.randint(1, 6)
    start = (0, 0)
    end = (ROWS - 1, COLS - 1)
    path_to_draw = []

# Main loop
randomize_map()
running = True
while running:
    screen.fill(WHITE)
    draw_grid()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            i, j = y // CELL_SIZE, x // CELL_SIZE
            if event.button == 1 and grid[i][j] == 1:
                start = (i, j)
                path_to_draw = []
                print("Start set to:", start)
            elif event.button == 3 and grid[i][j] == 1:
                end = (i, j)
                path_to_draw = []
                print("End set to:", end)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mode = "A*"
                astar()
            elif event.key == pygame.K_b:
                mode = "Bellman"
                bellman_ford()
            elif event.key == pygame.K_r:
                randomize_map()
            elif event.key == pygame.K_c:
                grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
                weights = [[1 for _ in range(COLS)] for _ in range(ROWS)]
                path_to_draw = []
            elif event.key == pygame.K_z:
                animate = not animate

pygame.quit()
sys.exit()
