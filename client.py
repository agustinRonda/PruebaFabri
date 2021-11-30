import socket
import json
import machine
import st7789

PORT = 8080
IPV4 = '192.168.0.76'
FORMAT = 'UTF-8'
HEADER = 16
DISPLAY_DIMENSION = (240, 240)

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
    spi = machine.SPI(1, baudrate=40000000, polarity=1)
    display = st7789.ST7789(spi, 240, 240, reset=machine.Pin(23, machine.Pin.OUT), dc=machine.Pin(22, machine.Pin.OUT))
    display.init()

    inicio_x = round((DISPLAY_DIMENSION - image_info_json['width']) / 2)
    inicio_y = round((DISPLAY_DIMENSION - image_info_json['height']) / 2)

    for i in range(len(rows)):
        for j in range(len(rows[i])):
            color = color565(rows[i][j][0], rows[i][j][1], rows[i][j][2])
            ST7789.pixel(inicio_x + j, inicio_y + i, color)

# https://github.com/devbis/st7789_mpy/