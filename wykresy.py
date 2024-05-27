import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
                             QLineEdit, QLabel, QMessageBox, QCheckBox)
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
        main_layout.addWidget(self.canvas, stretch=3)

        # Right layout for controls
        control_layout = QVBoxLayout()

        self.label = QLabel("Wybierz plik Excel:", self)
        control_layout.addWidget(self.label)

        self.button = QPushButton("Wybierz plik", self)
        self.button.clicked.connect(self.wybierz_plik)
        control_layout.addWidget(self.button)

        self.label2 = QLabel("", self)
        control_layout.addWidget(self.label2)

        self.freq_label = QLabel("", self)
        control_layout.addWidget(self.freq_label)

        freq_input_layout = QHBoxLayout()
        self.freq_min_input = QLineEdit(self)
        self.freq_min_input.setPlaceholderText("Min")
        self.freq_min_input.setEnabled(False)
        freq_input_layout.addWidget(self.freq_min_input)

        self.freq_max_input = QLineEdit(self)
        self.freq_max_input.setPlaceholderText("Max")
        self.freq_max_input.setEnabled(False)
        freq_input_layout.addWidget(self.freq_max_input)

        control_layout.addLayout(freq_input_layout)

        self.columns_input = QLineEdit(self)
        self.columns_input.setPlaceholderText("Podaj numery kolumn dla osi Y (oddzielone spacją lub przecinkiem)")
        self.columns_input.setEnabled(False)
        control_layout.addWidget(self.columns_input)

        self.y_label_input = QLineEdit(self)
        self.y_label_input.setPlaceholderText("Podaj etykietę osi Y")
        self.y_label_input.setEnabled(False)
        control_layout.addWidget(self.y_label_input)

        self.checkbox_y = QCheckBox("Log dla osi Y", self)
        self.checkbox_y.setEnabled(False)
        control_layout.addWidget(self.checkbox_y)

        self.checkbox_x = QCheckBox("Log dla osi X", self)
        self.checkbox_x.setEnabled(False)
        control_layout.addWidget(self.checkbox_x)

        self.button2 = QPushButton("Rysuj wykres", self)
        self.button2.setEnabled(False)
        self.button2.clicked.connect(self.rysuj_wykres)
        control_layout.addWidget(self.button2)

        self.save_button = QPushButton("Zapisz wykres jako JPG", self)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.zapisz_wykres)
        control_layout.addWidget(self.save_button)

        control_layout.addStretch()

        main_layout.addLayout(control_layout, stretch=1)

        self.setLayout(main_layout)
        self.setWindowTitle('Wykres z Excela')
        self.setGeometry(100, 100, 1200, 600)  # Poszerzone okno

    def wybierz_plik(self):
        options = QFileDialog.Options()
        self.filename, _ = QFileDialog.getOpenFileName(self, "Wybierz plik Excel", "", "Excel files (*.xlsx)", options=options)
        if self.filename:
            self.df = pd.read_excel(self.filename)
            if 'omega' in self.df.columns:
                self.df = self.df.drop(columns=['omega'])
            num_columns = len(self.df.columns)
            self.label2.setText(f"Liczba kolumn w pliku: {num_columns}")

            min_freq = self.df.iloc[:, 0].min()
            max_freq = self.df.iloc[:, 0].max()
            self.freq_label.setText(f"Zakres częstotliwości: {min_freq} - {max_freq}")

            # Enable input fields and buttons
            self.freq_min_input.setEnabled(True)
            self.freq_max_input.setEnabled(True)
            self.columns_input.setEnabled(True)
            self.y_label_input.setEnabled(True)
            self.checkbox_y.setEnabled(True)
            self.checkbox_x.setEnabled(True)
            self.button2.setEnabled(True)
            self.save_button.setEnabled(True)
        else:
            self.label2.setText("Nie wybrano pliku")
            self.freq_label.setText("")

    def rysuj_wykres(self):
        if self.df is not None:
            freq_min_str = self.freq_min_input.text()
            freq_max_str = self.freq_max_input.text()
            columns_str = self.columns_input.text()
            y_label = self.y_label_input.text() or 'Value'
            
            try:
                if freq_min_str.strip() and freq_max_str.strip():
                    freq_min, freq_max = float(freq_min_str), float(freq_max_str)
                elif freq_min_str.strip():
                    freq_min = float(freq_min_str)
                    freq_max = self.df.iloc[:, 0].max()
                elif freq_max_str.strip():
                    freq_min = self.df.iloc[:, 0].min()
                    freq_max = float(freq_max_str)
                else:
                    freq_min, freq_max = self.df.iloc[:, 0].min(), self.df.iloc[:, 0].max()

                columns = [int(col) for col in columns_str.replace(",", " ").split()] if columns_str.strip() else range(1, len(self.df.columns))

                if freq_min >= freq_max:
                    QMessageBox.critical(self, "Błąd", "Minimalna wartość częstotliwości musi być mniejsza niż maksymalna.")
                    return

                if any(col < 1 or col >= len(self.df.columns) for col in columns):
                    QMessageBox.critical(self, "Błąd", "Podano nieprawidłowe numery kolumn.")
                    return

                self.ax.clear()
                freq_data = self.df.iloc[:, 0]
                mask = (freq_data >= freq_min) & (freq_data <= freq_max)
                x_data = freq_data[mask]

                for col in columns:
                    self.ax.plot(x_data, self.df.iloc[:, col][mask], marker='o', linestyle='-', label=f"Tp {self.df.columns[col]}")
                
                if self.checkbox_y.isChecked():
                    self.ax.set_yscale('log')
                else:
                    self.ax.set_yscale('linear')
                
                if self.checkbox_x.isChecked():
                    self.ax.set_xscale('log')
                else:
                    self.ax.set_xscale('linear')

                self.ax.set_xlabel('Frequency', fontsize=14)
                self.ax.set_ylabel(y_label, fontsize=14)
                self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)
                self.ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                self.figure.tight_layout()
                self.canvas.draw()
            except ValueError:
                QMessageBox.critical(self, "Błąd", "Wprowadzono nieprawidłowe wartości.")
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
