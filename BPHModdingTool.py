import os, shutil, json5, json, PyQt5, sys, PIL, fnmatch, dotenv, random, QFlowLayout, math
from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QStaticText, QMouseEvent, QPixmap, QImage
from PIL import Image, ImageDraw, ImageFont
dotenv.load_dotenv()
global loe
loe = 0
directory = os.getenv("WORKSHOP")
def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result
def ligma(dir):
    i=1
    filename: str
    outputstr = ''
    types = {}
    rarities = {}
    for filename in os.listdir(dir):
        if filename.endswith('.json'):
            try:
                f = dir + "/" + filename
                print(i,"Converting",filename)
                json_string=open(f).read()
                json_string=json_string[json_string.find('{'):] # Filter out garbage characters at the beginning of the file
                json_in=json5.loads(json_string)
                itemstr={}
                # item name
                rarity = str(json_in["rarity"])[0].upper() + str(json_in["rarity"])[1:]
                print(rarity)
                itemstr["name"]=json_in["name"]
                itemstr["type"]=json_in["type"]
                itemstr["rarity"]=json_in["rarity"]
                outputstr += f'{itemstr["name"]} ('
                if rarity in rarities.keys(): rarities.update({rarity: rarities[rarity] + 1})
                else: rarities[rarity] = 1
                for ie in itemstr["type"]:
                    ie2 = ie
                    if not str(ie)[0].isupper(): ie2 = str(ie)[0].upper() + (str(ie)[1:])
                    if ie2 in types.keys(): types.update({ie2: types[ie2] + 1})
                    else: types[ie2] = 1
                    outputstr += ie2
                    if not ie == itemstr["type"][len(itemstr["type"]) - 1]: outputstr += ', '
                outputstr += ')\n'
                i+=1
            except: continue
    outputcount = dict(sorted(types.items(), key=lambda x:x[1], reverse=True))
    outputrarities = dict(sorted(rarities.items(), key=lambda x:x[1], reverse=True))
    countstr = ''
    raritiesstr = ''
    print(outputcount)
    for ir in outputcount.items():
        countstr += f'{str(ir[1])} {str(ir[0])}\n'
    for ir in outputrarities.items():
        raritiesstr += f'{str(ir[1])} {str(ir[0])}\n'
    outputstr = countstr + '\n' + raritiesstr + '\n' + outputstr
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
#class QCScrollArea(QScrollArea):
#    def resizeEvent(self, event):
#        try:
#            if not event.oldSize().width() // 190 == event.size().width() // 190:
#                #mainWin.splitter.setSizes([190*(event.oldSize().width()//190), mainWin.splitter.width() % 190 + mainWin.splitter.sizes()[1]])
#                #mainWin.canvas.setGeometry(0, 26, 190*round(mainWin.buttonarea.width()/190), mainWin.buttonarea.height())
#                mainWin.content.setGeometry(0, 26, 190*(event.oldSize().width()//190), mainWin.buttonarea.height())
#            else:
#                
#                mainWin.content.setGeometry(0, 26, event.oldSize().width(), mainWin.buttonarea.height())
#            mainWin.splitter.setSizes([event.oldSize().width(), event.oldSize().height()])
#        except: print("hi")
print(os.path.exists(("/".join((os.path.abspath('./').split('common')[0]).split('\\'))) + "workshop/content/1970580/"))
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(1200, 800))    
        self.setWindowTitle("Crafty's Backpack Hero Modding Tools") 
        self.setStatusBar(QStatusBar(self))
        global ligmalable
        ligmalable = QLabel(self)
        ligmalable.setText("hi")
        ligmalable.setStyleSheet("""QLabel{font-family:Edit Undo BRK;font-size:}""")
        ligmalable.move(QPoint(0, ligmalable.height()))
        # Load Individual Folder
        global eeee
        eeee = QWidget()
        global loadinddir
        loadinddir = QAction("Load a mod from a folder", self)
        loadinddir.setStatusTip("Load Directory")
        loadinddir.triggered.connect(self.onMyToolBarButtonClick)
        self.pbar = QProgressBar(self)
        self.pbar.setFormat(f'Reading Items %p%')
        self.pbar.setGeometry(self.width()-300, 26, 300, 29)
        self.pbar.setHidden(True)
        # Load Mods From Steam
        global loadsteam
        loadsteam = QAction("Load Mods From Steam", self)
        loadsteam.setStatusTip("Load all the mods you've subscribed to from the Workshop (Don't Click or Tab Out while it's loading or it'll say it's not responding (it still will though))")
        loadsteam.setDisabled(True)
        if directory:
            if(directory.endswith("1970580/")): loadsteam.setEnabled(True)
        loadsteam.setIcon(QIcon("./Assets/Icons/steam.png"))
        loadsteam.triggered.connect(self.loadAtlas)
         # Automatic Search For Workshop Folder

        global setsteamauto
        setsteamauto = QAction("Search For Workshop Folder (Slow, and the program will think it's not responding, but it shouldn't take more than like 5 minutes)", self)
        setsteamauto.setStatusTip("Searches for the BPH workshop path")
        setsteamauto.triggered.connect(self.slowFindWorkshopDirectory)

        global steammanual
        steammanual = QAction("Manually Select Steam Workshop Folder (Select */workshop/* Folder pls)", self)
        steammanual.setStatusTip("Manually select workshop path")
        steammanual.triggered.connect(self.manualSteamDir)

        global listmanual
        listmanual = QAction("Compile List", self)
        listmanual.setStatusTip("Grabs all the item JSONs in the folder and makes a list (plus counts of each item type)")
        listmanual.triggered.connect(self.makeListFromManual)

        # setting text to the label
        global menu
        menu = self.menuBar()
        global file_menu
        file_menu = menu.addMenu("File")
        file_menu.setToolTipsVisible(True)
        # file_menu.addSeparator()
        # file_menu.addAction(loadinddir)
        if directory: file_menu.addAction(loadsteam)
        else:
            file_steammenu = file_menu.addMenu("Set Path To Workshop")
            file_steammenu.setIcon(QIcon("./Icons/steam.png"))
            file_steammenu.addAction(steammanual)
            file_steammenu.addAction(setsteamauto)
        tools_menu = menu.addMenu("Tools")
        tools_menu.addAction(listmanual)
    def manualSteamDir(self, s):
        ligdirectory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select the Steam Workshop directory')
        if os.path.exists(ligdirectory + "/content/1970580/"):
            directory2 = (ligdirectory + "/content/1970580/")
            loadsteam.setEnabled(True)
            file_menu.addAction(loadsteam)
        try:
            dotenv.set_key("./.env","WORKSHOP", directory2)
            global directory
            directory = directory2
        except: print("Directory Incorrect", ligdirectory)
    def onMyToolBarButtonClick(self, s):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        loadinddir.setText(f'{directory}')
        print(f'{directory}/icon.png')
        loadinddir.setIcon(QIcon(f'{directory}/icon.png'))
        #pybutton.setStyleSheet(f"background-image : url({directory}/icon.png);")

    def slowFindWorkshopDirectory(self, s):
        directory2 = find_path(["Steam","workshop","content","1970580"])
        if directory2:
            dotenv.set_key("./.env","WORKSHOP", directory2)
            global directory
            directory = directory2
        else: print("could not find workshop folder")
        setsteamauto.setDisabled(True)

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
        mainWin.loadAtlas()

    def makeListFromManual(self, s):
        ligdirectory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        ligma(ligdirectory + '/Items/')

    def listMods(self, s):
        count = 0
        for dir in os.listdir(directory):
            for path in os.listdir(f'{directory}{dir}/Items/'):
                if str(path).endswith(".json"):
                    count += 1
        print(count)
        self.item = QScrollArea(self)
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
        self.item.layout = (QVBoxLayout(content))
        
        print(mapping)
        self.buttons = []
        for key, value in mapping.items():
            self.buttons.append(QPushButton(key, self))
            self.buttons[-1].clicked.connect(partial(mainWin.loadFromSteam, data=value))
            self.item.layout.addWidget(self.buttons[-1])
            print("hi")
        self.item.setWidget(content)
        self.item.setGeometry(0, 26, 1000, 1000)
    
    def loadAtlas(self, s):
        self.pbar.setHidden(False)
        precount = 0
        for dir in os.listdir(directory):
            for path in os.listdir(f'{directory}{dir}/Items/'):
                if str(path).endswith(".json"):
                    precount += 1
        count = 0
        text = {}
        for dir in os.listdir(directory):
            for path in os.listdir(f'{directory}{dir}/Items/'):
                if str(path).endswith(".json"):
                    try:
                        json_string=open(f'{directory}{dir}/Items/{path}').read()
                        json_string=json_string[json_string.find('{'):] # Filter out garbage characters at the beginning of the file
                        json_in=json5.loads(json_string)
                        text.update({str(count): {"name":str(json_in["name"])}})
                        text[str(count)]["sprite"] = f'{directory}{dir}/Items/{json_in["sprite"]}'
                        text[str(count)]["type"] = json_in["type"]
                        try: text[str(count)]["group"] = json_in["group"]
                        except: fe = 1
                        text[str(count)]["rarity"] = json_in["rarity"]
                        text[str(count)]["shape"] = json_in["shape"]
                        try: text[str(count)]["flavor"] = json_in["flavor"]
                        except: fe = 1
                        try: text[str(count)]["use_costs"] = json_in["use_costs"]
                        except: fe = 1
                        try: text[str(count)]["use_limits"] = json_in["use_limits"]
                        except: fe = 1
                        try: text[str(count)]["combat_effects"] = json_in["combat_effects"]
                        except: fe = 1
                        try: text[str(count)]["modifiers"] = json_in["modifiers"]
                        except: fe = 1
                        try: text[str(count)]["add_modifiers"] = json_in["add_modifiers"]
                        except: fe = 1
                        try: text[str(count)]["movement_effects"] = json_in["movement_effects"]
                        except: fe = 1
                        try: text[str(count)]["add_modifiers"] = json_in["add_modifiers"]
                        except: fe = 1
                        try: text[str(count)]["create_effects"] = json_in["create_effects"]
                        except: fe = 1
                        count += 1
                        self.pbar.setValue(math.ceil(count/precount*100))
                    except:
                        continue
        self.canvas = QWidget()
        self.canvas.setGeometry(0, 56, mainWin.width(), mainWin.height() - 56)
        self.pbar.setFormat(f'Generating Image Buttons %p%')
        self.searchbar = QLineEdit(self)
        self.buttonarea = QScrollArea(self.canvas)
        # making qwidget object
        self.cardcontent = QWidget(self)
        self.cardarea = QScrollArea(self)
        self.content = QWidget(self)
        self.cardarea.layout = (QHBoxLayout(self.cardcontent))
        # vertical box layout
        mapping = text
        self.buttonarea.layout = (QFlowLayout.FlowLayout(self.content))
        self.buttonarea.layout._vspacing = 0
        self.buttonarea.layout._hspacing = 0
        self.buttons = []
        io = 0
        for key, value in mapping.items():
            self.buttons.append(QPushButton('', self))
            try: 
                r = (str(value["sprite"]).split("[")[0] + str(value["sprite"]).split("[")[1][:-1].split(",")[0][1:-1])
                e = 1
            except: e = 0
            try:
                if not e: image = Image.open(str(value["sprite"]))
                else: image = Image.open(str(value["sprite"]).split("[")[0] + str(value["sprite"]).split("[")[1][:-1].split(",")[0][1:-1])
                W = 190
                H = 240
                # creating a copy of original image
                watermark_image = image.copy()
                ligmaimage = Image.new(mode="RGB", size=[W,H])
                if watermark_image.width > watermark_image.height: numb = watermark_image.width
                else: numb = watermark_image.height
                watermark_image = watermark_image.resize([int((160/numb)*watermark_image.width), int((160/numb)*watermark_image.height)], Image.Resampling.NEAREST)
                self.buttons[-1].clicked.connect(partial(mainWin.generateCard, data=value, image = image))
                # Draw function and assigned to draw
                draw = ImageDraw.Draw(ligmaimage)
                draw.rectangle((1,1, W - 2, H -2), (70, 46, 11))
                draw.rectangle((10,10, W - 11, H - 11), (137,88,45))
                draw.rectangle((1,180, 190, 189), (70, 46, 11))
                fontsize = 30
                font = ImageFont.truetype("Assets/editundo.ttf", fontsize)
                _, _, w, h = draw.textbbox((0, 0), str(value["name"]), font=font)
                while h < 30:
                    font = ImageFont.truetype("Assets/editundo.ttf", fontsize)
                    _, _, w, h = draw.textbbox((0, 0), str(value["name"]), font=font)
                    fontsize += 1
                while w > ligmaimage.width - 30:
                    font = ImageFont.truetype("Assets/editundo.ttf", fontsize)
                    _, _, w, h = draw.textbbox((0, 0), str(value["name"]), font=font)
                    fontsize -= 1
                ligmaimage.paste(watermark_image, (int(max(((W-watermark_image.width)/2), 0)), int((160 - watermark_image.height)/2) + 15), watermark_image)
                draw.text((W/2, 210), str(value["name"]), font=font, anchor="mm")
                ligmaimage.save(f"Temp/image{io}.png")
                self.buttons[-1].setStyleSheet(f"background-image : url(./Temp/image{io}.png); border:0px")
            except: e= 2
            self.buttons[-1].setFixedSize(W,H)
            self.buttons[-1].setFlat(True)
            self.buttonarea.layout.addWidget(self.buttons[-1])
            self.pbar.setValue(math.ceil(io/precount*100))
            io += 1
        self.card = QLabel(self)
        self.cardarea.layout.addWidget(self.card)
        self.buttonarea.setWidget(self.content)
        self.cardarea.setWidget(self.cardcontent)
        
        self.searchbar.textChanged.connect(partial(self.updateSearch, m=mapping))
        self.buttonarea.setGeometry(0, 0, 380, 774)
        self.canvas.setGeometry(0, 56, mainWin.width(), mainWin.height() - 56)
        self.buttonarea.layout.setContentsMargins(0, 0, 0, 0)
        self.cardarea.layout.setContentsMargins(0, 0, 0, 0)
        self.buttonarea.setWidgetResizable(True)
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setGeometry(0, 56, mainWin.width(), mainWin.height() - 56)
        self.splitter.addWidget(self.buttonarea)
        self.splitter.addWidget(self.cardarea)
        self.buttonarea.setStyleSheet('background-color: #d7b594;')
        self.cardarea.setStyleSheet('background-color: #d7b594;')
        self.searchbar.setGeometry(0, 26, 800, 29)
        QtGui.QFontDatabase.addApplicationFont("./Assets/editundo.ttf")
        self.searchbar.setFont(QtGui.QFont("Edit Undo BRK", 15))
        self.leftbutton = QPushButton("<", self)
        self.resetbutton = QPushButton("\\", self)
        self.rightbutton = QPushButton(">", self)
        self.leftbutton.clicked.connect(partial(self.resizeLayout, -1))
        self.resetbutton.clicked.connect(partial(self.resizeLayout, 0))
        self.rightbutton.clicked.connect(partial(self.resizeLayout, 1))
        self.leftbutton.setGeometry(801, 26, 30, 29)
        self.resetbutton.setGeometry(832, 26, 30, 29)
        self.rightbutton.setGeometry(863, 26, 30, 29)
        self.cardarea.setMinimumWidth(524)
        self.splitter.setChildrenCollapsible(False)
        mainWin.layout().addWidget(self.rightbutton)
        mainWin.layout().addWidget(self.resetbutton)
        mainWin.layout().addWidget(self.leftbutton)
        mainWin.layout().addWidget(self.searchbar)
        mainWin.layout().addWidget(self.splitter)
        self.splitter.setSizes([214, self.splitter.sizes()[1] + self.splitter.sizes()[0] - 214])
        self.splitter.setSizes([594, self.splitter.sizes()[1] + self.splitter.sizes()[0] - 594])
    def resizeLayout(self, direction):
        try:
            widgetLsize = 0
            widgetRsize = 0
            if direction == 0:
                widgetLsize = 214
                widgetRsize = self.splitter.sizes()[1] + self.splitter.sizes()[0] - 214
            else:
                if self.splitter.sizes()[1] <= 690 and direction == 1: return
                else:
                    widgetLsize = self.splitter.sizes()[0] + (direction*190)
                    widgetRsize = self.splitter.sizes()[1] - (direction*190)
                    if widgetLsize <= 214:
                        widgetLsize = 214
                        widgetRsize = self.splitter.sizes()[1] + self.splitter.sizes()[0] - 214
            self.buttonarea.setMinimumWidth(widgetLsize)
            self.cardarea.setMinimumWidth(widgetRsize)
            self.splitter.setSizes([widgetLsize, widgetRsize])
            #self.card.move(QPoint(int((widgetRsize - 24) / 2), 0))
        except: print("hi")

    def generateCard(self, data: dict, image: Image):
        print(data)
        print(self.card.pixmap())
        W = self.splitter.sizes()[1] - 24
        H = 3000
        cardimage = Image.new("RGBA", [W, 3000])
        draw = ImageDraw.Draw(cardimage)
        font = ImageFont.truetype("Assets/editundo.ttf", 42)
        _, _, w, h = draw.textbbox((0, 0), str(data["name"]), font=font)
        draw.rectangle(((W/2)-(w/2)-15 , 0, (W/2)-(w/2) + w + 15, h + 30), (116, 84, 64))
        draw.rectangle(((W/2)-(w/2)-4, 10, (W/2)-(w/2) + w + 5, h + 20), (173, 119, 87))
        draw.text((int(W/2-w/2) + 2, (h + 30)/2), str(data["name"]), font=font, anchor="lm")
        draw.rectangle((20, h + 21, W-20, H-20), (116, 84, 64))
        draw.rectangle((30, h + 31, W-30, H-30), (173, 119, 87))
        #draw.rectangle(((0)-(w/2)-5, 10, (W/2)-(w/2) + w + 5, h + 20), (173, 119, 87))
        dh = h + 31
        font = ImageFont.truetype("Assets/editundo.ttf", 25)
        itemtypestring = ''
        for itemtype in range(len(data["type"])):
            itemtypestring += str(data["type"][itemtype])
            if not itemtype == len(data["type"]) - 1: itemtypestring += '\n'
        print(itemtypestring)
        if image.width > image.height: numb = image.width
        else: numb = image.height
        image = image.resize([int((160/numb)*image.width), int((160/numb)*image.height)], Image.Resampling.NEAREST)
        cardimage.paste(image, (int(max(((W-image.width)/2), 0)), int((160-image.height)/2 + dh + 10)), image)
        draw.rectangle((40, dh + 160 + 20, W-40, dh + 160 + 25), (255, 255, 255))
        _, _, w, h = draw.textbbox((0, 0), itemtypestring, font=font)
        draw.text((40, dh + 174), itemtypestring, font=font, anchor="ld")
        color = (255, 255, 255, 255)
        if str(data["rarity"]).lower() == "uncommon": color = (43, 248, 52)
        if str(data["rarity"]).lower() == "rare": color = 'rgb(238, 248, 43)'
        if str(data["rarity"]).lower() == "legendary": color = 'rgb(234, 40, 238)'
        draw.text((W-40, dh + 174), str(data["rarity"]), fill=color, font=font, anchor="rs")
        line_spacing = 1.3  # Adjust this value based on your needs
        wrapped_text = wrap_text(str(data), 500, font)
        x = (cardimage.width - 455) // 2
        y = (cardimage.height - int(30 * len(wrapped_text) * line_spacing)) // 2
     
        for line in wrapped_text:
            line_width = font.getlength(line)
            draw.text(((cardimage.width - line_width) // 2, y), line, "white", font=font)
            y += int(30 * line_spacing)
        cardimage.save(f"Temp/card.png")
        for key, value in data.items():
            moddict = {}
            if key == 'modifiers':
                indox = 0
                tem: dict
                for tem in value:
                    if str(tem["trigger"]).lower() == "constant": print("e")
            print(key, value, type(value))
        cardmap = QPixmap("Temp/card.png")
        print(cardmap)
        self.card.setPixmap(cardmap)
        self.cardcontent.setFixedSize(self.splitter.sizes()[1] - 24, cardmap.height())
        #self.cardcontent.move(int((self.splitter.sizes()[1] - 24) / 2 - 250), 0)
        print('hi')
        #self.cardarea.resize(self.splitter.sizes()[1], self.splitter.height())
        #self.cardcontent.move(QPoint(int((self.cardcontent.width() - 24) / 2 - 250), 0))
        

    def updateSearch(self, text: str, m):
        print(self.splitter.sizes())
        il = 0
        index = 0
        if text.startswith("#"):
            for yr in self.buttons:
                if text[1:].lower() in str(m[str(il)].get("type")).lower(): yr.setHidden(False)
                else: yr.setHidden(True)
                il+=1
        elif text.startswith("%"):
            for yr in self.buttons:
                if str(m[str(il)].get("rarity")).lower().startswith(text[1:].lower()): yr.setHidden(False)
                else: yr.setHidden(True)
                il+=1
        elif text.startswith("?"):
            for yr in self.buttons:
                if text[1:].lower() in str(m[str(il)].get("flavor")).lower(): yr.setHidden(False)
                else: yr.setHidden(True)
                il+=1
        else:
            for yr in self.buttons:
                if text.lower() in m[str(il)].get("name").lower(): yr.setHidden(False)
                else: yr.setHidden(True)
                il+=1
    
    def resizeEvent(self, event):
        try:
            self.splitter.setGeometry(0, 56, mainWin.width(), mainWin.height() - 56)
            self.pbar.setGeometry(mainWin.width()-100, 26, 100, 29)
        except: q=2
        QMainWindow.resizeEvent(self, event)

def wrap_text(text, max_width, font):
    lines = []
    words = text.split(' ')
     
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        line_width = font.getlength(test_line)
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line[:-1])
            current_line = word + ' '
 
    lines.append(current_line[:-1])
    return lines
class FormWidget(QWidget):

    def __init__(self, parent):        
        super(FormWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.button1 = QPushButton("Button 1")
        self.layout.addWidget(self.button1)

        self.button2 = QPushButton("Button 2")
        self.layout.addWidget(self.button2)

        self.setLayout(self.layout)
app = QtWidgets.QApplication(sys.argv)
QtGui.QFontDatabase.addApplicationFont("Assets\editundo.ttf")
stylesheet = open('./style.qss').read()
app.setStyleSheet(stylesheet)
mainWin = MainWindow()
mainWin.show()
sys.exit(app.exec_())