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
