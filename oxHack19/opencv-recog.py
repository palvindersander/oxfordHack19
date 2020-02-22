import numpy as np
import cv2 as cv
import io
import os
#from google.cloud import vision
#from google.cloud.vision import types
#from google.cloud import storage

#client = vision.ImageAnnotatorClient()

def detect_document(path):
    global client
    file_name = os.path.abspath(path)
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.document_text_detection(image=image)
    print(response.full_text_annotation.pages)
    
def det_text(path):
    global client
    file_name = os.path.abspath(path)
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    for text in texts:
        print('\n"{}"'.format(text.description))
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices)))

imo = cv.imread('./Test Data/img.png')
imoriginal = cv.imread('./Test Data/img.png')
img = cv.cvtColor(imo, cv.COLOR_BGR2GRAY)
(thresh, imb) = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

def rescale_frame(frame, wpercent=50, hpercent=50):
    width = int(frame.shape[1] * wpercent / 100)
    height = int(frame.shape[0] * hpercent / 100)
    return cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)

ret, thresh = cv.threshold(imb, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
contours = contours[1:]
hierarchy = hierarchy[0][1:]
cv.drawContours(imo, contours, -1, (0,255,0), 1)
for a in range(0,len(contours)):
    if hierarchy[a][3] != 0:
        pass
    else:
        cnt  = contours[a]
        x,y,w,h = cv.boundingRect(cnt)
        if a%3 == 0:
            colour = (255,0,0)
        elif a%3 == 1:
            colour = (0,255,0)
        elif a%3 == 2:
            colour = (0,0,255)
        M = cv.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv.circle(imo, (cx, cy), 4, (255, 0, 255),-1)
        cv.rectangle(imo,(x,y),(x+w,y+h),colour,1)
        letter = imoriginal[y:y+h,x:x+w]
        letter = cv.copyMakeBorder( letter, 10, 10, 10, 10, cv.BORDER_CONSTANT, value=(255,255,255))
        cv.imwrite("./output/"+str(a)+".jpg",letter)
        #det_text("./output/"+str(a)+".jpg")
        cv.destroyAllWindows()
        cv.imshow('letters',letter)
        cv.waitKey(0)
        
cv.imshow("recog", rescale_frame(imo))          
cv.waitKey(0)
cv.destroyAllWindows()
