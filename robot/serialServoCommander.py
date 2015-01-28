import serial
from threading import Thread
import time
from Queue import Queue



pos = 0

class SerialComms(Thread):
    ser = None

    def __init__(self):
        print "starting serial"
        Thread.__init__(self)
        self.ser = serial.Serial(port='/dev/ttyUSB0',
                        baudrate=115200,
                        timeout=0.0001)
        self.running = True
        self.queue = Queue()
        print "serial connection stabilished, starting thread"


    def run(self):
        print "thread running"
        while self.running:

            if not self.queue.empty():
                f = self.queue.get()
                self.ser.readall()
                f()
                time.sleep(0.01)
            else:
                time.sleep(0.01)
            # data= self.ser.readall()
            # if len(data):
            #     print data
        self.ser.close()


    def send_16(self, value):
        high = chr(value >> 8)
        low = chr(value % 256)
        self.ser.write(low)
        self.ser.write(high)

    def move_servo_to(self, servo, pos):
        self.ser.write(">$a")
        self.ser.write(chr(servo))
        self.send_16(pos)

    def read_imu(self):
        self.ser.write(">$c")