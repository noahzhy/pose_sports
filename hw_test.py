import pyrealsense2 as rs
import numpy as np
import cv2

pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 320, 240, rs.format.bgr8, 30)
pipe.start(config)

try:
    while True:
        frames = pipe.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        cv2.namedWindow("preview", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("preview", color_image)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

finally:
    pipe.stop()