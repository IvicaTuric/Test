#!/usr/bin/env python
# coding: utf-8

# In[60]:


import pandas as pd 
import pyodbc
import numpy as np
import matplotlib as plt
from pandas import DataFrame



# 
# <h3>1. Indeksi i ogranicenja</h3><br>
#     Baza sadrzi indeks za pretragu restorana u Splitu (filtrirajuci), i UNIQUE indeks na MjestoAktivnost (ista aktivnost moze samo jednom biti u istom mjestu). Dodano je i ogranicenje na Gost i Vlasnik da nemogu biti uneseni ako je Ime i Prezime isto

# In[91]:


# Spoji se na bazu
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-JBH3HM3\APARTMANI;'
                      'Database=Apartmani;'
                      'Trusted_Connection=yes;'
                      'UID=App_Uloga;'
                      'PWD=Apartman123')
cursor = conn.cursor()

# Prvi indeks
sql = "SELECT * FROM Destinacija.Restoran WHERE IDMjesto=1"
data = pd.read_sql(sql,conn)
print("--> Dohvati sve restorane u Splitu")
display(data)


# Drugi indeks
print("--> Pokusaj dodati istu aktivnost u isti grad (Split->Windsurf)\n")
try:
    cursor.execute("INSERT INTO Destinacija.MjestoAktivnost (IDMjesto, IDAktivnost) VALUES ('1', '2')")
    conn.commit()
except pyodbc.Error as err:
    print(err)
    print("\n")
    
print("--> Dohvati sve Aktivnosti")
sql = ("SELECT * FROM Destinacija.MjestoAktivnost"
       " INNER JOIN Destinacija.Mjesto ON MjestoAktivnost.IDMjesto=Mjesto.ID"
       " INNER JOIN Destinacija.Aktivnost ON MjestoAktivnost.IDAktivnost=Aktivnost.ID")
data = pd.read_sql(sql,conn)
display(data)


# Ogranicenje na Gost
print("--> Pokusaj dodati gosta s istim imenom i prezimenom (OIB drugaciji)\n")
try:
    cursor.execute("INSERT INTO Osoba.Gost (Ime, Prezime, OIB) VALUES ('Matko','Matic','44442444444')")
    conn.commit()
except pyodbc.Error as err:
    print(err)
    print("\n")

cursor.close()
conn.close()

# <h3>2. Uskladištene procedure i funkcije </h3><br>
#     

# In[107]:


# Spoji se na bazu
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-JBH3HM3\APARTMANI;'
                      'Database=Apartmani;'
                      'Trusted_Connection=yes;'
                      'UID=App_Uloga;'
                      'PWD=Apartman123')
cursor = conn.cursor()

# Prva procedura
print("--> Dohvati samo dobro ocijenje apartmane")
sql = "EXEC usp_DobroOcjeneniApartmani"
data = pd.read_sql(sql,conn)
display(data)


# Druga procedura - 
print("\n--> Dohvati apartmane koji su blizu neke aktivnosti")
sql = "EXEC usp_ApartmaniBlizuAktivnosti 'Jet Ski'"
data = pd.read_sql(sql,conn)
display(data)


# Treca procedura
print("\n--> Unosimo rezervaciju u apartman koji je slobodan u tom periodu")
cursor.execute("EXEC usp_UnosRezervacije 1, 4, 3, '2020-11-02'")
conn.commit()   
               
sql = "SELECT * FROM Smjestaj.Rezervacija"     
data = pd.read_sql(sql,conn)
display(data)

print("\n--> Unosimo rezervaciju u apartman koji nije slobodan u tom periodu")
try:
    cursor.execute("EXEC usp_UnosRezervacije 1, 4, 3, '2020-11-02'")
    conn.commit()
except pyodbc.Error as err:
    print(err)
    print("\n")


# Cetvrta procedura - 
print("\n--> Dohvati koliko je dana zauzet apartman (od danas na dalje)")
cursor.execute("EXEC usp_ZauzetostApartmana 2")
for row in cursor:
    print("Apartman je zauzet " + str(row[0]) + " dan")



cursor.close()
conn.close()

# <h3>3. Okidaci </h3><br>
# Prvi provjerava dali je korisnik koristio apartman prije nego sto ostavi ocjenu. Drugi i treci provjeravaju ispravnost OIBa
#     

# In[115]:


# Spoji se na bazu
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-JBH3HM3\APARTMANI;'
                      'Database=Apartmani;'
                      'Trusted_Connection=yes;'
                      'UID=App_Uloga;'
                      'PWD=Apartman123')
cursor = conn.cursor()

# Prvi okidac
print("--> Pokusaj ostaviti recenziju od gost koji nije koristio apartman\n")
try:
    cursor.execute("INSERT INTO Smjestaj.Ocjena (Ocjena, IDApartman, IDGost, Komentar) VALUES ('1', '4', '2','Pre lose')")
    conn.commit()
except pyodbc.Error as err:
    print(err)
    print("\n")

# Drugi okidac
print("--> Pokusaj dodati gosta sa neispravnim OIBom\n")
try:
    cursor.execute("INSERT INTO Osoba.Gost (Ime, Prezime, OIB) VALUES ('Testko','Tests','1122112')")
    conn.commit()
except pyodbc.Error as err:
    print(err)
    print("\n")


    
cursor.close()
conn.close()

# <h3>4. Sheme </h3><br>
# Tablice su rasporedjene po sljedecim shemama:
# 
# Smjestaj
# - apartman
# - ocjena
# - rezervacija
# 
# Destinacija
# - mjesto
# - aktivnost
# - mjestoAktivnost
# - restoran
# 
# Osobe
# - gost
# - vlasnik

# <h1> PRESKOCIO SAM 5 6 7</h1>

#   <h3>8. Kriptografija </h3><br>
#   Broj kartice je dodan na gosta i vlasnika. Uz procedure za sifrirnje i desifriranje imamo i procedure za svaki unos koji poziva te procedure

# In[165]:


# Spoji se na bazu
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-JBH3HM3\APARTMANI;'
                      'Database=Apartmani;'
                      'Trusted_Connection=yes;'
                      'UID=App_Uloga;'
                      'PWD=Apartman123')
cursor = conn.cursor()

# Prvi okidac
print("--> Pokusaj dodati karticu za gosta 1\n")
try:
    cursor.execute("EXEC usp_UnosKarticeGost 1, '2222-1111-4444-2222'")
    conn.commit()
except pyodbc.Error as err:
    print(err)
    print("\n")

print("--> Dohvati podatke gosta 1")
sql = "SELECT * FROM Osoba.Gost WHERE ID=1"
data = pd.read_sql(sql,conn)
display(data)


# Sto god probam nemogu dohvatiti nazada broj kartice
# U SSMS normalno vrati tablicu tu ne radi
#print("--> Dohvati desifrirani broj kartice od gost 1")
#sql = "EXEC usp_BrojKarticeGost 1"
#data = pd.read_sql(sql,conn)
#display(data)


cursor.close()
conn.close()

# In[164]:


# Spoji se na bazu
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-JBH3HM3\APARTMANI;'
                      'Database=Apartmani;'
                      'Trusted_Connection=yes;'
                      'UID=App_Uloga;'
                      'PWD=Apartman123')
cursor = conn.cursor()
print("--> Dohvati podatke gostiju koristeci korisnika koji vidi maskirane podatke")
sql = "EXEC usp_DohvatiMaskiranePodatke"
data = pd.read_sql(sql,conn)
display(data)

cursor.close()
conn.close()
