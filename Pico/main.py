#Imported packages
##Machine package imports functions required for communicating with the microcontroller
import machine
from machine import Pin
##sleep function is used to put the board to sleep. This is done to give a buffer preventing overloading of data
import time
##From servo, the class Servo is imported that helps make controlling servos easier
from servo_old import Servo

print("DATA IMPORTED")

#Config variables
##Pin variables
ulTrigger_pin = 14
ulEcho_pin = 13

relay_pin = 15

s1_Pin = 19
s2_Pin = 18
s3_Pin = 20

s1_bufferPos = 65 

toggle_Pin = 6

##USER HAS TO INITIALIZE THIS VALUE
number_of_objects = 3

##Initial position when no object
s1_inPos = 125
s2_inPos = 65
s3_inPos = 120

##Middle poisiton for picking of object
s1_midPos = 45
s2_midPos = 0
s3_midPos = 100

##Final poisiton for placement of object
s1_finPos = 55
s2_finPos = []
#s2_finP	os = [93,121,149]
s3_finPos = 100

##For data transfer
b = None
msg = 'NO DATA'

print("GLOBAL VARIABLES DEFINED")

#Initialize pins

###SERVO
##Front and Back
s1Servo = Servo(s1_Pin)
##Left and Right
s2Servo = Servo(s2_Pin)
##Up and Down
s3Servo = Servo(s3_Pin)

###ONBOARD LED
onboardLED = Pin("LED",Pin.OUT)
onboardLED.value(1)
###ULTRASONIC
trigger = Pin(14, Pin.OUT)
echo = Pin(13, Pin.IN)

###RELAY
relay = Pin(relay_pin,Pin.OUT)
relay.value(0)
###TOGGLE PIN
##Toggle pin is for switching from UART to WIFI
toggle = Pin(toggle_Pin,Pin.IN)

button = Pin(16,Pin.IN)

print("INITIALIZE PIN")

#Setup

##If pin is not powered; function using UART
onboardLED.value(0)
uart = machine.UART(0, 115200)
print(uart)
b = 'Data sent from Pico'
msg = b.encode("utf-8")
uart.write(msg)

onboardLED.value(1)
onboardLED.value(0)
##If pin is powered; function using WIFI



def final_pos_calc(minAngle = 65,maxAngle = 170):
    angle_val = (maxAngle-minAngle)/(number_of_objects)
    s2_finPos.append(minAngle+angle_val)
    for i in range (1,number_of_objects):
        s2_finPos.append(int(s2_finPos[i-1]+angle_val))

final_pos_calc()
print(s2_finPos)


##Function for checking if object is close to arm
def ulson():
   trigger.low()
   time.sleep_us(2)
   trigger.high()
   time.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = time.ticks_us()
   while echo.value() == 1:
       signalon = time.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   if (distance <= 10):
       return(True)

##Set arm to home position
def inPos():
    print("Going to home position")
    s1Servo.servo_Angle(s1_inPos)
    time.sleep(2)
    s3Servo.servo_Angle(s3_inPos)
    time.sleep(2)
    s2Servo.servo_Angle(s2_inPos)
    time.sleep(2)    
    print("Arm at home position")

inPos()

##Set arm to picking up position
def pickPos():
    print("Going to pick object")
    s2Servo.servo_Angle(s2_midPos)
    time.sleep(2)
    s3Servo.servo_Angle(s3_midPos)
    time.sleep(2)
    s1Servo.servo_Angle(s1_bufferPos)
    time.sleep(2)
    s1Servo.servo_Angle(s1_midPos)
    time.sleep(2)
    print("Pciked object")
    #time.sleep(100000)

#Pick object and place it
def finPos(msg):
    for i in range(s1_midPos,s1_inPos):
        s1Servo.servo_Angle(i)
        time.sleep(0.15)
    time.sleep(2)
    inPos()
    time.sleep(2)
    print("Picking up object")
    s2Servo.servo_Angle(s2_finPos[msg])
    time.sleep(2)
    s1Servo.servo_Angle(s1_finPos)
    time.sleep(2)
    s3Servo.servo_Angle(s3_finPos)
    time.sleep(2)
    print("Object droppped in designated area")
    #Turn off magnetic EE
    relay.value(0)
    time.sleep(5)
    inPos()
    
onboardLED.value(0)

while (button.value() == 0):
    onboardLED.value(1)
    time.sleep(0.2)
    onboardLED.value(0)
    time.sleep(0.2)

while True:
    onboardLED.value(1)
    if ulson() == True:
        print("Object detected")
        b = 'ulson'
        msg = b.encode("utf-8")
        uart.write(msg)
        msg = 'dummy'
        while msg is 'dummy':
            if uart.any():
                b = uart.readline()
            try:
                msg = b.decode('utf-8')
            except:
                pass
        ##Activate magnetic EE
        relay.value(1)
        ##Delay for picking up objects
        time.sleep(3)
        pickPos()
        time.sleep(1)
        finPos(int(msg))
        time.sleep(1)
        
        





    