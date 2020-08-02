import pymysql
conn=pymysql.connect(host="localhost",user="root",passwd="",db="pythonmysql")
mycursor=conn.cursor()
UID=str(input("enter uid"))
choice=str(input("enter choice"))
try:
    vote="insert into voted(UID,Votedfor) values(%s,%s)"
    val=(UID,choice)
    mycursor.execute(vote,val)
    conn.commit()
    conn.close()
    print("voted succefully")
except:
    print("already voted")
