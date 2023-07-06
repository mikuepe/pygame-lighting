import pygame
import math


def rotate_point(point, origin, angle):
    print(point)
    radians = math.radians(angle)
    temp = (point[0] - origin[0], point[1] - origin[1])
    temp = (temp[0] * math.cos(radians) - temp[1] * math.sin(radians),
            temp[0] * math.sin(radians) + temp[1] * math.cos(radians))
    print(temp)


class Ray:
    def __init__(self, pos, angle):
        self._X = pos[0]
        self._Y = pos[1]

        self._angle = angle
        self._radians = math.radians(angle)
        
        self._X_dir = math.cos(self._radians)
        self._Y_dir = math.sin(self._radians)

    def __repr__(self):
        return f"({self._X} {self._Y})  {self._angle}"

    def collide_circle(self, center, radius):
        x0 = self._X
        y0 = self._Y

        x1 = self._X_dir + x0
        y1 = self._Y_dir + y0

        x2 = self.center[0]
        y2 = self.center[1]

        
        numerator = abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1))
        denominator = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return (numerator / denominator) < radius

    def collide_circle2(self, center, radius):
        newX = self._X_dir * math.cos(-self._radians) - self._Y_dir * math.sin(-self._radians)
        newY = self._X_dir * math.sin(-self._radians) + self._Y_dir * math.cos(-self._radians)
        return newX,newY
