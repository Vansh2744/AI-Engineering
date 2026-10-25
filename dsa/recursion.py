def print_series(start, end):
    print(start)
    if start == end:
        return
    print_series(start+1, end)

print_series(1,10)