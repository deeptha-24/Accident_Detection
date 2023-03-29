import cv2
from detection import AccidentDetectionModel
import numpy as np
import os

model = AccidentDetectionModel("model.json", '123.h5')
font = cv2.FONT_HERSHEY_SIMPLEX


class Camera(object):

    def __init__(self):
        self.video = cv2.VideoCapture('cars3.mp4')
        self.prob=0

    def probability(self):
        while True:
            ret, frame = self.video.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(gray_frame, (250, 250))
            pred, self.prob = model.predict_accident(roi[np.newaxis, :, :])
            if pred == "Accident":
                self.prob = (round(self.prob[0][0] * 100, 2))
            return self.prob


    def startapplication(self):

        while True:
            ret, frame = self.video.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(gray_frame, (250, 250))

            pred, self.prob = model.predict_accident(roi[np.newaxis, :, :])
            if pred == "Accident":
                self.prob = (round(self.prob[0][0] * 100, 2))
                if self.prob>65:
                    print("Alert Hospital")
                    print(self.prob)

            # to beep when alert:
            # if(prob > 90):
            #     os.system("say beep")

                # cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
                # cv2.putText(frame, pred + " " + str(self.prob), (20, 30), font, 1, (255, 255, 0), 2)

            # if cv2.waitKey(33) & 0xFF == ord('q'):
            #     return
            ret, jpg = cv2.imencode('.jpg', frame)
            return jpg.tobytes()

#
# if __name__ == '__main__':
#     startapplication()