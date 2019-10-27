#Libraries
import RPi.GPIO as GPIO
import time
import get_weather
 
 
class Distance_Sensor:
    
    def __init__(self, trigger=4, echo=27, sonic_speed=34300):
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        
        #set GPIO Pins
        self.GPIO_TRIGGER = trigger
        self.GPIO_ECHO = echo
        self.sonic_speed = sonic_speed
        
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #, pull_up_down=GPIO.PUD_DOWN
    
    def distance(self):
        
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * self.sonic_speed) / 2
        return distance


    def get_sonic_speed(self, city = "none"):
        #takes city and returns sonic speed in cm/s based on temperature data from the openweathermap API
        if city == "ask":
            city = input("City: ")
        if city == "none" or city == "def" or city == "":
            #skips API call
            print("Using default sonic speed of 34300 cm/s")
            self.sonic_speed = 34300        
        temp_k = get_weather.get_weather(city)
        if temp_k != -1:
            temp_c = temp_k - 273.15
            ss = 100 * (331.4 + 0.6 * temp_c)
            print("Temperature (c): ", temp_c)
            print("Sonic Speed (cm/s): ", ss)
            self.sonic_speed = ss
        else:
            print("Using default sonic speed of 34300 cm/s")
            self.sonic_speed = 34300
            
    def __del__(self):
        GPIO.cleanup()
    
    
if __name__ == '__main__':
    try:
        d = Distance_Sensor()
        sleep_time = .12
        while True:
            dist = d.distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(sleep_time)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("\nMeasurement stopped by User")
        del d
