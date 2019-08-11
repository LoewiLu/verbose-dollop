#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 16:27:11 2019

@author: loewi

一个大写字母的字符串，允许改变最多两个字符（也允许不变或者只变一个），使字符串中所包含的最长的连续的“N”字符串长度最长。
例：'NNTH'-'NNNN' 4
"""
import itertools

def luckyN(s):
    mylist = []
    for i in range(len(s)):
        if s[i]!='N':
            mylist.append(i)

    if len(mylist) <= 2: 
        return len(s)
    
    res = 0
    ls = list(s)

    for i in range(len(mylist)):
        
        a, b = mylist[i-1] if i>=1 else mylist[i], mylist[i]
        ls[a] = 'N'
        ls[b] = 'N'
        
        for k, g in itertools.groupby(ls):
            if k == 'N':
                res = max(len(list(g)), res)
                
        ls[a] = 'X'
        ls[b] = 'X'
    
    return res


if __name__ == '__main__':	
	lst = ['NGN','NNTH','NNNNGGNNNN','NGNNNNGNNNNNNNNSNNNN']
	result = [3,4,10,18]
	assert result == list(map(luckyN, lst)), "wrong!"
	print("Test pass！")
#%%
