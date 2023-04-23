# Q2
import sys
from collections import deque

input = []
for line in sys.stdin:
    input.append(list(map(int, line.strip().split())))

# moving logic of knight
x = [2, 2, 1, -1, -2, -2, -1, 1]
y = [1, -1, 2, 2, 1, -1, -2, -2]

i = 0

while i < len(input):
    map_size = input[i][0]
    board = [[-1 for col in range(map_size)] for row in range(map_size)]
    i += 1
    x_s, y_s = input[i]
    board[x_s-1][y_s-1] = 0
    i += 1
    x_f, y_f = input[i]
    i += 1
    queue = deque()
    queue.append((x_s-1, y_s-1))
    while len(queue) != 0:
        r , c = queue.popleft()
        temp_r = r
        temp_c = c
        for j in range(0,8):
            temp_r = r+x[j]
            temp_c = c+y[j]
            if (temp_r >= 0 and temp_c >= 0 and temp_r < map_size and temp_c < map_size) and (board[temp_r][temp_c] == -1):
                board[temp_r][temp_c] = board[r][c] + 1
                queue.append((temp_r, temp_c))
                if temp_r == x_f-1 and temp_c == y_f-1:
                    break
        if temp_r == x_f-1 and temp_c == y_f-1:
            break
    print(board[x_f-1][y_f-1])