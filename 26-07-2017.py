# try:
#     print(x)
# except:
#     print('x tanımlı değil.')

# try:
#     yas = int(input('Yaş: '))
#     print(yas)
# except ValueError as err:
#     print('String girmeyiniz\n',err.args[0],sep='')
# print('lyk')

# for i in ['5',(5,4),9,'m','6']:
#     try:
#         print(int(i)*2)    
#     except TypeError as err:
#         print('Tip hatası',err)
#     except ValueError as err:
#         print('Değer hatası',err)

# while 1:
#     try:
#         number1 = int(input('Sayı 1: '))
'''
n tane değer alıncak int olmayacak, dizinin içindeki her elemanın harf sayısını bulcaz
2 ye bölünüyorsa true değilse false

["sey","ma"]
[3,2]
[false,true]
{  }
'''
stringArray  = []
lengthArray  = []
booleanArray = []
dictThing    = {}

def checkIfNumberPresent(text): # check if number is present
    for i in range(0,10):
        if str(i) in text:
            return True
    else: return False

def appendToVariables(text): # add text to variables
    # global stringArray
    # global lengthArray
    # global booleanArray
    # global dictThing

    boolOfText = None

    stringArray.append(text)
    lengthArray.append(len(text))

    if len(text) % 2 == 0:
        boolOfText = True
    else:
        boolOfText = False

    booleanArray.append(boolOfText)

    dictThing[text] = (len(text),boolOfText)

def printAllVariables():
    print('\n\n')
    print(stringArray)
    print(lengthArray)
    print(booleanArray)
    print(dictThing)

def main(): # main screen
    try:
        iterateCount = int(input('Kaç kelime? '))
        counter = 0
        while 1:
            text    = input('Yazı gir -> ')
            
            try:
                if checkIfNumberPresent(text) == True:
                    print('Sayı girme kardeş!')
                else:
                    raise Exception
            except:
                appendToVariables(text)

                counter += 1
                if counter >= iterateCount:
                    printAllVariables()
                    break
    except ValueError:
        print('Lütfen sayı giriniz!')
        main()

main()
