# 在本问题中，你将根据以下规范实现两个类：一个容器类和一个栈类（容器类的子类）。

# 我们的容器类将初始化一个空列表。我们将拥有的两个方法是计算列表大小和添加元素。
# 第二个方法将由子类继承。现在，我们希望创建一个子类，以便能够添加更多功能——从列表中移除元素的能力。
# 栈类将以相同的方式向列表添加元素，但在移除元素时会有不同的行为。

# 栈是一种后进先出的数据结构。想象一下一摞煎饼。
# 当你制作煎饼时，你会将它们堆叠起来，旧的煎饼放在底部，新的煎饼放在顶部。
# 当你开始吃煎饼时，你会从顶部取一个，这样你移除的是最近添加到栈中的煎饼。
# 在实现栈类时，你需要考虑列表的哪一端包含在列表中时间最短的元素。
# 这就是你想要移除并返回的元素。

class Container(object):
    """
    A container object is a list and can store elements of any type
    容器对象是一个列表，能够存储任意类型的元素。
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

class Stack(Container):
    """
    A subclass of Container. Has an additional method to remove elements.
    Container 的一个子类。额外提供了一个用于移除元素的方法。
    """
    def remove(self):
        """
        The newest element in the container list is removed
        Returns the element removed or None if the queue contains no elements
        容器列表中最新的元素已被移除
        返回被移除的元素，如果队列为空则返回 None
        """
        # Your code here
        if self.size() > 0:
            return self.myList.pop()
        else:
            return None