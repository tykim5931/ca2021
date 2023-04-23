# Q3
# 프로그래머스 - 조이스틱
import sys
import numpy as np

# get input file
_me, in_f = sys.argv
f=open(in_f, 'r')
lines = f.readlines()
f.close()

# Algorithm
alphabet = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,
            'O':12,'P':11,'Q':10,'R':9,'S':8,'T':7,'U':6,'V':5, 'W':4, 'X':3,'Y':2,'Z':1}

for name in lines:
    name = name.strip().upper()
    name_len = len(name)
    alpha_sum = 0
    for alpha in name:
        alpha_sum += alphabet[alpha]

    if name.find('A') == -1:
        sum = name_len -1 +alpha_sum #for removing last move
        print(sum)
    elif name.count('A') == name_len:
        print(0)
    else:
        sum = 0
        # find longest 'A' bunch in the name
        i_lst, len_lst = [0], [0]
        name_temp = name
        while (True):
            temp = name_temp.find('A')
            if(temp == -1):
                break
            i_lst.append(i_lst[-1]+len_lst[-1] + temp)
            i=temp
            for j in range(temp, len(name_temp)):
                if(name_temp[j] != 'A'):
                    break
                i += 1
            len_lst.append(i-temp)
            name_temp = name_temp[i:]
        longest_a_idx = np.argmax(len_lst)
    
        a_first = i_lst[longest_a_idx]
        a_last = a_first+len_lst[longest_a_idx]
        
        # going through right side
        a_start = len(name)
        if(name[-1] == 'A'):
            for i, a in enumerate(name[::-1]):
                if(a!='A'):
                    a_start = len(name)-i
                    break
        r_sum = a_start
        if(r_sum): # 0이 아닌 경우에!
            r_sum -= 1

        # going through left side
        a_start = 0
        if(name[0]=='A'):
            for i, a in enumerate(name):
                if(a!='A'):
                    a_start = i
                    break
        l_sum = name_len - a_start

        # 갔다가 돌아가는 경우(right first)
        rb_sum = 0
        rb_sum=a_first*2
        if(rb_sum): # 0이 아닌 경우에!
            rb_sum -= 2
        rb_sum += name_len-a_last

        # 갔다가 돌아가는 경우(left first)
        lb_sum=0
        lb_sum += (name_len-a_last)*2
        if(lb_sum): # 0이 아닌 경우에!
            lb_sum -= 1
        lb_sum += a_first

        sum = min(l_sum, r_sum, rb_sum, lb_sum)
        #print(np.argmin([l_sum, r_sum, rb_sum, lb_sum]))
        sum += alpha_sum
        print(sum)