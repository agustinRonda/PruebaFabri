import requests
import socket
import threading
import json

from io import BytesIO
from PIL import Image

API_BASE_URL = "https://pokeapi.co/api/v2"
HEADER = 16
PORT = 8080
FORMAT = 'utf-8'
IPV4 = '192.168.2.138'                  #socket.gethostbyname(socket.gethostname())
ADDR = (IPV4, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send(msg, sock):
    msg = msg.encode(FORMAT)
    msg_length = len(msg)                               # Get the length of the message
    print(f"Voy a mandar {msg_length} bytes")
    send_length = str(msg_length).encode(FORMAT)        
    send_length += b' ' * (HEADER - len(send_length))   # Add the necessary bytes to get to the HEADER length
    sock.send(send_length)
    sock.send(msg)

    

def handle_client(conn, addr):
    
    print(f"[NEW CONNECTION] {addr} connected.")

    connected  = True
    while connected:
        id = conn.recv(1024).decode(FORMAT)
        if id:
            print(f"Recibi: id={id}")
            try:
                response = requests.get(f"{API_BASE_URL}/pokemon/{id}").json()
                sprite_url = response["sprites"]["front_default"]
                
                name = response["name"].capitalize()
                types_json = response["types"]
                types = []
                for type in types_json:
                    types.append(type["type"]["name"].capitalize())

                response = requests.get(sprite_url)
                sprite = Image.open(BytesIO(response.content))

                sprite = sprite.convert('RGB')    
                width = sprite.width
                height = sprite.height

                response = json.dumps(
                    {   'id' : id, 
                        'name' : name, 
                        'types' : types, 
                        'sprite_url' : sprite_url, 
                        'width' : width, 
                        'height' : height
                    })
                send(response, conn)

                full_image = []
                for h in range(width):
                    row = []
                    for w in range(height):
                        r, g, b = sprite.getpixel((w, h))
                        row.append((r, g, b))
                    full_image.append(row)
                
                for row in full_image:
                    print(len(full_image))
                    response = json.dumps({'row' : row})
                    send(response, conn)
                
                print("Image fully sent")

            except Exception as e:
                print(e)

def tcp_server():
    server.listen(10)
    print(f"[LISTENING] Server is listening on {IPV4}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

tcp_thread = threading.Thread(target=tcp_server)
tcp_thread.start()
print(f"[TCP SERVER STARTING]")

