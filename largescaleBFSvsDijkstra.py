import pygame
import sys
import random
import heapq

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 100, 100
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
pygame.display.set_caption("BFS vs Dijkstra Pathfinding")
clock = pygame.time.Clock()

# Grid setup
grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
weights = [[1 for _ in range(COLS)] for _ in range(ROWS)]
start = (0, 0)
end = (ROWS - 1, COLS - 1)
mode = "BFS"
animate = False

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
            clock.tick(60)

# Movement directions
moves = [(-1,0), (1,0), (0,-1), (0,1)]

def bfs():
    queue = [start]
    visited = set()
    came_from = {}
    while queue:
        current = queue.pop(0)
        if current == end:
            reconstruct_path(came_from, current)
            return
        visited.add(current)
        for dx, dy in moves:
            ni, nj = current[0] + dx, current[1] + dy
            if 0 <= ni < ROWS and 0 <= nj < COLS and grid[ni][nj] == 1:
                neighbor = (ni, nj)
                if neighbor not in visited and neighbor not in queue:
                    came_from[neighbor] = current
                    queue.append(neighbor)
                    if animate:
                        pygame.draw.rect(screen, BLUE, (nj * CELL_SIZE, ni * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        pygame.display.update()
                        clock.tick(60)

def dijkstra():
    pq = [(0, start)]
    distances = {start: 0}
    came_from = {}
    visited = set()
    while pq:
        cost, current = heapq.heappop(pq)
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
                new_cost = distances[current] + weights[ni][nj]
                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    came_from[neighbor] = current
                    heapq.heappush(pq, (new_cost, neighbor))
                    if animate:
                        pygame.draw.rect(screen, YELLOW, (nj * CELL_SIZE, ni * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        pygame.display.update()
                        clock.tick(60)

def randomize_map():
    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < 0.2:
                grid[i][j] = 0
                weights[i][j] = float('inf')
            else:
                grid[i][j] = 1
                weights[i][j] = random.randint(1, 6)

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

        elif pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            i, j = y // CELL_SIZE, x // CELL_SIZE
            if (i, j) != end:
                start = (i, j)

        elif pygame.mouse.get_pressed()[2]:
            x, y = pygame.mouse.get_pos()
            i, j = y // CELL_SIZE, x // CELL_SIZE
            if (i, j) != start:
                end = (i, j)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                mode = "BFS"
                bfs()
            elif event.key == pygame.K_d:
                mode = "Dijkstra"
                dijkstra()
            elif event.key == pygame.K_r:
                randomize_map()
            elif event.key == pygame.K_c:
                grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
                weights = [[1 for _ in range(COLS)] for _ in range(ROWS)]
            elif event.key == pygame.K_a:
                animate = not animate

pygame.quit()
sys.exit()
