import json

'''
1- kullanıcı kayıt edilecek (kullanici adi, parola, ad, soyad, okul, bolum) (kullanıcı adı önceden alındı mı araştır)
2- öğrenci giriş sistemi yapılacak
3- giriş yapan öğrencileri bir menü karşılayacak
    a) aldığın dersleri gör
    b) aldığın derslerin notlarını gör
    c) aldığın derslere ders ekle
    d) aldığın derslerden ders sil
    e) ders notu güncelle
******************************************************************
4- öğretmen kayıt
5- öğretmen giriş
6- öğretmen öğrenci ekleyebilcek, silebilecek, not ekle, not sil
******************************************************************
Ege Bilecen
'''
path = {
    'student' : 'veritabani/ogrenci.txt',
    'teacher' : 'veritabani/ogretmen.txt'
}

STUDENT_LIST = []
TEACHER_LIST = []
CURRENT_USER = ''
LOGGED = {
    'student':False,
    'teacher':False
}

#######
STUDENT_INDEX = 0
TEACHER_INDEX = 0
#######

# öğrencileri hafızaya kayıt et
def updateStudentList(clearArray=True):
    if clearArray == True:
        global STUDENT_LIST
        global STUDENT_INDEX
        STUDENT_LIST  = []
        STUDENT_INDEX = 0
    _f = open(path['student'],'r')
    _r = _f.read().split('\n')[:-1]
    for STUDENT_INDEX in range(len(_r)):
        if _r[STUDENT_INDEX] != '':
            STUDENT_LIST.append( json.loads(_r[STUDENT_INDEX]) )
    _f.close()

### STUDENT FUNCTIONS ###
def saveStudent(student,studentIndex, saveToDatabase=True):
    STUDENT_LIST[studentIndex] = student

    if saveToDatabase == True:
        data = []
        
        for i in range(len(STUDENT_LIST)):
            std = STUDENT_LIST[i]
            data.append( json.dumps(std) )
        
        f = open(path['student'],'w')
        f.write( '\n'.join( data )+'\n' )
        f.close()

def createStudent():
    student = {
        'username'  : input('Kullanıcı adı: '),
        'password'  : input('Parola: '),
        'name'      : input('Ad: '),
        'surname'   : input('Soyad: '),
        'school'    : input('Okul: '),
        'section'   : input('Bölüm: '),
        'lessons'   : []
    }
    return student

def studentLogin():
    data = {
        'username': input('Kullanıcı adı: '),
        'password': input('Şifre: ')
    }
    for std in STUDENT_LIST:
        if data['username'] == std['username'] and data['password'] == std['password']:
            print('Başarıyla giriş yaptınız.')
            studentScreen(std,STUDENT_INDEX)
            break
    else:
        print('[!] Kullanıcı adı veya şifre yanlış!')
        startScreen()

def studentRegister(customText='\nBaşarıyla kayıt olundu!\n',runFunc='startScreen'):
    while True:
        ourStudent = createStudent()

        f = open(path['student'],'r')
        r = f.read().split('\n')[:-1]
        
        for std in STUDENT_LIST:
            if ourStudent['username'] == std['username']:
                print('[!] Kullanıcı adı alınmış!\n')
                break
        else: 
            f = open(path['student'],'a')
            f.write( json.dumps(ourStudent)+'\n' )
            f.close()
            print(customText)
            if runFunc == 'startScreen':
                startScreen()
            elif runFunc == 'teacherScreen':
                teacherMenuScreen()
            elif runFunc == 'studentScreen':
                studentMenuScreen()
            updateStudentList()
            break

def studentMenuScreen():
    print('|== İşlemler ==|\n',
          'a) Dersleri Gör\n',
          'b) Ders Notlarını Gör\n',
          'c) Ders Ekle\n',
          'd) Ders Sil\n',
          'e) Ders Notu Güncelle\n')

