def add_to_list(item, some_list=None):
    if some_list is None:
        some_list = []
    some_list.append(item)
    return some_list


l1 = add_to_list(0)  # [0]
print(l1)

l2 = add_to_list(1)  # [1]
print(l2)

