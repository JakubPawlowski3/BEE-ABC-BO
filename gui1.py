from PySide6.QtCore import Qt, QRect, QPropertyAnimation
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QHBoxLayout
from PySide6.QtGui import QPixmap, QIcon, Qt

class Application(QWidget):
    def __init__(self):
        super().__init__()

        self.menu_width = 200
        self.animation_duration = 200
        self.setStyleSheet('background-color:#')

        self.setup()
        
    def setup(self):
        
        self.setGeometry(100, 100, 800, 600)

        self.layoutV1 = QVBoxLayout()
        self.layoutV2 = QVBoxLayout()
        self.layoutH1 = QHBoxLayout()
        self.layoutH2 = QHBoxLayout()
        self.layoutH3 = QHBoxLayout()
        self.main_layout = QVBoxLayout()
        self.layoutV1.addLayout(self.layoutH1)
        self.layoutV2.addLayout(self.layoutH2)
        self.layoutV1.addLayout(self.layoutH3)
        self.main_layout.addLayout(self.layoutV1)
        self.main_layout.addLayout(self.layoutV2)
        self.setLayout(self.main_layout)

        self.menu_btn = QPushButton(self)
        self.menu_pixmap = QPixmap('icons8-menu-64.png')
        self.menu_btn.setIcon(QIcon(self.menu_pixmap))
        self.menu_btn.setIconSize(self.menu_btn.size())
        self.menu_btn.setFlat(True)
        self.menu_btn.clicked.connect(self.slidemenu)
        self.layoutH2.addWidget(self.menu_btn, alignment= Qt.AlignTop | Qt.AlignCenter)
        self.layoutH2.addStretch(2000)

        self.menu_frame = QFrame(self)
        self.menu_frame.setGeometry(QRect(-self.menu_width, 100, self.menu_width, self.height()))
        self.menu_layout = QVBoxLayout(self.menu_frame)


        self.menu_layout.addWidget(QPushButton("Parametry", self.menu_frame))
        
        self.menu_animation = QPropertyAnimation(self.menu_frame, b"geometry")
        self.menu_animation.setDuration(self.animation_duration)
        



        self.show()

    def slidemenu(self):
        if self.menu_animation.state() == QPropertyAnimation.Running:
            # Jeśli animacja jest w trakcie, zakończ ją
            self.menu_animation.stop()

        if self.menu_frame.geometry().x() == -self.menu_width:
            self.menu_animation.setStartValue(QRect(0, 0, 0, self.height()))
            self.menu_animation.setEndValue(QRect(0, 0, self.menu_width, self.height()))
        else:
            self.menu_animation.setStartValue(QRect(0, 0, self.menu_width, self.height()))
            self.menu_animation.setEndValue(QRect(-self.menu_width, 0, 0, self.height()))
        self.menu_btn.raise_()
        self.menu_animation.start()
        
app = QApplication([])
login = Application()
app.exec()