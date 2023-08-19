import os, shutil, json5, json, PyQt5, sys, PIL, fnmatch, dotenv, random
from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QStaticText
from PIL import Image, ImageDraw
dotenv.load_dotenv()
directory = os.getenv("WORKSHOP")
def ligma(dir):
    i=1
    filename: str
    outputstr = ''
    types = {}
    for filename in os.listdir(dir):
        if filename.endswith('.json'):
            f = dir + "/" + filename
            print(i,"Converting",filename)
            json_string=open(f).read()
            json_string=json_string[json_string.find('{'):] # Filter out garbage characters at the beginning of the file
            json_in=json5.loads(json_string)
            itemstr={}
            # item name
            itemstr["name"]=json_in["name"]
            itemstr["type"]=json_in["type"]
            outputstr += f'{itemstr["name"]} ('
            for ie in itemstr["type"]:
                ie2 = ie
                if not str(ie)[0].isupper(): ie2 = str(ie)[0].upper() + (str(ie)[1:])
                if ie2 in types.keys(): types.update({ie2: types[ie2] + 1})
                else: types[ie2] = 1
                outputstr += ie2
                if not ie == itemstr["type"][len(itemstr["type"]) - 1]: outputstr += ', '
            outputstr += ')\n'
            i+=1
    outputcount = dict(sorted(types.items(), key=lambda x:x[1], reverse=True))
    countstr = ''
    print(outputcount)
    for ir in outputcount.items():
        countstr += f'{str(ir[1])} {str(ir[0])}\n'
    outputstr = countstr + '\n' + outputstr
    with open("output.txt", 'w') as ere:
        ere.write(outputstr)
    print(countstr)
def find_path(folderpathsnip: list):
    ci = 0
    search_path = ['C:/']
    for ei in folderpathsnip:
        result = []
        for sp in search_path:
            for root, dir, file in os.walk(sp):
                if folderpathsnip[ci] in dir:
                    result.append(os.path.join(root, folderpathsnip[ci]))
        search_path = result
        ci+=1
    if result: return (("/".join(str(result[0]).split("\\")) + "/"))
    else: return False
class ModList(QScrollArea):
    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        # making qwidget object
        content = QWidget(self)
        text = {}
        # vertical box layout
        for ir in os.listdir(directory):
            fe = directory + ir + "/modpack.json"
            json_string=open(fe).read()
            json_string=json_string[json_string.find('{'):] # Filter out garbage characters at the beginning of the file
            json_in=json5.loads(json_string)
            text[ir] = (json_in["name"])
        mapping = text
        layout = QVBoxLayout(content)
        print(mapping)
        self.buttons = []
        self.buttons = []
        for key, value in mapping.items():
            self.buttons.append(QPushButton(key, self))
            self.buttons[-1].clicked.connect(partial(mainWin.loadFromSteam, data=value))
            layout.addWidget(self.buttons[-1])
        self.setGeometry(100, 100, 1000, 30)
        self.setWidget(content)
