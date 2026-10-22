def is_number_armstrong(num:int)->bool:
    given_num = num
    count = len(str(given_num))
    res = 0

    while given_num > 0:
        end_digit = given_num % 10
        res += (end_digit**count)
        given_num //= 10

    return res == num

print(is_number_armstrong(153))