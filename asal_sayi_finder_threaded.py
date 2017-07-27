'''
 Ege Bilecen - Threaded Asal Sayı Bulucu

 egebilecen.tk
'''

import threading
import math
from queue import Queue
from sys import exit as sys_exit

print_lock = threading.Lock()

# GLOBALS #
allAsalSayiList = []

def asalSayiBul( sayiDizisi ):
    global allAsalSayiList
    
    for sayi in sayiDizisi:
        if sayi == 1: continue
        for onceki_sayi in range(2,len(sayiDizisi)):
            if sayi % onceki_sayi == 0 and sayi != onceki_sayi:
                break
        else:
            allAsalSayiList.append(sayi)

def runWorker():
    array = q.get()
    asalSayiBul(array)
    q.task_done()

# Variables #
THREAD_COUNT = int(input('Thread sayısı: '))
q = Queue()

startNumbersList = list(range(1,int(input('Hangi sayıya kadar asal sayı bulunacak? '))+1))
numberArray = []

queueCount = math.ceil(len(startNumbersList) / THREAD_COUNT)
lastTaken  = 0 # last taken index of array

for i in range(queueCount):
    numberArray.append( startNumbersList[lastTaken:lastTaken+THREAD_COUNT] )
    lastTaken += THREAD_COUNT

# Create workers #
for i in range(1,THREAD_COUNT+1):
    i = threading.Thread(target=runWorker)
    i.daemon = True
    i.start()

# Create queue #
for i in numberArray:
    q.put(i)
q.join()

print('\n=== Sonuçlar ===\n',allAsalSayiList,sep='')