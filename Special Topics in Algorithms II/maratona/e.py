# Read input dimensions
n, m = map(int, input().split())

# Initialize the grid
grid = []
start_i, start_j = -1, -1
direction = -1  # 0: Up, 1: Left, 2: Down, 3: Right

# Direction mappings
dir_map = {'U': 0, 'L': 1, 'D': 2, 'R': 3}
# Movement deltas for directions: Up, Left, Down, Right
di = [-1, 0, 1, 0]
dj = [0, -1, 0, 1]

# Read the grid and find the starting position and direction
for i in range(n):
    row = input()
    for j in range(m):
        if row[j] in dir_map:
            start_i, start_j = i, j
            direction = dir_map[row[j]]
            # Replace the starting position with empty space
            row = row[:j] + '.' + row[j+1:]
    grid.append(row)

# Set to keep track of visited positions
visited = set()
visited.add((start_i, start_j))

# Initialize robot's position
i, j = start_i, start_j

# Simulation loop
while True:
    rotations = 0
    moved = False
    # Try to move up to 4 times (rotating if necessary)
    while rotations < 4:
        # Calculate next position
        ni = i + di[direction]
        nj = j + dj[direction]
        # Check if next position is within bounds and not a wall
        if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] != '#':
            # Move to the next position
            i, j = ni, nj
            visited.add((i, j))
            moved = True
            break  # Exit rotation loop after moving
        else:
            # Rotate 90 degrees counterclockwise
            direction = (direction + 1) % 4
            rotations += 1
    if not moved:
        # Cannot move after trying all directions
        break

# Output the number of distinct squares visited
print(len(visited))