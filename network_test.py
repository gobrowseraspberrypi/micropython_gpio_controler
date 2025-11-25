#part of this code was from the raspbery pi founation. 
import network
import socket
from time import sleep
import machine
import rp2
import sys
ssid = 'whyyoulookingatmyssid?'
password = 'pleasedontstealmypassword'
target_host = 'google.com'
port =80
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
connect()
'''
try:
    print("Pinging {}...".format(target_host))
    addr = socket.getaddrinfo(target_host, port)[0][-1]
    
    # Create a socket and connect
    s = socket.socket()
    s.connect(addr)
    
    # Send a simple HTTP GET request
    request = 'GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(target_host)
    s.send(request)
    
    # Wait for a response
    response = s.recv(1024)
    
    print("Ping successful! Response received from {}. Status code: (approx.) {}".format(
        target_host,
        response.decode('utf-8').split('\r\n')[0]
    ))
    
    s.close()

except Exception as e:
    print("Ping failed: {}".format(e))
'''
