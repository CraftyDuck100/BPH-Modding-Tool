import os, shutil, json5, json, PyQt5, sys, PIL, fnmatch, dotenv
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QStaticText
dotenv.load_dotenv()
directory = os.getenv("WORKSHOP")
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
class ScrollLabel(QScrollArea):
 
    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
 
        # making widget resizable
        self.setWidgetResizable(True)
 
        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)
 
        # vertical box layout
        lay = QVBoxLayout(content)
 
        # creating label
        self.label = QLabel(content)
 
        # setting alignment to the text
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
 
        # making label multi-line
        self.label.setWordWrap(True)
 
        # adding label to the layout
        lay.addWidget(self.label)
 
    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)
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
        ligmalable.setFont(QtGui.QFont("Sanserif", 20))
        ligmalable.move(QPoint(100, 100))
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
        loadsteam.setIcon(QIcon("./Icons/steam.png"))
        loadsteam.triggered.connect(self.loadFromSteam)

        global setsteamauto
        setsteamauto = QAction("Search For Workshop Folder (Slow, and the program will think it's not responding, but it shouldn't take more than 5 minutes)", self)
        setsteamauto.setStatusTip("Searches for the BPH workshop path")
        setsteamauto.triggered.connect(self.findWorkshopDirectory)
        # Automatic Search For Workshop Folder
        text = ''
        if directory:
            for i in os.listdir(directory):
                text += f'{i}\n'
        # creating scroll label
        label = ScrollLabel(self)
        label.setGeometry(100, 26, 200, 80)
        # setting text to the label
        label.setText(text)
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.setToolTipsVisible(True)
        # file_menu.addSeparator()
        # file_menu.addAction(loadinddir)
        if directory: file_menu.addAction(loadsteam)
        else:
            file_steammenu = file_menu.addMenu("Set Path To Workshop")
            file_steammenu.setIcon(QIcon("./Icons/steam.png"))
            file_steammenu.addAction(setsteamauto)
        tools_menu = menu.addMenu("Tools")

    def onMyToolBarButtonClick(self, s):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        loadinddir.setText(f'{directory}')
        print(f'{directory}/icon.png')
        loadinddir.setIcon(QIcon(f'{directory}/icon.png'))

        #pybutton.setStyleSheet(f"background-image : url({directory}/icon.png);")
    def findWorkshopDirectory(self, s):
        
        #directory = find_path(["Steam","workshop","content","1970580"])
        if directory:
            dotenv.set_key("./.env","WORKSHOP", directory)
        else: print("could not find workshop folder")

    def loadFromSteam(self, s):
        loadinddir.setText(f'{directory}')
        print(f'{directory}/icon.png')
        loadinddir.setIcon(QIcon("./Icons/steam.png"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )

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