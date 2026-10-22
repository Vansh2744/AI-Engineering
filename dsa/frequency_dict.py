# def store_frequency(nums:list[int])->dict:
#     res = {}
#     for num in nums:
#         if num in res:
#             res[num] += 1
#         else:
#             res[num] = 1

#     return res

#------------------------------------------

def store_frequency(nums:list[int])->dict:
    res = {}
    for num in nums:
        res[num] = res.get(num, 0) + 1

    return res

print(store_frequency([1,2,3,3,2,2,1,1,4,4,5]))