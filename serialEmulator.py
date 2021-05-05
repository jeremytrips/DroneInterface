from serial import Serial

ser = Serial("COM10")

ser.open()
while 1:
    rcv = input("> ")
    if rcv == "quit" or rcv == "q":
        break
    else:
        ser.write(rcv.encode())
ser.close()