class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
print(os.path.exists(("/".join((os.path.abspath('./').split('common')[0]).split('\\'))) + "workshop/content/1970580/"))
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(1200, 800))    
        self.setWindowTitle("Crafty's Backpack Hero Modding Tools") 
        self.setStatusBar(QStatusBar(self))
        global ligmalable
        ligmalable = QLabel(self)
        ligmalable.setText("hi")
        ligmalable.setStyleSheet("""QLabel{font-family:Edit Undo BRK;font-size:}""")
        ligmalable.move(QPoint(0, ligmalable.height()))
        # Load Individual Folder
        global loadinddir
        loadinddir = QAction("Load a mod from a folder", self)
        loadinddir.setStatusTip("Load Directory")
        loadinddir.triggered.connect(self.onMyToolBarButtonClick)
        
        # Load Mods From Steam
        global loadsteam
        loadsteam = QAction("Load Mods From Steam", self)
        loadsteam.setStatusTip("Load all the mods you've subscribed to from the Workshop")
        loadsteam.setDisabled(True)
        if directory:
            if(directory.endswith("1970580/")): loadsteam.setEnabled(True)
        loadsteam.setIcon(QIcon("./Assets/Icons/steam.png"))
        loadsteam.triggered.connect(self.loadFromSteam)
         # Automatic Search For Workshop Folder
        global quicksteam
        quicksteam = QAction("Quick Search For Workshop Folder (Only works if BPH is installed on the same Drive Steam is)", self)
        # Search For Workshop Folder (Slow, and the program will think it's not responding, but it shouldn't take more than 5 minutes)
        quicksteam.setStatusTip("Searches for the BPH workshop path")
        quicksteam.triggered.connect(self.quickFindWorkshopDirectory)

        global setsteamauto
        setsteamauto = QAction("Search For Workshop Folder (Slow, and the program will think it's not responding, but it shouldn't take more than like 5 minutes)", self)
        setsteamauto.setStatusTip("Searches for the BPH workshop path")
        setsteamauto.triggered.connect(self.slowFindWorkshopDirectory)

        global listmanual
        listmanual = QAction("Compile List", self)
        listmanual.setStatusTip("Grabs all the item JSONs in the folder and makes a list (plus counts of each item type)")
        listmanual.triggered.connect(self.makeListFromManual)
        
        # setting text to the label
        global menu
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.setToolTipsVisible(True)
        # file_menu.addSeparator()
        # file_menu.addAction(loadinddir)
        if directory: file_menu.addAction(loadsteam)
        else:
            file_steammenu = file_menu.addMenu("Set Path To Workshop")
            file_steammenu.setIcon(QIcon("./Icons/steam.png"))
            file_steammenu.addAction(quicksteam)
            file_steammenu.addAction(setsteamauto)
        tools_menu = menu.addMenu("Tools")
        tools_menu.addAction(listmanual)
    def onMyToolBarButtonClick(self, s):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        loadinddir.setText(f'{directory}')
        print(f'{directory}/icon.png')
        loadinddir.setIcon(QIcon(f'{directory}/icon.png'))

        #pybutton.setStyleSheet(f"background-image : url({directory}/icon.png);")
    def quickFindWorkshopDirectory(self, s):
        if os.path.exists(("/".join((os.path.abspath('./').split('common')[0]).split('\\'))) + "workshop/content/1970580/"):
            directory = (("/".join((os.path.abspath('./').split('common')[0]).split('\\'))) + "workshop/content/1970580/")
        if directory:
            dotenv.set_key("./.env","WORKSHOP", directory)
        else: print("could not find workshop folder")
        setsteamauto.setDisabled(True)
        quicksteam.setDisabled(True)

    def slowFindWorkshopDirectory(self, s):
        directory = find_path(["Steam","workshop","content","1970580"])
        if directory:
            dotenv.set_key("./.env","WORKSHOP", directory)
        else: print("could not find workshop folder")
        setsteamauto.setDisabled(True)
        quicksteam.setDisabled(True)

    def loadFromSteam(self, s):
        text = {}
        loadinddir.setText(f'{directory}')
        print(f'{directory}/icon.png')
        loadinddir.setIcon(QIcon("./Icons/steam.png"))
        for ir in os.listdir(directory):
            fe = directory + ir + "/modpack.json"
            json_string=open(fe).read()
            json_string=json_string[json_string.find('{'):] # Filter out garbage characters at the beginning of the file
            json_in=json5.loads(json_string)
            text[ir] = (json_in["name"])
        logma = text
        print(logma)
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Pls do this to make program work cause I suck at coding")
        dlg.setText("Please restart the program")
        dlg.exec()

    def makeListFromManual(self, s):
        ligdirectory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        ligma(ligdirectory + '/Items/')
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont("Assets\editundo.ttf")
    stylesheet = open('./style.qss').read()
    app.setStyleSheet(stylesheet)
    mainWin = MainWindow()
    loade = ModList(mainWin)
    mainWin.show()
    sys.exit(app.exec_())