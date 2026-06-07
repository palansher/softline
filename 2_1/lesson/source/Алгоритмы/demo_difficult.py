def find_max(my_list):
    """Пример сложности O(N)"""
    item_max = my_list[0] #O(1)
    for i in range(1, len(my_list)): #O(N-1)
        if my_list[i] > item_max:
            item_max = my_list[i]
    return item_max#O(1)

# O(1) + O(N-1) + O(1) = O(1 + N - 1 + 1) = O(N + 1) = O(N)

def is_dublicate(my_list):
    """Проверка списка на наличие дубликатов"""
    for i in range(len(my_list)): #O(N)
        for j in range(len(my_list) / 2):#O(N/2)
            if i != j:
                if my_list[i] == my_list[j]:
                    return True
    return False


