#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 16:27:11 2019

@author: loewi
"""


def luckyN(s):
    mylist = []
    for i in range(len(s)):
        if s[i]!='N':
            mylist.append(i)
    
    ls = list(s)
    if len(mylist) <2: 
        return len(s)
    
    long = 0
    res = 0
    comb = list(itertools.combinations(mylist,2))
    dp = [0]*len(comb)
    
    for i, t in enumerate(comb):
        a, b = t
        ls[a] = 'N'
        ls[b] = 'N'
        
        for k, g in itertools.groupby(ls):
            if k == 'N':
                long = max(len(list(g)), long)
        ls[a] = 'X'
        ls[b] = 'X'       
        dp[i] = long
        
    res = max(res, dp[i])
    
    return res


if __name__ == '__main__':	
	lst = ['NGN','NNTH','NNNNGGNNNN','NGNNNNGNNNNNNNNSNNNN']
	result = [3,4,10,18]
	assert result == list(map(luckyN, lst)), "wrong!"
	print("Test pass！")
#%%