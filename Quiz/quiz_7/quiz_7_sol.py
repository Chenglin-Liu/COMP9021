# Written by Eric Martin for COMP9021


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
class Point:
    def __init__(self, x=None, y=None):
        if x is None and y is None:
            self.x = 0
            self.y = 0
        elif x is None or y is None:
            raise PointError('Cannot create point.')
        else:
            self.x = x
            self.y = y


class PointError(Exception):
    pass


# Will be tested only when passing no, one or two arguments,
# that have to be named; moreover, when an argument is passed,
# it will be a Point object.
class NonVerticalLine:
    def __init__(self, *, point_1=Point(), point_2=Point()):
        if not self._check_and_initialise(point_1, point_2):
            raise NonVerticalLineError('Cannot create nonvertical line.')

    def change_point_or_points(self, *, point_1=None, point_2=None):
        if not self._change_point_or_points(point_1, point_2):
            raise NonVerticalLineError('Cannot perform this change.')

    def _check_and_initialise(self, p1, p2):
        if p1.x == p2.x:
            return False
        self._update(p_1=p1, p_2=p2)
        return True

    def _change_point_or_points(self, p1, p2):
        if not p1 and not p2:
            return True
        if p1 and p2:
            if p1.x == p2.x:
                return False
            self._update(p1, p2)
            return True
        if p1:
            if p1.x == self.point_2.x:
                return False
            self._update(p_1=p1)
            return True
        if p2:
            if p2.x == self.point_1.x:
                return False
            self._update(p_2=p2)
            return True

    def _update(self, p_1=None, p_2=None):
        if p_1:
            self.point_1 = p_1
        if p_2:
            self.point_2 = p_2
        self.slope = (self.point_2.y - self.point_1.y) /\
                             (self.point_2.x - self.point_1.x)
        self.intercept = self.point_1.y - self.slope * self.point_1.x


class NonVerticalLineError(Exception):
    pass

