from json_ornek import KampOtomasyon
class Menu(KampOtomasyon):
    def __init__(self):
        self.permittedCommands = ["a","b","c","d","e"]

    def askCommand(self,functionsToRun,commandText="Komut >> ",_doAuto=True):
        while 1:
            command = input(commandText)

            if _doAuto:
                print("")
                self.runCommand(command,self.permittedCommands,functionsToRun)
                self.showMainMenu()
            else: return command

    def runCommand(self,command,permittedCommands,functionsToRun,errorMessage="Komut bulunamadı."):
        if command not in permittedCommands:
            print( errorMessage,end="\n\n" )
        else:
            commandIndex = permittedCommands.index(command)
            functionsToRun[ commandIndex ]()

    def showMainMenu(self):
        print("\n=== JSON - Kamp Bilgi Otomasyonu ===\n",
              "a)Öğrenci Ekle\n",
              "b)Öğrenci Sil\n",
              "c)Öğrenci Düzenle\n",
              "d)Öğrenci Ara\n"
              "e)Girilen Bilgileri Listele",sep="",end="\n\n")

        self.askCommand([self.mass_add_student,self.delete_student,self.edit_student,self.search_student,self.list_student])