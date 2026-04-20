import tkinter as tk
from queue import PriorityQueue
import numpy as np
from typing import List, Tuple, Set
import time


class TreasureHuntGUI:
    # Increased cell size for better visibility
    def __init__(self, root, grid_size: int, cell_size: int = 80):
        self.root = root
        self.root.title("Treasure Hunt - Best First Search")
        self.grid_size = grid_size
        self.cell_size = cell_size

        # Main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Initialize canvas
        canvas_size = grid_size * cell_size
        self.canvas = tk.Canvas(
            self.main_frame, width=canvas_size, height=canvas_size)
        self.canvas.pack(side=tk.LEFT)

        # Info panel
        self.info_panel = tk.Frame(self.main_frame)
        self.info_panel.pack(side=tk.LEFT, padx=20, fill='y')

        # Control panel
        self.control_panel = tk.Frame(self.info_panel)
        self.control_panel.pack(fill='x', pady=10)

        # Start button
        self.start_button = tk.Button(
            self.control_panel, text="Start Search", command=self.start_search)
        self.start_button.pack(fill='x', pady=2)

        # Reset button
        self.reset_button = tk.Button(
            self.control_panel, text="Reset", command=self.reset)
        self.reset_button.pack(fill='x', pady=2)

        # Speed control
        speed_frame = tk.Frame(self.control_panel)
        speed_frame.pack(fill='x', pady=2)
        tk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
        self.speed_var = tk.StringVar(value="Normal")
        self.speed_menu = tk.OptionMenu(
            speed_frame, self.speed_var, "Slow", "Normal", "Fast")
        self.speed_menu.pack(side=tk.LEFT, padx=5)

        # Statistics
        self.stats_frame = tk.LabelFrame(
            self.info_panel, text="Statistics", padx=5, pady=5)
        self.stats_frame.pack(fill='x', pady=10)

        self.nodes_explored_var = tk.StringVar(value="Nodes explored: 0")
        tk.Label(self.stats_frame, textvariable=self.nodes_explored_var).pack(
            anchor='w')

        self.current_heuristic_var = tk.StringVar(value="Current heuristic: -")
        tk.Label(self.stats_frame, textvariable=self.current_heuristic_var).pack(
            anchor='w')

        self.path_length_var = tk.StringVar(value="Path length: -")
        tk.Label(self.stats_frame, textvariable=self.path_length_var).pack(
            anchor='w')

        # Legend
        self.legend_frame = tk.LabelFrame(
            self.info_panel, text="Legend", padx=5, pady=5)
        self.legend_frame.pack(fill='x', pady=10)

        legend_items = [
            ("Start", "green"),
            ("Target", "gold"),
            ("Current Node", "yellow"),
            ("Explored", "pink"),
            ("Path", "light blue"),
            ("Frontier", "light green")
        ]

        for text, color in legend_items:
            frame = tk.Frame(self.legend_frame)
            frame.pack(fill='x', pady=1)
            tk.Canvas(frame, width=20, height=20, bg=color).pack(
                side=tk.LEFT, padx=5)
            tk.Label(frame, text=text).pack(side=tk.LEFT)

        self.draw_grid()
        self.initialize_game()

    def get_animation_delay(self):
        speeds = {"Slow": 1000, "Normal": 500, "Fast": 100}
        return speeds[self.speed_var.get()]

    def draw_grid(self):
        """Draw the initial grid with heuristic values"""
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="white", outline="gray", tags="cell")

    def draw_cell(self, pos: Tuple[int, int], color: str, text: str = "", show_heuristic: bool = True):
        """Draw a colored cell with heuristic value and optional text"""
        x1 = pos[1] * self.cell_size
        y1 = pos[0] * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Create rectangle with given color
        self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=color, outline="gray")

        # Add text if provided
        if text:
            self.canvas.create_text(
                (x1 + x2)/2, (y1 + y2)/2 - 10, text=text, font=("Arial", 12, "bold"))

        # Show heuristic value
        if show_heuristic:
            heuristic = self.hunt.grid[pos]
            self.canvas.create_text((x1 + x2)/2, (y1 + y2)/2 + 10,
                                    text=f"h={heuristic:.1f}",
                                    font=("Arial", 10))

    def initialize_game(self):
        """Set up initial positions"""
        self.start_pos = (0, 0)
        self.treasure_pos = (self.grid_size-1, self.grid_size-1)
        self.hunt = TreasureHunt(self.grid_size, self.treasure_pos)

        # Draw initial grid with heuristic values
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.draw_cell((i, j), "white")

        # Draw start and target positions
        self.draw_cell(self.start_pos, "green", "S")
        self.draw_cell(self.treasure_pos, "gold", "T")

        # Reset statistics
        self.nodes_explored_var.set("Nodes explored: 0")
        self.current_heuristic_var.set("Current heuristic: -")
        self.path_length_var.set("Path length: -")

    def highlight_frontier(self, frontier_nodes: List[Tuple[int, int]]):
        """Highlight frontier nodes in light green"""
        for pos in frontier_nodes:
            if pos != self.start_pos and pos != self.treasure_pos:
                self.draw_cell(pos, "light green")

    def animate_search(self, path: List[Tuple[int, int]], visited: List[Tuple[int, int]], frontier: List[Tuple[int, int]]):
        """Animate the search process"""
        if not visited:
            if path:
                # Show final path
                for pos in path:
                    if pos != self.start_pos and pos != self.treasure_pos:
                        self.draw_cell(pos, "light blue")
                self.path_length_var.set(f"Path length: {len(path)}")
            return

        current_pos = visited.pop(0)
        current_frontier = frontier.pop(0)

        # Update statistics
        self.nodes_explored_var.set(
            f"Nodes explored: {len(path) - len(visited)}")
        self.current_heuristic_var.set(
            f"Current heuristic: {self.hunt.grid[current_pos]:.1f}")

        # Highlight current node and frontier
        if current_pos != self.start_pos and current_pos != self.treasure_pos:
            self.draw_cell(current_pos, "yellow")  # Current node in yellow
        self.highlight_frontier(current_frontier)

        # Schedule next animation step
        self.root.after(self.get_animation_delay(),
                        lambda: self.animate_search(path, visited, frontier))

        # After showing current node, change it to pink (explored)
        self.root.after(self.get_animation_delay() - 50,
                        lambda: self.draw_cell(current_pos, "pink") if current_pos != self.start_pos and current_pos != self.treasure_pos else None)

    def start_search(self):
        """Start the search animation"""
        self.start_button.config(state=tk.DISABLED)
        path, nodes_explored, visited, frontiers = self.hunt.best_first_search(
            self.start_pos)

        if path:
            self.animate_search(path, visited, frontiers)
        else:
            self.current_heuristic_var.set("No path found!")

    def reset(self):
        """Reset the grid and controls"""
        self.draw_grid()
        self.initialize_game()
        self.start_button.config(state=tk.NORMAL)


