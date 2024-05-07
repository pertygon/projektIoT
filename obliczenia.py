import os
import pandas as pd
from pathlib import Path
import wzory
import glob
import natsort
from numpy import nan 
#Zrobic mozliwosc czytania z excela
#nazwy plikow musza byc liczbami
#dodac odpowiednie reagowanie na zla nazwe pliku
f = None # czestotliwosc9i
def folderObliczone(sciezka):
    try:
        path = os.path.join(sciezka, "obliczone") 
        os.mkdir(path)
    except:
        pass
def petlaObliczen(sciezka,opcja,dl,sz,gr,ppk):
    folderObliczone(sciezka)
    csv_files = glob.glob(os.path.join(sciezka, "*.csv"))
    for plik in csv_files:
        obliczenia(sciezka,plik,opcja,dl,sz,gr,ppk)
    do_wykresow(sciezka)
def obliczenia(sciezka,plik,opcja,dl,sz,gr,ppk):
#pododawac bloki try except do wykrycia bledow
#czytanie danych
    nazwaPliku = Path(plik).stem
    df = pd.read_csv(plik,sep=';',encoding="utf-8")
    #czyszczenie danych
    df.columns = df.columns.str.strip()
    try:
        df['Temp'] = int(nazwaPliku)
    except:
        df['Temp'] = 0
    df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
    df.replace(',','.',inplace = True)
    df['PHASe'] = df['PHASe'].str.replace(',','.').astype(float)
    df['Cp'] = df['Cp'].str.replace(',','.').astype(float)
    df['D'] = df['D'].str.replace(',','.').astype(float)
    df['Rp'] = df['Rp'].str.replace(',','.').astype(float)
    global f
    f = df['Freq']
    #Tworzenie nowych kolumn i tworzenie obliczen
    if opcja == 1:
        df['Konduktywnosc sigma'] = wzory.cip(wzory.Rho(df['Rp']),gr*sz,dl)
    else:
        df['Konduktywnosc sigma'] = wzory.cpp(wzory.Rho(df['Rp']),gr,ppk)
    df['rho'] = wzory.Rho(df['Rp'])
    df['Tp w K'] = df['Temp'] + 273
    df['1000/Tp w K'] = 1000/df['Tp w K']
    df['wspl. kond. alfa'] = wzory.wsplKonduktywnosci(df['Konduktywnosc sigma'],df['Freq'])
    df['Re skladowa przenikalonsci dielekt.'] = wzory.rSkladowaPrzenikalnosci(df['Cp'],wzory.C0(ppk,gr))
    df['Im skladowa przenikalonsci dielekt.'] = wzory.iSkladowaPrzenikalnosci(df['Konduktywnosc sigma'],wzory.omega(df['Freq']))
    doZapisania = os.path.join(sciezka,'obliczone\\')
    df.to_excel(doZapisania+nazwaPliku+'.xlsx',index = False)
def do_wykresow(sciezka):
    """
    stworz dataframe - my dla potrzebnych parametrow
    otworz folder
    czytaj plik po pliku 
    zapisuj wartosci do plikow

    """
    wspAlfa,wspCp,wspEps,wspR,wspRo,wspSigma,wspTeta,wspTgDelta = (pd.DataFrame() for i in range(8))
    dfLista = [wspAlfa,wspCp,wspEps,wspR,wspRo,wspSigma,wspTeta,wspTgDelta]
    pathWykresy = os.path.join(sciezka, "wykresy") 
    pathObliczone = os.path.join(sciezka, "obliczone")
    os.mkdir(pathWykresy)
    xlxsPliki = glob.glob(os.path.join(pathObliczone, "*.xlsx"))
    xlxsPliki = natsort.natsorted(xlxsPliki,reverse=False)
    global f
    #dodawanie kolumn f, temp
    for i in dfLista:
        i['Freq'] = f
        for j in range(10,20):
            i[j] = nan
    #reszta
    for plik in xlxsPliki:
        nazwaPliku = Path(plik).stem
        df = pd.read_excel(plik)
        wspAlfa[nazwaPliku] = df['wspl. kond. alfa']
        wspCp[nazwaPliku] = df['Cp']
        #?????
        wspEps[nazwaPliku] = 0
        wspR[nazwaPliku] = df['Rp']
        wspRo[nazwaPliku] = df['rho']
        wspSigma[nazwaPliku] = df['Konduktywnosc sigma']
        wspTeta[nazwaPliku] = df['PHASe']
        wspTgDelta[nazwaPliku] = df['D']
    wspAlfa.to_excel(pathWykresy+'\\'+'wsp alfa'+'.xlsx',index = False)
    wspCp.to_excel(pathWykresy+'\\'+'wsp Cp'+'.xlsx',index = False)
    wspEps.to_excel(pathWykresy+'\\'+'wsp Epsilon'+'.xlsx',index = False)
    wspR.to_excel(pathWykresy+'\\'+'wsp R'+'.xlsx',index = False)
    wspRo.to_excel(pathWykresy+'\\'+'wsp Ro'+'.xlsx',index = False)
    wspSigma.to_excel(pathWykresy+'\\'+'wsp sigma'+'.xlsx',index = False)
    wspTeta.to_excel(pathWykresy+'\\'+'wsp teta'+'.xlsx',index = False)
    wspTgDelta.to_excel(pathWykresy+'\\'+'wsp tg delta'+'.xlsx',index = False)
#do_wykresow(r"D:\STUDIA\Projekt_IoT\projekt_IoT_MELJON")