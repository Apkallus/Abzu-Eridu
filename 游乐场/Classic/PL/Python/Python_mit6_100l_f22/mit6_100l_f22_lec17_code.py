#################
## EXAMPLE: simple Coordinate class
#################
class Coordinate(object):
    """ A coordinate made up of an x and y value """
    def __init__(self, x, y):
        """ Sets the x and y values """
        self.x = x
        self.y = y

# c = Coordinate(3,4)
# a = 0
# origin = Coordinate(a,a)
# print(c.x)
# print(origin.x)


class Coordinate(object):
    """ A coordinate made up of an x and y numerical value """
    def __init__(self, x, y):
        """ Sets the x and y values """
        self.x = x
        self.y = y
    def getX(self):
        """ Returns how far away self is on the x axis """
        return self.x
    def getY(self):
        """ Returns how far away self is on the y axis """
        return self.y
    def distance(self, other):
        """ Returns the euclidean distance between two Coordinate objects """
        x_diff_sq = (self.x-other.x)**2
        y_diff_sq = (self.y-other.y)**2
        return (x_diff_sq + y_diff_sq)**0.5

c = Coordinate(3,4)
a = 0
origin = Coordinate(a,a)

# these 3 calls returns the same thing
#print(c.distance(origin))
#print(Coordinate.distance(c, origin))
#print(origin.distance(c))


###########################################################
################ AT HOME #####################
###########################################################
# Question 1:
# Write a class definition for a vehicle. A vehicle is defined by attributes:
# Number of wheels
# Number of occupants
# Color 
# Decide the type of each data attribute and document this
# 编写一个车辆类的定义。车辆由以下属性定义：
# 车轮数量
# 载客数量
# 颜色
# 确定每个数据属性的类型并记录如下
class car(object):
    def __init__(self, wheels, occupants, color):
        self.wheels = wheels
        self.occupants = occupants
        self.color = color

# Question 2:
# Create 2 vehicle instances using the class we wrote previously. 
# One red vehicle with 2 wheels, and 1 occupant
# One green vehicle with 18 wheels, and 3 occupants
# Print the first one's number of occupants
# Print the second one's color
# 使用我们之前编写的类创建2个车辆实例。
# 一辆红色车辆，有2个轮子和1名乘员
# 一辆绿色车辆，有18个轮子和3名乘员
# 打印第一辆车的乘员数量
# 打印第二辆车的颜色
# car1 = car(2,1,'red')
# car2 = car(18,3,'green')
# print(car1.occupants)
# print(car2.color)

# Question 3:
# Add on to the code from above for class Vehicle.
# Create another method for the vehicle class named add_n_occupants, 
# which takes in an int n. When called, self's number of occupants 
# increases by n. It returns the total occupants after the increase. 
# 在上面的Vehicle类代码基础上进行扩展。
# 为Vehicle类创建另一个名为add_n_occupants的方法，
# 该方法接收一个整数n作为参数。当调用时，self的乘员数量
# 增加n。它返回增加后的总乘员数。

class Vehicle(object):
    def __init__(self, w, o, c='black'):
        self.wheels = w
        self.occ = o
        self.color= c
        self.max_occupancy = 5
    # add method add_n_occupants here
    def add_n_occupants(self, n):
        if self.occ+n > self.max_occupancy:
            raise ValueError("out of max_occupancy")
        self.occ += n
        return self.occ
        
v1 = Vehicle(4,2,'blue')
# print(v1.occ)   # prints 2
# print(v1.add_n_occupants(3))   # prints 5
# print(v1.occ)

# Question 4:
# Add another data attribute to the Vehicle class, called max_occupancy,
# which is always 5. This attribute is not passed in as a parameter, but 
# is defined in the init.
# Modify the add_n_occupants methods such that if adding the occupants 
# exceeds the max_occupancy allowed for that vehicle, 
#   * you do not perform the increase, and
#   * you raise a ValueError with an apprpriate message
# 向Vehicle类添加另一个数据属性，名为max_occupancy，
# 该属性始终为5。此属性不作为参数传入，而是在init中定义。
# 修改add_n_occupants方法，使得如果添加的乘员数超过该车辆允许的max_occupancy，
#   * 不执行增加操作，并且
#   * 抛出一个带有适当消息的ValueError

#Question 5:
# Modify the Vehicle class __init__ such that if a vehicle is created
# without specifying a color then the color is set to "black".
# Hint: remember default parameters?
# 修改 Vehicle 类的 __init__ 方法，使得如果创建车辆时未指定颜色，则颜色默认为 "黑色"。
# 提示：还记得默认参数吗？

###########################################################


###########################################################
################ ANSWERS TO AT HOME ############
###########################################################

# Question 1
# class Vehicle(object):
#     def __init__(self, w, o, c):
#         self.wheels = w
#         self.occ = o
#         self.color= c

# Question 2
# car1 = Vehicle(2, 1, 'red')
# car2 = Vehicle(18, 3, 'green')
# print(car1.occ)
# print(car2.color)

# Question 3
# class Vehicle(object):
#     def __init__(self, w, o, c):
#         self.wheels = w
#         self.occ = o
#         self.color= c
#     # add method add_n_occupants here
#     def add_n_occupants(self, n):
#         self.occ += n
#         return self.occ

# v1 = Vehicle(4,2,'blue')
# print(v1.occ)
# print(v1.add_n_occupants(2))
# print(v1.occ)

# Question 4
# class Vehicle(object):
#     def __init__(self, w, o, c):
#         self.wheels = w
#         self.occ = o
#         self.color= c
#         self.max_occ = 5
#     def add_n_occupants(self, n):
#         new_occ = self.occ + n
#         if new_occ > self.max_occ:
#             raise ValueError("exceeded max occupancy")
#         else:
#             self.occ = new_occ
#             return self.occ

# v1 = Vehicle(4,2,'blue')
# print(v1.occ)
# print(v1.add_n_occupants(2))   # should print 4
# print(v1.add_n_occupants(2))   # should raise ValueError

# Question 5
# class Vehicle(object):
#     def __init__(self, w, o, c='black'):
#         self.wheels = w
#         self.occ = o
#         self.color= c
#         self.max_occ = 5
#     def add_n_occupants(self, n):
#         new_occ = self.occ + n
#         if new_occ > self.max_occ:
#             raise ValueError("exceeded max occupancy")
#         else:
#             self.occ = new_occ
#             return self.occ

# v1 = Vehicle(4,3,'red')
# print(v1.color)     # prints 'red'
# v2 = Vehicle(2,1)
# print(v2.color)     # prints 'black'