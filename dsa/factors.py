#Solution - 1-----------------------

# def get_factors(num:int)->list[int]:
#     res = []
#     for i in range(1, num+1):
#         if num%i == 0:
#             res.append(i)

#     return res

#Solution - 2-------------------------

# def get_factors(num:int)->list[int]:
#     res = []
#     for i in range(1, (num//2)+1):
#         if num%i == 0:
#             res.append(i)

#     res.append(num)
#     return res

#Solution - 3--------------------------

from math import sqrt

def get_factors(num:int)->list[int]:
    num_sqrt = sqrt(num)
    res = []

    for i in range(1, int(num_sqrt)+1):
        if num%i == 0:
            res.append(i)
            rem = num//i
            if rem != i:
                res.append(rem)  

    return res          

print(get_factors(15))