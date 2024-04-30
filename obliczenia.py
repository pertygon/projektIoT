import os
import pandas as pd
from pathlib import Path
import wzory
import glob 
#Sprawdzic czy wszystkie biblioteki sa potrzebne
#Zrobic mozliwosc zapisywania do excela
#Zrobic mozliwosc czytania z excela
def folderObliczone(sciezka):
    try:
        path = os.path.join(sciezka, "obliczone") 
        os.mkdir(path)
    except:
        pass
def petlaObliczen(sciezka):
    folderObliczone(sciezka)
    csv_files = glob.glob(os.path.join(sciezka, "*.csv"))
    for plik in csv_files:
        print(plik)
        obliczenia(sciezka,plik)
def obliczenia(sciezka,plik):
#pododawac bloki try except do wykrycia bledow
#czytanie danych
    nazwaPliku = Path(plik).stem
    df = pd.read_csv(plik,sep=';',encoding="utf-8")
    #czyszczenie danych
    df.columns = df.columns.str.strip()
    df['Temp']=int(nazwaPliku)
    df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
    df.replace(',','.',inplace = True)
    df['PHASe'] = df['PHASe'].str.replace(',','.').astype(float)
    df['Cp'] = df['Cp'].str.replace(',','.').astype(float)
    df['D'] = df['D'].str.replace(',','.').astype(float)
    df['Rp'] = df['Rp'].str.replace(',','.').astype(float)
    #Tworzenie nowych kolumn i tworzenie obliczen
    # DODAC TUTAJ PARAMETRY ZAMIAST LICZB I SPRAWDZIC WARUNEK
    #if CIP.isChecked():
    df['Konduktywnosc sigma'] = wzory.cip(wzory.Rho(df['Rp']),1,1)
    #else"
    #df['Konduktywnosc sigma'] = wzory.cpp(wzory.Rho(df['Rp']),1,1)
    df['rho'] = wzory.Rho(df['Rp'])
    df['Tp w K'] = df['Temp'] + 273
    df['1000/Tp w K'] = 1000/df['Tp w K']
    df['wspl. kond. alfa'] = wzory.wsplKonduktywnosci(10,12)
    df['Re skladowa przenikalonsci dielekt.'] = wzory.rSkladowaPrzenikalnosci(df['Cp'],wzory.C0(1,1))
    df['Im skladowa przenikalonsci dielekt.'] = wzory.iSkladowaPrzenikalnosci(df['Konduktywnosc sigma'],wzory.omega(df['Freq']))
    doZapisania = os.path.join(sciezka,'obliczone\\')
    df.to_excel(doZapisania+nazwaPliku+'.xlsx',index = False)
