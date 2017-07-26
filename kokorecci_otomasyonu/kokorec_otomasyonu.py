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

    try:
        # ürün listesi için okuma işlemini yap, \n den parçala ve değişkene ata
        PRODUCT_LIST = readFile(VALID_PATHS['product']).split('\n')[:-1]
        # hepsini sözlüke çevir
        for i in range(len(PRODUCT_LIST)): PRODUCT_LIST[i] = json.loads(PRODUCT_LIST[i])

        # sipariş için okuma işlemini yap, \n den parçala ve değişkene ata
        ORDER_LIST   = readFile(VALID_PATHS['order']).split('\n')[:-1]
        for i in range(len(ORDER_LIST)): ORDER_LIST[i] = json.loads(ORDER_LIST[i])
    except:
        while True:
            print('FATAL ERROR!!!')

def saveDBtoFile():
    productData = ''
    orderData   = ''

    # i ye product listteki product'ı ata
    for i in PRODUCT_LIST:
        productData += json.dumps(i)+'\n' # parse işlemini yap

    # i ye order listteki order'ı ata
    for i in ORDER_LIST:
        orderData += json.dumps(i)+'\n' # parse işlemini yap
    
    writeFile(VALID_PATHS['product'],productData) # dosyaya yaz
    writeFile(VALID_PATHS['order'],orderData) # dosyaya yaz

### FILE FUNCTIONS ###
# @param fileName = okunacak dosyanın adı
# @return = başarılı olur ise okunan dosyanı içeriği, başarısız olursa false
def readFile(fileName):
    try:
        with open(fileName,'r') as f:
            r = f.read()
        return r
    except:
        return 0

# @param fileName  = okunacak dosyanın adı
# @param writeData = dosyaya yazılacak data
# @return = başarılı olur ise true, başarısız olursa false
def writeFile(fileName,writeData):
    try:
        with open(fileName,'w') as f:
            f.write(writeData)
        return 1
    except:
        return 0

# @param fileName  = okunacak dosyanın adı
# @param writeData = dosyaya yazılacak data
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
# @param product = ürün
# @param address = sipariş veren kişinin adresi
def createNewOrder(product,address):
    # verileri saklıyacağımız sözlüğü oluştur
    orderData = {
        'name':product['name'],
        'address':address,
        'cost':product['cost'],
        'type':product['type']
    }
    
    orderData = json.dumps(orderData) # parse orderData
    
    if appendFile( VALID_PATHS['order'], orderData ): # dosya ya kayıt et
        updateDB()
        return 1
    else:
        return 0

def createNewFis(productName,cost):
    print('''
*-----------------*
* Koko Restorant  *
*-----------------*
Ürün  : {}
Ücret : {}TL
Kdv   : %8
Total : {}TL
*******************
    '''.format(productName,cost, cost + cost*8/100))

### RESTAURANT FUNCTIONS ###
# @param name  = Ürün Adı
# @param stock = Stocktaki ürün miktarı
# @param cost  = Ürün fiyatı
# @param type  = Ürün tipi (yiyecek,içecek,tatlı)
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

# @param product = restaurantAddProduct fonksiyonundan gelen product(ürün)
def restaurantSaveProduct(product):
    if appendFile( VALID_PATHS['product'], product ) == 1: # başarı ile yazarsak
        updateDB() # veritabanını güncelle
        return 1
    else:
        return 0

def restaurantDeleteProduct():
    print('\n')
    
    i = 0 # index tutucu
    # product listteki elemanları sırayla product'a aktar
    for product in PRODUCT_LIST:
        print('#'+str(i),product['name']) # index kullanarak ekrana yazdır
        i += 1
    
    try:
        print('\n')
        productID = int(input('Silmek istediğiniz id? ')) # ürün id'sini tutuyoruz
        
        if productID >= i: # id yanlış ise
            print('\n\nDoğru bir ID giriniz!')
            restaurantDeleteProduct()
        else: # doğru ise sil ve veritabanına kayıt et
            del PRODUCT_LIST[productID]
            saveDBtoFile()

            print('\n\nBaşarıyla sildiniz.')
            showRestaurantMenu()
    except TypeError: # sayı girilmez ise
        print('\n\nLütfen bir sayı giriniz')
        restaurantDeleteProduct()

def restaurantShowProducts():
    print('\n')
    # product listteki elemanları sırayla product'a aktar
    for product in PRODUCT_LIST:
        print('Ürün adı: {}, Stok: {}'.format(product['name'],str(product['stock'])))
    print('\n')
    showRestaurantMenu()

def restaurantShowOrders():
    print('\n')
    # order listteki elemanları sırayla order'a aktar
    i = 1
    for order in ORDER_LIST:
        print(str(i)+'. Sipariş\n','Ürün adı: {}, Sipariş adresi: {}, Ürün tipi: {}\n'.format(order['name'],order['address'],order['type']),sep='')
        i += 1
    print('\n')
    showRestaurantMenu()

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
    print('\n\n=== MENÜ ===\n\n')

    i = 0# index tutucu
    # product listteki elemanları sırayla product'a aktar
    for product in PRODUCT_LIST:
        print('#'+str(i),product['name'],' | Stok: {}'.format(str(product['stock']))) # sırayla ekrana bastır
        i += 1 # indexi 1 arttır
    
    try:
        print('\n')
        productID = int(input('Neyi tercih edersiniz? ')) # ürün id sini al

        if productID >= i: # eğer id geçersiz ise
            print('\n\nLütfen geçerli bir id giriniz.')
            showProductMenu()
        else: # id geçerli ise
            if PRODUCT_LIST[productID]['stock'] < 1: # eğer stokta kalmamış ise
                print('\n\nBu ürünün stoku kalmamıştır.')
                showProductMenu()
            toWhere = input('Adrese sipariş mi, yoksa dükkana mı? (adres,dükkan) ') # adresi al

            if toWhere not in ['adres','dükkan']: # sipariş yerini yanlış yazar ise
                print('Geçerli bir seçim yapınız.')
                showProductMenu()
            elif toWhere == 'adres': # adrese sipariş ise
                address = input('Adresinizi giriniz: ') # adresi al
            else: # adres dükkana ise
                address = 'dükkan'
            
            if createNewOrder(PRODUCT_LIST[productID],address): # yeni sipariş oluştur
                # ürünün stokunu 1 azalt
                PRODUCT_LIST[productID]['stock'] -= 1
                saveDBtoFile()

                print('\n\nSiparişiniz başarıyla verildi.\n\nFişiniz:')
                createNewFis(PRODUCT_LIST[productID]['name'],PRODUCT_LIST[productID]['cost']) # yeni fiş oluştur

    except ValueError:
        print('\n\nLütfen bir sayı giriniz.')
        showProductMenu()

def showRestaurantMenu():
    print('Ürün Ayarları\n','-'*10,
          '\na) Ekle\n','b) Sil\n\n',
          'Stok\n','-'*10,
          '\nc) Göster',
          '\nd) Siparişler\n',sep='')
    while 1:
        command = input('[Yönetici] Komut >> ')

        # yöneticinin gönderdiği komuta göre işlem yap
        if doCommand(command,['a','b','c','d'],[restaurantAddProduct,restaurantDeleteProduct,restaurantShowProducts,restaurantShowOrders]) == 1:
            break

### OFF-FUNCTIONS ###
# @param command = komut (string)
# @param permissionList = doğru olan komutlar (array)
# @param runFuncOnPermission = eğer komut doğru ise çağırılacak fonksiyonların listesi (array)
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
