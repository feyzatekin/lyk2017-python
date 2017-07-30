ayarlar = {
    'toplamElSayisi'  : int(input('Kaç el oyun oynanacak? ')),
    'oynananElSayisi' : 0
}
skor = {
    'oyuncu1':0,
    'oyuncu2':0
}
durumlar = {
    'taş'  : 'makas', # taş, makasa karşı güçlü
    'makas': 'kağıt', # makas, kağıda karşı güçlü
    'kağıt': 'taş'    # kağıt, taşa karşı güçlü
}

def dogruHamleMi(hamle): 
    if hamle != 'taş' and hamle != 'kağıt' and hamle != 'makas':
        return False

def hamleKontrolEt(hamle1,hamle2):
    if durumlar[hamle1] == hamle2:
        return 1 # 1. oyuncu kazandı
    elif hamle1 == hamle2:
        return 3 # berabere
    else:
        return 2 # 2. oyuncu kazandı

while True:
    oyuncu1 = input('1. oyuncu: ')
    if dogruHamleMi(oyuncu1) == False:
        print('Lütfen geçerli bir hamle girin: taş, kağıt, makas')
        continue
    oyuncu2 = input('2. oyuncu: ')
    if dogruHamleMi(oyuncu2) == False:
        print('Lütfen geçerli bir hamle girin: taş, kağıt, makas')
        continue
    if hamleKontrolEt(oyuncu1,oyuncu2) == 1:
        print('==1. oyuncu kazandı==')
        skor['oyuncu1'] += 1
    elif hamleKontrolEt(oyuncu1,oyuncu2) == 2:
        print('==2. oyuncu kazandı==')
        skor['oyuncu2'] += 1
    else:
        print('==Berabere kalındı==')
    ayarlar['oynananElSayisi'] += 1

    if ayarlar['oynananElSayisi'] >= ayarlar['toplamElSayisi']:
        print('Oyun bitti.\n\n==SKORLAR==\nOyuncu 1: {}\nOyuncu 2: {}'.format(skor['oyuncu1'],skor['oyuncu2']))
        break
    else:
        print('\n','-'*10,end='\n\n')