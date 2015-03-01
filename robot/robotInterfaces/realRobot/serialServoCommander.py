import serial
from threading import Thread
import time
from queue import Queue
import time


pos = 0

class SerialComms(Thread):
    ser = None

    def __init__(self):
        print ("starting serial")
        Thread.__init__(self)
        self.ser = serial.Serial(port='/dev/ttyUSB0',
                        baudrate=115200,
                        timeout=0.0001)
        self.input_pins = 15
        self.running = True
        self.imu = [0,0,0]
        self.queue = Queue()
        print ("serial connection stabilished, starting thread")


    def run(self):
        print ("thread running")
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
        self.serwrite(">$b")
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
        self.serwrite(">$c")
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
            # print("----------------------------------------")
            # print("sending value:", value)
            high = chr(value >> 8)
            low = chr(value % 256)
            if ord(low) > 128:
                print ("bugou")
            # print("encoded:", ord(high) , ord(low),  (ord(high)<<8) + ord(low))
            # print("high:", ord(high))
            # print("low:", ord(low))
            # self.serwrite(low)
            # print(bin(ord(high)), bin(ord(low)))
            # print (len(bin(ord(low)))-2)
            self.serwrite(low)
            self.serwrite(high)
            check = ord(low)^ord(high)
            # print("chk:",check)
            self.serwrite(chr(check))
            # print("-----------")


        except Exception as e:
            print ("SERIAL ERROR!" , e)

    def serwrite(self, s):
       self.ser.write(bytes(s, 'UTF-8'))


    def move_servo_to(self, servo, pos):
        self.serwrite(">$a")
        self.serwrite(chr(servo))
        self.send_16(pos)
        time.sleep(0.01)
        # print(self.ser.readall().decode())
        # for i in range(10):
        #     # print (self.ser.read(1))
        #     if 'a' in str(self.ser.read(1)):
        #         if '!' in str(self.ser.read(1)):
        #             print("ok!")
        #             return
