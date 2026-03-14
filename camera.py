import cv2

class CameraStream:
    def __init__(self, sources):
        """
        sources: list of camera indices or video paths
        """
        self.caps = [cv2.VideoCapture(src) for src in sources]

    def read_frames(self):
        frames = []
        for cap in self.caps:
            ret, frame = cap.read()
            if not ret:
                frame = None
            frames.append(frame)
        return frames

    def release(self):
        for cap in self.caps:
            cap.release()