from socket import *
from Item import *

# To get the 2nd part of the request which is the path.
def getPath(request):
    return request.split(" ")[1]

# Response to the cliet's request, to open a file.
def inResponse(type, fileN):
    response = (f"HTTP/1.0 200 OK\r\nContent-Type: {type}\r\n\r\n").encode()
    file = None
    if(fileN.find(".png") or fileN.find(".jpg")):
        file = open(fileN, "rb")
        response += file.read()
    else:
        file = open(fileN, "r")
        response += file.read().encode()
    file.close()
    return response

def sortItems(fileN, type):
    itemList = []
    file = open("items.txt", "r")
    Lines = file.readlines()
    for line in Lines:
        # To take the first word from line = name of the item
        name = line.split(" ")[0]
        # To take the second word from line = price of the item
        price = line.split(" ")[1]
        itemList.append(Item(name, int(price)))

    # To sort the items
    if type == "SortByName":
        itemList.sort(key = lambda x: x.name, reverse = False)
    elif type == "SortByPrice":
        itemList.sort(key = lambda x: x.price, reverse = False)
    file.close()
    return itemList

def requests(request, connection, cAddress):
    path = getPath(request)
    # Checks the client's request
    if (path == "/") or (path == "/index.html"):
        connection.send(inResponse("text/html", "main.html"))

    elif path == "/file.html":
        connection.send(inResponse("text/html", "file.html"))

    elif path == "/style.css":
        connection.send(inResponse("text/css", "style.css"))

    elif path == "/image1.png":
        connection.send(inResponse("image/png", "image1.png"))

    elif path == "/image2.jpg":
        connection.send(inResponse("image/jpeg", "image2.jpg"))

    elif path == "/SortByName":
        connection.send(("HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n").encode())
      # To open HTML page which contains the result of sorting items.
        connection.send(("""<!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <title>Sorted Items by name</title>
                                <link rel="stylesheet" href="style.css">
                            </head>
                            <body><div class='table'>""").encode())
        connection.send(("""<div class='title'><span>Item</span><span>Price</span></div>""").encode())
        itemList = sortItems("items.txt", "SortByName")
        # To print the sorted items one by one
        for item in itemList:
            connection.send((f"<div class='item'><span>{item.name}</span><span>{item.price}</span></div>").encode())

        connection.send(("""</div></body></html>""").encode())

    elif path == "/SortByPrice":
        connection.send(("HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n").encode())
        # To open HTML page which contains the result of sorting items.
        connection.send(("""<!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Sorted Items by price</title>
                        <link rel="stylesheet" href="style.css">
                    </head>
                    <body><div class='table'>""").encode())
        connection.send(("""<div class='title'><span>Item</span><span>Price</span></div>""").encode())
        itemList = sortItems("items.txt", "SortByPrice")
        for item in itemList:
            connection.send((f"<div class='item'><span>{item.name}</span><span>{item.price}</span></div>").encode())
      
        connection.send(("""</div></body></html>""").encode())

    # If the request is wrong or the file doesn’t exist:
    else:
        # Set response status = 404 not found.
        connection.send(('HTTP/1.1 404 Not Found').encode())
        connection.send(("\r\nContent-Type: text/html\r\n\r\n").encode())
        # Open HTML page which contains the following texts.
        connection.send((f"""<!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <title>Error</title>
                                <link rel="stylesheet" href="style.css">
                            </head>
                            <body class='error'>
                            <div class='error-msg'>The file is not found</div>
                            <div class='members'>
                                <div class='member'><span>Hana Kafri</span><span>1190084</span></div>
                                <div class='member'><span>Shahd Khawaldeh</span><span>1191102</span></div>
                                <div class='member'><span>Roa Hanoun</span><span>1190886</span></div>
                            </div>
                            <div class='client-info'>
                            <div class='ip'>Ip: {cAddress[0]}</div>
                            <div class='port'>Port: {str(cAddress[1])}</div>
                            </div>
                            """).encode())

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 6500

# Create socket
# TCP Connection
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    # Waiting for socket connection

    # Get the client connection and client address from accept method, 
    # which returns a new socket representing the connection,and client address
    cConnection, cAddress = server_socket.accept()

    request = cConnection.recv(1024).decode()

    if (len(request) > 0):
        requests(request, cConnection, cAddress)

    print(request)

    # Closing the connection
    cConnection.close()

# Close socket
server_socket.close()