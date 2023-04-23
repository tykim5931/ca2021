# Q2
import sys

# get input file
_me, in_f = sys.argv
f=open(in_f, 'r')
lines = f.readlines()
f.close()


# Algorithm

N_MAX = 100
DP = [[0 for i in range(N_MAX)] for j in range(N_MAX)]

n = int(lines[0].strip())

for i in range(1, n+1):
    line = lines[i]
    arr = list(map(int, line.strip('\n').split(' ')))
    for j in range(len(arr)):
        DP[i][j] = arr[j]

for i_rev in range(n-1, 0, -1):
    for j in range(i_rev):
        DP[i_rev][j] = max( DP[i_rev][j] + DP[i_rev+1][j] ,  DP[i_rev][j] + DP[i_rev+1][j+1] )

print(DP[1][0])