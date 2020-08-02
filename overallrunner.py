import cv2
import numpy as np
import os
from PIL import Image
import pickle
import pymysql
import getpass
def admin():
    faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
    cam=cv2.VideoCapture(0);
    conn=pymysql.connect(host="localhost",user="root",passwd="",db="pythonmysql")
    mycursor=conn.cursor()
    print("ENTER VOTER DETAILS:...")
    ID=str(input('ENTER ID:'))
    name=str(input('ENTER NAME:'))
    sex=str(input("ENTER GENDER:"))
    uid=str(input("ENTER UID:"))
    sql="insert into people(ID,Name,Sex,UID) values(%s,%s,%s,%s)"
    val=(ID,name,sex,uid)
    mycursor.execute(sql,val)
    print("VOTER DATA IS SUCCEFULLY ENTERED IN DATABASE PLEASE PROVIDE FACIAL IMAGE")
    conn.commit()
    conn.close()
    sn=0;
    id=int(ID)
    while(True):
        ret,img=cam.read();
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        for(x,y,w,h) in faces:
            sn=sn+1;
            cv2.imwrite("dataSet/user."+str(id)+"."+str(sn)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.waitKey(100);
        cv2.imshow("face",img);
        cv2.waitKey(1);
        if(sn>50):
            break;
    cam.release()
    cv2.destroyAllWindows()
    print("THANK YOU!!!VOTER FACIAL IMG IS CAPTURED")
#training started
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
             cv2.waitKey(10)
        return faces,np.array(IDs)
    faces,Ids=getid(path)
    recognizer.train(faces,Ids)
    recognizer.save('recognizer/trainingData.yml')
    cv2.destroyAllWindows()
def people():
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
    show=0
    while(True):
        ret,img=cam.read();
        do="NOT REGISTERED"
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            profile=getprofile(id)
            if(profile!=None):
                #cv2.putText(img,str(profile[0]),(x,y+h+30),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255, 0, 255))
                cv2.putText(img,str(profile[1]),(x,y+h+30),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0, 255, 255))
                cv2.putText(img,str(profile[2]),(x,y+h+60),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255, 255, 0))
                #cv2.putText(img,str(profile[3]),(x,y+h+120),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0, 255, 255))
            else:
                cv2.putText(img,str(do),(x,y+h+30),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255, 0, 255))
                show=1
                  
        cv2.imshow("face",img);
        if(cv2.waitKey(1)==ord('q')):
            break;
  
    cam.release()
    cv2.destroyAllWindows()
    if(show==1):
        print("PLEASE!!! REGISTER BEFORE VOTING")
        exit(1)

    uid=str(input('ENTER YOUR UID:'))
    if(uid==str(profile[3])):
        print("YES!!!...... YOU ARE ALLOWED TO VOTE.....")
        flag=1
    else:
        print("No!!!!.... YOU ARE NOT AUTORIZED VOTER...")

    if(flag==1):
        choice=int(input("1.BJP\n2.CNG\n3.JDS\nENTER YOUR CHOICE:"))
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
                print("YOU VOTED FOR BJP.....")
                conn=pymysql.connect(host="localhost",user="root",passwd="",db="pythonmysql")
                mycursor=conn.cursor()
                sql1="SELECT * FROM vote WHERE ID=1"
                count_bjp=mycursor.execute(sql1)
                for row in mycursor:
                    count_bjp=row
                c=int(count_bjp[2])
                c=c+1
                sq="UPDATE vote SET Count="+str(c)+" WHERE ID=1"
                mycursor.execute(sq)
                conn.commit()
                conn.close()
            elif(choice==2):
                print("YOU VOTED FOR CNG")
                conn=pymysql.connect(host="localhost",user="root",passwd="",db="pythonmysql")
                mycursor=conn.cursor()
                sql1="SELECT * FROM vote WHERE ID=2"
                count_cng=mycursor.execute(sql1)
                for row in mycursor:
                    count_cng=row
                c=int(count_cng[2])
                c=c+1
                sq="UPDATE vote SET Count="+str(c)+" WHERE ID=2"
                mycursor.execute(sq)
                conn.commit()
                conn.close()
            elif(choice==3):
                print("YOU VOTED FOR JDS")
                conn=pymysql.connect(host="localhost",user="root",passwd="",db="pythonmysql")
                mycursor=conn.cursor()
                sql1="SELECT * FROM vote WHERE ID=3"
                count_jds=mycursor.execute(sql1)
                for row in mycursor:
                    count_jds=row
                c=int(count_jds[2])
                c=c+1
                sq="UPDATE vote SET Count="+str(c)+" WHERE ID=3"
                mycursor.execute(sq)
                conn.commit()
                conn.close()
        except:
            print("SORRY!!! YOU CAN'T VOTE MORE THAN ONCE")
    
print("***********WELCOME TO VOTING***********")
ch=int(input("1.ADMIN\n2.PEOPLE\nENTER YOUR CHOICE:"))
if(ch==1):
    psw=str(input('ENTER THE PASSWORD:'))
    if(psw=="988051"):
        admin()
    else:
        print("SORRY!!!YOU ENTERED WRONG PASSWORD")
elif(ch==2):
    people()
else:
    print("YOU ENTERED WRONG CHOICE")
            




