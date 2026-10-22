def is_palindrome(num:int)->bool:
    given_num = num
    res_num = 0

    while given_num > 0:
        end_digit = given_num % 10
        res_num = (res_num*10)+end_digit
        given_num //= 10

    return res_num == num

print(is_palindrome(3443))