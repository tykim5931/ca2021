from queue import PriorityQueue
import sys
import math

pq = PriorityQueue()
INF = float("inf")

input = []
for line in sys.stdin:
    input.append(list(map(float, line.strip().split(','))))

for i in range(0, len(input)):
    ans = []

    # creating a node graph
    map_size = input[i][0]
    x_o = input[i][1]
    y_o = input[i][2]
    for j in range(3, len(input[i]), 2):
        # tuple (priority(weight), x, y)
        len_with_o = math.sqrt((input[i][j]-x_o)**2 + (input[i][j+1]-y_o)**2)
        if(len_with_o > 101):
            len_with_o = INF
        pq.put((len_with_o, input[i][j], input[i][j+1], j)) #dist, x, y, ID
    while not pq.empty():
        closest, x_c, y_c, id_c = pq.get()
        ans.append((closest, x_c, y_c, id_c))
        pq_temp = PriorityQueue()
        for k in range(0, pq.qsize()):
            d, x, y, id= pq.get()
            len_with_c = math.sqrt((x-x_c)**2 + (y-y_c)**2)
            if (closest + len_with_c) < d:
                d = closest+len_with_c
            pq_temp.put((d,x,y,id))
        pq = pq_temp

    for items in ans:
        if(items[3] == len(input[i])-2):
            if items[0] == INF:
                print(-1)
            else:
                print('{:.2f}'.format(items[0]))
