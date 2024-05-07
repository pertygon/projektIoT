from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, 
    QPushButton, QRadioButton, QVBoxLayout, 
    QHBoxLayout, QVBoxLayout,QProgressBar,
    QLineEdit, QButtonGroup, QListWidget,
    QFileDialog, QGroupBox, QMessageBox
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
        self.opcja = None
        self.dlugosc = None
        self.szerokosc = None
        self.grubosc = None
        self.ppkont = None
    def wyswietlPliki(self):
        try:
            self.podgladLista.clear()
            self.dir_name = QFileDialog.getExistingDirectory(self, "Wybierz folder z danymi pomiarowymi")
            pliki = os.listdir(self.dir_name)
            for plik in pliki:
                self.podgladLista.addItem(plik)
        except:
            pass
    def wyswietlCIP(self):
        self.cipGrupa.show()
        self.opcja = 1
        self.cppGrupa.hide()
    def wyswietlCPP(self):
        self.cppGrupa.show()
        self.opcja = 0
        self.cipGrupa.hide()
    def oblicz(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("Błąd")
        msgBox.setStandardButtons(QMessageBox.Ok)
        try:
            self.grubosc = float(grProbki.text())
            if self.opcja == 1:
                self.dlugosc = float(dlProbki.text())
                self.szerokosc = float(szProbki.text())
            elif self.opcja == 0:
                self.ppkont = float(ppKontaktu.text())
        except:
            msgBox.setText("Wystąpił błąd. Sprawdź czy wpisałeś liczby i użyłeś kropki. Można też użyć notacji naukowej.")
            return msgBox.exec()
        #czy wszystkie potrzebne pola zostaly uzupelnione?
        if self.dir_name == "" or self.dir_name == None:
            msgBox.setText("Źła ścieżka do plików")
            return msgBox.exec()
        elif self.opcja == None:
            msgBox.setText("Nie wybrano sposobu pomiaru")
            return msgBox.exec()
        elif self.opcja == 1:
            if self.dlugosc == None:
                msgBox.setText("Pole długość próbki nie zostało uzupełnione")
                return msgBox.exec()
            if self.szerokosc == None:
                msgBox.setText("Pole szerokość próbki nie zostało uzupełnione")
                return msgBox.exec()
        elif self.opcja == 0:
            if self.ppkont == None:
                msgBox.setText("Pole pole powierzchni kontaktu nie zostało uzupełnione")
                return msgBox.exec()
        elif self.grubosc == None:
            msgBox.setText("Pole grubość próbki nie zostało uzupełnione")
            return msgBox.exec()
        obliczenia.petlaObliczen(self.dir_name,self.opcja,self.dlugosc,self.szerokosc,self.grubosc,self.ppkont)
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
        global szProbki, grProbki, dlProbki, ppKontaktu
        dlProbkiEt = QLabel("Długość próbki")
        dlProbki = QLineEdit()
        szProbkiEt = QLabel("Szerokość próbki")
        szProbki = QLineEdit()
        grProbkiEt = QLabel("Grubość próbki")
        grProbki = QLineEdit()
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
        c2r4 = QHBoxLayout()
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
        g1m.addLayout(g1r1)
        g1m.addLayout(g1r2)
        self.cipGrupa.setLayout(g1m)
        #groupbox CPP
        g2r1.addWidget(ppKontaktuEt)
        g2r1.addWidget(ppKontaktu)
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
        c2r4.addWidget(grProbkiEt)
        c2r4.addWidget(grProbki)
        column1.addLayout(c1r1)
        column1.addLayout(c1r2)
        column1.addLayout(c1r3)
        column2.addLayout(c2r1)
        column2.addLayout(c2r2)
        column2.addLayout(c2r3)
        column2.addLayout(c2r4)
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