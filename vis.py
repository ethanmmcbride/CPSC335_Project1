import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Algorithm Efficiency Comparison')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont('Arial', 20)

# Algorithm names
algorithms = ['Bubble Sort', 'Merge Sort', 'Quick Sort', 'Radix Sort', 'Linear Search']

# Dummy sorting functions with timing
def bubble_sort(arr):
    start_time = time.time()
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return time.time() - start_time

def merge_sort(arr):
    start_time = time.time()
    # Merge sort code
    return time.time() - start_time

def quick_sort(arr):
    start_time = time.time()
    # Quick sort code
    return time.time() - start_time

def radix_sort(arr):
    start_time = time.time()
    # Radix sort code
    return time.time() - start_time

def linear_search(arr, target):
    start_time = time.time()
    for i in range(len(arr)):
        if arr[i] == target:
            break
    return time.time() - start_time

# Bar graph drawing function
def draw_bar_graph(times):
    screen.fill(WHITE)
    max_time = max(times)
    bar_width = width // len(times)
    for i, time_taken in enumerate(times):
        bar_height = (time_taken / max_time) * (height - 50)
        pygame.draw.rect(screen, BLUE, [i * bar_width, height - bar_height, bar_width - 10, bar_height])
        # Draw the algorithm name
        text = font.render(algorithms[i], True, BLACK)
        screen.blit(text, (i * bar_width, height - 30))
        # Draw the time taken
        time_text = font.render(f'{time_taken:.4f}s', True, BLACK)
        screen.blit(time_text, (i * bar_width, height - bar_height - 20))
    pygame.display.update()

# Main function
def main():
    running = True
    clock = pygame.time.Clock()

    # Generate a random array
    arr = random.sample(range(1, 100), 50)

    # Times taken by each algorithm
    times = [0] * len(algorithms)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Run algorithms and record times
        times[0] = bubble_sort(arr[:])
        times[1] = merge_sort(arr[:])
        times[2] = quick_sort(arr[:])
        times[3] = radix_sort(arr[:])
        times[4] = linear_search(arr[:], random.choice(arr))

        # Draw the bar graph with updated times
        draw_bar_graph(times)

        # Control the frame rate
        clock.tick(1)  # Update every second

    pygame.quit()

if __name__ == "__main__":
    main()



