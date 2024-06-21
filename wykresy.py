import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
                             QLineEdit, QLabel, QMessageBox, QCheckBox, QSlider)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ultralytics import YOLO
import json
import os

class WykresApp(QWidget):
    def __init__(self):
        super().__init__()

        
        self.df = None
        self.filename = None
        self.model = None
        self.model_path = None
        self.conf_threshold = 0.5
        self.initUI()
        # Załaduj na starcie sciezke do modelu
        self.load_model()
    #wybierz model ktory ma sie wczytywac na starcie
    def select_model_stup(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Wybierz model YOLO", "", "PyTorch files (*.pt)", options=options)
        if filename:
            with open('model.json', 'w') as model_file:
                json.dump({"path": filename}, model_file)
            self.model_path = filename
            self.model_label.setText(f"Aktualny model: {filename}")
        else:
            QMessageBox.critical(self, "Błąd", "Nie wybrano modelu.")
    #zaladuj model
    def load_model(self):
        try:
            with open('model.json', 'r') as model_file:
                data = json.load(model_file)
                self.model = YOLO(data['path'])
                self.model_path = data['path']
                self.model_label.setText(f"Aktualny model: {data['path']}")
        except Exception as e:
            self.model_label.setText("Brak załadowanego modelu")
            QMessageBox.critical(self, "Błąd", f"Nie znaleziono modelu. {str(e)}")
    #wybierz model jednorazowo
    def select_model(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Wybierz model YOLO", "", "PyTorch files (*.pt)", options=options)
        if filename:
            self.model = YOLO(filename)
            self.model_path = filename
            self.model_label.setText(f"Aktualny model: {filename}")
        else:
            QMessageBox.critical(self, "Błąd", "Nie wybrano modelu.")
        
    def initUI(self):
        main_layout = QHBoxLayout()

        # Lewy layout
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas, stretch=3)

        # Prawy layout
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

        self.pred_button = QPushButton("Wykryj zjawisko", self)
        self.pred_button.setEnabled(False)
        self.pred_button.clicked.connect(self.predict_yolo)
        control_layout.addWidget(self.pred_button)

        self.conf_slider = QSlider(Qt.Horizontal)  # Ustawienie orientacji suwaka
        self.conf_slider.setMinimum(0)
        self.conf_slider.setMaximum(100)
        self.conf_slider.setValue(int(self.conf_threshold * 100))
        self.conf_slider.setEnabled(False)
        self.conf_slider.valueChanged.connect(self.update_conf_threshold)
        control_layout.addWidget(self.conf_slider)


        self.conf_label = QLabel(f"Próg pewności: {self.conf_threshold:.2f}", self)
        control_layout.addWidget(self.conf_label)

        self.sel_model = QPushButton("Wybierz domyślny model", self)
        self.sel_model.clicked.connect(self.select_model_stup)
        control_layout.addWidget(self.sel_model)

        self.ld_model = QPushButton("Załaduj inny model", self)
        self.ld_model.clicked.connect(self.select_model)
        control_layout.addWidget(self.ld_model)

        self.model_label = QLabel("Brak załadowanego modelu", self)
        control_layout.addWidget(self.model_label)

        self.pred_label = QLabel("", self)
        control_layout.addWidget(self.pred_label)

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

            # Wlacz przyciski
            self.freq_min_input.setEnabled(True)
            self.freq_max_input.setEnabled(True)
            self.columns_input.setEnabled(True)
            self.y_label_input.setEnabled(True)
            self.checkbox_y.setEnabled(True)
            self.checkbox_x.setEnabled(True)
            self.button2.setEnabled(True)
            self.save_button.setEnabled(True)
            self.pred_button.setEnabled(True)
            self.conf_slider.setEnabled(True)
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

    def predict_yolo(self):
        if self.model and self.df is not None:
            # Zapisz wykres jako jpg
            temp_image_path = "temp_plot.jpg"
            self.figure.savefig(temp_image_path)

            # Wykryj zjawisko
            results = self.model.predict(source=temp_image_path, conf=self.conf_threshold)

            # Wyswietl klasy jakie zostaly wykryte
            if results:
                predicted_labels = set()
                for result in results:
                    for box in result.boxes:
                        if box.conf >= self.conf_threshold:
                            predicted_labels.add(self.model.names[int(box.cls)])

                prediction_text = f"Predykcje: {', '.join(predicted_labels)}" if predicted_labels else "Brak predykcji"
                self.pred_label.setText(prediction_text)
            else:
                self.pred_label.setText("Brak predykcji")

            # usun zjdecie
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
        else:
            QMessageBox.critical(self, "Błąd", "Model nie jest załadowany lub brak danych do predykcji.")

    def update_conf_threshold(self):
        self.conf_threshold = self.conf_slider.value() / 100.0
        self.conf_label.setText(f"Próg pewności: {self.conf_threshold:.2f}")
