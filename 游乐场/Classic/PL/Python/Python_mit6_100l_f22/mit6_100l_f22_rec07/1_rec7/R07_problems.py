# Dictionaries Practice

# Problem 1: 
# Write a function that takes as input a dictionary and returns a new dictionary,
# where 5 is added to each value of the original dictionary, assuming all values are integers.
# 编写一个函数，该函数接收一个字典作为输入，并返回一个新字典，
# 其中原字典的每个值都增加了5，假设所有值都是整数。
# e.g
# {"item1": 2, "item2": 7, "item3": 20} returns {"item1": 7, "item2": 12, "item3": 25}
def new_dict(input_dict):
    # 使用列表推导式将值+5
    return {k:v+5 for k,v in input_dict.items()}
    
input_dict = {"item1": 2, "item2": 7, "item3": 20}
# print(new_dict({"item1": 2, "item2": 7, "item3": 20})) # expect {"item1": 7, "item2": 12, "item3": 25}



# Problem 2:
# Write a function to check all values are same in a dictionary. 
# Return True if they are all the same, False otherwise
# 编写一个函数来检查字典中的所有值是否相同。
# 如果所有值都相同，则返回 True，否则返回 False
# e.g 
# {'item1': 'apple', 'item2': 'apple', 'item3': 'apple'} returns True, 
# {'item1': 'apple', 'item2': 'apple', 'item3': 'orange'} return False

def check_same_values(input_dict):
    # 得到values的t视图后转换为set,得到u唯一对象，判断set的元素数量
    return len(set(input_dict.values())) <= 1

# testing
input_dict = {'item1': 'apple', 'item2': 'apple', 'item3': 'apple'}
# print(check_same_values(input_dict))  # expect True
input_dict = {'item1': 'apple', 'item2': 'apple', 'item3': 'orange'}
# print(check_same_values(input_dict))  # expect False



# Problem 3: 
# Convert a dictionary to a list of lists where each sublist is in the 
# form [key, value]. Return a sorted version of this list where we sort 
# by decreasing values. 
# 将字典转换为一个由子列表组成的列表，每个子列表的形式为 [键, 值]。
# 返回该列表的排序版本，按值降序排列。
# Example input: {'a': 1, 'b': 5, 'c': 10, 'd': 3, 'e': 2} 
# Example output: [['c', 10], ['b', 5], ['d', 3], ['e', 2], ['a', 1]]

def dict_to_sorted_list(input_dict):
    res_list = [[k,v] for k,v in input_dict.items()]
    res_list.sort(key=lambda x: -x[1])
    return res_list

# testing
input_dict = {'a': 1, 'b': 5, 'c': 10, 'd': 3, 'e': 2}  
# print(dict_to_sorted_list(input_dict))  # expect: [['c', 10], ['b', 5], ['d', 3], ['e', 2], ['a', 1]]



# Problem 4:
# Given a list of dictionaries with item names and amounts in the form {'item': 'my_item_name', 'amount': 'my_amount'}
# write function to combine these items into a single dictionary. See example below. 
# 给定一个包含物品名称和数量的字典列表，格式为 {'item': '物品名称', 'amount': '数量'}
# 编写一个函数，将这些物品合并为一个单独的字典。示例如下。
# # Example input: [{'item': 'item1', 'amount': 400}, {'item': 'item2', 'amount': 300}, {'item': 'item1', 'amount': 750}]
# Expected Output: {'item1': 1150, 'item2': 300}

def combine_dicts(input_dicts):
    res_dict = {}
    for e in input_dicts:
        k = e['item']
        v = e['amount']
        res_dict[k] = res_dict.get(k, 0) + v
    return res_dict
    

# testing
input_dicts = [{'item': 'item1', 'amount': 400}, {'item': 'item2', 'amount': 300}, {'item': 'item1', 'amount': 750}]
print(combine_dicts(input_dicts))  # expect {'item1': 1150, 'item2': 300}


    