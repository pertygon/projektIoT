from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, 
    QPushButton, QRadioButton, QVBoxLayout, 
    QHBoxLayout, QVBoxLayout,QProgressBar,
    QLineEdit, QButtonGroup, QListWidget,
    QFileDialog, QGroupBox
)
import obliczenia
import os
import sys
class oknoWyboru(QWidget):
    def __init__(self):
        super().__init__()
        self.dir_name = None
        self.podgladLista = None
        self.cipGrupa = None
        self.cppGrupa = None
    def wyswietlPliki(self):
        try:
            self.dir_name = QFileDialog.getExistingDirectory(self, "Wybierz folder z danymi pomiarowymi")
            pliki = os.listdir(self.dir_name)
            for plik in pliki:
                self.podgladLista.addItem(plik)
        except:
            pass
    def wyswietlCIP(self):
        self.cipGrupa.show()
        self.cppGrupa.hide()
    def wyswietlCPP(self):
        self.cppGrupa.show()
        self.cipGrupa.hide()
    def oblicz(self):
        obliczenia.petlaObliczen(self.dir_name)
    def interface(self):
#ustawienia okna
        self.resize(800,400)
        self.setWindowTitle("Projekt automatyzacji stanowiska do spektroskopii impedancyjnej")
#kontrolki       
        radioGroupBox = QGroupBox("Wybierz sposób wykonania pomiaru")
        radioGroup = QButtonGroup()
        CIP = QRadioButton("CIP")
        CPP = QRadioButton("CPP")
        radioGroup.addButton(CIP)
        radioGroup.addButton(CPP)
        dlProbkiEt = QLabel("Długość próbki")
        dlProbki = QLineEdit()
        szProbkiEt = QLabel("Szerokość próbki")
        szProbki = QLineEdit()
        grProbkiEt1 = QLabel("Grubość próbki")
        grProbki1 = QLineEdit()
        grProbkiEt2 = QLabel("Grubość próbki")
        grProbki2 = QLineEdit()
        ppKontaktuEt = QLabel("Pole powierzchni kontaktu")
        ppKontaktu = QLineEdit()
        podgladEtykieta = QLabel("Podgląd wybranych plików")
        self.podgladLista = QListWidget()
        podgladPrzycisk = QPushButton("Wybierz folder")
        obliczPrzycisk = QPushButton("Wykonaj Obliczenia")
        self.cipGrupa = QGroupBox("Wprowadź informacje o sposobie wykonania pomiaru")
        self.cppGrupa = QGroupBox("Wprowadź informacje o sposobie wykonania pomiaru")

#layouty
        mainLayout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        column1 = QVBoxLayout()
        column2 = QVBoxLayout()
        #kolumna 1
        c1r1 = QHBoxLayout()
        c1r2 = QHBoxLayout()
        c1r3 = QHBoxLayout()
        #kolumna 2
        c2r1 = QHBoxLayout()
        c2r2 = QHBoxLayout()
        c2r3 = QHBoxLayout()
        #groupbox CIP
        g1m = QVBoxLayout()
        g1r1 = QHBoxLayout()
        g1r2 = QHBoxLayout()
        #groupbox CPP
        g2m = QVBoxLayout()
        g2r1 = QHBoxLayout()
        g2r2 = QHBoxLayout()
        #groupbox radio
        radioH = QHBoxLayout()
#dodawanie elementów do layoutów
        #groupbox CIP
        g1r1.addWidget(dlProbkiEt)
        g1r1.addWidget(dlProbki)
        g1r1.addWidget(szProbkiEt)
        g1r1.addWidget(szProbki)
        g1r2.addWidget(grProbkiEt1)
        g1r2.addWidget(grProbki1)
        g1m.addLayout(g1r1)
        g1m.addLayout(g1r2)
        self.cipGrupa.setLayout(g1m)
        #groupbox CPP
        g2r1.addWidget(ppKontaktuEt)
        g2r1.addWidget(ppKontaktu)
        g2r2.addWidget(grProbkiEt2)
        g2r2.addWidget(grProbki2)
        g2m.addLayout(g2r1)
        g2m.addLayout(g2r2)
        self.cppGrupa.setLayout(g2m)
        #groupbox radio
        radioH.addWidget(CPP)
        radioH.addWidget(CIP)
        radioH.addStretch(1)
        radioGroupBox.setLayout(radioH)
        #okno
        c1r1.addWidget(podgladEtykieta)
        c1r2.addWidget(self.podgladLista)
        c1r3.addWidget(podgladPrzycisk)
        c2r1.addWidget(radioGroupBox)
        c2r3.addWidget(self.cipGrupa)
        c2r3.addWidget(self.cppGrupa)

        column1.addLayout(c1r1)
        column1.addLayout(c1r2)
        column1.addLayout(c1r3)
        column2.addLayout(c2r1)
        column2.addLayout(c2r2)
        column2.addLayout(c2r3)
        row1.addLayout(column1)
        row1.addLayout(column2)
        row2.addWidget(obliczPrzycisk)
        mainLayout.addLayout(row1)
        mainLayout.addLayout(row2)
        self.setLayout(mainLayout)
        self.show()
        self.cipGrupa.hide()
        self.cppGrupa.hide()
        podgladPrzycisk.clicked.connect(self.wyswietlPliki)
        CIP.clicked.connect(self.wyswietlCIP)
        CPP.clicked.connect(self.wyswietlCPP)
        obliczPrzycisk.clicked.connect(self.oblicz)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = oknoWyboru()
    okno.interface()
    sys.exit(app.exec_())