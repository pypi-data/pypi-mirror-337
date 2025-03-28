def rand_missing_seq(n=10):
    if n <= 1:
        my_list = [1]
    else:
        from random import randint, shuffle
        my_list = [i for i in range(1, n+1)]
        missing = randint(0, n-1)
        del my_list[missing]
        shuffle(my_list)
    return my_list