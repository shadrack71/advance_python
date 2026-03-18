input_array = [1, 1, 2, 3, 4, 5, 7, 5, 2]

#solution 1
def function_1(input):
    set_array = set(input)
    small_data = 1

    for i in set_array:

        if i > small_data:
            small_data += 1
    print(small_data)

#solution 2
def function_2(input_array):
    input_array.sort()
    new_item = []
    small_number = 1

    # remove duplicate
    for item in input_array:
        if item not in new_item:
            new_item.append(item)

    for i in new_item:
        if i > small_number:
            small_number+=1

    print(small_number)


if __name__ == "__main__":

    function_1(input_array)
    function_2(input_array)
