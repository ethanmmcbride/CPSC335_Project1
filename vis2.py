import pygame
import sys
import random
import time
import math
import multiprocessing

# Algorithm names
ALGORITHMS = ["Bubble Sort", "Merge Sort", "Quick Sort", "Radix Sort", "Linear Search"]

# Fonts, Colors, and Pygame initialization will be moved inside the main function.

# Checkbox class
class Checkbox:
    def __init__(self, x, y, text):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.checked = False
        self.text = text

    def draw(self, surface, SMALL_FONT, BLACK):
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        if self.checked:
            pygame.draw.line(surface, BLACK, (self.rect.left, self.rect.top), (self.rect.right, self.rect.bottom), 2)
            pygame.draw.line(surface, BLACK, (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.top), 2)
        text_surface = SMALL_FONT.render(self.text, True, BLACK)
        surface.blit(text_surface, (self.rect.right + 10, self.rect.top - 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked

# InputBox class
class InputBox:
    def __init__(self, x, y, w, h, FONT, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (0, 0, 0)  # BLACK
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.FONT = FONT

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle the active state if the user clicked on the input box
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (255, 100, 100) if self.active else (0, 0, 0)  # RED or BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass  # Do nothing on enter
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.isdigit():
                    self.text += event.unicode
                # Re-render the text
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def draw(self, surface):
        # Blit the text
        surface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect
        pygame.draw.rect(surface, self.color, self.rect, 2)

# Button class
class Button:
    def __init__(self, x, y, w, h, text, FONT):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (100, 100, 255)  # BLUE
        self.text = text
        self.FONT = FONT

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.FONT.render(self.text, True, (255, 255, 255))  # WHITE
        surface.blit(text_surface, (self.rect.x + (self.rect.w - text_surface.get_width()) / 2,
                                    self.rect.y + (self.rect.h - text_surface.get_height()) / 2))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# Sorting and searching algorithms
def bubble_sort(arr):
    n = len(arr)
    start_time = time.perf_counter()
    for i in range(n):
        swapped = False  # Optimization to stop if the array is sorted
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    end_time = time.perf_counter()
    return end_time - start_time

def iterative_merge_sort(arr):
    start_time = time.perf_counter()
    width = 1
    n = len(arr)
    while width < n:
        l = 0
        while l < n:
            r = min(l + (width * 2 - 1), n - 1)
            m = min(l + width - 1, n - 1)
            if m < r:
                merge(arr, l, m, r)
            l += width * 2
        width *= 2
    end_time = time.perf_counter()
    return end_time - start_time

def merge(arr, l, m, r):
    left = arr[l:m+1]
    right = arr[m+1:r+1]
    i = j = 0
    k = l
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i +=1
        else:
            arr[k] = right[j]
            j +=1
        k +=1
    while i < len(left):
        arr[k] = left[i]
        i +=1
        k +=1
    while j < len(right):
        arr[k] = right[j]
        j +=1
        k +=1

def iterative_quick_sort(arr):
    start_time = time.perf_counter()
    size = len(arr)
    stack = []
    stack.append((0, size - 1))

    while stack:
        pos = stack.pop()
        low, high = pos[0], pos[1]
        pivot = partition(arr, low, high)
        if pivot - 1 > low:
            stack.append((low, pivot - 1))
        if pivot + 1 < high:
            stack.append((pivot + 1, high))
    end_time = time.perf_counter()
    return end_time - start_time

def partition(arr, low, high):
    pivot = arr[high]
    i = low -1
    for j in range(low, high):
        if arr[j] <= pivot:
            i+=1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high]= arr[high], arr[i+1]
    return i+1

def radix_sort(arr):
    start_time = time.perf_counter()
    max1 = max(arr)
    exp =1
    while max1//exp >0:
        counting_sort(arr, exp)
        exp *=10
    end_time = time.perf_counter()
    return end_time - start_time

def counting_sort(arr, exp1):
    n = len(arr)
    output = [0]*n
    count = [0]*10
    for i in range(0, n):
        index = arr[i]//exp1
        count[(index)%10] +=1
    for i in range(1,10):
        count[i] += count[i-1]
    i = n-1
    while i>=0:
        index = arr[i]//exp1
        output[count[(index)%10] -1] = arr[i]
        count[(index)%10] -=1
        i -=1
    for i in range(0,len(arr)):
        arr[i]=output[i]

def linear_search(arr, target):
    start_time = time.perf_counter()
    for item in arr:
        if item == target:
            break
    end_time = time.perf_counter()
    return end_time - start_time

# Function to run algorithms in separate processes
def run_algorithm(alg_name, array_size, seed):
    # Generate the same array for each algorithm using the seed
    random.seed(seed)
    array = [random.randint(1, 1000000) for _ in range(array_size)]
    arr_copy = array.copy()
    try:
        if alg_name == "Bubble Sort":
            runtime = bubble_sort(arr_copy)
        elif alg_name == "Merge Sort":
            runtime = iterative_merge_sort(arr_copy)
        elif alg_name == "Quick Sort":
            runtime = iterative_quick_sort(arr_copy)
        elif alg_name == "Radix Sort":
            runtime = radix_sort(arr_copy)
        elif alg_name == "Linear Search":
            target = random.choice(arr_copy)
            runtime = linear_search(arr_copy, target)
        return (alg_name, runtime)
    except MemoryError:
        return (alg_name, "MemoryError")
    except RecursionError:
        return (alg_name, "RecursionError")

def main():
    # Initialize pygame
    pygame.init()
    # Set up display
    WIDTH, HEIGHT = 900, 700  # Window dimensions
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sorting Algorithms Runtime Comparison")
    # Fonts
    FONT = pygame.font.SysFont('Arial', 24)
    SMALL_FONT = pygame.font.SysFont('Arial', 18)
    X_AXIS_FONT = pygame.font.SysFont('Arial', 16)  # Smaller font for x-axis labels
    # Colors
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    LIGHT_GRAY = (230, 230, 230)
    BLACK = (0, 0, 0)
    BLUE = (100, 100, 255)
    GREEN = (100, 255, 100)
    RED = (255, 100, 100)
    YELLOW = (255, 255, 100)

    clock = pygame.time.Clock()
    checkboxes = []
    for idx, alg in enumerate(ALGORITHMS):
        checkbox = Checkbox(50, 50 + idx * 40, alg)
        checkboxes.append(checkbox)
    input_box = InputBox(50, 50 + len(ALGORITHMS) * 40 + 30, 150, 40, FONT)
    go_button = Button(220, 50 + len(ALGORITHMS) * 40 + 30, 100, 40, "Go", FONT)
    runtimes = {}
    warning_messages = []
    processing = False
    async_results = {}
    seed = None
    pool = None

    running = True
    while running:
        window.fill(WHITE)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for checkbox in checkboxes:
                checkbox.handle_event(event)
            input_box.handle_event(event)
            if go_button.is_clicked(event):
                selected_algorithms = [cb.text for cb in checkboxes if cb.checked]
                if input_box.text.isdigit() and selected_algorithms:
                    array_size = int(input_box.text)
                    # Clear previous warnings
                    warning_messages.clear()
                    # Warn the user if array size is very large
                    if array_size > 1000000:
                        warning_messages.append("Warning: Large array size may cause high memory usage.")
                    # Clear previous runtimes and async results
                    runtimes.clear()
                    async_results.clear()
                    processing = True
                    seed = random.randint(0, 1000000)
                    # Create a pool of processes
                    pool = multiprocessing.Pool()
                    # Submit tasks to the pool
                    for alg in selected_algorithms:
                        res = pool.apply_async(run_algorithm, args=(alg, array_size, seed))
                        async_results[alg] = res
                        # Warn for Bubble Sort on large arrays
                        if alg == "Bubble Sort" and array_size > 10000:
                            warning_messages.append("Bubble Sort is very slow for large arrays.")

        # Update runtime results from processes
        if processing:
            for alg, res in list(async_results.items()):
                if res.ready():
                    try:
                        result = res.get()
                        alg_name, runtime = result
                        if runtime == "MemoryError":
                            warning_messages.append(f"Memory Error during {alg_name}.")
                        elif runtime == "RecursionError":
                            warning_messages.append(f"Recursion Error during {alg_name}.")
                        else:
                            runtimes[alg_name] = runtime
                    except Exception as e:
                        warning_messages.append(f"Error during {alg}: {e}")
                    finally:
                        del async_results[alg]
            if not async_results:
                processing = False
                pool.close()
                pool.join()

        # Draw UI elements
        for checkbox in checkboxes:
            checkbox.draw(window, SMALL_FONT, BLACK)
        input_box.draw(window)
        go_button.draw(window)
        # Labels
        array_size_label = SMALL_FONT.render("Array Size:", True, BLACK)
        window.blit(array_size_label, (50, input_box.rect.y - 25))
        # Display warning messages
        for idx, msg in enumerate(warning_messages):
            warning_surface = SMALL_FONT.render(msg, True, RED)
            window.blit(warning_surface, (50, input_box.rect.y + input_box.rect.height + 10 + idx * 20))
        # Display processing message
        if processing:
            processing_surface = FONT.render("Processing...", True, BLUE)
            window.blit(processing_surface, (350, 50))
        # Draw bar graph
        if runtimes:
            max_runtime = max(runtimes.values())
            if max_runtime == 0:
                max_runtime = 1e-8  # Set a very small number to avoid division by zero

            # Graph dimensions and positions
            left_margin = 100  # Increased left margin to accommodate labels
            right_margin = 50
            bottom_margin = 100  # Increased to accommodate rotated labels
            top_margin = input_box.rect.y + 100
            graph_width = WIDTH - left_margin - right_margin
            graph_height = HEIGHT - top_margin - bottom_margin

            num_bars = len(runtimes)
            max_label_width = 0
            for alg in runtimes.keys():
                text_surface = X_AXIS_FONT.render(alg, True, BLACK)
                max_label_width = max(max_label_width, text_surface.get_width())

            # Calculate optimal bar width and gap
            angle_deg = 45
            angle_rad = math.radians(angle_deg)
            label_space = max_label_width * math.cos(angle_rad) + 20  # Additional padding
            available_width_per_bar = graph_width / num_bars
            bar_width = min(50, available_width_per_bar - label_space)
            gap = available_width_per_bar - bar_width

            if bar_width < 10:  # Minimum bar width
                bar_width = 10
                gap = max(5, available_width_per_bar - bar_width)

            start_x = left_margin + (graph_width - (num_bars * bar_width + (num_bars - 1) * gap)) / 2

            for idx, (alg, runtime) in enumerate(runtimes.items()):
                bar_height = (runtime / max_runtime) * (graph_height - 50)  # Adjusted for available space
                bar_x = start_x + idx * (bar_width + gap)
                bar_y = top_margin + graph_height - bar_height

                pygame.draw.rect(window, GREEN, (bar_x, bar_y, bar_width, bar_height))
                # Rotated x-axis labels
                alg_text = X_AXIS_FONT.render(alg, True, BLACK)
                alg_text = pygame.transform.rotate(alg_text, angle_deg)
                alg_text_rect = alg_text.get_rect()
                alg_text_rect.center = (bar_x + bar_width / 2, top_margin + graph_height + alg_text_rect.height / 2 + 10)
                window.blit(alg_text, alg_text_rect)
                # Runtime text
                time_text = SMALL_FONT.render(f"{runtime:.6f}s", True, BLACK)
                time_text_rect = time_text.get_rect(center=(bar_x + bar_width / 2, bar_y - 15))
                window.blit(time_text, time_text_rect)

            # Axes
            pygame.draw.line(window, BLACK, (left_margin, top_margin + graph_height), (WIDTH - right_margin, top_margin + graph_height), 2)
            pygame.draw.line(window, BLACK, (left_margin, top_margin), (left_margin, top_margin + graph_height), 2)

            # Y-axis labels and grid lines
            num_lines = 6
            for i in range(num_lines + 1):
                y = top_margin + graph_height - i * (graph_height / num_lines)
                pygame.draw.line(window, GRAY, (left_margin, y), (WIDTH - right_margin, y), 1)
                label = SMALL_FONT.render(f"{(max_runtime * i / num_lines):.6f}s", True, BLACK)
                label_x_position = left_margin - 90  # Adjusted label position
                window.blit(label, (label_x_position, y - 10))

        # Update display
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
