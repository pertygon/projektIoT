import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class WykresApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.df = None
        self.filename = None

    def initUI(self):
        main_layout = QHBoxLayout()

        # Left layout for the plot
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # Right layout for controls
        control_layout = QVBoxLayout()

        self.label = QLabel("Wybierz plik Excel:", self)
        control_layout.addWidget(self.label)

        self.button = QPushButton("Wybierz plik", self)
        self.button.clicked.connect(self.wybierz_plik)
        control_layout.addWidget(self.button)

        self.label2 = QLabel("", self)
        control_layout.addWidget(self.label2)

        self.wiersze_input = QLineEdit(self)
        self.wiersze_input.setPlaceholderText("Podaj numery wierszy oddzielone spacją lub przecinkiem")
        control_layout.addWidget(self.wiersze_input)

        self.button2 = QPushButton("Rysuj wykres", self)
        self.button2.clicked.connect(self.rysuj_wykres)
        control_layout.addWidget(self.button2)

        self.save_button = QPushButton("Zapisz wykres jako JPG", self)
        self.save_button.clicked.connect(self.zapisz_wykres)
        control_layout.addWidget(self.save_button)

        control_layout.addStretch()

        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Wykres z Excela')
        self.setGeometry(100, 100, 1000, 600)

    def wybierz_plik(self):
        options = QFileDialog.Options()
        self.filename, _ = QFileDialog.getOpenFileName(self, "Wybierz plik Excel", "", "Excel files (*.xlsx)", options=options)
        if self.filename:
            self.df = pd.read_excel(self.filename)
            if 'omega' in self.df.columns:
                self.df = self.df.drop(columns=['omega'])
            num_rows = len(self.df)
            self.label2.setText(f"Liczba wierszy w pliku: {num_rows}")
        else:
            self.label2.setText("Nie wybrano pliku")

    def rysuj_wykres(self):
        if self.df is not None:
            numer_wierszy_str = self.wiersze_input.text()
            if numer_wierszy_str.strip() == "":
                QMessageBox.critical(self, "Błąd", "Nie wprowadzono numerów wierszy.")
                return

            try:
                numery_wierszy = [int(num) for num in numer_wierszy_str.replace(",", " ").split()]

                self.ax.clear()
                for numer_wiersza in numery_wierszy:
                    if numer_wiersza < 1 or numer_wiersza > len(self.df):
                        QMessageBox.critical(self, "Błąd", f"Numer wiersza {numer_wiersza} jest poza zakresem.")
                        continue
                    tp_label = self.df.columns[numer_wiersza + 1] if numer_wiersza + 1 < len(self.df.columns) else f"Wiersz {numer_wiersza}"
                    self.ax.plot(self.df.iloc[numer_wiersza - 1][2:], marker='o', linestyle='-', label=f"Tp {tp_label}")
                self.ax.set_title(f'Wykres dla pliku {self.filename.split("/")[-1]}', fontsize=16, color='red')
                self.ax.set_xlabel('Frequency', fontsize=14)
                self.ax.set_ylabel('Value', fontsize=14)
                self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)
                self.ax.legend()
                self.canvas.draw()
            except ValueError:
                QMessageBox.critical(self, "Błąd", "Wprowadzono nieprawidłowe numery wierszy.")
        else:
            QMessageBox.critical(self, "Błąd", "Nie wybrano pliku.")

    def zapisz_wykres(self):
        if self.df is not None:
            save_options = QFileDialog.Options()
            save_path, _ = QFileDialog.getSaveFileName(self, "Zapisz wykres jako JPG", "", "JPEG files (*.jpg);;All Files (*)", options=save_options)
            if save_path:
                self.figure.savefig(save_path)
                QMessageBox.information(self, "Sukces", "Wykres został zapisany.")
            else:
                QMessageBox.warning(self, "Błąd", "Nie podano ścieżki do zapisu.")
        else:
            QMessageBox.critical(self, "Błąd", "Brak danych do zapisania. Najpierw wczytaj plik i narysuj wykres.")

