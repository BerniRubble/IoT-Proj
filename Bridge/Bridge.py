import serial
import serial.tools.list_ports
import requests

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

    def useLevelData(self):
        print(f"\nId_fusto: {self.inputBuffer[1]+self.inputBuffer[2]+self.inputBuffer[3]}")
        print(f"\nHo ricevuto i dati sul livello {self.inputBuffer[4]}")
        requests.post("http://iotproj.ddns.net/level", data=self.inputBuffer[1]+self.inputBuffer[2]+self.inputBuffer[3]+self.inputBuffer[4])
        #1,2,3 è l'ID
        #4 è lo stato


    def loop(self):
        state_packet=False
        while(True):
            if self.ser is not None:
                if self.ser.in_waiting>0:
                    lastchar=self.ser.read(1).decode('utf-8')

                    if lastchar=='S' and state_packet is False:
                        state_packet=True

                    if lastchar=='\n':

                        if state_packet is True:
                            self.useLevelData()
                            self.inputBuffer = []
                            state_packet =False
                    else:
                        #E' inutile salvarsi nel buffer il carattere terminatore
                        self.inputBuffer.append(lastchar)




if __name__ == '__main__':
    br=Bridge()
    br.setup()
    br.loop()