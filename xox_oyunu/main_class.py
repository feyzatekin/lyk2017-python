import random
class Oyun():
    def __init__(self,genislik=3,yukseklik=3,elSayisi=5):
        self.oyunAyarlari = {
            "genislik":genislik,
            "yukseklik":yukseklik,
            "object":["X","O"],
            "objectSahip":{
                "X":None,
                "O":None
            }
        }
        self.oyuncular = {
            "oyuncu1":{
                "text":"Oyuncu 1",
                "object":None,
                "skor":0
            },
            "oyuncu2":{
                "text":"Oyuncu 2",
                "object":None,
                "skor":0
            }
        }
        self.oyun = {
            "toplamElSayisi": elSayisi,
            "suankiElSayisi":0
        }
        self.oyunTahtasi = []
        self.oyunTahtasiOlustur()
        self.oynananHamleler = []
        self.oyunDurum = True # true->devam | false -> oyun bitti

    def oyunuBaslat(self):
        obj1 = random.randrange(0,2)
        obj2 = None
        if obj1 == 1: obj2 = 0
        else: obj2 = 1

        self.oyuncular["oyuncu1"]["object"] = self.oyunAyarlari["object"][obj1]; self.oyunAyarlari["objectSahip"][self.oyunAyarlari["object"][obj1]] = self.oyuncular["oyuncu1"]
        self.oyuncular["oyuncu2"]["object"] = self.oyunAyarlari["object"][obj2]; self.oyunAyarlari["objectSahip"][self.oyunAyarlari["object"][obj2]] = self.oyuncular["oyuncu2"]

        print("1. oyuncu {} oldu!\n2. oyuncu {} oldu!\n\n".format(self.oyunAyarlari["object"][obj1],self.oyunAyarlari["object"][obj2]))

    # oyun tahtasını oluşturur
    def oyunTahtasiOlustur(self):
        for i in range(0,self.oyunAyarlari["yukseklik"]):
            self.oyunTahtasi.insert(i,[])
            for j in range(0,self.oyunAyarlari["genislik"]):
                self.oyunTahtasi[i].insert(j,[])
        return 1

    # oyun tahtasini döndürür
    def oyunTahtasiDondur(self):
        return self.oyunTahtasi

    def oyunculariDondur(self):
        return self.oyuncular

    def oyunTahtasiGoruntu(self):
        printData = ""
        for satir in range(0,len(self.oyunTahtasi)): # [ [],[],[] ]
            for sutun in range(0,len(self.oyunTahtasi[satir])): # []
                if len(self.oyunTahtasi[satir][sutun]) == 0:
                    printData += "["+str(satir)+":"+str(sutun)+"]"
                else:
                    printData += "["+self.oyunTahtasi[satir][sutun]+"]"
            printData += "\n"
        print(printData,end="")

    def oyunTahtasiDuzenle(self,satir,sutun,object):
        self.oyunTahtasi[satir][sutun] = object

    def oyunTahtasiSifirla(self):
        self.oyunTahtasi = []
        self.oyunTahtasiOlustur()

    def elSayisiniArttir(self):
        self.oyun["suankiElSayisi"] += 1

        if self.oyun["suankiElSayisi"] >= self.oyun["toplamElSayisi"]:
            self.oyunDurum = False
            print("\n\nOyun bitti.\nOyuncu 1'in Skoru: {}\nOyuncu 2'nin Skoru: {}".format(self.oyuncular["oyuncu1"]["skor"],self.oyuncular["oyuncu2"]["skor"]))

    def hamleKontrol(self,satir,sutun):
        if len(self.oyunTahtasi[satir][sutun]) >= 1: return False # içinde bir object var yani X ya da O
        elif self.oyunTahtasi[satir][sutun] == []: return True # index doğru ama içi boş
        else: return False #index yok, hata falan birşeyler var

    def hamleYap(self,oyuncu):
        if oyuncu == "oyuncu1": oyuncuObj = self.oyuncular["oyuncu1"]
        else: oyuncuObj = self.oyuncular["oyuncu2"]
        hamle = input("{} yer numarası giriniz: ({}) ".format(oyuncuObj["text"],oyuncuObj["object"]))

        try:
            hamle = hamle.split(':')
            satir = int(hamle[0]); sutun = int(hamle[1])

            if self.hamleKontrol(satir,sutun):
                self.oyunTahtasiDuzenle(satir,sutun,oyuncuObj["object"])
                self.oyunTahtasiGoruntu()
                if self.hamleKontrolEt():
                    self.elSayisiniArttir()
                    return True
                else:
                    return False
            else:
                print("Lütfen geçerli bir konum giriniz!")
                self.hamleYap(oyuncu)
        except Exception as err:
            print("HATA: ",err)
            print("Lütfen doğru bir yer numarası giriniz!")
            self.hamleYap(oyuncu)

    def hamleKontrolEt(self): # oyun tahtasindaki yerleri bu kontrol ediyor
        if not self.hamleKontrolEtYatay():
            if not self.hamleKontrolEtDikey():
                if not self.hamleKontrolEtCapraz():
                    return False
                else:
                    return True
            else:
                return True
        else: return  True

    def objedenOyuncuPuanArttir(self,obje):
        self.oyunAyarlari["objectSahip"][obje]["skor"] += 1
        print("{}, 1 puan kazandı!\n".format(self.oyunAyarlari["objectSahip"][obje]["text"]))

    # 3 tane X,O yan yana mı kontrol eder
    def hamleKontrolEtYatay(self):
        for satir in range(0,len(self.oyunTahtasi)): # [ [],[],[] ]
            objX = 0 # X sayısı
            objO = 0 # O sayısı
            for sutun in range(0,self.oyunAyarlari["yukseklik"]): # []
                if self.oyunTahtasi[satir][sutun] == "X": objX += 1
                elif self.oyunTahtasi[satir][sutun] == "O": objO += 1
            if objX >= 3: self.objedenOyuncuPuanArttir("X"); self.oyunTahtasiSifirla(); return True
            elif objO >= 3: self.objedenOyuncuPuanArttir("O"); self.oyunTahtasiSifirla(); return True
        else: return False

    def hamleKontrolEtDikey(self):
        for sutun in range(0,self.oyunAyarlari["genislik"]):
            objX = 0 # X sayısı
            objO = 0 # O sayısı
            for satir in range(0,self.oyunAyarlari["yukseklik"]):
                if self.oyunTahtasi[satir][sutun] == "X": objX += 1
                elif self.oyunTahtasi[satir][sutun] == "O": objO += 1
            if objX >= 3: self.objedenOyuncuPuanArttir("X"); self.oyunTahtasiSifirla(); return True
            elif objO >= 3: self.objedenOyuncuPuanArttir("O"); self.oyunTahtasiSifirla(); return True
        else: return False

    # 3 tane X,O çarpraz mı kontrol eder
    def hamleKontrolEtCapraz(self):
        for satir in range(0,self.oyunAyarlari["yukseklik"]):
            for sutun in range(0,self.oyunAyarlari["genislik"]):
                objX = 0; objO = 0
                lastSatir = satir
                lastSutun = sutun
                if self.oyunTahtasi[satir][sutun] == "X": objX += 1
                elif self.oyunTahtasi[satir][sutun] == "O": objO += 1

                for i in range(0,self.oyunAyarlari["genislik"]):
                    try:
                        lastSatir += 1
                        lastSutun += 1
                        if self.oyunTahtasi[lastSatir][lastSutun] == "X":
                            objX += 1
                        elif self.oyunTahtasi[lastSatir][lastSutun] == "O":
                            objO += 1
                    except:
                        pass

                if objX >= 3: self.objedenOyuncuPuanArttir("X"); self.oyunTahtasiSifirla(); return True
                elif objO >= 3: self.objedenOyuncuPuanArttir("O"); self.oyunTahtasiSifirla(); return True
