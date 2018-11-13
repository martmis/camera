from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
import sys
import cv2
from pyzbar import pyzbar


class Camera(QDialog):
    def __init__(self):
        super(Camera, self).__init__()
        uic.loadUi("camera.ui", self)
        self.image = None
        self.startCam.clicked.connect(self.start_clicked)
        self.capCam.clicked.connect(self.cap_clicked)
        self.camera_on = False
        self.show()


    def cap_clicked(self):
        self.timer.stop()
        cv2.imwrite('cam.png',self.image)


    def start_clicked(self):
        # this 0 is a port num
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera_on = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        ret,self.image = self.camera.read()
        self.image = cv2.flip(self.image,1)
        frame = QImage(
            self.image,
            self.image.shape[1],
            self.image.shape[0],
            self.image.shape[1] * 3,
            QImage.Format_RGB888
        )
        self.cam.setPixmap(QPixmap.fromImage(frame))
        self.cam.show()


def main():
    app = QApplication(sys.argv)
    ex = Camera()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()