'''
Adam Asmaca - Ege Bilecen - egebilecen.tk
'''
import random

bulunacakKelime = random.choice(['php','perl','python','ruby','javascript'])
harfHavuzu = []
kalanHak   = 6
replaceCharacter = '_'
gosterimYazisi = list(replaceCharacter*len(bulunacakKelime))

dongu = 1

while dongu:
    print(' '.join(gosterimYazisi),end='\n\n')
    alinanHarf = input('Bir harf giriniz: ')

    try:
        int(alinanHarf)
        print('Doğru bir şeyler girdiğinden emin ol.\n')
    except:
        if len(alinanHarf) > 1:
            print('Harf giriniz!\n')
        else:
            if alinanHarf in harfHavuzu:
                print('Bu harfi zaten girdiniz.\n')
            else:
                bulduk = None
                for i in range(len(bulunacakKelime)):
                    if alinanHarf == bulunacakKelime[i]:
                            bulduk = True
                            gosterimYazisi[i] = alinanHarf
                            harfHavuzu.append(alinanHarf)

                            if replaceCharacter not in gosterimYazisi:
                                print(' '.join(gosterimYazisi))
                                print('\nTebrikler kelimeyi buldunuz!')
                                dongu = 0
                else:
                    if bulduk != True:
                        kalanHak -= 1
                        print('Yanlış harf. Kalan hakkınız: {}\n'.format(kalanHak))
                        harfHavuzu.append(alinanHarf)
                
                if kalanHak == 0:
                    print('Kaybettin. Doğru kelime "{}" idi.\n'.format(bulunacakKelime))
                    break
