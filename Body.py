import json
from collections import namedtuple
from typing import Sequence
from collections import namedtuple
from json import JSONEncoder
import numpy as np


Coordinate = namedtuple("Coordinate", ["x", "y"])
SkeletonKeypoints = namedtuple("SkeletonKeypoints", ["joints", "confidences", "id"])

class Keypoint:
    def __init__(self, points):
        self.x = dict(points._asdict())['x']
        self.y = dict(points._asdict())['y']
    
    def to_tuple(self):
        return (round(self.x, 2), round(self.y, 2))


class Body:
    def __init__(self):
        self.body = None
        self.head_coordinates = (.0, .0)

    def set_body(self, body):
        self.body = body._asdict()["joints"]
        self.head_coordinates = Keypoint(self.body[0]).to_tuple()

    def get_head_coordinates(self):
        return self.head_coordinates

    # def parser(self):
    #     for keypoint in self.body:
    #         self.parsed_keypoint.append(Keypoint(keypoint).to_tuple())
    #     return self.parsed_keypoint

    def angle(self, B, A, C):
        # calculate the angle of A
        try:
            a = np.array(A)
            b = np.array(B)
            c = np.array(C)
            e1, e2 = (c-a, b-a)
            num = np.dot(e1, e2)
            denom = np.linalg.norm(e1) * np.linalg.norm(e2)
            angle = np.arccos(num/denom) * 180 / np.pi
            return int(angle)
        except Exception as e:
            return -1

    def association_point(self, key):
        return ((1, key+1) if key in [5, 8, 11] else (key-1, key+1))

    def calculate_angles(self):
        angles_list = []
        evaluate_position = [1, 2, 3, 5, 6, 8, 9, 11, 12]
        for i in evaluate_position:
            (pre, nex) = self.association_point(i)
            angle = self.angle(self.body[pre], self.body[i],self.body[nex])
            angles_list.append(angle)
        return angles_list

    def compare_skps_angles(self, error_rate, standard):
        """
        1. error rate, 2. standard angles answer, 3. user angles
        """
        without_empty = list()
        correct_score = 0
        user = self.calculate_angles()
        for x, y in zip(user, standard):
            if not (x < 0 or y < 0):
                without_empty.append(abs(x-y))
        for i in without_empty:
            if i < error_rate:
                correct_score += int(100 / len(without_empty))
        return correct_score


if __name__ == "__main__":
    bodies = [SkeletonKeypoints(joints=[Coordinate(x=394.66668701171875, y=272.0), Coordinate(x=426.66668701171875, y=442.66668701171875), Coordinate(x=266.66668701171875, y=453.3333435058594), Coordinate(x=224.0, y=730.6666870117188), Coordinate(x=-1.0, y=-1.0), Coordinate(x=597.3333740234375, y=442.66668701171875), Coordinate(x=682.6666870117188, y=752.0), Coordinate(x=490.66668701171875, y=720.0), Coordinate(x=288.0, y=933.3333740234375), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=480.0, y=976.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=352.0, y=240.0), Coordinate(x=426.66668701171875, y=229.33334350585938), Coordinate(x=309.3333435058594, y=261.3333435058594), Coordinate(x=490.66668701171875, y=218.6666717529297)], confidences=[0.9431966543197632, 0.8282583951950073, 0.7755342125892639, 0.6829060912132263, 0.0, 0.8233133554458618, 0.7878410220146179, 0.840853750705719, 0.29739099740982056, 0.0, 0.0, 0.32887616753578186, 0.0, 0.0, 0.9171513319015503, 0.9690274596214294, 0.7840135097503662, 0.9125882983207703], id=0)]

    for i in bodies:
        body = Body()
        body.set_body(i)
        print(body.calculate_angles())
        print(body.get_head_coordinates())
