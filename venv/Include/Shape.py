import random
from Point import Point


class Circle:

    def __init__(self, p0, r):
        self.p0 = p0
        self.r = r

    def randPoint(self): 
        while(True):
            tmpX = random.uniform(self.p0.x - self.r, self.p0.x + self.r)
            tmpY = random.uniform(self.p0.y - self.r, self.p0.y + self.r)
            point = Point(tmpX, tmpY)
            if self.check(point):
                break
        return point

    def check(self, point):
        check = True
        tmp = (point.x - self.p0.x) ** 2 + (point.y - self.p0.y) ** 2
        if tmp > self.r:
            check = False
        return check

class Rectangle:

    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        
    def randPoint(self):
        tmpX = random.uniform(self.p0.x, self.p1.x)
        tmpY = random.uniform(self.p0.y, self.p1.y)
        point = Point(tmpX, tmpY)
        return point

class Line:

    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        self.a = (p0.y - p1.y)/(p0.x - p1.x)
        self.b = p0.y - self.a * p0.x

    def randPoint(self):
        tmpX = random.uniform(self.p0.x, self.p1.x)
        tmpY = self.a * tmpX + self.b
        point = Point(tmpX, tmpY)
        return point