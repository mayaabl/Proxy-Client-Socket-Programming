########################CLient code#######################################################
#Maya Abou Lteif
import socket
import time
import uuid #to display the physical MAC address of the machine

ip = input("Enter IP address: ")

def client(ip):
    #create client socket
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(("localhost", 8080)) #connect socket to the proxy server
    
    #send requests to proxy server
    request = ("GET /index.html HTTP/1.1\r\n"f"Host: {ip}\r\n""Connection: close\r\n""\r\n")
    clientsocket.sendall(request.encode()) #send http request to proxy server
    print(f"Sent request to proxy server at {time.time()}: {request}")
    
    requesttime = time.time() #get time
    response = b''  
    while True:
        data = clientsocket.recv(1024)
        if not data: # check if the most recently received data is empty
            break 
        response += data 
    
    responsetime = time.time() #get time
    
    #record the time the response was received
    rtt = (responsetime - requesttime)
    
    clientsocket.close() # close socket
    
    print(f"Response from proxy server is : {response.decode('utf-8')}")
    print(f"Round-trip time is: {rtt} s")

    #get the MAC address of the computer 
    MACaddress = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff)
                           for i in range(0, 8 * 6, 8)][::-1])

    # Print the MAC address
    print(f"MAC address: {MACaddress}")
    
    
client(ip)

