def reverse_number(num:int)->int:
    given_num = num
    res = 0

    while given_num != 0:
        end_digit = given_num % 10
        res = (res*10)+end_digit

        given_num //= 10

    return res

print(reverse_number(234))

