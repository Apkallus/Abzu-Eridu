# Problem Set 4A
# Name:
# Collaborators:

from tree import Node # Imports the Node object used to construct trees

# Part A0: Data representation
# Fill out the following variables correctly.
# If correct, the test named test_data_representation should pass.
tree1 = Node(8, Node(2, Node(1), Node(6)), Node(10)) #TODO
tree2 = Node(7, Node(2, Node(1), Node(5, Node(3), Node(6))), Node(9, Node(8), Node(10))) #TODO
tree3 = Node(5, Node(3, Node(2), Node(4)), Node(14, Node(12), Node(21, Node(20), Node(26)))) #TODO

def find_tree_height(tree):
    '''
    Find the height of the given tree
    Input:
        tree: An element of type Node constructing a tree
    Output:
        The integer depth of the tree
    '''
    # TODO: Remove pass and write your code here
    # 得到根节点到=最远叶节点的距离，使用递归
    ###
    # tree = Node()
    # 当前节点为空时返回0
    # if tree == None:
    #     return 0
    # else:
    #     # 只在子节点不为空时+1
    #     lt = find_tree_height(tree.get_left_child()) + (1 if tree.get_left_child() != None else 0)
    #     rt = find_tree_height(tree.get_right_child()) + (1 if tree.get_right_child() != None else 0)
    #     return max(lt, rt)
    ###
    # 当前节点为空时返回0
    # if tree == None:
    #     return 0
    # # 当前节点为叶节点时返回0
    # elif tree.get_left_child() == None and tree.get_right_child() == None:
    #     return 0
    # else:
    #     # 仅在当前节点不为叶节点时进入，直接+1
    #     lt = find_tree_height(tree.get_left_child()) + 1
    #     rt = find_tree_height(tree.get_right_child()) + 1
    #     return max(lt, rt)
    ###
    # 初始化左右为0,如果存在左或右节点，则分别递归调用
    lt, rt = 0, 0
    left_child = tree.get_left_child()
    right_child = tree.get_right_child()

    if left_child != None:
        lt = find_tree_height(left_child) + 1
    if right_child != None:
        rt = find_tree_height(right_child) + 1
    return max(lt, rt)

def is_heap(tree, compare_func):
    '''
    Determines if the tree is a max or min heap depending on compare_func
    Inputs:
        tree: An element of type Node constructing a tree
        compare_func: a function that compares the child node value to the parent node value
            i.e. op(child_value,parent_value) for a max heap would return True if child_value < parent_value and False otherwise
                 op(child_value,parent_value) for a min meap would return True if child_value > parent_value and False otherwise
    Output:
        True if the entire tree satisfies the compare_func function; False otherwise
    '''
    # TODO: Remove pass and write your code here
    # 最大堆为根节点最大，最小堆为根节点最小，使用提供的compare_func
    # 使用之前的便利结构，再添加大小比较
    lt, rt = True, True
    left_child = tree.get_left_child()
    right_child = tree.get_right_child()

    if left_child != None:
        if not compare_func(left_child.get_value(), tree.get_value()):
            return False
        lt = is_heap(left_child, compare_func)

    if right_child != None:
        if not compare_func(right_child.get_value(), tree.get_value()):
            return False        
        rt = is_heap(right_child, compare_func)
    # 返回值只要有1个false则为false，逻辑运算应当使用and
    return lt and rt 


if __name__ == '__main__':
    # You can use this part for your own testing and debugging purposes.
    # IMPORTANT: Do not erase the pass statement below if you do not add your own code
    pass
