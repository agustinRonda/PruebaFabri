import socket
import json
import colorama
from colorama import Fore


PORT = 8080
IPV4 = '192.168.2.138'
FORMAT = 'UTF-8'
HEADER = 16
DISPLAY_DIMENSION = (240, 240)

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def send_msg(client, msg, header):
    client.send(header.encode(FORMAT))      #Enviar largo del mensaje del cliente
    client.send(msg)                        #Enviar mensaje del cliente

addr = (IPV4, PORT)

client = socket.socket()
client.connect(addr)


msg = input("Number between 1-898: ").encode(FORMAT)     #Pedir mensaje al usuario
len_msg = len(msg)          
header = str(len_msg)
header += ' ' * (HEADER - len(header))    #Calcular y rellenar espacios del mensaje del cliente

send_msg(client, msg, header)


lenght = client.recv(500).decode(FORMAT)

lenght = int(lenght)

image_info = client.recv(lenght)
image_info_json = json.loads(image_info.decode(FORMAT))

print(image_info_json)

rows = []

show_image = True

for i in range(int(image_info_json['height'])):

    try:
        lenght = int(client.recv(500).decode(FORMAT))

        data = client.recv(lenght)
        jdata = json.loads(data.decode(FORMAT))

        rows.append(jdata)

    except Exception as e:
        print(f"PAQUETE NUMERO {i} RECIBIDO INCORRECTAMENTE")
        show_image = False
        break

if show_image:

    inicio_x = round((DISPLAY_DIMENSION[0] - image_info_json['width']) / 2)
    inicio_y = round((DISPLAY_DIMENSION[1] - image_info_json['height']) / 2)

    for row in rows:
        # print(row['row'][0])
        for i in range(len(row['row'])):

            pixel = row['row'][i]

            text = '█'
            colored_text = colored(pixel[0], pixel[1], pixel[2], text)
            
            if i == (len(row['row']) - 1):
                print(colored_text)
            else:
                print(colored_text, end='')