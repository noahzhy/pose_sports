import cv2


class VideoControl:
    def __init__(self, video='sports_res_video/squat_001.avi'):
        self.video = video
        self.cap = cv2.VideoCapture(self.video)
        self.wait_frame = int(1000/self.cap.get(cv2.CAP_PROP_FPS))
        self.key_frame = 45
        self.status_stop = True

    def start_video(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                cv2.imshow('frame', frame)
                # cv2.waitKey(self.wait_frame)
                if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.key_frame:
                    self.status_stop = True
                    while True:
                        cv2.waitKey(1)
                        if not self.status_stop:
                            break
                    
                if cv2.waitKey(self.wait_frame) & 0xFF == ord('q'):
                    break
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 1)

        self.cap.release()
        cv2.destroyAllWindows()

    def continue_video(self):
        self.status_stop = False

    def stop_video(self):
        self.status_stop = True

    def set_key_frames(self, key_frame):
        self.key_frame = key_frame


if __name__ == "__main__":
    # vc = VideoControl()
    # t1 = threading.Thread(target=vc.start_video, name='control')
    # t1.start()

    # time.sleep(3)
    # print("continue_video")
    # vc.continue_video()
    # time.sleep(5)
    # print("continue_video")
    # vc.continue_video()
    pass
