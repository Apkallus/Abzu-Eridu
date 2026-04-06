from dateutil import parser

# =============================================================================
# EXAMPLE: Workout class
# =============================================================================
class Workout(object):
    """A class to keep track of workouts"""

    # Class variable to compute calories burned from workout time
    cal_per_hr = 200
    
    def __init__(self, start, end, calories=None):
        """Creates a workout class;  start and end are strings representing
        the start and end time (e.g., "1/1/2021 1:23 PM");  
        calories is an optional float specifying the calories burned 
        in the workout"""
        # note use of dateutil.parser to convert strings to datetime objects
        self.start = parser.parse(start)  
        self.end = parser.parse(end)
        self.icon = '😓'
        self.type = 'Workout'
        self.calories = calories

    def get_calories(self):
        """Return the total calories burned in the workout"""
        if (self.calories == None):
            # calc the calories based on the length of the workout and cal_per_hr
            return Workout.cal_per_hr * (self.end - self.start).total_seconds() / 3600.0
        else:
            return self.calories

    def get_duration(self):
        """Return the duration of the workout, as a datetime.interval object"""
        return self.end-self.start

    def get_start(self):
        """Return the start time of the workout, as a datetime.datetime object"""
        return self.start

    def set_calories(self, calories):
        """Set the calories of the workout to calories"""
        self.calories = calories

    def set_start(self, start):
        """Set the start time of the workout to the supplied start string"""
        self.start = parser.parse(start)

    def get_type(self):
        """Return the type of the workout as a string"""
        return self.type

    def __eq__(self, other):
        """Returns true if this workout is equal to another workout, false o.w."""
        # the \ breaks up the line
        return type(self) == type(other) and \
                self.start == other.start and \
                self.end == other.end and \
                self.type == other.type and \
                self.get_calories() == other.get_calories()

    def __str__(self):
        """Return a text-based graphical depiction of the workout"""
        width = 16
        retstr =  f"|{'–'*width}|\n"
        retstr += f"|{' ' *width}|\n"
        retstr += f"| {self.icon}{' '*(width-3)}|\n"  #assume width of icon is 2 chars - len('🏃🏽‍♀️');  doesn't do what you'd expect
        retstr += f"| {self.type}{' '*(width-len(self.type)-1)}|\n"
        retstr += f"|{' ' *width}|\n"
        duration_str = str(self.get_duration())
        retstr += f"| {duration_str}{' '*(width-len(duration_str)-1)}|\n"
        cal_str = f"{round(self.get_calories(),1)}"
        retstr += f"| {cal_str} Calories {' '*(width-len(cal_str)-11)}|\n"

        retstr += f"|{' ' *width}|\n"
        retstr +=  f"|{'_'*width}|\n"

        return retstr