class TreasureHunt:
    def __init__(self, grid_size: int, treasure_pos: Tuple[int, int]):
        self.grid_size = grid_size
        self.treasure_pos = treasure_pos
        self.grid = self.create_grid_with_heuristic()

    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def create_grid_with_heuristic(self) -> np.ndarray:
        grid = np.zeros((self.grid_size, self.grid_size))
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                grid[i][j] = self.manhattan_distance((i, j), self.treasure_pos)
        return grid

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dx, dy in directions:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                neighbors.append((new_x, new_y))
        return neighbors

    def best_first_search(self, start_pos: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], int, List[Tuple[int, int]], List[List[Tuple[int, int]]]]:
        frontier = PriorityQueue()
        frontier.put((self.grid[start_pos], start_pos))
        frontier_nodes = set([start_pos])

        came_from = {start_pos: None}
        nodes_explored = 0
        visited = []  # Keep track of visited nodes for visualization
        frontiers = []  # Keep track of frontier at each step

        while not frontier.empty():
            current_cost, current_pos = frontier.get()
            frontier_nodes.remove(current_pos)
            visited.append(current_pos)
            # Save current frontier state
            frontiers.append(list(frontier_nodes))
            nodes_explored += 1

            if current_pos == self.treasure_pos:
                path = self.reconstruct_path(came_from, current_pos)
                return path, nodes_explored, visited, frontiers

            # Expand neighbors
            for neighbor in self.get_neighbors(current_pos):
                if neighbor not in came_from:
                    came_from[neighbor] = current_pos
                    frontier.put((self.grid[neighbor], neighbor))
                    frontier_nodes.add(neighbor)

        return [], nodes_explored, visited, frontiers  # No path found

    def reconstruct_path(self, came_from: dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path


if __name__ == "__main__":
    root = tk.Tk()
    app = TreasureHuntGUI(root, grid_size=5)
    root.mainloop()
