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
        #self.inputBufferBarrels=[]

    def setup(self):
        #Funzione da aggiornare ogni volta che si aggiunge un setup
        self.setupSerial()
    def useIData(self):
        print(f"\nHo ricevuto un id {self.inputBuffer[1]+self.inputBuffer[2]+self.inputBuffer[3]}")
        requests.post("http://127.0.0.1:8080/", data=self.inputBuffer[1]+self.inputBuffer[2]+self.inputBuffer[3])
    def useLevelData(self):
        print(f"\nId_fusto: {self.inputBuffer[1]+self.inputBuffer[2]+self.inputBuffer[3]}")
        print(f"\nHo ricevuto i dati sul livello {self.inputBuffer[4]}")
        requests.post("http://127.0.0.1:8080/level", data=self.inputBuffer[1]+self.inputBuffer[2]+self.inputBuffer[3]+self.inputBuffer[4])
        #1,2,3 è l'ID
        #4 è lo stato
        #Da collegare con il server

    def loop(self):
        id_packet=False #Variabile che mi dice se il pacchetto che sto leggedo è un ID
        state_packet=False #Come sopra ma con lo stato
        while(True):
            if self.ser is not None:
                if self.ser.in_waiting>0:
                    lastchar=self.ser.read(1).decode('utf-8')

                    if lastchar =='C' and id_packet is False and state_packet is False:
                        id_packet=True
                    elif lastchar=='S' and id_packet is False and state_packet is False:
                        state_packet=True

                    if lastchar=='\n':
                        if id_packet is True:
                            self.useIData()
                            self.inputBuffer=[]
                            id_packet=False
                        elif state_packet is True:
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