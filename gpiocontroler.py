from machine import Pin
from utime import sleep
import network
import socket
from time import sleep
import machine
import rp2
import sys
#setting up all the variables and lists
pins = []
pinled = Pin("LED", Pin.OUT)
for i in range(28):
    pins.append(Pin(i+1, Pin.OUT))
valid_inputs_menu = ["1","2","3","4","5","6","7","8","I","i","Q","q","h","9","10","11","12","c",1,2,3,4,5,6,7,8,9,1,11,12]
valid_numbers = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28"]
valid_numbers_input = ["1","0",1,0]
gpio_total_states = []
gpio_pins_on = []
gpio_pins_off = []
action_info = {"1":"You can set a pin GPIO state to HIGH or LOW. unfortunately, the pins are set to OUT mode, so they cannot resive signals. This mode is meant to specially test the power output of ONE gpio pin.","2":"You can see the state of ONE gpio pin. It will print out 1 or 0. If it prints out 1, then it is on. If it prints out 0, then it it off.","3":"A list of all the GPIO pins that are ON right now.","4":"Lists out all the pins that are OFF right now.", "5":"Tests pins, one by one, and will turn them no for a duration of 3 sec, and then will turn it off to go to the next pin. This is meant for individual pins.  You may connect your pico to a breadboard with LEDS to see if the pins work.","6":"Blinks the LED around 10 times.","7":"Turns all the gpio pins ON. You can check the state of the pins by pressing 3.","8":"Turns all the GPIO OFF. You can check with with #4.","h":"This menu. Tells you more about the commands that this runs","q":"Quits the script. Runs a cleanup function that turn OFF all the pins for a clean shutdown. If this script crashes, run it again and press Q to clean it up.", "9":"Settings:Lets you change your pico version for more options, depending on what model you have", "10":"Lets you, on pico w, set up a network connection. Type in your ssid and password, and you can test it out with function [11].","11":"Checks the pico wifi by pinging a website you choose. Not ips, but you will be able to ping ips soon.","12":"Tells you the IP of the pico, but you can see this on the top of the menu anyway."}
userinput = None
ssid_func = None
global pico_version
global ip
ip = None
pico_version = "1"
network_timeout = 10
network_time = 0
#checking Pico Version, IDK how to get this automatic.

print("Welcome to Pico GPIO Controller! The most advanced controller to ever exist(i think.)")
print("Made by Gobrowse")
print("")
def optionboard():
    if pico_version == "2W" or pico_version == "W":
        global ip
        global wlan
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if wlan.isconnected() ==  True:
            ip = wlan.ifconfig()[0]
        else:
            ip = "0.0.0.0"
    print("Pico Version:", pico_version)
    if pico_version == "2W" or pico_version == "W":
        global ip
        print("IP is,", ip)
    print("What do you want to do?")
    print("[1] Set GPIO state")
    print("[2] See GPIO state")
    print("[3] See all GPIO pins that are ON")
    print("[4] See all GPIO pins that are OFF")
    print("[5] Test all GPIO pins (Get a Voltmeter!)")
    print("[6] See if LED works")
    print("[7] Turn ALL GPIO on")
    print("[8] Turn ALL GPIO off")
    print("[9] Settings")
    if pico_version == "W" or pico_version == "2W":
        print("[10] Connect to Wifi")
        print("[11] Check Wifi of Pico")
        print("[12] Check Pico IP")
    print("[c] Run CleanUp script")
    print("[i or h] Get more detailed description of each action")
    print("[q] Quit")
    choice = str(input("Press the # or letter to choose one: "))
    if not (choice in valid_inputs_menu):
        print("invalid Option. Choose again.")
    else:
        actions(choice)

def connect(ssid,password):
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    timeout = 20
    timenow = 0
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        timenow = timenow + 1
        print('Waiting for connection...')
        sleep(1)
    if timenow == timeout and wlan.isconnected() == False:
        print("Timeout:", timeout)
        optionboard()
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    optionboard()

def ping(target_host,port):
    print("Pinging {}...".format(target_host))
    addr = socket.getaddrinfo(target_host, port)[0][-1]
    # Create a socket and connect
    pingsocket = socket.socket()
    pingsocket.connect(addr)
    # Send a simple HTTP GET request
    request = 'GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(target_host)
    pingsocket.send(request)
    # Wait for a response
    response = pingsocket.recv(1024)
    print("Ping successful! Response received from {}.")
    pingsocket.close()
    optionboard()


