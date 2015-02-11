import serial
from threading import Thread
import time
from Queue import Queue
import time


pos = 0

class SerialComms(Thread):
    ser = None

    def __init__(self):
        print "starting serial"
        Thread.__init__(self)
        self.ser = serial.Serial(port='/dev/ttyUSB1',
                        baudrate=115200,
                        timeout=0.0001)
        self.input_pins = 15
        self.running = True
        self.imu = [0,0,0]
        self.queue = Queue()
        print "serial connection stabilished, starting thread"


    def run(self):
        print "thread running"
        while self.running:

            if not self.queue.empty():
                f = self.queue.get()
                # self.ser.readall()
                f()
                # time.sleep(0.01)
            else:
                time.sleep(0.001)
            # data= self.ser.readall()
            # if len(data):
            #     print data
        self.ser.close()

    def read_pins(self):
        self.ser.write(">$b")
        buff = ""
        start = time.time()
        while "pins:" not in buff:
            if time.time() - start > 0.05:
                return
            buff += self.ser.read(1)
        try:
            self.ser.read(1)
            data = ord(self.ser.read(1)) & 0b00001111
        except:
            return
        # print "data:", data , buff
        self.input_pins = data

    def read_imu(self):
        self.ser.write(">$c")
        buff = ""
        start = time.time()
        while "imu:" not in buff:
            if time.time() - start > 0.05:
                return
            buff += self.ser.read(1)

        buff = buff.split("imu:")[-1]
        while "!<" not in buff:
            if time.time() - start > 0.05:
                return
            try:
                data = self.ser.read(1)
                buff += data
            except:
                pass
        imu = buff.split("!<")[0]
        self.imu = imu.split(',')
        try:
            self.imu = [float(i)/10 for i in self.imu]
        except:
            self.imu = [0,0,0]


    def send_16(self, value):
        try:
            high = chr(value >> 8)
            low = chr(value % 256)
            self.ser.write(low)
            self.ser.write(high)
        except:
            print "SERIAL ERROR!"

    def move_servo_to(self, servo, pos):
        self.ser.write(">$a")
        self.ser.write(chr(servo))
        self.send_16(pos)
        for i in range(10):
            if 'a' in self.ser.read(1):
                if '!' in self.ser.read(1):
                    # print "ok!"
                    return
