import os
import pandas as pd
from pathlib import Path
import wzory
import glob
import natsort
from numpy import nan, concatenate
#Zrobic mozliwosc czytania z excela
#nazwy plikow musza byc liczbami
#dodac odpowiednie reagowanie na zla nazwe pliku
f = None # czestotliwosci

def folderObliczone(sciezka):
    try:
        path = os.path.join(sciezka, "obliczone") 
        os.mkdir(path)
    except:
        pass

def petlaObliczen(sciezka,opcja,dl,sz,gr,ppk,progres):
    folderObliczone(sciezka)
    csv_files = glob.glob(os.path.join(sciezka, "*.csv"))
    total_files = len(csv_files)
    for i,plik in enumerate(csv_files):
        obliczenia(sciezka,plik,opcja,dl,sz,gr,ppk)
        progres.setValue(int((i+1)/total_files*50))
        print(progres.value())
    do_wykresow(sciezka)

def obliczenia(sciezka,plik,opcja,dl,sz,gr,ppk):
#pododawac bloki try except do wykrycia bledow
#czytanie danych
    try:
        nazwaPliku = Path(plik).stem
        df = pd.read_csv(plik,sep=';',encoding="utf-8")
    except:
        print("blad w czytaniu")
    #czyszczenie danych
    try:
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
    except:
        print("blad podczas czyszczenia")
    global f
    f = df['Freq']
    #Tworzenie nowych kolumn i tworzenie obliczen
    try:
        if opcja == 1:
            df['Konduktywnosc sigma'] = wzory.cip(wzory.Rho(df['Rp']),gr*sz,dl)
        else:
            df['Konduktywnosc sigma'] = wzory.cpp(wzory.Rho(df['Rp']),gr,ppk)
    except:
        print("blad w obliczaniu konduktacji")
    try:
        df['rho'] = wzory.Rho(df['Rp'])
    except:
        print("blad w obliczaniu rho")

    df['Tp w K'] = df['Temp'] + 273
    df['1000/Tp w K'] = 1000/df['Tp w K']

    df['wspl. kond. alfa'] = wzory.wsplKonduktywnosci(df['Konduktywnosc sigma'],df['Freq'])
    try:
        if opcja == 1:
            df['Re dielekt.'] = wzory.rSkladowaPrzenikalnosci(df['Cp'],wzory.C0(dl*sz,gr))
        else:
            df['Re dielekt.'] = wzory.rSkladowaPrzenikalnosci(df['Cp'],wzory.C0(ppk,gr))
    except:
        print("blad w obliczaniu re skladowej")
    
    df['Im dielekt.'] = wzory.iSkladowaPrzenikalnosci(df['Konduktywnosc sigma'],wzory.omega(df['Freq']))
    try:
        doZapisania = os.path.join(sciezka,'obliczone\\')
        df.to_excel(doZapisania+nazwaPliku+'.xlsx',index = False)
    except:
        print("blad podczas zapisywania")
def do_wykresow(sciezka):
    """
    stworz dataframe - my dla potrzebnych parametrow
    otworz folder
    czytaj plik po pliku 
    zapisuj wartosci do plikow

    """
    wspAlfa,wspCp,wspEps,wspR,wspRo,wspSigma,wspTeta,wspTgDelta,imskld = (pd.DataFrame() for i in range(9))
    dfLista = [wspAlfa,wspCp,wspEps,wspR,wspRo,wspSigma,wspTeta,wspTgDelta,imskld]
    pathWykresy = os.path.join(sciezka, "wykresy") 
    pathObliczone = os.path.join(sciezka, "obliczone")
    try:
        os.mkdir(pathWykresy)
    except:
        pass
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
        wspEps[nazwaPliku] = df['Re dielekt.']
        wspR[nazwaPliku] = df['Rp']
        wspRo[nazwaPliku] = df['rho']
        wspSigma[nazwaPliku] = df['Konduktywnosc sigma']
        wspTeta[nazwaPliku] = df['PHASe']
        wspTgDelta[nazwaPliku] = df['D']
        imskld[nazwaPliku] = df['Im dielekt.']
    for i in dfLista:
        if i.keys()[-1] == "pok":
            to_move = i.pop(i.keys()[-1])
            i.insert(1,"pok",to_move)

    del dfLista[-1]

    wspEps.insert(1,"omega",wzory.omega(wspEps['Freq']))

    #Zapis do pliku
    wspAlfa.to_excel(pathWykresy+'\\'+'wsp alfa'+'.xlsx',index = False)
    wspCp.to_excel(pathWykresy+'\\'+'wsp Cp'+'.xlsx',index = False)
    wspEps.to_excel(pathWykresy+'\\'+'wsp Epsilon'+'.xlsx',index = False)
    wspR.to_excel(pathWykresy+'\\'+'wsp R'+'.xlsx',index = False)
    wspRo.to_excel(pathWykresy+'\\'+'wsp Ro'+'.xlsx',index = False)
    wspSigma.to_excel(pathWykresy+'\\'+'wsp sigma'+'.xlsx',index = False)
    wspTeta.to_excel(pathWykresy+'\\'+'wsp teta'+'.xlsx',index = False)
    wspTgDelta.to_excel(pathWykresy+'\\'+'wsp tg delta'+'.xlsx',index = False)
    imskld.to_excel(pathWykresy+'\\'+'Im skladowa'+'.xlsx',index = False)