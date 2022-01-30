import RPi.GPIO as GPIO
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from time import sleep
import threading

GPIO.setmode(GPIO.BCM)

# init list with pin numbers

pinList = [22, 23, 17, 27]
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
servo1 = GPIO.PWM(12,50)
servo1.start(0)
servo2 = GPIO.PWM(13,50)
servo2.start(0)
print ("Waiting for 2 seconds")
time.sleep(2)
duty1=0
A1=90
duty2=0
A2=90
# loop through pins and set mode and state to 'high'

for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

SleepTimeL = 6
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


db = firestore.client()

# CREATE OPERATION
db.collection('output1').document('Laser').set(
     {
         'status' : True
     }
)
db.collection('output2').document('MLX').set(
  {
         'status' : True
     }
)
db.collection('output3').document('Servo_1').set(
     {
         'status' : 3
     }
)
db.collection('output4').document('Servo_2').set(
     {
         'status' : 3
     }
)

# READ OPERATION
while True:
    readStatus01 = db.collection('output2').document('MLX').get()
    docDict = readStatus01.to_dict()
    Laserstatus = docDict['status']


    if(Laserstatus== True):
          GPIO.output(22, GPIO.HIGH)
        
        
    else :
        GPIO.output(22, GPIO.LOW)
        print ("MLX")

    readStatus02 = db.collection('output1').document('Laser').get()
    docDict = readStatus02.to_dict()
    MLXstatus = docDict['status']
    if(MLXstatus== True):
          GPIO.output(23, GPIO.HIGH)
        
        
    else :
        GPIO.output(23, GPIO.LOW)
        print ("Lasser")
    
    readStatus03 = db.collection('output3').document('Servo_1').get()
    docDict = readStatus03.to_dict()
    Servo_1_status = docDict['status']
    if(Servo_1_status== 0): 
        duty1=A1/18+2
        print (A1)
        sleep(2)
        if (A1<=180) and (A1>=0) :
            for i in range(0,100):
                servo1.ChangeDutyCycle(duty1)
            A1=A1+10
        else:
            print("Not Valid Angle Value_1") 
            A=90
            servo1.ChangeDutyCycle(duty1)
         

    elif(Servo_1_status== 1):
        duty=A1/18+2
        print (A1)
        sleep(2)
        if (A1<=180) and (A1>=0) :
            for i in range(0,100):
                servo1.ChangeDutyCycle(duty1)
            A1=A1-10   
        else:
            print("Not Valid Angle Value_1") 
            A1=90 
            servo1.ChangeDutyCycle(duty1)
        
    else :
        sleep(2)
        servo1.ChangeDutyCycle(duty1)

    readStatus04 = db.collection('output4').document('Servo_2').get()
    docDict = readStatus04.to_dict()
    Servo_2_status = docDict['status']
    if(Servo_2_status== 0): 
        duty2=A2/18+2
        print (A2)
        sleep(2)
        if (A2<=180) and (A2>=0) :
            for i in range(0,100):
                servo2.ChangeDutyCycle(duty2)
            A2=A2+10
        else:
            print("Not Valid Angle Value_2") 
            A2=90
            servo2.ChangeDutyCycle(duty2)
         

    elif(Servo_2_status== 1):
        duty2=A2/18+2
        print (A2)
        sleep(2)
        if (A2<=180) and (A2>=0) :
            for i in range(0,100):
                servo2.ChangeDutyCycle(duty2)
            A2=A2-10   
        else:
            print("Not Valid Angle Value_2") 
            A2=90 
            servo2.ChangeDutyCycle(duty2)
        
    else :
        sleep(2)
        servo2.ChangeDutyCycle(duty2)


