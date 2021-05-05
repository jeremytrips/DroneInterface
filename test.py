from random import randint

data = [randint(0, 255) for i in range(64)]



to_send = ""
for i in range(len(data)):
    to_send += '{:03d}'.format(data[i])
    if i == len(data) - 1:
        to_send+= "a"
    else:
        to_send+= ","
print(len(to_send))