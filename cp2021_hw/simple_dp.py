# Q1
import sys

# get input file
_me, in_f = sys.argv
f=open(in_f, 'r')
lines = f.readlines()
f.close()

# Algorithm
N_MAX = 70
DP = [0 for i in range(N_MAX)]
DP[0] = 1
DP[1] = 1
DP[2] = 2
DP[3] = 4

for input in lines:
    n = int(input)
    count = 0
    if DP[n] != 0:
        print(DP[n])
    else:
        for i in range(4, n+1):
            if DP[i] != 0:
                continue
            DP[i] = DP[i-1]+DP[i-2]+DP[i-3]+DP[i-4]
        print(DP[n])
