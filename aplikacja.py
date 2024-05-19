from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, 
    QPushButton, QRadioButton, QVBoxLayout, 
    QHBoxLayout, QVBoxLayout,QProgressBar,
    QLineEdit, QButtonGroup, QListWidget,
    QFileDialog, QGroupBox, QMessageBox, QMenuBar
)
from PyQt5.QtGui import QRegExpValidator
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
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.setWindowTitle("Błąd")
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.progresBar = QProgressBar()
        self.progresBar.setRange(0,100)
    def wyswietlPliki(self):
        try:
            self.podgladLista.clear()
            self.dir_name = QFileDialog.getExistingDirectory(self, "Wybierz folder z danymi pomiarowymi")
            pliki = os.listdir(self.dir_name)
            for plik in pliki:
                if plik.endswith('.csv'):
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
        #czy wszystkie potrzebne pola zostaly uzupelnione?
        if self.dir_name == "" or self.dir_name == None:
            self.msgBox.setText("Źła ścieżka do plików lub jej brak")
            return self.msgBox.exec()
        elif self.opcja == None:
            self.msgBox.setText("Nie wybrano sposobu pomiaru")
            return self.msgBox.exec()
        elif self.podgladLista.count() == 0:
            self.msgBox.setText("Nie ma plików albo nie są w formacie CSV")
            return self.msgBox.exec()
        try:
            self.grubosc = float(grProbki.text())
            if self.opcja == 1:
                self.dlugosc = float(dlProbki.text())
                self.szerokosc = float(szProbki.text())
            elif self.opcja == 0:
                self.ppkont = float(ppKontaktu.text())
        except:
            self.msgBox.setText("Wystąpił błąd. Sprawdź czy wpisałeś liczby i użyłeś kropki. Można też użyć notacji naukowej.")
            return self.msgBox.exec()
        self.msgBox.setIcon(QMessageBox.Warning)
        obliczenia.petlaObliczen(self.dir_name,self.opcja,self.dlugosc,self.szerokosc,self.grubosc,self.ppkont,self.progresBar,self.msgBox)
        self.msgBox.setWindowTitle("Sukces")
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText("Operacja zakończona sukcesem")
        status = self.msgBox.exec()
        if status == QMessageBox.Ok:
            self.progresBar.reset()


    def interface(self):
#ustawienia okna
        regex = QRegExp("[0-9eE.-]*")
        validator = QRegExpValidator(regex)
        self.resize(600,400)
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
        dlProbki.setValidator(validator)
        szProbki.setValidator(validator)
        grProbki.setValidator(validator)
        ppKontaktu.setValidator(validator)
        podgladPrzycisk = QPushButton("Wybierz folder")
        obliczPrzycisk = QPushButton("Wykonaj Obliczenia")
        self.cipGrupa = QGroupBox("Wprowadź informacje o sposobie wykonania pomiaru")
        self.cppGrupa = QGroupBox("Wprowadź informacje o sposobie wykonania pomiaru")
        

#layouty
        mainLayout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
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
        row2.addWidget(self.progresBar)
        row3.addWidget(obliczPrzycisk)
        mainLayout.addLayout(row1)
        mainLayout.addLayout(row2)
        mainLayout.addLayout(row3)
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