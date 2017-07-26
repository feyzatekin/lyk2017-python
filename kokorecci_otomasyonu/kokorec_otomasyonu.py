'''
LYK2017 - Kokoreç Otomasyonu - Ege Bilecen ~ egebilecen.tk
'''
### MODULES ###
import json

### GLOBALS ###
PRODUCT_LIST = []
ORDER_LIST   = []
VALID_PATHS  = { 'order':'veritabani/siparis.txt', 'product':'veritabani/urun.txt' }

### DATABASE FUNCTIONS ###
def updateDB():
    # değişkenleri global yap
    global PRODUCT_LIST
    global ORDER_LIST
    
    # veri tutulan değişkenleri sıfırla
    PRODUCT_LIST = []
    ORDER_LIST   = []

    # ürün listesi için okuma işlemini yap, \n den parçala ve değişkene ata
    PRODUCT_LIST = readFile(VALID_PATHS['product']).split('\n')[:-1]

    # sipariş için okuma işlemini yap, \n den parçala ve değişkene ata
    ORDER_LIST   = readFile(VALID_PATHS['order']).split('\n')[:-1]

### FILE FUNCTIONS ###
# @par fileName = okunacak dosyanın adı
# @return = başarılı olur ise okunan dosyanı içeriği, başarısız olursa false
def readFile(fileName):
    try:
        with open(fileName,'r') as f:
            r = f.read()
        return r
    except:
        return 0

# @par fileName  = okunacak dosyanın adı
# @par writeData = dosyaya yazılacak data
# @return = başarılı olur ise true, başarısız olursa false
def writeFile(fileName,writeData):
    try:
        with open(fileName,'w') as f:
            f.write(writeData)
        return 1
    except:
        return 0

# @par fileName  = okunacak dosyanın adı
# @par writeData = dosyaya yazılacak data
# @return = başarılı olur ise true, başarısız olursa false
def appendFile(fileName,writeData,autoEOL=True):
    try:
        with open(fileName,'a') as f:
            if autoEOL == True:
                writeData += '\n'
            f.write(writeData)
        return 1
    except:
        return 0

### CLIENT FUNCTIONS ###

### RESTAURANT FUNCTIONS ###
# @par name  = Ürün Adı
# @par stock = Stocktaki ürün miktarı
# @par cost  = Ürün fiyatı
# @par type  = Ürün tipi (yiyecek,içecek,tatlı)
def restaurantAddProduct():
    print('\n')
    # ürünü oluştur
    product = {
        'name':input('Ürün adı: '),
        'stock':int(input('Stokta Olacak Ürün Sayısı: ')),
        'cost':int(input('Ürün Fiyatı: ')),
        'type':input('Ürün tipi(yiyecek, içecek, tatlı): ')
    }

    # eğer ürün tipi istediğimiz gibi değil ise hata ver ve bu fonksiyonu tekrar çağır
    if product['type'] not in ['yiyecek','içecek','tatlı']:
        print('\n\nLütfen geçerli bir ürün tipi giriniz.\n\n')
        restaurantAddProduct()

    # json formatına çevir (dosyaya kayıt etmek için)
    product = json.dumps(product)

    # veritabanına kayıt et
    if not restaurantSaveProduct(product): # eğer fonksiyondan False dönerse aşağıyı çalıştır
        print('\n\nÜrün eklenirken bir hata oluştu\n\n')
    else:
        print('\n\nÜrün başarıyla eklendi.\n\n')
    showRestaurantMenu() # restorant yönetimi bölümünü tekrar göster

# @par product = restaurantAddProduct fonksiyonundan gelen product(ürün)
def restaurantSaveProduct(product):
    if appendFile( VALID_PATHS['product'], product ) == 1: # başarı ile yazarsak
        updateDB() # veritabanını güncelle
        return 1
    else:
        return 0

def restaurantDeleteProduct():
    print('\n')
    print(PRODUCT_LIST)

### MENU/SCREEN FUNCTIONS ###
def showMainScreen():
    print('=== KOKOREÇ OTOMASYONU ===\n\n',
          'a) Müşteri\n',
          'b) Restorant Yetkilisi\n')

def showClientScreen():
    print('=== Koko restorantına hoşgeldiniz! ===\n\n')
    showClientMenu() # menuyu ekrana bas
    while 1:
        command = input('[Müşteri] Komut >> ')

        # müşterinin gönderdiği komuta göre işlem yap
        if doCommand(command,['a'],[showProductMenu]) == 1:
            break

def showRestaurantScreen():
    print('\n\n=== Hoşgeldiniz, restorant yöneticisi. ===\n\n')
    showRestaurantMenu()

### MENU ###
def showClientMenu():
    print('a) Menü\n')

def showProductMenu():
    print('\n\n=== MENÜ ===\n\n',
          'Kokoreç\n','-'*10)

def showRestaurantMenu():
    print('Ürün Ayarları\n','-'*10,
          '\na) Ekle\n','b) Sil\n\n',
          'Stok\n','-'*10,
          '\nc) Göster','\n',sep='')
    while 1:
        command = input('[Yönetici] Komut >> ')

        # yöneticinin gönderdiği komuta göre işlem yap
        if doCommand(command,['a','b','c'],[restaurantAddProduct]) == 1:
            break

### OFF-FUNCTIONS ###
# @par command = komut (string)
# @par permissionList = doğru olan komutlar (array)
# @par runFuncOnPermission = eğer komut doğru ise çağırılacak fonksiyonların listesi (array)
def doCommand(command,permissionList,runFuncOnPermission):
    if command not in permissionList:
        print('\nGeçerli bir komut girin!\n')
        return 0
    else:
        runFuncOnPermission[ permissionList.index(command) ]()
        return 1

### START OF SCREEN ###
try:
    updateDB() # veritabanını güncelle
    showMainScreen() # ana ekranı göster
    while 1:
        command = input('Komut >> ')

        # ana ekrandan alınan komutu işle
        if doCommand(command,['a','b'],[showClientScreen,showRestaurantScreen]) == 1:
            break
except KeyboardInterrupt:
    print('\n\nGüle Güle!\n\n')