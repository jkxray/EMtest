'''
Prologix GPIB-USB wrapper module

Author: Kon Aoki
Date: 2019-06-21

Dependency: pySerial
'''
import serial
class Prologix:
    def __init__(self, port):
        self.port = port
        self.address_var=0
        self.timeout=1 #0.1 second timeout for readline
        self.eol = '\n'
        
        self.ser = serial.Serial(port,timeout=self.timeout) #opens serial port
        self.ser.write(str.encode('++ver'+self.eol)) #asks the prologix adapter for its version for sanity check
        ans = self.ser.readline() #readback from the adapter
        self.ser.write(str.encode('++mode 1'+self.eol)) #sets adapter to controller mode
        self.ser.write(str.encode('++read_tmo_ms 100'+self.eol)) #1ms timeout for each character read
        
    def address(self, addr=None):
        if addr != None:
            self.address_var=addr
            self.ser.write(str.encode('++addr '+str(self.address_var)+self.eol)) #Note 1
        return self.address_var
    def write(self, command, addr=None):
        if addr != None:
            self.address_var=addr
            self.ser.write(str.encode('++addr '+str(self.address_var)+self.eol)) #Note 1
        type='SCPI'
        if command[0]=='+' and command[1]=='+': #checks if command is ++something
            type='Prologix'
        if type=='SCPI':
            self.listen() #Note 2
        r = self.ser.write(str.encode(command+self.eol))
        
        return r
    def readline(self, addr=None):
        if addr != None:
            self.address_var=addr
            self.ser.write(str.encode('++addr '+str(self.address_var)+self.eol)) #Note 1
        self.talk() #Note 3
        return self.ser.readline().decode().strip()
    def readlines(self, addr=None):
        if addr != None:
            self.address_var=addr
            self.ser.write(str.encode('++addr '+str(self.address_var)+self.eol)) #Note 1
        output=''
        self.talk() #Note 3
        line=self.ser.readline()
        for line in self.ser:
            output+=line.decode()
        return output
    def listen(self):
        self.ser.write(str.encode('++auto 0'+self.eol)) #Note 1
    def talk(self):
        self.ser.write(str.encode('++auto 1'+self.eol)) #Note 1
    def close():
        self.ser.close()
    def open():
        elf.ser = serial.Serial(port,timeout=self.timeout)

#Note 1: don't need to set instrument to listen because this is a prologix command
#Note 2: sets instrument to listen mode before sending a command
#Note 3: sets instrument to talk mode before reading from it
'''
#EXAMPLE
pro = Prologix('/dev/ttyUSB6')
pro.address(27)
pro.write('*IDN?')
print(pro.readline())
pro.address(12)
pro.write('*IDN?')
print(pro.readline())
pro.write('++help')
print(pro.readlines())
'''
        