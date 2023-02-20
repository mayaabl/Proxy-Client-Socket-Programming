import socket 
import time
#Maya Abou Lteif
#######################################Server Code##################################################################
def proxyserver(port):
    try:
        #create a socket to listen to incoming connections
        #we define the start server function to implement the proxy server
        proxysocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        proxysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow reuse of the socket
        proxysocket.bind(('',port)) # we create the socket and bind it to the IP address and port
        proxysocket.listen(5) #we use this to listen for incoming connections
        print("Proxy server is listening on port", port)
        
    except Exception as error:
        print("failed to start the proxy server",error)
        return
    
    while True:
        #accept the incoming client connection
        clientsocket, clientaddress = proxysocket.accept()
        print ("Connection is accepted from: ", clientaddress)
        
        try:
            
            # receive the client's request
            req = clientsocket.recv(4096)
            request = req.decode('utf-8') 
            print("Request Received: ", request, time.time() )
            
            # extract the destination hostname or IP address from the request
            lines = request.split('\r\n')
            destihost = lines[1].split(' ')[1]
            destiport = 80
            
            # check if the request specifies a port other than 80 for the destination server
            if ':' in destihost:
                destihost, destiport = destihost.split(':')
                destiport = int(destiport)
            
            # connect to destination server by creating a socket
            destisocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            destisocket.connect((destihost, destiport))
            print("Connected to destination server at ", time.time())
            
            # forward request to destination server
            destisocket.sendall(req)
            print("Request forwarded to destination server")
            
            # receive response from destination server
            response = b''
            while True:
                data = destisocket.recv(4096)
                if not data:
                    break
                response += data
            
            print("Response received: ", response.decode('utf-8'))
            
            # forward response to client
            clientsocket.sendall(response)
            print("Response forwarded to client")
        
        except Exception as error:
            print ("Error :", error)
            clientsocket.sendall(b'HTTP/1.0 500 Internal Server Error\r\n\r\n')
        
        # close sockets
        clientsocket.close()
        destisocket.close()

proxyserver(8080)
