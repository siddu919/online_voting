import cv2
import numpy as np
from PIL import Image
import pickle
import pymysql

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
#vediocapture object
cam=cv2.VideoCapture(0);
rec=cv2.face.LBPHFaceRecognizer_create();
rec.read("recognizer\\trainingData.yml")


def getprofile(id):
    conn=pymysql.connect(host="localhost",user="root",passwd="",db="pythonmysql")
    mycursor=conn.cursor()
    sql="select * from people where id="+str(id)
    mycursor.execute(sql)
    profile=None
    for row in mycursor:
        profile=row
    conn.close()
    return profile

n=0
flag=0
while(True):
    ret,img=cam.read();
    do="not redistred"
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        profile=getprofile(id)
        if(profile!=None):
            cv2.putText(img,str(profile[0]),(x,y+h+30),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255, 0, 255))
            cv2.putText(img,str(profile[1]),(x,y+h+60),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0, 255, 255))
            cv2.putText(img,str(profile[2]),(x,y+h+90),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255, 255, 0))
            cv2.putText(img,str(profile[3]),(x,y+h+120),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0, 255, 255))
        else:
            cv2.putText(img,str(do),(x,y+h+30),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255, 0, 255))
          
    cv2.imshow("face",img);
    if(cv2.waitKey(1)==ord('q')):
        break;
  
cam.release()
cv2.destroyAllWindows()

uid=str(input('enter uid'))
if(uid==str(profile[3])):
    print("YES!!!...... you are allowed to voter")
    flag=1
else:
    print("No you are not autarized voter")

if(flag==1):
    choice=int(input("1.BJP\n2.CNG\n3.JDS\nenter choice:"))
    conn=pymysql.connect(host="localhost",user="root",passwd="",db="pythonmysql")
    mycursor=conn.cursor()
    try:
        vote="insert into voted(UID,Votedfor) values(%s,%s)"
        val=(uid,choice)
        mycursor.execute(vote,val)
        conn.commit()
        conn.close()
        print("voted succefully")
        if(choice==1):
            print("you voted for cng")
            conn=pymysql.connect(host="localhost",user="root",passwd="",db="pythonmysql")
            mycursor=conn.cursor()
            sql1="SELECT * FROM vote WHERE ID=1"
            count_bjp=mycursor.execute(sql1)
            for row in mycursor:
                count_bjp=row
            print(count_bjp[2])
            c=int(count_bjp[2])
            c=c+1
            sq="UPDATE vote SET Count="+str(c)+" WHERE ID=1"
            mycursor.execute(sq)
            conn.commit()
            conn.close()
        elif(choice==2):
            print("you voted for cng")
            conn=pymysql.connect(host="localhost",user="root",passwd="",db="pythonmysql")
            mycursor=conn.cursor()
            sql1="SELECT * FROM vote WHERE ID=2"
            count_cng=mycursor.execute(sql1)
            for row in mycursor:
                count_cng=row
            c=int(count_cng[2])
            c=c+1
            print(c)
            sq="UPDATE vote SET Count="+str(c)+" WHERE ID=2"
            mycursor.execute(sq)
            conn.commit()
            conn.close()
        elif(choice==3):
            print("you voted for jds")
            conn=pymysql.connect(host="localhost",user="root",passwd="",db="pythonmysql")
            mycursor=conn.cursor()
            sql1="SELECT * FROM vote WHERE ID=3"
            count_jds=mycursor.execute(sql1)
            for row in mycursor:
                count_jds=row
            print(count_jds[2])
            c=int(count_jds[2])
            c=c+1
            print(c)
            sq="UPDATE vote SET Count="+str(c)+" WHERE ID=3"
            mycursor.execute(sq)
            conn.commit()
            conn.close()
    except:
        print("already voted")
    

