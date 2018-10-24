# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 20:29:26 2018

@author: kys
"""
    
#def solution(number, k):
#    answer = ''
#    while k:
#        nums = [number]*len(number)
#        for i in range(len(number)):
#            nums[i] = number[:i] + number[i+1:]
#        number = max(nums)
#        k-=1
#    answer = number
#    return answer
#
#num = '4177252841'
#n = len(num)
#print(solution(num, 4))

def solution(number, k):
    while k > 0:
        i = 1
        changed = False
        while i < len(number) and k > 0:
            if number[i] > number[i-1]:
                number = number[:i-1] + number[i:]
                changed = True
                k-=1
                break
            i+=1
        if i == len(number) and not changed and k > 0:
            number = number[:-1]
            k-=1
    return number
print(solution("1924",2))
print(solution("1231234",3))
print(solution("4177252841",3))
print(solution("4177252841",1))
print(solution("656566",1))