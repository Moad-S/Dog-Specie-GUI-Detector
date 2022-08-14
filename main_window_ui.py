import sys , os 
from PyQt5 import QtWidgets, uic , QtCore
from PyQt5.QtWidgets import QFileDialog,QMessageBox
import subprocess, platform
from PyQt5.QtGui import QIcon, QPixmap
script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir,"yolov5")
sys.path.append(mymodule_dir)

import detect as detect

class Ui(QtWidgets.QMainWindow):
    fileName=""
    save_dir=""
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('ui/main.ui', self) # Load the .ui file
        self.setFixedSize(800, 600)
        self.btnSelectImage.clicked.connect(self.imageLoad)
        self.btnDetectDogs.clicked.connect(self.imagedogprocess)
        self.btnOpenSaveFolder.clicked.connect(self.openSavedFolder)
        self.show() # Show the GUI

    def updateImage(self):
        pixmap = QPixmap(self.fileName)
        w = self.imageView.width();
        h = self.imageView.height();
        self.imageView.setPixmap(pixmap.scaled(w,h,QtCore.Qt.KeepAspectRatio))
    
    def imageLoad(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self,"Select Image", filter="Images (*.jpeg *.jpg *.png ")   
        if self.fileName:
            self.updateImage()
            self.btnDetectDogs.setEnabled(True)
    def imagedogprocess(self):
            # import subprocess
            # save_path ,save_dirm,label
            self.fileName , self.save_dir, label=detect.run(self.fileName)
            self.updateImage()
            self.breedText.setPlainText(label)
            self.btnOpenSaveFolder.setEnabled(True)

    def openSavedFolder(self):
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', self.save_dir))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(self.save_dir)
        else:                                   # linux variants
            subprocess.call(('xdg-open', self.save_dir))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui() # Create an instance of our class
    app.exec_() # Start the application

