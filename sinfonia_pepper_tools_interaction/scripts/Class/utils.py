import cv2
from cv_bridge import CvBridge
import os
import sys


class Utils:

    def __init__(self,source, percent_of_face):
        self.source = source
        self.percent_of_face = percent_of_face
        self.bridge = CvBridge()

    def setProps(self, people,frame_size):
        props = []
        prop = 0
        for face_detected in people:
            pi = (face_detected['faceRectangle']['left'],face_detected['faceRectangle']['top'])
            pf = (face_detected['faceRectangle']['left']+face_detected['faceRectangle']['width'],face_detected['faceRectangle']['top']+face_detected['faceRectangle']['height'])
            prop = (face_detected['faceRectangle']['width']*face_detected['faceRectangle']['height'])
            # guarda el calculo de las proporciones en cada ciclo
            props.append({"pi": pi, "pf": pf, "prop": round(prop*100/float(frame_size), 4)})
        return props

    def take_picture_source(self):
        source = self.source
        print("take picture from source {}", format(source))
        if source == 1:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            frame = cv2.GaussianBlur(frame, (5, 5), 0)
            cap.release()
        elif source == 2:
            ROOT_PATH = os.path.dirname(sys.modules['__main__'].__file__)
            frame = cv2.imread(ROOT_PATH+"/Resources/gente2.jpg")
        else:
            rospy.wait_for_service("sIA_take_picture")
            takePicture = rospy.ServiceProxy("sIA_take_picture", TakePicture)
            imageRos = takePicture("Take Picture", [0, 2, 11, 30]).response
            frame = self.bridge.imgmsg_to_cv2(imageRos, "bgr8")
        return frame

    def add_features_to_image(self, frame, people):
        frame_size = frame.shape[0]*frame.shape[1]
        percent = []
        isInFront = False
        if people:
            font = cv2.FONT_HERSHEY_SIMPLEX
            props = self.setProps(people,frame_size)
            for prop in props:
                cv2.rectangle(frame, prop['pi'], prop['pf'], (0, 255, 0), 3)
                cv2.putText(frame, str(prop['prop']), prop['pi'], font, 1, (255, 150, 0), 2, cv2.LINE_AA)

            if 'name' in people[0]:
                cv2.putText(frame, str(people[0]['name']), props[0]['pi'], font, 1, (255, 150, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, str(props[0]["prop"])+'%', props[0]['pi'], font, 1, (255, 150, 0), 2, cv2.LINE_AA)
            
            if props[0]['prop'] > self.percent_of_face:
                isInFront = True
                # Remarca la cara mayor
                cv2.rectangle(frame, props[0]['pi'],props[0]['pf'], (0, 0, 255), 5)
        response = {"frame": self.bridge.cv2_to_imgmsg(frame, "bgr8"), "isInFront": isInFront}
        return response
