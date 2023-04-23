# Q4
import sys

# get input file
_me, in_f = sys.argv
f=open(in_f, 'r')
lines = f.readlines()
f.close()

# Algorithm
n_cases = int(lines[0])

for i in range(n_cases):
    n_box = lines[1+i*2]
    h_lst = list(map(int, lines[2+i*2].split(' ')))
    h_lst.sort()
    odd, even = [], []
    a = len(h_lst)
    if(a%2):
        a = a-1
    for i in range(0,a-1,2):
        even.append(h_lst[i])
        odd.append(h_lst[i+1])
    if(len(h_lst)%2):
        even.append(h_lst[-1])
    even = even[::-1]
    odd.extend(even)
    odd.append(odd[0])
    ans = abs(odd[1] - odd[0])
    for i in range(2, len(odd)):
        tmp = abs(odd[i]-odd[i-1])
        if(tmp > ans):
            ans = tmp
    print(ans)