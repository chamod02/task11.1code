import requests
import gpiod
import time
from secrets import THINGSPEAK_CHANNEL_ID, THINGSPEAK_READ_APIKEY # type: ignore

# GPIO Settings
PUMP_PIN = 17
CHIP = gpiod.Chip('gpiochip4')
LINE = CHIP.get_line(PUMP_PIN)
LINE.request(consumer='main', type=gpiod.LINE_REQ_DIR_OUT)

# Thresholds
MOISTURE_THRESHOLD_HIGH = 70
MOISTURE_THRESHOLD_MEDIUM = 65
MOISTURE_THRESHOLD_LOW = 60
TEMPERATURE_HIGH = 40
TEMPERATURE_MEDIUM = 30
HUMIDITY_LOW_THRESHOLD = 40

# Function to get data from ThingSpeak
def get_latest_data():
    url = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json?api_key={THINGSPEAK_READ_APIKEY}&results=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        feeds = data['feeds'][0]
        temperature = float(feeds['field1'])
        humidity = float(feeds['field2'])
        soil_moisture = float(feeds['field3'])
        sunlight = bool(int(feeds['field4']))
        return temperature, humidity, soil_moisture, sunlight
    else:
        print("Error fetching data from ThingSpeak")
        return None

# Function to determine if watering is needed
def should_water(temperature, humidity, soil_moisture, sunlight):
    duration = 0

    # Determine temperature level
    if temperature > TEMPERATURE_HIGH:
        temp_level = 3  # High
    elif temperature > TEMPERATURE_MEDIUM:
        temp_level = 2  # Medium
    else:
        temp_level = 1  # Low

    # Determine soil moisture level
    if soil_moisture > MOISTURE_THRESHOLD_HIGH:
        return False, duration  # No watering needed
    elif soil_moisture > MOISTURE_THRESHOLD_MEDIUM:
        duration = 5  # Low watering
    elif soil_moisture > MOISTURE_THRESHOLD_LOW:
        duration = 10  # Medium watering
    else:
        duration = 15  # High watering

    # Adjust duration based on humidity
    if humidity < HUMIDITY_LOW_THRESHOLD:
        duration += 5

    # Adjust duration based on sunlight
    if sunlight:
        duration += 5

    # Further adjust based on temperature
    if temp_level == 3:
        duration += 5  # Increase duration for high temperature
    elif temp_level == 1:
        duration -= 5  # Decrease duration for low temperature

    return True, duration

# Function to control the pump
def control_pump(action, duration):
    if action:
        print(f"Watering plants for {duration} seconds")
        LINE.set_value(1)
        time.sleep(duration)
        LINE.set_value(0)
    else:
        print("No need to water the plants.")

def main():
    try:
        while True:
            data = get_latest_data()
            if data:
                temperature, humidity, soil_moisture, sunlight = data
                print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Soil Moisture: {soil_moisture}, Sunlight: {'Yes' if sunlight else 'No'}")
                action, duration = should_water(temperature, humidity, soil_moisture, sunlight)
                control_pump(action, duration)
            time.sleep(60)  # Wait for 60 seconds before checking again
    except KeyboardInterrupt:
        print("Program terminated")

if __name__ == "__main__":
    main()
