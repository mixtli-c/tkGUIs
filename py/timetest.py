from time import time,sleep

for i in range(10):
    t1=time()
    t2=time()
    print('%.2f\r' %((t2-t1)*1000000),end='')
    sleep(1)

