import cv2
import mediapipe as mp

#llama al modulo
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

#El proceso solo se hara si la deteccion super el 0.5
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        #Abrimos imagen
        image = cv2.imread("Maick.jpg")
        #Hallamos las dimensiones de la imagen
        height, width, _ = image.shape
        #pasamos a escala RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #hacemos la magia del ML
        result = face_detection.process(image_rgb)
        #imprimimos resultados
        print("Detections: ", result.detections)

        #Acceder a todos los puntos
        if result.detections is not None:
            for detection in result.detections:
                #bounding Box
                xmin= int(detection.location_data.relative_bounding_box.xmin*width)
                print(xmin)
                ymin = int(detection.location_data.relative_bounding_box.ymin*height)
                print(ymin)
                w= int(detection.location_data.relative_bounding_box.width* width)
                h= int(detection.location_data.relative_bounding_box.height*height)
                cv2.rectangle(image, (xmin, ymin),(xmin+w,ymin+h),(0,255,0),2)

                #Ojo Derecho
                x_RE=int(detection.location_data.relative_keypoints[0].x*width)
                y_RE=int(detection.location_data.relative_keypoints[0].y*height)
                cv2.circle(image,(x_RE,y_RE),3,(255,0,255),2)

                #Ojo Derecho
                x_LE=int(detection.location_data.relative_keypoints[1].x*width)
                y_LE=int(detection.location_data.relative_keypoints[1].y*height)
                cv2.circle(image,(x_LE,y_LE),3,(255,0,255),2)

        '''
        #Dibujamos en la imagen los puntos
        if result.detections is not None:
            for detection in result.detections:
                mp_drawing.draw_detection(image, detection,
                mp_drawing.DrawingSpec(color=(255,0,255), thickness=3, circle_radius=3),
                mp_drawing.DrawingSpec(color=(0,0,255), thickness=3))
        '''
    
        #mostramos
        cv2.imshow("image",image)
        cv2.waitKey(0)
cv2.destroyAllWindows()