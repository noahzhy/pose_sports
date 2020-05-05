import cv2


class VideoControl:
    def __init__(self):
        self.video = 'sports_res_video/squat_001.avi'
        self.cap = cv2.VideoCapture(self.video)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.key_frame = 45

    def start_video(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                cv2.imshow('frame', frame)

                if int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)) == self.key_frame:
                    cv2.waitKey(0)

                if cv2.waitKey(int(1000/self.fps)) & 0xFF == ord('q'):
                    break
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 1)

    def continue_video(self):
        cv2.waitKey(int(1000/self.fps))
        # self.cap.release()
        # cv2.destroyAllWindows()

if __name__ == "__main__":
    vc = VideoControl()
    vc.start_video()
    vc.continue_video()
