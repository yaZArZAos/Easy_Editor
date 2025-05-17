from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
import os 
from PIL import Image, ImageOps, ImageFilter
from PyQt5.QtGui import QPixmap


class ImageProcessor():
    def __init__(self):
        self.filename = None
        self.image = None
        self.dir = None
        self.save_dir = 'Modified/'

    def loadImage(self, filename):
        self.filename = filename
        self.dir = workdir
        image_path = os.path.join(self.dir, self.filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width = picture.width()
        label_height = picture.height()
        scaled_pixmap = pixmapimage.scaled(label_width,
                                            label_height,
                                            Qt.KeepAspectRatio)
        picture.setPixmap(scaled_pixmap)
        picture.setVisible(True)  

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        if line.selectedItems():
            self.image = ImageOps.grayscale(self.image)
            self.saveImage()
            image_path = os.path.join(
                self.dir, self.save_dir,self.filename
            )
            self.showImage(image_path)
        else:
            error_win = QMessageBox()
            error_win.setText('Выберите картинку')
            error_win.exec()

    def do_mirror(self):
        if line.selectedItems():
            self.image = ImageOps.mirror(self.image)
            self.saveImage()
            image_path = os.path.join(
                self.dir, self.save_dir,self.filename
            )
            self.showImage(image_path)
        else:
            error_win = QMessageBox()
            error_win.setText('Выберите картинку')
            error_win.exec()

    def do_sharpness(self):
        if line.selectedItems():
            try:
                self.image = self.image.filter(ImageFilter.SHARPEN)
            except:
                error_win = QMessageBox()
                error_win.setText('Изображение не редактируется')
                error_win.exec()
            self.saveImage()
            image_path = os.path.join(
                self.dir, self.save_dir,self.filename
            )
            self.showImage(image_path)
        else:
            error_win = QMessageBox()
            error_win.setText('Выберите картинку')
            error_win.exec()

    def do_left(self):
        if line.selectedItems():
            self.image = self.image.rotate(90)
            self.saveImage()
            image_path = os.path.join(
                self.dir, self.save_dir,self.filename
            )
            self.showImage(image_path)
        else:
            error_win = QMessageBox()
            error_win.setText('Выберите картинку')
            error_win.exec()

    def do_right(self):
        if line.selectedItems():
            self.image = self.image.rotate(-90)
            self.saveImage()
            image_path = os.path.join(
                self.dir, self.save_dir,self.filename
            )
            self.showImage(image_path)
        else:
            error_win = QMessageBox()
            error_win.setText('Выберите картинку')
            error_win.exec()

workimage = ImageProcessor()

def showChosenImage():
    if line.currentRow() >= 0:
        filename = line.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workimage.dir, 
                                  filename)
        workimage.showImage(image_path)

workdir = '' 

def chooseWorkDir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = list()
    for file1 in files:
        for extension in extensions:
            if file1.endswith(extension):
                result.append(file1)
    return result

def showFilenamesList():
    chooseWorkDir()
    extensions = ['.jpg', '.jpeg', '.png', '.gif']
    files = os.listdir(workdir)
    files = filter(files, extensions)
    line.clear()
    line.addItems(files)

editor = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(700, 500)
picture = QLabel()
picture.setText('Картинка')
line = QListWidget()

bleft = QPushButton('Лево')
bright = QPushButton('Право') 
bfolder = QPushButton('Папка')
bmirror = QPushButton('Зеркало')
bsharpness = QPushButton('Резкость')
bHB = QPushButton('Ч/Б')

lines = QHBoxLayout()
VL1 = QVBoxLayout()
VL2 = QVBoxLayout()
HL1 = QHBoxLayout()
VL1.addWidget(bfolder)
VL1.addWidget(line)
HL1.addWidget(bleft)
HL1.addWidget(bright)
HL1.addWidget(bmirror)
HL1.addWidget(bsharpness)
HL1.addWidget(bHB)
VL2.addWidget(picture)
VL2.addLayout(HL1)
lines.addLayout(VL1)
lines.addLayout(VL2)

bright.clicked.connect(workimage.do_right)
bleft.clicked.connect(workimage.do_left)
bsharpness.clicked.connect(workimage.do_sharpness)
bmirror.clicked.connect(workimage.do_mirror)
bHB.clicked.connect(workimage.do_bw)
line.currentRowChanged.connect(showChosenImage)
bfolder.clicked.connect(showFilenamesList)
main_win.setLayout(lines)
main_win.show()
editor.exec_()