import pygame
import sys
import random
import time
import math
import multiprocessing
from multiprocessing import Process, Queue

# Algorithm names
ALGORITHMS = ["Bubble Sort", "Merge Sort", "Quick Sort", "Radix Sort", "Linear Search"]

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
    def __init__(self, x, y, w, h, text, FONT, color=(100, 100, 255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color  # Default color
        self.text = text
        self.FONT = FONT

    def draw(self, surface, text_color=(255, 255, 255)):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.FONT.render(self.text, True, text_color)
        surface.blit(text_surface, (self.rect.x + (self.rect.w - text_surface.get_width()) / 2,
                                    self.rect.y + (self.rect.h - text_surface.get_height()) / 2))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# Sorting and searching algorithms
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False  # Optimization to stop if the array is sorted
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

def iterative_merge_sort(arr):
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
    max1 = max(arr)
    exp =1
    while max1//exp >0:
        counting_sort(arr, exp)
        exp *=10

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
    for item in arr:
        if item == target:
            break

# Function to run algorithms in separate processes
def run_algorithm(alg_name, array_size, seed, queue):
    # Generate the same array for each algorithm using the seed
    random.seed(seed)
    array = [random.randint(1, 1000000) for _ in range(array_size)]
    arr_copy = array.copy()
    start_time = time.perf_counter()
    try:
        if alg_name == "Bubble Sort":
            bubble_sort(arr_copy)
        elif alg_name == "Merge Sort":
            iterative_merge_sort(arr_copy)
        elif alg_name == "Quick Sort":
            iterative_quick_sort(arr_copy)
        elif alg_name == "Radix Sort":
            radix_sort(arr_copy)
        elif alg_name == "Linear Search":
            target = random.choice(arr_copy)
            linear_search(arr_copy, target)
        end_time = time.perf_counter()
        runtime = end_time - start_time
        queue.put(runtime)
    except MemoryError:
        queue.put("MemoryError")
    except RecursionError:
        queue.put("RecursionError")

def main():
    # Initialize pygame
    pygame.init()
    # Set up display
    WIDTH, HEIGHT = 1000, 800  # Increased window size for better layout
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
    pause_button = Button(340, 50 + len(ALGORITHMS) * 40 + 30, 120, 40, "Pause", FONT, color=(255, 165, 0))  # Orange
    resume_button = Button(480, 50 + len(ALGORITHMS) * 40 + 30, 120, 40, "Resume", FONT, color=(0, 255, 0))  # Green
    reset_button = Button(620, 50 + len(ALGORITHMS) * 40 + 30, 120, 40, "Reset", FONT, color=(255, 0, 0))  # Red

    runtimes = {}
    warning_messages = []
    processing = False
    async_results = {}
    seed = None
    processes = {}
    queues = {}
    start_times = {}
    final_runtimes = {}
    paused = False
    paused_time = 0
    pause_start = None

    running = True
    while running:
        window.fill(WHITE)
        current_time = time.perf_counter()
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Terminate all running processes before quitting
                for proc in processes.values():
                    proc.terminate()
                running = False
            for checkbox in checkboxes:
                checkbox.handle_event(event)
            input_box.handle_event(event)
            if go_button.is_clicked(event):
                if processing:
                    continue
                selected_algorithms = [cb.text for cb in checkboxes if cb.checked]
                if input_box.text.isdigit() and selected_algorithms:
                    array_size = int(input_box.text)
                    # Clear previous warnings
                    warning_messages.clear()
                    # Clear previous runtimes and async results
                    runtimes.clear()
                    final_runtimes.clear()
                    warning_messages.clear()
                    # Reset pause state
                    paused = False
                    pause_start = None
                    paused_time = 0
                    # Clear existing processes and queues
                    for proc in processes.values():
                        proc.terminate()
                    processes.clear()
                    queues.clear()
                    start_times.clear()
                    # Initialize processing state
                    processing = True
                    seed = random.randint(0, 1000000)
                    # Create and start a process for each selected algorithm
                    for alg in selected_algorithms:
                        q = Queue()
                        proc = Process(target=run_algorithm, args=(alg, array_size, seed, q))
                        proc.start()
                        processes[alg] = proc
                        queues[alg] = q
                        start_times[alg] = current_time
                        runtimes[alg] = 0  # Initialize runtime
                else:
                    warning_messages.append("Please enter a valid array size and select at least one algorithm.")
            if pause_button.is_clicked(event) and processing and not paused:
                paused = True
                pause_start = time.perf_counter()
            if resume_button.is_clicked(event) and processing and paused:
                paused = False
                if pause_start:
                    paused_time += time.perf_counter() - pause_start
                    pause_start = None
            if reset_button.is_clicked(event):
                # Terminate all running processes
                for proc in processes.values():
                    proc.terminate()
                processes.clear()
                queues.clear()
                start_times.clear()
                runtimes.clear()
                final_runtimes.clear()
                warning_messages.clear()
                processing = False
                paused = False
                paused_time = 0
                pause_start = None

        # Update runtime results from processes
        if processing and not paused:
            for alg, proc in list(processes.items()):
                if proc.is_alive():
                    # Update runtime based on elapsed time
                    elapsed = current_time - start_times[alg] - paused_time
                    runtimes[alg] = elapsed
                else:
                    # Process has finished
                    if alg not in final_runtimes:
                        if not queues[alg].empty():
                            result = queues[alg].get()
                            if isinstance(result, str):
                                warning_messages.append(f"{alg}: {result}")
                                runtimes[alg] = 0
                            else:
                                final_runtimes[alg] = result
                                runtimes[alg] = result
                        else:
                            final_runtimes[alg] = 0
                            runtimes[alg] = 0
                    # Remove the process from the active list
                    proc.join()
                    del processes[alg]
                    del queues[alg]
            if not processes:
                processing = False

        # Draw UI elements
        for checkbox in checkboxes:
            checkbox.draw(window, SMALL_FONT, BLACK)
        input_box.draw(window)
        go_button.draw(window)
        pause_button.draw(window)
        resume_button.draw(window)
        reset_button.draw(window)
        # Labels
        array_size_label = SMALL_FONT.render("Array Size:", True, BLACK)
        window.blit(array_size_label, (50, input_box.rect.y - 25))
        # Display warning messages
        for idx, msg in enumerate(warning_messages):
            warning_surface = SMALL_FONT.render(msg, True, RED)
            window.blit(warning_surface, (50, input_box.rect.y + input_box.rect.height + 10 + idx * 20))
        # Draw bar graph
        if runtimes:
            max_runtime = max(runtimes.values()) if runtimes else 1
            if max_runtime == 0:
                max_runtime = 1e-8  # Set a very small number to avoid division by zero

            # Graph dimensions and positions
            left_margin = 100  # Increased left margin to accommodate labels
            right_margin = 50
            bottom_margin = 100  # Increased to accommodate rotated labels
            top_margin = input_box.rect.y + 150
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
                # Use final runtime if available
                display_runtime = final_runtimes.get(alg, runtime)
                # For visualization, cap the runtime at max_runtime
                normalized_runtime = display_runtime if display_runtime <= max_runtime else max_runtime
                bar_height = (normalized_runtime / max_runtime) * (graph_height - 50)  # Adjusted for available space
                bar_x = start_x + idx * (bar_width + gap)
                bar_y = top_margin + graph_height - bar_height

                pygame.draw.rect(window, GREEN if alg not in final_runtimes else BLUE, (bar_x, bar_y, bar_width, bar_height))
                # Rotated x-axis labels
                alg_text = X_AXIS_FONT.render(alg, True, BLACK)
                alg_text = pygame.transform.rotate(alg_text, angle_deg)
                alg_text_rect = alg_text.get_rect()
                alg_text_rect.center = (bar_x + bar_width / 2, top_margin + graph_height + alg_text_rect.height / 2 + 10)
                window.blit(alg_text, alg_text_rect)
                # Runtime text
                time_text = SMALL_FONT.render(f"{display_runtime:.6f}s" if isinstance(display_runtime, float) else f"{display_runtime}", True, BLACK)
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
                label = SMALL_FONT.render(f"{(max_runtime * i / num_lines):.2f}s", True, BLACK)
                label_x_position = left_margin - 90  # Adjusted label position
                window.blit(label, (label_x_position, y - 10))

        # Update display
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    multiprocessing.freeze_support()  # For Windows support
    main()
