import cv2
import mediapipe as mp

#llama al modulo
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)

#image=cv2.VideoCapture.read(cap)
#height, width, _ = image.shape

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH ))   # float `width`
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
    

with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        
        frame = cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = face_detection.process(frame_rgb)

        #graficar los 6 puntos y la caja automaticamente
        '''
        if result.detections is not None:
            for detection in result.detections:
                mp_drawing.draw_detection(frame, detection,
                    mp_drawing.DrawingSpec(color=(0,255,255), circle_radius=5),
                    mp_drawing.DrawingSpec(color=(255,0,255)))
        '''

        if result.detections is not None:
            for detection in result.detections:
                #bounding Box
                xmin= int(detection.location_data.relative_bounding_box.xmin*width)
                #print(xmin)
                ymin = int(detection.location_data.relative_bounding_box.ymin*height)
                #print(ymin)
                w= int(detection.location_data.relative_bounding_box.width* width)
                h= int(detection.location_data.relative_bounding_box.height*height)
                cv2.rectangle(frame, (xmin, ymin),(xmin+w,ymin+h),(0,255,0),2)
                #cv2.circle(frame,(xmin, ymin),1,(255,0,255),2)
                #cv2.circle(frame,(xmin+w,ymin+h),1,(255,0,255),2)
                posx = xmin+w/2
                posy = ymin+h/2
                print("Posicion: ",posx, posy)
                print("Diferencial: ",width/2-posx, height/2-posy)
        cv2.imshow("Frame",frame)
        k=cv2.waitKey(1) & 0xFF
        if k ==27:
            break
cap.release()
cv2.destroyAllWindows

