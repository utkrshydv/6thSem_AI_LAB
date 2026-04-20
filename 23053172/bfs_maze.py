maze = [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1]
]

sx, sy = map(int, input("Enter start (sx sy): ").split())
gx, gy = map(int, input("Enter goal (gx gy): ").split())

start = (sx, sy)
end = (gx, gy)

queue = [[start]]
visited = {start}
nodes_bfs = 0

while queue:
    path = queue.pop(0)
    r, c = path[-1]
    nodes_bfs += 1

    if (r, c) == end:
        print(f"BFS Path: {path}")
        print(f"BFS Nodes Explored: {nodes_bfs}")
        break

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = r + dx, c + dy
        if 0 <= nr < 5 and 0 <= nc < 5 and maze[nr][nc] == 1 and (nr, nc) not in visited:
            visited.add((nr, nc))
            queue.append(path + [(nr, nc)])
