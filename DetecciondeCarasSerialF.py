from ast import Global
import cv2
import mediapipe as mp
import time
import serial
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
import numpy as np
from pynput import keyboard as kb

def pulsa(tecla):
	if tecla == kb.KeyCode.from_char('q'):
		comu.write(str.encode('hh'))

escuchador = kb.Listener(pulsa)
escuchador.start()

#while escuchador.is_alive():
#	pass

#llama al modulo
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap=cv2.VideoCapture(1,cv2.CAP_DSHOW)

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH ))   # float `width`
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`7y

print("width",width,"height",height)
centrox=int(width/2)
centroy=int(height/2)
difX=0
difY=0
auxx=1
auxy=1
grafica='x'
try:
    comu = serial.Serial(port='COM3', baudrate=9600,timeout=1)
    time.sleep(2)
except:
    print("Serial no disponible")

#grafica
matplotlib.use('TkAgg')
fig = plt.figure()
global t, x, y2, dif
dif=80

t = [0]
cenx = [centrox]
x = [centrox]
ceny = [centroy]
y = [centroy]
line1, = plt.plot(np.linspace(0, width), np.linspace(0, width), 'b-')
line2, = plt.plot(np.linspace(0, height), np.linspace(0, height), 'k-')
cota=0

contador=1
with mp_face_detection.FaceDetection(min_detection_confidence=1) as face_detection:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        
        frame = cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = face_detection.process(frame_rgb)
        #Horizontal
        cv2.line(frame, (int(width/2),0), (int(width/2),height), (255,0,0),3)
        cv2.line(frame, (int(width/2)-dif,0), (int(width/2)-dif,height), (255,0,0),1)
        cv2.line(frame, (int(width/2)+dif,0), (int(width/2)+dif,height), (255,0,0),1)

        cv2.line(frame, (0,int(height/2)), (width,int(height/2)), (255,0,0),3)
        cv2.line(frame, (0,int(height/2)-dif), (width,int(height/2)-dif), (255,0,0),1)
        cv2.line(frame, (0,int(height/2)+dif), (width,int(height/2)+dif), (255,0,0),1)
        #graficar los 6 puntos y la caja automaticamente
        '''
        if result.detections is not None:
            for detection in result.detections:
                mp_drawing.draw_detection(frame, detection,
                    mp_drawing.DrawingSpec(color=(0,255,255), circle_radius=5),
                    mp_drawing.DrawingSpec(color=(255,0,255)))
        '''
        if result.detections is None and cota>50:
            try:
                comu.write(str.encode('px'))
                comu.write(str.encode('\n'))
                comu.write(str.encode('py'))
                comu.write(str.encode('\n'))
                print("cots")
                cota=0
            except:
                pass
        else:
            cota=cota+1

        if result.detections is not None:
            detection=result.detections[0]
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
            #posx = int(xmin+w/2)
            posx= int(xmin+w/2)
            posy = int(ymin+h/2)
            cv2.circle(frame,(posx,posy),5,(255,0,255))


            if posx > centrox+dif:
                auxx=1
                #difX=int((width/2-posx)*90/(width/2))
                #posx_=posx
                try:
                    comu.write(str.encode('dx'))
                    comu.write(str.encode('\n'))
                    #time.sleep(1)
                    
                    print("dx")
                except:
                    pass
            
            if posx < centrox-dif:
                auxx=1
                #posx_=posx
                try:
                    comu.write(str.encode('ix'))
                    comu.write(str.encode('\n'))
                    #time.sleep(1)
                    
                    print("ix")
                except:
                    pass
            if posx>=centrox-dif and posx<=centrox+dif and auxx==1:
                auxx=0
                #posx_=posx
                try:
                    comu.write(str.encode('px'))
                    comu.write(str.encode('\n'))
                    
                    print("px")
                except:
                    pass
            #####Y
            if auxx==0:
                if posy > centroy+dif:
                    auxy=1
                    #difX=int((width/2-posx)*90/(width/2))
                    #posy_=posy
                    try:
                        comu.write(str.encode('dy'))
                        comu.write(str.encode('\n'))
                        
                        print("dy")
                    except:
                        pass
                
                if posy < centroy-dif:
                    auxy=1
                    #posy_=posy
                    try:
                        comu.write(str.encode('iy'))
                        comu.write(str.encode('\n'))
                        
                        print("iy")
                    except:
                        pass
                if posy>=centroy-dif and posy<=centroy+dif and auxy==1:
                    auxy=0
                    #posy_=posy
                    try:
                        comu.write(str.encode('py'))
                        comu.write(str.encode('\n'))
                        
                        print("py")
                    except:
                        pass

            t.append(contador)
            x.append(posx)
            y.append(posy)
            cenx.append(centrox)
            ceny.append(centroy)
            contador=contador+1

        # update data
        if grafica=='x':
            line1.set_ydata(1*x)
            line1.set_xdata(1*t)
            line2.set_ydata(1*cenx)
            line2.set_xdata(1*t)
            fig.canvas.draw()
            
            # convert canvas to image
            img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8,
            sep='')
            img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

            # img is rgb, convert to opencv's default bgr
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            
            # display image with opencv or any operation you like
            cv2.imshow("plot",img)
        
        if grafica=='y':
            line1.set_ydata(1*y)
            line1.set_xdata(1*t)
            line2.set_ydata(1*ceny)
            line2.set_xdata(1*t)
            fig.canvas.draw()
            
            # convert canvas to image
            img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8,
            sep='')
            img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

            # img is rgb, convert to opencv's default bgr
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            
            # display image with opencv or any operation you like
            cv2.imshow("plot",img)

        
        cv2.imshow("Frame",frame)
        k=cv2.waitKey(1) & 0xFF
        
        if k ==27:
            break

cap.release()
cv2.destroyAllWindows
#comu.close()