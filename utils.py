# from tkinter import *
import os
import sys
import glob
import json
import math

from Body import Body
from collections import namedtuple
from estimate_keypoints import SKP


Coordinate = namedtuple("Coordinate", ["x", "y"])
SkeletonKeypoints = namedtuple("SkeletonKeypoints", ["joints", "confidences", "id"])

RES_PATH = 'arts_res'
SKP_PATH = 'skp_output'

def load_res():
    def mk_dir(path):
        if not os.path.isdir(path):
            print('[INFO] make folder')
            return True if os.mkdir(path) else False
        return True

    def get_file_basename(path):
        return os.path.splitext(os.path.basename(path))[0]

    arts_res = set()
    skp_res = set()
    print('[INFO] check folder')

    if mk_dir(RES_PATH):
        arts_res = set(map(get_file_basename, glob.glob(os.path.join(RES_PATH, '*.jpg'))))
        print('[INFO] check arts resources: {} files'.format(len(arts_res)))

    if mk_dir(SKP_PATH):
        skp_res = set(map(get_file_basename, glob.glob(os.path.join(SKP_PATH, '*.json'))))
        print('[INFO] check skp resources: {} files'.format(len(skp_res)))

    diff = arts_res.difference(skp_res)
    if diff:
        skp = SKP()
        for i in diff:
            skp.get_skp_from_pic(os.path.join(RES_PATH, '{}.jpg'.format(i)))


def get_distance(vector1, vector2):
    d = 0
    for a,b in zip(vector1, vector2):
        d += (a-b)**2
    return d**0.5


def find_closest(basename, detected_skps):
    """
    basename: basename of json file
    me: skps
    """
    def load_arts_skp(basename):
        with open(os.path.join(SKP_PATH, "{}.json".format(basename))) as f:
            return json.loads(f.read())

    dist_map = [[-1]*len(detected_skps) for i in range(len(detected_skps))]
    # print(dist_map)

    # json data
    res = load_arts_skp(basename)
    # (x, y) = me.get_head_coordinates()

    body = Body()
    for index_i, i in enumerate(detected_skps):
        body.set_body(i)
        head = body.get_head_coordinates()
        for index_j, j in enumerate(res):
            dist = get_distance(head, res[j]['head'])
            # print(head, dist)
            dist_map[index_i][index_j] = dist

    print(dist_map)
    for i in dist_map:
        for j in i:
            print(j)
    # print((x, y))
    # print(res)

    min_distance = sys.maxsize
    min_id = 10


        # dist = get_distance((x, y), (res[i]['head'][0], res[i]['head'][1]))
    #     print("dist:", dist)
    #     if min_distance > dist:
    #         min_distance = dist
    #         min_id = i

    return min_id


def load_res_by_persons(num):
    res_support = glob.glob(os.path.join(RES_PATH, '{:03d}_*.jpg'.format(num)))
    if not res_support:
        return [os.path.join(RES_PATH, '999_000.jpg')]
    return res_support


if __name__ == "__main__":
    bodies = [
        SkeletonKeypoints(
            joints=[
                Coordinate(x=241.25, y=78.75), Coordinate(x=233.75, y=121.25), Coordinate(x=201.25, y=116.25), 
                Coordinate(x=188.75, y=168.75), Coordinate(x=196.25, y=203.75), Coordinate(x=263.75, y=126.25),
                Coordinate(x=258.75, y=181.25), Coordinate(x=251.25, y=211.25), Coordinate(x=198.75, y=211.25), 
                Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=236.25, y=218.75), 
                Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=236.25, y=68.75), 
                Coordinate(x=248.75, y=73.75), Coordinate(x=226.25, y=73.75), Coordinate(x=261.25, y=81.25)
            ],
            confidences=[
                0.9365450143814087, 0.8258265256881714, 0.7434385418891907, 
                0.5684559941291809, 0.20085489749908447, 0.7587136030197144, 
                0.2790355086326599, 0.1256263554096222, 0.28881335258483887, 
                0.0, 0.0, 0.29619401693344116,
                0.0, 0.0, 0.9608742594718933,
                0.9468154311180115, 0.8347669243812561, 0.8204925060272217
            ], 
            id=0
        ), 
        
        SkeletonKeypoints(
            joints=[
                Coordinate(x=133.75, y=53.75), Coordinate(x=138.75, y=113.75), Coordinate(x=96.25, y=131.25), 
                Coordinate(x=98.75, y=153.75), Coordinate(x=-1.0, y=-1.0), Coordinate(x=176.25, y=91.25), 
                Coordinate(x=178.75, y=121.25), Coordinate(x=156.25, y=93.75), Coordinate(x=133.75, y=228.75), 
                Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=176.25, y=228.75), 
                Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=116.25, y=53.75), 
                Coordinate(x=138.75, y=41.25), Coordinate(x=103.75, y=78.75), Coordinate(x=153.75, y=48.75)
            ], 
            confidences=[
                0.8488292694091797, 0.6395670175552368, 0.6180622577667236, 
                0.21119025349617004, 0.0, 0.48279309272766113, 
                0.21377024054527283, 0.5299386978149414, 0.21255280077457428, 
                0.0, 0.0, 0.22222042083740234, 
                0.0, 0.0, 0.8606398105621338, 
                0.9005011320114136, 0.8303616046905518, 0.20512905716896057
            ], 
            id=1
            )
        ]

    # for i in bodies:
    #     body = Body()
    #     body.set_body(i)
    #     id = find_closest("001_002", body)
    #     print(id)

    # print(load_res_by_persons(5))
    id = find_closest("002_002", bodies)
    print(id)
    pass
