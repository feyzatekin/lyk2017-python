import main_class

kacEl = int( input("Kaç el oynanacak? ") )
Oyun = main_class.Oyun(elSayisi=kacEl)

Oyun.oyunuBaslat()

while Oyun.oyunDurum:
    Oyun.oyunTahtasiGoruntu()
    print("{}. el\n".format(Oyun.oyun["suankiElSayisi"]+1))
    if Oyun.hamleYap("oyuncu1"):
        continue
    if Oyun.hamleYap("oyuncu2"):
        continue
    Oyun.elSayisiniArttir()
    print("\n")