def studentScreen(student, studentIndex):
    CURRENT_USER = student
    LOGGED['student'] = True
    print('\n=== Hoşgeldiniz, {ad} {soyad}. ===\n\n'.format(ad=student['name'],soyad=student['surname']))
    
    studentMenuScreen()

    while True:
        if LOGGED['student'] == True and LOGGED['teacher'] == False:
            command = input('[Öğrenci] Komut >> ')
            
            if command not in ['a','b','c','d','e']:
                print('Yanlış komut!\n')
            elif command == 'a': # DERSLERI GORUNTULE
                text = ''
                if len(student['lessons']) < 1:
                    text = 'Yok'
                else:
                    for i in student['lessons']:
                        text  += i['lesson'] + ' '
                print('\nAldığınız dersler: {}\n'.format(text))

                studentMenuScreen()
            elif command == 'b': # NOTLARI GORUNTULE
                text = ''
                if len(student['lessons']) < 1:
                    text = '\n[!]Eklenmiş not yok.\n'
                    print(text)
                else:
                    for i in student['lessons']:
                        text = '{}: '.format(i['lesson'])

                        for j in i['notes']:
                            text += str(j) + ' '
                        print(text+'\n')
                        text = ''
                studentMenuScreen()
            elif command == 'c': # DERS EKLEME
                lessonCount = int(input('Kaç ders ekliceksiniz? '))
                for i in range(lessonCount):
                    print('\n')
                    lessonName  = input('Ders adı: ')
                    lessonNotes = input('Notlarınızı virgül(,) ile giriniz: ')
                    student['lessons'].append({'lesson':lessonName,'notes':lessonNotes.split(',')})
                print('\nBaşarıyla ders eklediniz.\n')
                saveStudent(student,studentIndex)
                studentMenuScreen()
            elif command == 'd': # ders sil
                print('== Silmek İstediğiniz Dersi Girin ==')
                counter = 0
                for i in student['lessons']:
                    print('#'+str(counter),i['lesson'])
                    counter += 1
                while True:
                    id = int(input('\nSilincek dersin ID\'sini giriniz: '))

                    if id > counter:
                        print('\n[!] Doğru bir ID giriniz!')
                    else:
                        del student['lessons'][id]
                        saveStudent(student,studentIndex)
                        print('\nBaşarıyla silindi.\n')
                        studentMenuScreen()
                        break
            elif command == 'e': # not güncelle
                print('== Not Düzenleme ==')
                counter = 0
                while True:
                    for i in student['lessons']:
                        print('#'+str(counter),i['lesson'])
                        counter += 1
                    id = int(input('Düzenlemek istediğiniz notun dersinin ID\'sini giriniz: '))
                    if id > counter:
                        print('\n[!] Doğru bir ID giriniz!')
                    else:
                        notes = input('Notlarınızı virgül(,) ile giriniz: ') 
                        student['lessons'][id]['notes'] = notes.split(',')
                        saveStudent(student,studentIndex)
                        print('\nBaşarıyla düzenlediniz.\n')
                        studentMenuScreen()
                        break

### TEACHER FUNCTIONS ###
def updateTeacherList():
    _f = open(path['teacher'],'r')
    _r = _f.read().split('\n')[:-1]
    for TEACHER_INDEX in range(len(_r)):
        if _r[TEACHER_INDEX] != '':
            TEACHER_LIST.append( json.loads(_r[TEACHER_INDEX]) )
    _f.close()

def createTeacher():
    teacher = {
        'username'  : input('Kullanıcı adı: '),
        'password'  : input('Parola: '),
        'name'      : input('Ad: '),
        'surname'   : input('Soyad: '),
        'school'    : input('Okul: ')
    }
    return teacher

def teacherRegister():
    while True:
        ourTeacher = createTeacher()

        f = open(path['teacher'],'r')
        r = f.read().split('\n')[:-1]
        
        for std in TEACHER_LIST:
            if ourTeacher['username'] == std['username']:
                print('[!] Kullanıcı adı alınmış!\n')
                break
        else: 
            f = open(path['teacher'],'a')
            f.write( json.dumps(ourTeacher)+'\n' )
            f.close()
            print('Başarıyla kayıt olundu!')
            startScreen()
            updateStudentList()
            break

def teacherMenuScreen():
    print('|== İşlemler ==|\n',
          'a) Öğrenci Ekle\n',
          'b) Öğrenci Sil\n',
          'c) Not Ekle/Sil\n')

