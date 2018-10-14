#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 11:40:41 2018

@author: loewi
"""

'''
dialing number L-ish like knight in the chess game: 
    two steps horizontally, 1 step vertically
or  two steps vertically, 1 step horizontally    
if start at 7, 1 hop, then 7 - (skip14/89) - 2/6, 2 numbers
if start at 7, 0 hop, then 7 , just 1 number
123
456
789
*0#
'''
'''
Q: how many distinct numbers can you dial in N hops from a particular starting position?
'''
Next_Map = {
        0:(4,6), 
        1:(6,8),
        2:(7,9),
        3:(4,8),
        4:(3,9,0),
        5:tuple(),
        6:(1,7,0),
        7:(2,6),
        8:(1,3),
        9:(2,4),         
        }

def next(pos):
    return Next_Map[pos]

#next(6) #(1,7,0)

#%% way 1
    
def dialing(start_pos, hop):
    
    if hop == 0:
        return 1
    
    num = 0
    for current_pos in next(start_pos):
#        print(current_pos)
        num += dialing(current_pos, hop-1)
        
    return num 

if __name__ == "__main__":
    print(dialing(6,2))
    

#%% way 2
    
def dialing(start_pos, hop):
    
    old = [1]*10
    now = [0]*10
    now_hop = 1
    
    while now_hop <= hop:
        now = [0]*10
        now_hop += 1

        for pos in range(0,10):
#            print(pos) # 0 ~ 9
            for naechst in next(pos):
#                print(naechst) #4,6 ~ 2,4
                now[pos] += old [naechst] 
#                print(now) # 1 hop : [2, 2, 2, 2, 3, 0, 3, 2, 2, 2]
        old = now
#        print(old)
    return now[start_pos]

if __name__ == "__main__":
    print(dialing(6,2))
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #%%