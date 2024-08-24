import machine
import utime
from ssd1306 import SSD1306_I2C
import network
import urequests
from utime import sleep_ms
from machine import RTC
import ntptime

 #wifi
WIFI_SSID = "V2022"
WIFI_PASSWORD = "ShivaniS2003"
SERVER_URL = "https://envg2kxy7ptz.x.pipedream.net"
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
while not wifi.isconnected():
    utime.sleep(1)

print("Connected to Wi-Fi")

# Define buzzer and OLED pins
buzzer_pin = 2 # Change this to the pin connected to the buzzer
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))  # Change the pins based on your setup
oled = SSD1306_I2C(128, 64, i2c)

# Define medication schedule in seconds (adjust as needed)
# Initialize buzzer
buzzer = machine.Pin(buzzer_pin, machine.Pin.OUT)

lis=[13,14,15]
lis1=[9,10,12,14,15,17,19,21,23,25]
def next_time(i,j):
    activate_buzzer()
    print(i)
    print(j)
    i=lis[i]
    j=lis1[j]
    message1 = f"Next medication in {i}: {j}"
    display_message(message1)
    send_message_to_phone(message1)

def send_message_to_phone(message):
    try:
        # Send a message to the server
        response = urequests.post(SERVER_URL, data=message)
        print("Sent message:", message)
        print("Server response:", response.text)
        response.close()
        utime.sleep(10)  # Send message every 30seconds
    except Exception as e:
        print("Error:", e)
        utime.sleep(5)

def activate_buzzer():
    # Function to activate the buzzer
    buzzer.value(1)  # Set buzzer pin to HIGH
    utime.sleep(1)   # Buzz for 1 second
    buzzer.value(0)  # Set buzzer pin to LOW


def display_message(message, duration=2):
    # Function to display a message on the OLED screen
    oled.fill(0)  # Clear the display
    oled.text(message, 0, 0)
    oled.show()
    utime.sleep(duration)

def main():
    global k
    global u
    k=0
    u=0
    print("Medication Schedule Program Started")
    try:
        i=1
        while True:
                        
            # Read the current date and time
            current_time = RTC().datetime()

            # Read the time when the RTC was last synced
            last_synced_time = RTC().datetime()

            # If the RTC was never synced before, initialize it with the current time
            if last_synced_time[0] == 2000:
                ntptime.settime()

            # If the RTC was synced more than a day ago, synchronize it again with the current time
            if (current_time[0] * 10000 + current_time[1] * 100 + current_time[2]) - \
               (last_synced_time[0] * 10000 + last_synced_time[1] * 100 + last_synced_time[2]) > 1:
                ntptime.settime()

            print("Current date and time: {}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                current_time[0], # Year
                current_time[1], # Month
                current_time[2], # Day
                current_time[4], # Hour
                current_time[5], # Minute
                current_time[6]   # Second
            ))
            if i==1:
                activate_buzzer()  # alert msg by Activating the buzzer
            message1='Hello'
            display_message(message1)# Display message on OLED
          # Activate the buzzer
            for i in lis:
                for j in lis1:
                    u+=1
                    if u==7:
                        u=0
                    if i==current_time[4] and j==current_time[5]:
                        if(u==0):
                            k=k+1
                            if(k==3):
                                k=0
                        activate_buzzer()
                        message3 = "Time to take medication!"
                        display_message(message3)  # Display message on OLED
                        send_message_to_phone(message3)
                        next_time(k,u)
                    if u==7:
                        k+=1
                          
    except KeyboardInterrupt:
        print("\nMedication Schedule Program Terminated")

if __name__ == "__main__":
    main()
