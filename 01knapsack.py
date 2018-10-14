#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 21:12:53 2018

@author: loewi
"""

#%%01knapsack problem
'''    
        c = capacity of the knapsack
        n = len(items)
        w = weight of items
        v = value of items
        ks = knapsack, dx = dongxi东西
        n-1：A）list中的位置(python是0打头)，用m表示； B）回到上一行
'''

def ks(n, c):
    m = n-1 #其实m就是n，只不过为了定位(python是0打头) 
    if n == 0 or c == 0 : #没东西or没包，不玩儿了
        result = 0
    elif w[m] > c : #自个儿就超重了，不带你玩儿了 
        result = ks(n-1, c) #回到上一行没有你的时候
    else:
        tmp1 = ks(n-1, c) #上一行没有你的时候
        tmp2 = v[m] + ks(n-1, c-w[m]) #你的体重+回到上一行/减去你体重的包容量的时候
        result = max(tmp1, tmp2)#抉择要不要你的时候到了
    return result

def dx(n, c):

    itemsValue = []  
    for n in range(n,0,-1): #pointer为表的右下角，也就是第n行第c列
        m = n-1 #其实m就是n，只不过为了定位(python是0打头) 
        if ks(n,c) != ks(n-1,c): #跟楼上n-1行比，如果一样，证明东西没被扔到包里
            itemsValue.append(v[m]) #如果不一样，证明此物乃囊中之物
            c = c - w[m] #pointer到了第n-1行第（c-此物重量）列，然后循环继续
    itemsValue.reverse()#从后往前倒的，所以要再反过来
    return itemsValue
        
        
if __name__=='__main__':
    n=5
    c=int(input('Plz decide the capacity of your bag.\nNote: less than 20 would be better: '))
    w=[3,2,1,8,6]
    v=[1,4,5,2,7]
    print('The maximum value you can carry is', ks(n,c), end='.\nThe items\' values are, respectively, ')    
    print(*dx(n, c),sep = ',', end = '.')