def actions(userinput):
    if userinput == 1 or userinput == "1":
        print("GPIO state is being set. What GPIO pin do you want to set up? (GPIO #, ex: gpio 2 = 2. DO NOT PUT LETTERS) ")
        pin_setup = input()
        if not (pin_setup in valid_numbers):
            print("invalid input. ")
            optionboard()
        else:
            pin_setup = int(pin_setup)
            print("What value you want to set? (1 is high and 0 is low) ")
            pin_value = input()
            if not (pin_value in valid_numbers_input):
                print("invalid input. quitting")
                optionboard()
            else:
                pin_value = int(pin_value)
                if (pin_setup <= len(pins)) and (pin_setup > 0):
                    pins[pin_setup - 1].value(pin_value)
                    print("Set Pin ", pin_setup, "to value ", pin_value)
                    optionboard()
                else:
                    print("Something went wrong.")
                    optionboard()
    elif userinput == 2 or userinput == "2":
        print("What GPIO port do you want to see?")
        gpio_state_number = input()
        if not (gpio_state_number in valid_numbers):
            print("invalid input.")
            optionboard()
        else:
            gpio_state_number = int(gpio_state_number)
            if (gpio_state_number <= len(pins) and gpio_state_number > 0):
                gpio_state = pins[gpio_state_number - 1].value()
                print("Pin # ", gpio_state_number, "value is ", gpio_state)
                optionboard()
    if userinput == 3 or userinput == "3":
        gpio_total_states.clear()
        gpio_pins_on.clear()
        testvar = 0
        forlooprange = len(pins)
        for x in range(1, len(pins)):
            gpio_total_states.append(pins[x-1].value())
            if pins[x-1].value() == 1:
                gpio_pins_on.append(x-1)
            testvar = testvar + 1
        print(len(gpio_total_states))
        print("Pins # ",gpio_pins_on, "are ON")
        optionboard()
    if userinput == 4 or userinput == "4":
        gpio_total_states.clear()
        gpio_pins_off.clear()
        testvar = 0
        forlooprange = len(pins)
        for x in range(1, len(pins)):
            gpio_total_states.append(pins[x-1].value())
            if pins[x-1].value() == 0:
                gpio_pins_off.append(x-1)
            print(gpio_total_states)
            testvar = testvar + 1
        print(len(gpio_total_states))
        print("Pins # ",gpio_pins_off, "are OFF")
        optionboard()
    if userinput == 5 or userinput == "5":
        print('Blinking all GPIO pins one by one for 3 sec each', )
        pinnumbertest = 0
        for x in range(1, len(pins)):
            print("blinking pin #", pinnumbertest+1)
            pins[pinnumbertest].toggle()
            sleep(3)
            pins[pinnumbertest].toggle()
            pinnumbertest = pinnumbertest + 1
        optionboard()
    if userinput == 6 or userinput == "6":
        print("Blinking onboard LED 10 times....")
        for x in range(0,10):
            pinled.toggle()
            sleep(1)
        optionboard()
    if userinput == 7 or userinput == "7":
        pinumberallon = 0
        for x in range(1, len(pins)):
            pins[pinumberallon].value(1)
            pinumberallon = pinumberallon + 1
        print("All Pins ON")
        optionboard()
    if userinput == 8 or userinput == "8":
        global pinumberalloff
        pinumberallofff = 0
        for x in range(1, len(pins)):
            pins[pinumberalloff].value(0)
            pinumberalloff = pinumberalloff + 1
        print("All Pins OFF")
        optionboard()
    if userinput == "10" or userinput == 10:
        if wlan.isconnected() == False or ip == None or ip == "0.0.0.0":
            print("Ok, what is your network SSID?")
            ssid_func = input()
            print('Ok, what is your SSID password?')
            ssid_passphrase = input()
            connect(ssid_func,ssid_passphrase)
        elif wlan.isconnected() == True:
            print("Connected to wifi. IP:", ip)
            optionboard()
        else:
            print("Error. Something went wrong.")
            optionboard()
    if userinput == "11" or userinput == 11:
        if wlan.isconnected() == False:
            print("Ok, what is your network SSID?")
            ssid_func = input()
            print('Ok, what is your SSID password?')
            ssid_passphrase = input()
            connect(ssid_func,ssid_passphrase)
        elif wlan.isconnected() == True:
            print("What is your target host? (ex. google.com). Please No numbers, or IPs. deafilts to port 80")
            target_host = input()
            ping(target_host,80)
        else:
            print("Error. Something went wrong.")
            optionboard()
        optionboard()
    if userinput == 9 or userinput == "9":
        global pico_version
        print("Settings")
        print("[1] Change Pico Version")
        choice_setting = input()
        if choice_setting == "1":
            print("What version of PICO do you own?")
            print("OPTIONS")
            print("[1] Pico 1")
            print("[2] Pico W")
            print("[3] Pico 2")
            print("[4] Pico 2 W")
            pico_version_choice = input()
            if pico_version_choice == '1':
                pico_version = '1'
            elif pico_version_choice == "2":
                pico_version = "W"
            elif pico_version_choice == "3":
                pico_version = '2'
            elif pico_version_choice == "4":
                pico_version = "2W"
            else:
                print("invalid version.")
                optionboard()
        optionboard()
        if userinput == 11 or userinput == "11":
            ifconfig = wlan.ifconfig()
            print(ifconfig)
            
    if userinput == "i":
        print("What action do you want more informaiton about?")
        actioninfo = input()
        if actioninfo == "h" or actioninfo == "i":
            print(action_info["h"])
            optionboard()
        else:
            print(action_info[actioninfo])
            optionboard()
    if userinput == "c":
        cleanup(True)
    if userinput == "q":
        cleanup(False)
def cleanup(returntomenu):
    pinsloop = 1
    for x in range(len(pins) - 1):
        pins[pinsloop].value(0)
        pins[pinsloop].off()
        pinsloop = pinsloop + 1
    pinled.value(0)
    pins[0].value(0)
    if returntomenu == False:
        print("Thanks! Come Again Next time!")
    elif returntomenu == True:
        optionboard()
    
#frist tests
#pin0 = Pin(1, Pin.OUT)
#pin0.value(1)
#in_state = pin0.value()
#print(in_state)
#pin0.off()

optionboard()