def bin_search(my_list,target):
    my_list.sort()
    print(my_list)

    start_index = 0
    end_index = len(my_list) - 1
    middle_index = (start_index + end_index) // 2 #индекс центрального элемента

    while my_list[middle_index] != target and start_index <= end_index:
        if target > my_list[middle_index]:
            start_index = middle_index + 1
        else:
            end_index = middle_index - 1
        middle_index = (start_index + end_index) // 2
    if start_index > end_index:
        print("Элемент не найден")
        return -1
    return middle_index #если элемент найден, вернем индекс найденного элемента

print(bin_search([1,2,3,4,5,6,7,8],40))