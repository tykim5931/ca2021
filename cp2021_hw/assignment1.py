# Question 1. Reversed List

import sys

input_lst = []  # input list contains list of graphs. [[lst1[node1][node2][...]][lst2[][]]]
output_lst = [] # output list contains reversed list.
cnt = 0
while(True):
    n = int(input()) # get number of input graph node 
    if n == 0 : # if zero, input terminated.
        break
    else:
        input_lst.append([])
        output_lst.append([])
    for i in range(0, n):   # for number of nodes, get linked nodes
        lst = list(map(int, sys.stdin.readline().split()))
        input_lst[cnt].append(lst)
        output_lst[cnt].append([])
    cnt+=1

for i in range(0,len(input_lst)):
    for j in range(0,len(input_lst[i])):
        for item in input_lst[i][j]:
            output_lst[i][item].append(j)

# print answer
for i in range(0, len(output_lst)):
    print(len(output_lst[i]))
    for j in range(0, len(output_lst[i])):
        for item in output_lst[i][j]:
            print(item, end = ' ')
        print()
print(0)



