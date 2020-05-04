# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION

# Defines two classes, Point and NonVerticalLine.
#
# Point:
# Either no coordinate or two coordinates should be passed to __init__(),
# as floating point numbers or as integers.
# In the first case, the coordinates are set to those of the point
# at the origin.
#
# NonVerticalLine:
# No, one or two named arguments, point_1 and point_2, of type Point,
# should be passed to __init__().
# When an argument is not passed, it is set to the point at the origin.
# Both points have to determine a nonvertical line.
# Such an object can be modified by changing one point or both points
# thanks to the change_point_or_points() method.
# At any stage, the object maintains correct values for slope and intersect.


# Will be tested only when passing no, one or two arguments; moreover,
# when an argument is passed, it will be a float or an int.
class PointError(Exception):
    pass


class Point:
    def __init__(self, x=None, y=None):
        if x is not None and y is not None:
            self.x = x
            self.y = y
        elif x is None and y is None:
            # Initialise to 0
            self.x = 0
            self.y = 0
        else:
            raise PointError('Cannot create point.')


# —————————————————— Test ————————————————————————
pt = Point()
pt.x, pt.y

Point(0)

pt = Point(0, 0)
pt.x, pt.y

pt = Point(2, 4.6)
pt.x, pt.y
# ————————————————————————————————————————————————


# Will be tested only when passing no, one or two arguments,
# that have to be named; moreover, when an argument is passed,
# it will be a Point object.
class NonVerticalLineError(Exception):
    pass


class NonVerticalLine:
    def __init__(self, *, point_1=None, point_2=None):
        if point_1 is None and point_2 is None:
            raise NonVerticalLineError('Cannot create nonvertical line.')
        elif point_1 is None:
            point_1 = Point()
        elif point_2 is None:
            point_2 = Point()

        self.point_1 = point_1
        self.point_2 = point_2
        self.checker()
        self.slope = self.compute_slope()
        self.intercept = self.compute_intercept()

    def compute_slope(self):
        # k = (y1 - y2) / (x1 - x2)
        k = (self.point_1.y - self.point_2.y) / (self.point_1.x - self.point_2.x)
        return 0.0 if self.point_1.y - self.point_2.y == 0 else k

    def compute_intercept(self):
        # b = y1 - k * x1
        return self.point_1.y - self.slope * self.point_1.x

    def checker(self, mode=0):
        # mode: 0: create; 1: change
        if (self.point_1.x == self.point_2.x) or (self.point_1 == self.point_2):
            if mode == 0:
                raise NonVerticalLineError('Cannot create nonvertical line.')
            if mode == 1:
                raise NonVerticalLineError('Cannot perform this change.')

    def change_point_or_points(self, point_1=None, point_2=None):
        if point_1 is not None:
            self.point_1 = point_1
        if point_2 is not None:
            self.point_2 = point_2
        if point_1 is not None and point_2 is not None:
            self.point_1 = point_1
            self.point_2 = point_2
        self.checker(1)
        self.slope = self.compute_slope()
        self.intercept = self.compute_intercept()


# —————————————————————— Test ———————————————————————
x = NonVerticalLine()
# quiz_7.NonVerticalLineError: Cannot create nonvertical line.

NonVerticalLine(pt)
# TypeError: __init__() takes 1 positional argument but 2 were given

line = NonVerticalLine(point_1=pt)
line.point_1.x, line.point_1.y, line.point_2.x, line.point_2.y

line = NonVerticalLine(point_2=pt)
line.point_1.x, line.point_1.y, line.point_2.x, line.point_2.y

NonVerticalLine(point_1=pt, point_2=pt)
# quiz_7.NonVerticalLineError: Cannot create nonvertical line.

p1 = Point(1, 2)
p2 = Point(4, 4)
line = NonVerticalLine(point_1=p1, point_2=p2)
line.slope
line.intercept

p3 = Point(1, 5)
NonVerticalLine(point_1=p1, point_2=p3)
# quiz_7.NonVerticalLineError: Cannot create nonvertical line.
line = NonVerticalLine(point_1=p1, point_2=p2)
line.change_point_or_points()
line.slope
line.intercept
line.change_point_or_points(point_2=p1)
# quiz_7.NonVerticalLineError: Cannot perform this change.
line.slope
line.change_point_or_points(point_2=p3)
# quiz_7.NonVerticalLineError: Cannot perform this change.
line.slope


p4 = Point(6, 2)
line.change_point_or_points(point_2=p4)
line.slope
line.intercept

p5 = Point(3, 1)
line.change_point_or_points(point_1=p5)
line.slope
line.intercept
line.change_point_or_points(point_1=p4)
# quiz_7.NonVerticalLineError: Cannot perform this change.
line.slope
line.change_point_or_points(point_1=p2, point_2=p1)
line.slope
line.intercept
# ———————————————————————————————————————————————————


