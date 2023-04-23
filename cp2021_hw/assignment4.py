from collections import deque
import sys

v_num = int(input()) # get N
graph = [[] for i in range(0,v_num)]
INF = float("inf")

# create graph
for line in sys.stdin:
    line_lst = (list(map(int, line.strip().split())))
    for j in range(1, len(line_lst),2):
        graph[line_lst[0]-1].append((line_lst[j], line_lst[j+1])) # ID, weight

# for checking path
check_q = deque()
ans = [([1,i+1], INF) for i in range(0,v_num)]
ans[0] = ([1], 0) # for fixing initial vertix #parents #distance
been_set ={1}    # 방문한 노드 & 방문 예정인 노드
check_q.append([1, 0])

# check negaitve cycle
def check_nc(prev_v, start_idx, sum):
    parents = ans[prev_v[0]-1][0]
    for i in range(start_idx, len(parents)-1):
        for v in graph[parents[i]-1]:
            if v[0] == parents[i+1]:
                sum += v[1]
    if(sum < 0):
        return 1
    else:
        return 0

# Bellman-Ford algorithm
def bellman_ford():
    while len(check_q) != 0:
        prev_v = check_q.popleft()
        for item in graph[prev_v[0]-1]:
            #지나온 경로에 있는 애가 또 방문 노드로 들어왔을 경우...
            if ans[prev_v[0] -1][1] + item[1] < ans[item[0]-1][1]:
                ans[item[0]-1] = (ans[prev_v[0]-1][0][:], ans[prev_v[0] -1][1] + item[1]) # 경로 수정
                ans[item[0]-1][0].append(item[0])   # 현재 위치까지 추가
            if(item[0] not in been_set):
                check_q.append(item)
                been_set.add(item[0])
            if (item[0] in ans[prev_v[0]-1][0]):
                sum = item[1]
                c_start = ans[prev_v[0]-1][0].index(item[0])
                if(check_nc(prev_v, c_start, sum)):
                    print("negative cycle")
                    return

    # print output
    for path in ans:
        for v in path[0]:
            print(v, end=' ')
        print(path[1])
    return

bellman_ford()