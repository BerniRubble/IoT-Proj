import serial
import serial.tools.list_ports

class Bridge():

    def setupSerial(self):

        self.ser=None
        print("Available ports: ")
        ports=serial.tools.list_ports.comports()

        self.port_name=None
        for port in ports:
            print(port.device)
            print(port.description)

            if 'arduino' or 'dispositivo' in port.description.lower():
                self.port_name=port.device
        print(f'Connecting to: {self.port_name}')

        try:
            if self.port_name is not None:
                self.ser=serial.Serial(self.port_name, 9600, timeout=0)
        except:
            self.ser = None

        self.inputBuffer=[]

    def setup(self):
        #Funzione da aggiornare ogni volta che si aggiunge un setup
        self.setupSerial()
    def loop(self):
        while(True):
            if self.ser is not None:
                if self.ser.in_waiting>0:
                    self.inputBuffer.append(self.ser.read(1))
                    for character in self.inputBuffer:
                        print(character.decode('utf-8'))


if __name__ == '__main__':
    br=Bridge()
    br.setup()
    br.loop()