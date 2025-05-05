import pygame
import sys
import random
import heapq

# ==== CONFIGURATION ====
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 100, 100
CELL_SIZE = WIDTH // COLS
FPS = 60

# ==== COLORS ====
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (180, 180, 180)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0)

# ==== INITIALIZE ====
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer: A* vs Bellman-Ford")
clock = pygame.time.Clock()

# ==== MAP ====
grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
weights = [[1 for _ in range(COLS)] for _ in range(ROWS)]
start = (0, 0)
end = (ROWS - 1, COLS - 1)
animate = False
algorithm = "A*"  # Default

def randomize_map():
    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < 0.2:
                grid[i][j] = 0  # obstacle
                weights[i][j] = float('inf')
            else:
                grid[i][j] = 1
                weights[i][j] = random.randint(1, 6)

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
                intensity = 255 - min(weights[i][j] * 30, 255)
                color = (intensity, intensity, 255)
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for i in range(ROWS):
        pygame.draw.line(screen, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
    for j in range(COLS):
        pygame.draw.line(screen, GREY, (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT))

def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        if current != start:
            pygame.draw.rect(screen, PURPLE, (current[1] * CELL_SIZE, current[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if animate:
            pygame.display.update()
            clock.tick(FPS)

# ==== ALGORITHMS ====

# Heuristic
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar():
    open_set = [(0 + heuristic(start, end), 0, start)]
    came_from = {}
    cost_so_far = {start: 0}
    visited = set()

    while open_set:
        _, current_cost, current = heapq.heappop(open_set)
        if current == end:
            reconstruct_path(came_from, current)
            return

        visited.add(current)
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            ni, nj = current[0] + dx, current[1] + dy
            if 0 <= ni < ROWS and 0 <= nj < COLS and grid[ni][nj] == 1:
                neighbor = (ni, nj)
                new_cost = current_cost + weights[ni][nj]
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, end)
                    heapq.heappush(open_set, (priority, new_cost, neighbor))
                    came_from[neighbor] = current
                    if animate:
                        pygame.draw.rect(screen, BLUE, (nj * CELL_SIZE, ni * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        pygame.display.update()
                        clock.tick(FPS)

def bellman_ford():
    distance = {start: 0}
    came_from = {}
    for _ in range(ROWS * COLS - 1):
        for i in range(ROWS):
            for j in range(COLS):
                if grid[i][j] == 1 and (i,j) in distance:
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < ROWS and 0 <= nj < COLS and grid[ni][nj] == 1:
                            neighbor = (ni, nj)
                            new_cost = distance[(i,j)] + weights[ni][nj]
                            if neighbor not in distance or new_cost < distance[neighbor]:
                                distance[neighbor] = new_cost
                                came_from[neighbor] = (i,j)
                                if animate:
                                    pygame.draw.rect(screen, YELLOW, (nj * CELL_SIZE, ni * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                                    pygame.display.update()
                                    clock.tick(FPS)
    if end in distance:
        reconstruct_path(came_from, end)

# ==== MAIN LOOP ====
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
            if pygame.mouse.get_pressed()[0]:
                if (i,j) != end:
                    start = (i,j)
            elif pygame.mouse.get_pressed()[2]:
                if (i,j) != start:
                    end = (i,j)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                randomize_map()
            elif event.key == pygame.K_c:
                grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
                weights = [[1 for _ in range(COLS)] for _ in range(ROWS)]
            elif event.key == pygame.K_a:
                animate = not animate
            elif event.key == pygame.K_1:
                algorithm = "A*"
                astar()
            elif event.key == pygame.K_2:
                algorithm = "Bellman"
                bellman_ford()

pygame.quit()
sys.exit()