def teacherScreen(teacher, teacherIndex):
    CURRENT_USER = teacher
    LOGGED['teacher'] = True
    print('\n=== Hoşgeldiniz, {ad} {soyad}. ===\n\n'.format(ad=teacher['name'],soyad=teacher['surname']))
    
    teacherMenuScreen()

    while True:
        if LOGGED['student'] == False and LOGGED['teacher'] == True:
            command = input('[Öğretmen] Komut >> ')
            
            if command not in ['a','b','c']:
                print('Yanlış komut!\n')
            elif command == 'a': # Öğrenci ekle
                print('\n== Öğrenci Ekleme ==\n')
                studentRegister(customText='\nÖğrenci başarıyla kayıt edildi!\n',runFunc='teacherScreen')
            elif command == 'b': # Öğrenci sil
                if len(STUDENT_LIST) > 0:
                    counter = 0
                    while True:
                        for i in STUDENT_LIST:
                            print('#'+str(counter),i['name']+' '+i['surname']+' - '+i['username'])
                            counter += 1
                        id = int(input('Silmek istediğiniz öğrencinin ID\'sini giriniz: '))
                        if id > counter:
                            print('\n[!] Doğru bir ID giriniz!')
                        else:
                            with open(path['student'],'r') as f:
                                r = f.read().split('\n')[:-1]
                                r.remove( r[id] )
                                r = '\n'.join(r)+'\n'
                            with open(path['student'],'w') as f:
                                f.write(r)
                            print('\nBaşarıyla sildiniz.\n')
                            updateStudentList(clearArray=True)
                            teacherMenuScreen()
                            break
                else:
                    print('\nÖğrenci bulunamadı!\n')
                    teacherMenuScreen()
            elif command == 'c': # not ekle / sil
                counter = 0
                for i in STUDENT_LIST:
                    print('#'+str(counter),i['name']+' '+i['surname']+' - '+i['username'])
                    counter += 1
                _id = int(input('Seçmek istediğiniz öğrencinin ID\'sini giriniz: '))
                if _id > counter:
                    print('\n[!] Doğru bir ID giriniz!')
                else:
                    counter = 0
                    for j in STUDENT_LIST[_id]['lessons']:
                        print('#'+str(counter),j['lesson'])
                        counter += 1
                    id = int(input('Düzenlemek istediğiniz notun dersinin ID\'sini giriniz: '))
                    if id > counter:
                        print('\n[!] Doğru bir ID giriniz!')
                    else:
                        notes = input('Notları virgül(,) ile giriniz: ')
                        STUDENT_LIST[_id]['lessons'][id]['notes'] = notes.split(',')
                        saveStudent(STUDENT_LIST[_id],_id)
                        print('\nBaşarıyla düzenlediniz.\n')
                        updateStudentList(clearArray=True)
                        teacherMenuScreen()
                        break

def teacherLogin():
    data = {
        'username': input('Kullanıcı adı: '),
        'password': input('Şifre: ')
    }
    for std in TEACHER_LIST:
        if data['username'] == std['username'] and data['password'] == std['password']:
            print('Başarıyla giriş yaptınız.')
            teacherScreen(std,TEACHER_INDEX)
            break
    else:
        print('[!] Kullanıcı adı veya şifre yanlış!')
        startScreen()

### OFF-FUNCTIONS ###
def startScreen():
    print('\n=== LYK2017 Öğretim Sistemi ===\n\n')
    print('|== Giriş Bölümü ==|\n','a) Öğrenci Girişi\n','b) Öğretmen Girişi','\n\n'
          '|== Kayıt Bölümü ==|\n','c) Öğrenci Kayıt Ol\n','d) Öğretmen Kayıt')

def main():
    startScreen()
    while True:
        if LOGGED['student'] == False and LOGGED['teacher'] == False:
            command = input('\nKomut >> ')

            if command not in ['a','b','c','d']:
                print('Yanlış komut!')
            else:
                if command == 'a': # öğrenci - giriş yap
                    print('\n== Öğrenci Giriş Sistemi ==')
                    studentLogin()
                elif command == 'b': # öğretmen - giriş yap
                    print('\n== Öğretmen Giriş Sistemi ==')
                    teacherLogin()
                elif command == 'c': # öğrenci - kayıt ol
                    print('== Öğrenci Kayıt Sistemi ==')
                    studentRegister()
                elif command == 'd':
                    print('== Öğretmen Kayıt Sistemi ==')
                    teacherRegister()
        else: break

# Show start screen
updateStudentList()
updateTeacherList()
main()