import json
import os
import json_ornek_modules.menu

class KampOtomasyon:
    def __init__(self):
        self.sayac = 0
        self.sozluk = {}

    def dict_to_json(self,data):
        return json.dumps(data)
        #sozluk tipinde gelen veriyi jsona donusturup geri gönderecektir

    def json_to_dict(self,data):
        self.sayac = 0
        bos= {}
        try:
            for i in json.loads(data).keys():
                if int(i)> self.sayac:
                    self.sayac = int(i)
            self.sayac+=1
        except:
            return bos
        #json dosyasından okudugumuz veriyi sozluk haline getirip geri gondurecegiz
        return json.loads(data)

    def read_file(self,file_path):
     #dosyayı acıp, okuyup geri gondereceğiz
        data = None
        if not self.is_non_zero_file(file_path):
            return data
        f = open(file_path,"r")
        data = f.read()
        f.close()
        return data

    def write_file(self,data,file_path):
    #dosyaya veriyi yazacagız.
        with open(file_path,'w') as f:
            f.write(data)

    def mass_add_student(self):
        howMuch = int(input("Kaç tane öğrenci eklenecek? "))
        for i in range(howMuch):
            student = {"adi": input("ad: "), "soyadi": input("soyad: "), "dogum tarihi": input("doğum tarihi: "), "okul": input("okul: "), "sehir": input("şehir: "),
                     "egitim": input("almak istediğin eğitimler(, ile ayır) ").split(",")}
            self.add_student(student)
            print("Başarıyla eklendi!")

    def add_student(self,sozluk):
        eski_sozluk= {}
        eski_bilgi = self.read_file("bilgiler.json")
        if eski_bilgi:
           eski_sozluk = self.json_to_dict(eski_bilgi)
        eski_sozluk[self.sayac] = sozluk
        yeni_json=self.dict_to_json(eski_sozluk)
        self.write_file(yeni_json,"bilgiler.json")

    def is_non_zero_file(self,fpath):
        if os.path.isfile(fpath) and os.path.getsize(fpath)>0:
            return True
        return False

    def delete_student(self):
        datas = json.loads(self.read_file("bilgiler.json"))

        for i in datas:
            print("#{}, {} {}".format(i,datas[i]["adi"],datas[i]["soyadi"]))

        targetID = input("\nSilinicek ID? ")
        if targetID not in list(datas.keys()):
            print("Geçerli bir ID giriniz!")
        else:
            del datas[targetID]
            datas = self.dict_to_json(datas)
            self.write_file(datas,"bilgiler.json")
            print("Başarıyla silindi.")


    def list_student(self):
        datas = json.loads(self.read_file("bilgiler.json"))
        for key in list(datas.keys()):
            student = datas[key]
            print("ad: {}, soyad: {}, dogum {}, okul: {}, sehir: {}, egitimler: {}".format(student["adi"],student["soyadi"],student["dogum tarihi"],student["okul"],student["sehir"]," - ".join(student["egitim"])))

    def search_student(self):
        studentSearchName  = input("Ad giriniz: ")
        studentDatas = self.json_to_dict(self.read_file("bilgiler.json"))
        searchResult = []
        print("\n=== Arama Sonucu ===")
        for key in studentDatas:
            student = studentDatas[key]
            if studentSearchName.lower() in student["adi"].lower():
                searchResult.append(student)
        if len(searchResult) >= 1:
            for std in searchResult:
                print("ad: {}, soyad: {}, dogum {}, okul: {}, sehir: {}, egitimler: {}".format(std["adi"],std["soyadi"],std["dogum tarihi"],std["okul"],std["sehir"]," - ".join(std["egitim"])))
        else:
            print("Sonuç bulunamadı.")

    def edit_student(self):
        datas = json.loads(self.read_file("bilgiler.json"))

        for i in datas:
            print("#{}, {} {}".format(i, datas[i]["adi"], datas[i]["soyadi"]))

        targetID = input("\nDüzeltilecek kişi ID?(Bütün alanları tekrar doldurmanız gerekcektir!) ")
        if targetID not in list(datas.keys()):
            print("Geçerli bir ID giriniz!")
        else:
            student = {"adi": input("ad: "), "soyadi": input("soyad: "), "dogum tarihi": input("doğum tarihi: "),
                       "okul": input("okul: "), "sehir": input("şehir: "),
                       "egitim": input("almak istediğin eğitimler(, ile ayır) ").split(",")}
            datas[targetID] = student
            datas = self.dict_to_json(datas)
            self.write_file(datas,"bilgiler.json")
            print("Başarıyla güncellendi!")

if __name__=='__main__':
    kamp = KampOtomasyon()
    Menu = json_ornek_modules.menu.Menu()
    Menu.showMainMenu()


    # bilgi= {"adi":"irem","soyadi":"ozer", "dogum tarihi": 94, "okul": "erciyes", "sehir":"kayseri", "egitim":['php','django'] }
    # bilgi2= {"adi":"başak", "soyadi": "şanlı","dogum tarihi": 97, "okul": "msgsu", "sehir":"istanbul", "egitim": ["python","php"]}
    #
    # kamp.add_student(bilgi)
    # kamp.add_student(bilgi2)
    # print(kamp.read_file("bilgiler.json"))