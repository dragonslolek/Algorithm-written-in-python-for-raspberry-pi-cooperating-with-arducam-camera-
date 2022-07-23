from picamera import PiCamera
import time
import cv2
import imutils
import numpy as np
from PIL import Image
import pytesseract

while True:
    camera = PiCamera()
    camera.resolution = (1200, 720)
    camera.vflip = True
    time.sleep(2)
    camera.capture("image1.jpg")

    zdj = cv2.imread('image1.jpg',cv2.IMREAD_COLOR)

    wyszarzoneZdjecie = cv2.cvtColor(zdj, cv2.COLOR_BGR2GRAY) 				
    wyszarzoneZdjecie = cv2.bilateralFilter(wyszarzoneZdjecie, 11, 17, 17) 		
    wkrawedzie = cv2.Canny(wyszarzoneZdjecie, 30, 200) 					

    konturyNaZdjeciu = cv2.findContours(wkrawedzie.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    konturyNaZdjeciu= imutils.grab_contours(konturyNaZdjeciu)
    konturyNaZdjeciu= sorted(konturyNaZdjeciu, key = cv2.contourArea, reverse = True)[:10]
    screen = None
   											
    for c in konturyNaZdjeciu:							
        p = cv2.arcLength(c, True)
        app = cv2.approxPolyDP(c, 0.022 * p, True)
        
        if len(app) == 4:
            screen = app
            break

    if screen is None:         
        znaleziono = 0
        print ("Brak tablic rejestracyjnych")
    else:
        znaleziono = 1

    if znaleziono == 1:						
        cv2.drawContours(zdj, [screen], -1, (0, 255, 0), 3)				
    mask = np.zeros(wyszarzoneZdjecie.shape,np.uint8)
    noweZdj = cv2.drawContours(mask,[screen],0,255,-1,)
    noweZdj = cv2.bitwise_and(zdj,zdj,mask=mask)
								
    (x, y) = np.where(mask == 255)
    (gorax, goray) = (np.min(x), np.min(y))
    (dolx, doly) = (np.max(x), np.max(y))
    wycieteZdjecie = wyszarzoneZdjecie[gorax:dolx+5, goray:doly+5]

    numer = pytesseract.image_to_string(wycieteZdjecie,config='--psm 13 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"')
    print("Wykryta tablica:",numer)
   