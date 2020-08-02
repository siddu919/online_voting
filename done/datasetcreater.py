import cv2
import numpy as np
import pymysql


faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
#vediocapture object
cam=cv2.VideoCapture(0);

conn=pymysql.connect(host="localhost",user="root",passwd="",db="pythonmysql")
mycursor=conn.cursor()
'''
mycursor.execute("""create table people
(
ID int primary key,
Name varchar(20),
Sex varchar(20),
UID varchar(20) not null
)
""")
'''
ID=str(input('ENTER ID'))
name=str(input('enter name'))
sex=str(input("enter sex"))
uid=str(input("enter uid"))

sql="insert into people(ID,Name,Sex,UID) values(%s,%s,%s,%s)"
val=(ID,name,sex,uid)
mycursor.execute(sql,val)
print("entered")
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
    if(sn>15):
        break;
cam.release()
cv2.destroyAllWindows()
