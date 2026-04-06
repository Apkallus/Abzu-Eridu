# 在这个问题中，你将根据以下规范实现两个类：一个 `Container` 类和一个 `Queue` 类（`Container` 的子类）。

# 我们的 `Container` 类将初始化一个空列表。我们将实现两个方法：
# 一个是计算列表的大小，另一个是添加元素。第二个方法将被子类继承。
# 现在，我们希望创建一个子类，以便增加更多功能——从列表中移除元素的能力。
# `Queue` 将以相同的方式向列表中添加元素，但在移除元素时会表现出不同的行为。

# 队列是一种先进先出（FIFO）的数据结构。想象一下商店的收银队列。在队列中等待时间最长的顾客将获得下一个可用的收银员。
# 在实现 `Queue` 类时，你需要考虑列表的哪一端包含在列表中时间最长的元素。这就是你将要移除并返回的元素。
class Container(object):
    """
    A container object is a list and can store elements of any type
    容器对象是一种列表，能够存储任意类型的元素。
    """
    def __init__(self):
        """
        Initializes an empty list
        初始化一个空列表
        """
        self.myList = []

    def size(self):
        """
        Returns the length of the container list
        返回容器列表的长度
        """
        # Your code here
        return len(self.myList)

    def add(self, elem):
        """
        Adds the elem to one end of the container list, keeping the end
        you add to consistent. Does not return anything
        将元素添加到容器列表的一端，并保持添加端的一致性。不返回任何内容。
        """
        # Your code here
        self.myList.append(elem)

class Queue(Container):
    """
    A subclass of Container. Has an additional method to remove elements.
    Container 的一个子类。具备一个额外的方法用于移除元素。
    """
    def remove(self):
        """
        The oldest element in the container list is removed
        Returns the element removed or None if the stack contains no elements
        容器列表中最旧的元素被移除
        返回被移除的元素，如果栈中不包含任何元素，则返回None
        """
        # Your code here
        return self.myList.pop(0) if self.size()>0 else None