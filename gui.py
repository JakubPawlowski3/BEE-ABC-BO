from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QApplication, QPushButton
from PySide6.QtCore import Qt
class Application(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Algorytm Pszczeli ABC")
        self.setFixedSize(640, 400)
        self.setStyleSheet("Background-color:#31145C")
        self.setup()

    def setup(self):

        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()
        layoutG = QGridLayout()
        layoutMain = QVBoxLayout()
        layoutMain.addLayout(layoutH)
        layoutMain.addLayout(layoutV)
        layoutMain.addLayout(layoutG)
        self.pshbtn = QPushButton("Button")
        layoutH.addWidget(self.pshbtn, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.show()



app = QApplication([])
login = Application()
app.exec()