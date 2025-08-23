# obliczenia.py
# -*- coding: utf-8 -*-
import os
import glob
from pathlib import Path

import natsort
import pandas as pd
from numpy import nan

import wzory


def _read_measurement_file(path: str) -> pd.DataFrame:       # NEW
    
    df = pd.read_csv(path, sep=";", decimal=",", encoding="utf-8")

    if df.shape[1] == 1:
        df = pd.read_csv(path, sep=",", decimal=".", encoding="utf-8")

    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]
    df.dropna(axis=1, how="all", inplace=True)

    df.columns = df.columns.str.strip()

    return df

def folderObliczone(sciezka: str) -> None:
    try:
        os.mkdir(os.path.join(sciezka, "obliczone"))
    except FileExistsError:
        pass


def petlaObliczen(sciezka: str, opcja: int, dl: float, sz: float, gr: float,
                  ppk: float, progres, msgBox) -> None:
    folderObliczone(sciezka)
    csv_files = glob.glob(os.path.join(sciezka, "*.csv"))
    total_files = len(csv_files)

    msgBox.setWindowTitle("Błąd")
    for i, plik in enumerate(csv_files):
        obliczenia(sciezka, plik, opcja, dl, sz, gr, ppk, msgBox)
        progres.setValue(int((i + 1) / total_files * 100))

    do_wykresow(sciezka, progres)


def obliczenia(sciezka: str, plik: str, opcja: int,
               dl: float, sz: float, gr: float, ppk: float, msgBox):
    nazwaPliku = Path(plik).stem

    try:
        df = _read_measurement_file(plik)                         
    except Exception as e:
        msgBox.setText(f"Błąd w czytaniu danych: {e}")
        msgBox.exec()
        return

    if df.shape[1] == 8:                                          
        if df.iloc[:, 7].notna().any():                           
            df.iloc[:, 2:7] = df.iloc[:, 3:8]                     
        df = df.iloc[:, :7]                                       
    elif df.shape[1] != 7:
        msgBox.setText(f"Nieoczekiwana liczba kolumn ({df.shape[1]}) w {plik}")
        msgBox.exec()
        return

    df.columns = ['Lp.', 'Freq', 'Temp', 'PHASe', 'Cp', 'D', 'Rp']

    try:
        df['Temp'] = int(nazwaPliku) if nazwaPliku.isdigit() else 0

        for col in ['PHASe', 'Cp', 'D', 'Rp']:
            df[col] = (df[col].astype(str)
                               .str.replace(',', '.', regex=False)
                               .astype(float))

    except Exception as e:
        msgBox.setText(f"Błąd w czyszczeniu danych: {e}")
        msgBox.exec()
        return

    try:
        if opcja == 1:  # CIP
            df['Konduktywnosc sigma'] = wzory.cip(df['Rp'], gr * sz, dl)
        else:           # CPP
            df['Konduktywnosc sigma'] = wzory.cpp(df['Rp'], gr, ppk)

        df['rho'] = wzory.Rho(df['Rp'])
        df['Tp w K'] = df['Temp'] + 273
        df['1000/Tp w K'] = 1000 / df['Tp w K']
        df['wspl. kond. alfa'] = wzory.wsplKonduktywnosci(df['Konduktywnosc sigma'],
                                                          df['Freq'])

        if opcja == 1:
            df['Re dielekt.'] = wzory.rSkladowaPrzenikalnosci(
                df['Cp'],
                wzory.C0(dl * sz, gr)
            )
        else:
            df['Re dielekt.'] = wzory.rSkladowaPrzenikalnosci(
                df['Cp'],
                wzory.C0(ppk, gr)
            )

        df['Im dielekt.'] = wzory.iSkladowaPrzenikalnosci(
            df['Konduktywnosc sigma'],
            wzory.omega(df['Freq'])
        )

    except Exception as e:
        msgBox.setText(f"Błąd w obliczeniach: {e}")
        msgBox.exec()
        return

    try:
        df.to_excel(os.path.join(sciezka, "obliczone", f"{nazwaPliku}.xlsx"),
                    index=False)
    except Exception as e:
        msgBox.setText(f"Błąd podczas zapisywania: {e}")
        msgBox.exec()
        return

    global f
    f = df['Freq']


def do_wykresow(sciezka: str, progres):
    """
    Zbierz kolumny z plików *.xlsx* w `ścieżka/obliczone/` i wygeneruj
    duże arkusze do dalszego rysowania w module `wykresy.py`.
    """
    wspAlfa, wspCp, wspEps, wspR, wspRo, wspSigma, wspTeta, wspTgDelta, imskld = (
        pd.DataFrame() for _ in range(9)
    )
    dfLista = [wspAlfa, wspCp, wspEps, wspR, wspRo,
               wspSigma, wspTeta, wspTgDelta, imskld]

    pathWykresy = os.path.join(sciezka, "wykresy")
    pathObliczone = os.path.join(sciezka, "obliczone")

    try:
        os.mkdir(pathWykresy)
    except FileExistsError:
        pass

    xlxsPliki = natsort.natsorted(
        glob.glob(os.path.join(pathObliczone, "*.xlsx")), reverse=False
    )

    global f
    # kolumna z częstotliwością + rezerwacja miejsca na temperatury (10-19)
    for df in dfLista:
        df['Freq'] = f
        for j in range(10, 20):
            df[j] = nan

    # odczyt kolejnych plików
    for i, plik in enumerate(xlxsPliki):
        nazwaPliku = Path(plik).stem
        df = pd.read_excel(plik)

        wspAlfa[nazwaPliku]   = df['wspl. kond. alfa']
        wspCp[nazwaPliku]     = df['Cp']
        wspEps[nazwaPliku]    = df['Re dielekt.']
        wspR[nazwaPliku]      = df['Rp']
        wspRo[nazwaPliku]     = df['rho']
        wspSigma[nazwaPliku]  = df['Konduktywnosc sigma']
        wspTeta[nazwaPliku]   = df['PHASe']
        wspTgDelta[nazwaPliku]= df['D']
        imskld[nazwaPliku]    = df['Im dielekt.']

        progres.setValue(int((i + 1) / len(xlxsPliki) * 80))

    # drobne porządki
    wspEps.insert(1, "omega", wzory.omega(wspEps['Freq']))
    progres.setValue(90)

    # zapis końcowy
    wspAlfa.to_excel(os.path.join(pathWykresy, 'wsp alfa.xlsx'),     index=False)
    wspCp.to_excel(os.path.join(pathWykresy, 'wsp Cp.xlsx'),         index=False)
    wspEps.to_excel(os.path.join(pathWykresy, 'wsp Epsilon.xlsx'),   index=False)
    wspR.to_excel(os.path.join(pathWykresy, 'wsp R.xlsx'),           index=False)
    wspRo.to_excel(os.path.join(pathWykresy, 'wsp Ro.xlsx'),         index=False)
    wspSigma.to_excel(os.path.join(pathWykresy, 'wsp sigma.xlsx'),   index=False)
    wspTeta.to_excel(os.path.join(pathWykresy, 'wsp teta.xlsx'),     index=False)
    wspTgDelta.to_excel(os.path.join(pathWykresy, 'wsp tg delta.xlsx'), index=False)
    imskld.to_excel(os.path.join(pathWykresy, 'Im skladowa.xlsx'),   index=False)

    progres.setValue(100)
