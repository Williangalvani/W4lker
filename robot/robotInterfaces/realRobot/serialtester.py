from serialServoCommander import SerialComms
import time

serial = SerialComms()
serial.start()
time.sleep(1)


for servo in range(5,12):
    print "servo n:", servo
    for i in range(30):
        serial.queue.put(lambda: serial.move_servo_to(servo,1500+i*10))
        time.sleep(0.5)
    serial.queue.put(lambda: serial.move_servo_to(servo, 1500))
    time.sleep(0.5)

