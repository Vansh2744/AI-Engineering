# def print_series(start, end):
#     print(start)
#     if start == end:
#         return
#     print_series(start+1, end)

# print_series(1,10)

#----------------------------------

def sum_of_number(num:int)->int:
    if num == 1:
        return 1
    return num + sum_of_number(num-1)

print(sum_of_number(5))