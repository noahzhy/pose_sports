import pyrealsense2 as rs
import numpy as np
import threading
import platform
import argparse
import time
import cv2
import os

from pprint import pprint
from cubemos.core.nativewrapper import CM_TargetComputeDevice
from cubemos.core.nativewrapper import initialise_logging, CM_LogLevel
from cubemos.skeleton_tracking.nativewrapper import Api, SkeletonKeypoints

from Body import *
from VideoControl import *
from utils import *
from test_code import *


# correct answer maintain time (seconds)
correct_maintain_time = 3
correct_rate = 72
confidence_threshold = 0.35
# skeleton_color = np.random.randint(256, size=3).tolist()
skeleton_color = (0, 255, 0)

pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 320, 240, rs.format.bgr8, 30)
pipe.start(config)

keypoint_ids = [
    (1, 2), (1, 5), (2, 3), (3, 4), (5, 6), (6, 7), (1, 8), (8, 9), (9, 10),
    (1, 11), (11, 12), (12, 13), (1, 0), (0, 14), (14, 16), (0, 15), (15, 17),
]


def default_log_dir():
    if platform.system() == "Windows":
        return os.path.join(os.environ["LOCALAPPDATA"], "Cubemos", "SkeletonTracking", "logs")
    elif platform.system() == "Linux":
        return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "logs")
    else:
        raise Exception("{} is not supported".format(platform.system()))


def default_license_dir():
    if platform.system() == "Windows":
        return os.path.join(os.environ["LOCALAPPDATA"], "Cubemos", "SkeletonTracking", "license")
    elif platform.system() == "Linux":
        return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "license")
    else:
        raise Exception("{} is not supported".format(platform.system()))


def check_license_and_variables_exist():
    license_path = os.path.join(default_license_dir(), "cubemos_license.json")
    if not os.path.isfile(license_path):
        raise Exception(
            "The license file has not been found at location \"" +
            default_license_dir() + "\". "
        )
    if "CUBEMOS_SKEL_SDK" not in os.environ:
        raise Exception(
            "The environment Variable \"CUBEMOS_SKEL_SDK\" is not set. "
        )


def get_valid_limbs(keypoint_ids, skeleton, confidence_threshold):
    limbs = [
        (tuple(map(int, skeleton.joints[i])),
         tuple(map(int, skeleton.joints[v])))
        for (i, v) in keypoint_ids
        if skeleton.confidences[i] >= confidence_threshold
        and skeleton.confidences[v] >= confidence_threshold
    ]
    valid_limbs = [
        limb
        for limb in limbs
        if limb[0][0] >= 0 and limb[0][1] >= 0 and limb[1][0] >= 0 and limb[1][1] >= 0
    ]
    return valid_limbs


def render_result(skeletons, img, confidence_threshold):
    for index, skeleton in enumerate(skeletons):
        limbs = get_valid_limbs(keypoint_ids, skeleton, confidence_threshold)
        for limb in limbs:
            cv2.line(
                img,
                limb[0],
                limb[1],
                skeleton_color,
                thickness=2,
                lineType=cv2.LINE_AA
            )


def run():
    try:
        check_license_and_variables_exist()
        sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
        api = Api(default_license_dir())
        model_path = os.path.join(
            sdk_path,
            "models",
            "skeleton-tracking",
            "fp32",
            "skeleton-tracking.cubemos"
        )
        api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)

        body = Body()
        vc = VideoControl()
        t1 = threading.Thread(target=vc.start_video, name='control')
        t1.start()

        while True:
            frames = pipe.wait_for_frames()
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            color_image = cv2.flip(color_image, 1)

            skeletons = api.estimate_keypoints(color_image, 192)
            new_skeletons = api.estimate_keypoints(color_image, 192)
            new_skeletons = api.update_tracking_id(skeletons, new_skeletons)
            render_result(skeletons, color_image, confidence_threshold)

            standard = [52, 105, -1, 34, 156, 26, 176, 29, 62]
            correct_score_list = list()

            for i in skeletons:
                body.set_body(i)
                correct_score_list.append(
                    body.compare_skps_angles(10, standard))

            # global correct_score
            correct_score = max(correct_score_list) if correct_score_list else 0

            if correct_score+50 >= correct_rate:
                cv2.putText(color_image, "success: {}".format(
                    correct_score+50), (20, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                vc.continue_video()
            else:
                cv2.putText(color_image, "correct score: {}".format(
                    correct_score+50), (20, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

            cv2.namedWindow("preview", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("preview", color_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    except Exception as ex:
        print("Exception occured: \"{}\"".format(ex))

    finally:
        pipe.stop()
        quit()


if __name__ == "__main__":
    run()
