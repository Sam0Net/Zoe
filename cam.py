# Lo que haremos con este programa es que la camara de nuestra pc reconozca
# Objetos de determinados colores y posteriormente pinte los contornos de ese
# mismo color. 
from itertools import count
from tkinter import Frame # Crear interfaces graficas 
import cv2 # Abrir la cámara y reconocer colores. 
import numpy as np # Jugar con arreglos, resolver op matematicas 

# Función Dibujar 
def draw(mask, color, frame_arg):
    # Esta linea va encontrar contornos 
    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 1000: 
            new_countour = cv2.convexHull(c)
            cv2.drawContours(frame_arg,[new_countour], 0, color, 3)
            M = cv2.moments(c)
            if(M["m00"]==0): M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            font = cv2.FONT_HERSHEY_COMPLEX
            if color == [0, 255, 255]:
                cv2.putText(frame_arg, 'Amarillo', (x+10, y), font, 0.75, (0,255,255),1, cv2.LINE_AA)
            elif color == [0, 0, 255]:
                cv2.putText(frame_arg, 'Rojo', (x+10, y), font, 0.75, (0,0,255),1, cv2.LINE_AA)
            elif color == [255, 0, 0]:
                cv2.putText(frame_arg, 'Azul', (x+10, y), font, 0.75, (255,0,0),1, cv2.LINE_AA)

def capture():
    cap = cv2.VideoCapture(0)
    # Creamos los valores para detectar los colores rojo, amarillo y azul.
    low_yellow = np.array([25, 190, 20], np.uint8)
    high_yellow = np.array([30, 255, 255], np.uint8)
    low_red1 = np.array([0, 100, 20], np.uint8)
    high_red1 = np.array([5, 255, 255], np.uint8)
    low_red2 = np.array([175, 100, 20], np.uint8)
    high_red2 = np.array([180, 255, 255], np.uint8)
    azulBajo = np.array([100,100,20], np.uint8)
    azulAlto = np.array([125,255,255], np.uint8)

    while True:
        comp,frame = cap.read()
        if comp == True:
            # Creamos mascaras basadas en los valores de los colores que creamos anteriormente.
            frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            yellow_mask = cv2.inRange(frame_HSV, low_yellow, high_yellow)
            red_mask1 = cv2.inRange(frame_HSV, low_red1, high_red1)
            red_mask2 = cv2.inRange(frame_HSV, low_red2, high_red2)
            red_mask = cv2.add(red_mask1, red_mask2)
            azul_mask3 = cv2.inRange(frame_HSV, azulBajo, azulAlto) 

            # Dibujamos los contornos de los objetos que sean igual a los colores declarados.
            draw(yellow_mask, [0, 255, 255], frame)
            draw(red_mask, [0, 0, 255], frame)
            draw(azul_mask3,[255, 0, 0], frame) 
            cv2.imshow('Webcam', frame) 

            # Para cerrar la ventana presionamos 1 o s 
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break
    cap.release()
    cv2.destroyAllWindows() 