# =============================================================================
# EXAMPLE: Subclass of workout to represent a swimming workout
# 示例：表示游泳锻炼的锻炼子类
# =============================================================================
class SwimWorkout(Workout):
    """Subclass of workout to representing swimming
        锻炼的子类，用于表示游泳"""
    
    # redefine class variable cal_per_hr
    cal_per_hr = 400
    
    def __init__(self, start, end, pace=2, calories=None, numlaps=0):
        """Create a new instance of a swimming workout, where start and
        end are strings representing the start and end time of the workout,
        and pace is the pace of the workout in min/100yd, and calories
        is an optional parameter specifying the calories burned in the workout
        创建一个新的游泳锻炼实例，
        其中`start`和`end`是表示锻炼开始和结束时间的字符串，
        `pace`是锻炼的配速，单位为分钟/100码，
        `calories`是一个可选参数，用于指定锻炼中消耗的卡路里。
        """
        super().__init__(start,end,calories)
        self.icon = '🏊‍'
        self.type = 'Swimming'
        self.pace = pace
        self.numlaps = numlaps

    def get_pace(self):
        """Return the pace of the workout
            返回锻炼的节奏"""
        return self.pace
    
    def get_calories(self):
        """Return the total calories burned in the swim workout
           using the SwimWorkout cal_per_hr class variable
           返回游泳锻炼中消耗的总卡路里
           使用 SwimWorkout 类的 cal_per_hr 变量"""
        if (self.calories == None):
            # calc the calories based on the length of the workout and cal_per_hr
            return SwimWorkout.cal_per_hr * (self.end - self.start).total_seconds() / 3600.0
        else:
            return self.calories
    
    def count_lap(self):
        '''当调用时，将`numlaps`的值增加1'''
        self.numlaps += 1

    def get_average_laptime(self):
        '''计算训练的平均每圈时间。如果`numlaps`为零，则返回`None`'''
        if self.numlaps == 0:
            return None
        return self.get_duration()/self.numlaps
        
    def __str__(self):
        """Return a text-based graphical depiction of the workout"""
        # 重写`__str__`魔法方法，使其显示圈数（Num Laps）
        width = 16
        retstr =  f"|{'–'*width}|\n"
        retstr += f"|{' ' *width}|\n"
        retstr += f"| {self.icon}{' '*(width-3)}|\n"  #assume width of icon is 2 chars - len('🏃🏽‍♀️');  doesn't do what you'd expect
        retstr += f"| {self.type}{' '*(width-len(self.type)-1)}|\n"
        retstr += f"|{' ' *width}|\n"
        duration_str = str(self.get_duration())
        retstr += f"| {duration_str}{' '*(width-len(duration_str)-1)}|\n"
        cal_str = f"{round(self.get_calories(),1)}"
        retstr += f"| {cal_str} Calories {' '*(width-len(cal_str)-11)}|\n"
        #
        retstr += f"| {self.numlaps} Num Laps {' '*(width-len(str(self.numlaps))-11)}|\n"
        #
        retstr += f"|{' ' *width}|\n"
        retstr +=  f"|{'_'*width}|\n"

        return retstr
    
    def end_swim_workout(self):
        print(f'Workout Complete\n{self}')

# Exercise 1: Modify the Swim Workout Class 
# 练习1：修改游泳训练类
# 1) Create a new attribute for swim workout called numlaps
# 1) 为游泳训练类创建一个新属性，命名为`numlaps`（圈数）

# 2) Write a new method count_lap which updates numlaps by +1 if called. 
# 2) 编写一个新方法`count_lap`，当调用时，将`numlaps`的值增加1。

# 3) Write a new method get_average_laptime which calculates the average 
# laptime for a workout. If numlaps is zero, return None. 
# Hint: what does get_duration() return?)
# 3) 编写一个新方法`get_average_laptime`，用于计算训练的平均每圈时间。如果`numlaps`为零，则返回`None`。
# 提示：`get_duration()`返回的是什么？

# 4) Overwrite the __str__ dunder method to display Num Laps
# 4) 重写`__str__`魔法方法，使其显示圈数（Num Laps）。

# 5) Write a new method end_swim_workout which prints Workout Complete and 
# the Workout summary given by the updated __str__ dunder method
# 5) 编写一个新方法`end_swim_workout`，打印“训练完成”以及由更新后的`__str__`魔法方法提供的训练总结。



# Exercise 2: Using the New Class 
# 练习2：使用新类
# 1) Create a new swim workout starting at '9/30/2021 2:20 PM', ending at '9/30/2021 2:50 PM'
# 1) 创建一个新的游泳训练，开始时间为'2021年9月30日 下午2:20'，结束时间为'2021年9月30日 下午2:50'
e2 = SwimWorkout('9/30/2021 2:20 PM', '9/30/2021 2:50 PM')
# 2) Swim 40 laps
# 2) 游40圈
for i in range(40):
    e2.count_lap()
# 3) Print average laptime
# 3) 打印平均每圈时间
print(e2.get_average_laptime())
# 4) Display workout summary
# 4) 显示训练总结    
e2.end_swim_workout()





    
        


