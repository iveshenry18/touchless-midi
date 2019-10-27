import requests, json


def get_weather(city_name = "denver"):
    api_key = "88d511329c5e53a2a3977464998a93a2"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    
    x = response.json()
    
    
    if x["cod"] != "404": 
  
        # store the value of "main" 
        # key in variable y 
        y = x["main"] 
  
        # store the value corresponding 
        # to the "temp" key of y 
        current_temperature = y["temp"]
        return current_temperature
        
    else:
        print("City Not Found")
        return -1
    
if __name__ == '__main__':
    city_name = input("City: ")
    temp = get_weather(city_name)
    if (temp != -1):
        print("Temperature (K): ", str(temp))
