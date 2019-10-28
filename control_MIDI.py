import distance_sensor
import time
import math
import RPi.GPIO as GPIO
import socket
import argparse


class MIDI_Distance_Controller():
    
    def __init__(self, cc=11, rate=0.12):
        if cc=='ask':
            self.cc = input("MIDI CC value: ")
        else:
            self.cc = cc
        self.rate=rate
    
    def initialize_sockets(self, port = 3000, shortport=3001):
        self.s = self.open_socket(port)
        s2 = self.open_socket(shortport)
        if s2 == None or self.s == None:
            print("Sockets failed, exiting")
            return -1
        try:
            s2.send((str(self.cc) + ';').encode())
        except UnicodeDecodeError as err:
            print("FAILED to send value %s,\nerror: %s" %(message, err))
            return -1
        self.close_socket(s2)
        return 0
    
    def open_socket(self, port):
        # opens socket and connects to given port
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("Socket error: ", err)
        host = '127.0.0.1'
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            print("Connection Refused on port", port)
            return
        return s
    
    def calibrate(self):
        self.d = distance_sensor.Distance_Sensor()
        #self.no_input = self.get_no_input()
        self.ceiling = self.get_ceiling()
        self.floor = self.get_floor()
        self.region_size = self.ceiling - self.floor
        self.multiplier = 127/self.region_size
        #print(self.no_input, self.ceiling, self.floor, self.region_size)
        ##TODO reverse mode?
    
    def get_no_input(self):
        input('\nClear sensing area and press Enter to begin calibration.')
        minval = 10000
        print('Calibrating...')
        for i in range(5):
            dist = self.d.distance()
            if i > 1 and dist < minval:
                minval = dist
            time.sleep(self.rate)
        if minval < 100:
            print('Warning: calibration may have been unsuccessful')
        return minval

    def get_ceiling(self):
        input('\nPlace hand at maximum end of sensing region (MIDI = 127) and press Enter')
        maxval = 0
        print('Calibrating...')
        for i in range(5):
            dist = self.d.distance()
            if i > 1 and dist > maxval:
                maxval = dist
            time.sleep(self.rate)
        return maxval
        
    def get_floor(self):
        input('\nPlace hand at minimum end of sensing region (MIDI = 0) and press Enter')
        minval = 1000
        print('Calibrating...')
        for i in range(5):
            dist = self.d.distance()
            if i > 1 and dist < minval:
                minval = dist
            time.sleep(self.rate)
        return minval

    def control_MIDI(self):
        try:
            print('Controlling MIDI')
            while(True):
                dist = self.d.distance()
                if dist <= self.ceiling and dist >= self.floor:
                    midi_val = math.floor((dist-self.floor)*self.multiplier)
                    self.send2Pd(midi_val)
                time.sleep(self.rate)
            
        except KeyboardInterrupt:
            print('\nMIDI Control stopped by User')
            return
    
    def send2Pd(self, message = ''):
        try:
            self.s.send((str(message) + ';').encode())
            print("Sent MIDI Value %s  \r" %(message), end="")
        except UnicodeDecodeError as err:
            print("FAILED to send value %s,\nerror: %s" %(message, err))

    def test_MIDI(self):
        try:
            print('Sensing MIDI')
            while(True):
                dist = self.d.distance()
                if dist <= self.ceiling and dist >= self.floor:
                    midi_val = math.floor((dist-self.floor)*self.multiplier)
                    print("MIDI Value Sensed: ", midi_val)
                time.sleep(self.rate)
            
        except KeyboardInterrupt:
            print('\nMIDI Control stopped by User')
            return
    
    def close_socket(self, s):
        # shuts down and closes socket
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        
    def __del__(self):
        if self.s != None:
            self.close_socket(self.s)


def getArgs():
    parser = argparse.ArgumentParser(description='Distance-sensing MIDI controller')
    parser.add_argument('-c', '--cc_value', type=int,\
         required=False, default=11, choices=range(0,128), help='continuous controller number')
    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = getArgs()
        m = MIDI_Distance_Controller(args.cc_value)
        m.calibrate()
        if m.initialize_sockets() >=0:
            m.control_MIDI()
        else:
            print("Socket connection unsuccessful. MIDI values will not be sent.")
            m.test_MIDI()
        
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("\nMeasurement stopped by User")
        del m
