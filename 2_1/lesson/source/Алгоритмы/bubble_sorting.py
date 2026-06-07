# def bubble_sort(my_list):
#     flag = True
#     while flag:
#         flag = False
#         for i in range(len(my_list) - 1):
#             if my_list[i] > my_list[i + 1]:
#                 my_list[i], my_list[i + 1] = my_list[i + 1], my_list[i]
#                 flag = True
#     return my_list
#
# print(bubble_sort([2,5,1,8,4]))

def bubble_sort_v2(my_list):
    size = len(my_list)
    for i in range(size - 1):
        for j in range(size - 1  - i):
            if my_list[j] > my_list[j + 1]:
                my_list[j], my_list[j + 1] = my_list[j + 1], my_list[j]
    return my_list

print(bubble_sort_v2([2,5,1,8,4]))