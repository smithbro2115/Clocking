import os
import time


os.startfile("C:/Users/Josh/PycharmProjects/Clocking/dist/Clocking.exe")

print('HEY!')
time.sleep(20)

os.system('TASKKILL /F /IM Clocking.exe')
