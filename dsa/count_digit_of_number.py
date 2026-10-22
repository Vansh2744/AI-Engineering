def count_digit(num:int)->int:
    given_num = num
    count = 0

    while given_num > 0:
        count += 1
        given_num //= 10

    return count

print(count_digit(356890))

# from math import log10

# print(int(log10(234785)+1))