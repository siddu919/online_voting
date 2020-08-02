import os
import cv2
import numpy as np
from PIL import Image

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
path=os.path.join(BASE_DIR,"dataSet")
recognizer=cv2.face.LBPHFaceRecognizer_create()
def getid(path):
    imagepaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    IDs=[]
    for imagepath in imagepaths:
         faceimage=Image.open(imagepath).convert("L");
         image_array=np.array(faceimage,"uint8")
         ID=int(os.path.split(imagepath)[-1].split('.')[1])
         faces.append(image_array)
         IDs.append(ID)
         cv2.imshow("training",image_array)
         cv2.waitKey(100)
    return faces,np.array(IDs)
faces,Ids=getid(path)
recognizer.train(faces,Ids)
recognizer.save('recognizer/trainingData.yml')
cv2.destroyAllWindows()
          
            
            

