import pyodbc
import requests
from bs4 import BeautifulSoup
import os
import datetime

path = os.path.dirname(__file__)

print(path)

#Funkcija za dohvaćanje dana u tjednu
def dan_u_tjednu(plus):
    datum = datetime.datetime.today().weekday()
    datum = datum + plus

    if datum == 7:
        datum = 0
    elif datum == 8:
        datum = 1
    elif datum == 9:
        datum = 2
        
    dani = {0:"Ponedjeljak",
            1:"Utorak",
            2:"Srijeda",
            3:"Četvrtak",
            4:"Petak",
            5:"Subota",
            6:"Nedjelja"}

    dan = dani[datum]
    return dan


#spajanje na Access bazu
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' + "DBQ={}\projekt.accdb;".format(path)
    )
connection = pyodbc.connect(conn_str)
cursor = connection.cursor()
cursor.execute("select naziv from vrijeme_sada")


gradovi = cursor.fetchall()
gradovi_list = []

#Update dan u tjednu u tablicama vrijeme_dan1, vrijeme_dan2 i vrijeme_dan3
cursor.execute("UPDATE vrijeme_dan1 SET dan = '{}'".format(dan_u_tjednu(1)))
cursor.execute("UPDATE vrijeme_dan2 SET dan = '{}'".format(dan_u_tjednu(2)))
cursor.execute("UPDATE vrijeme_dan3 SET dan = '{}'".format(dan_u_tjednu(3)))


#Prebacivanje popisa gradova u memoriju programa
for x in gradovi:
    gradovi_list.append(x[0])

#Mijenjanje hrvatskih znakova zbog pretrage na webu
gradovi_web = [x.lower().replace("č","c").replace("ć","c").replace("š","s").replace("ž","z").replace(" ","-").replace("đ","d") for x in gradovi_list ]

brojac = -1

#funkcija za dohvaćanje podataka o vremenu za sljedeća tri dana
def vrijeme_tri_dana(response):
    soup = BeautifulSoup(response.content,"html5lib")

    tablica = soup.find("div",{"id":"next-3-days"})
    tablica = tablica.find("tbody")

    #Prvi dan - jutro
    dan1_jutro = tablica.find_all("tr")[0]
    dan1_jutro = dan1_jutro.find_all("td")[0]
    dan1_jutro = dan1_jutro.find("ul",{"class":"forecast"})
    dan1_jutro = dan1_jutro.find("li",{"class":"temp"})
    dan1_jutro = dan1_jutro.find("span",{"class":"val"}).text.replace("°","")
    dan1_jutro = int(dan1_jutro)
    cursor.execute("UPDATE vrijeme_dan1 SET jutro = {} WHERE mjesto = '{}'".format(dan1_jutro,gradovi_list[brojac]))

    #Prvi dan - popodne
    dan1_popodne = tablica.find_all("tr")[1]
    dan1_popodne = dan1_popodne.find_all("td")[0]
    dan1_popodne = dan1_popodne.find("ul",{"class":"forecast"})
    dan1_popodne = dan1_popodne.find("li",{"class":"temp"})
    dan1_popodne = dan1_popodne.find("span",{"class":"val"}).text.replace("°","")
    dan1_popodne = int(dan1_popodne)
    cursor.execute("UPDATE vrijeme_dan1 SET popodne = {} WHERE mjesto = '{}'".format(dan1_popodne,gradovi_list[brojac]))

    #Prvi dan - večer
    dan1_večer = tablica.find_all("tr")[2]
    dan1_večer = dan1_večer.find_all("td")[0]
    dan1_večer = dan1_večer.find("ul",{"class":"forecast"})
    dan1_večer = dan1_večer.find("li",{"class":"temp"})
    dan1_večer = dan1_večer.find("span",{"class":"val"}).text.replace("°","")
    dan1_večer = int(dan1_večer)
    cursor.execute("UPDATE vrijeme_dan1 SET vecer = {} WHERE mjesto = '{}'".format(dan1_večer,gradovi_list[brojac]))

    #Prvi dan - noć
    dan1_noć = tablica.find_all("tr")[3]
    dan1_noć = dan1_noć.find_all("td")[0]
    dan1_noć = dan1_noć.find("ul",{"class":"forecast"})
    dan1_noć = dan1_noć.find("li",{"class":"temp"})
    dan1_noć = dan1_noć.find("span",{"class":"val"}).text.replace("°","")
    dan1_noć = int(dan1_noć)
    cursor.execute("UPDATE vrijeme_dan1 SET noc = {} WHERE mjesto = '{}'".format(dan1_noć,gradovi_list[brojac]))
    
    #####################################################################################################################################################################

    #Drugi dan - jutro
    dan2_jutro = tablica.find_all("tr")[0]
    dan2_jutro = dan2_jutro.find_all("td")[1]
    dan2_jutro = dan2_jutro.find("ul",{"class":"forecast"})
    dan2_jutro = dan2_jutro.find("li",{"class":"temp"})
    dan2_jutro = dan2_jutro.find("span",{"class":"val"}).text.replace("°","")
    dan2_jutro = int(dan2_jutro)
    cursor.execute("UPDATE vrijeme_dan2 SET jutro = {} WHERE mjesto = '{}'".format(dan2_jutro,gradovi_list[brojac]))

    #Drugi dan - popodne
    dan2_popodne = tablica.find_all("tr")[1]
    dan2_popodne = dan2_popodne.find_all("td")[1]
    dan2_popodne = dan2_popodne.find("ul",{"class":"forecast"})
    dan2_popodne = dan2_popodne.find("li",{"class":"temp"})
    dan2_popodne = dan2_popodne.find("span",{"class":"val"}).text.replace("°","")
    dan2_popodne = int(dan2_popodne)
    cursor.execute("UPDATE vrijeme_dan2 SET popodne = {} WHERE mjesto = '{}'".format(dan2_popodne,gradovi_list[brojac]))

    #Drugi dan - večer
    dan2_večer = tablica.find_all("tr")[2]
    dan2_večer = dan2_večer.find_all("td")[1]
    dan2_večer = dan2_večer.find("ul",{"class":"forecast"})
    dan2_večer = dan2_večer.find("li",{"class":"temp"})
    dan2_večer = dan2_večer.find("span",{"class":"val"}).text.replace("°","")
    dan2_večer = int(dan2_večer)
    cursor.execute("UPDATE vrijeme_dan2 SET vecer = {} WHERE mjesto = '{}'".format(dan2_večer,gradovi_list[brojac]))

    #Drugi dan - noć
    dan2_noć = tablica.find_all("tr")[3]
    dan2_noć = dan2_noć.find_all("td")[1]
    dan2_noć = dan2_noć.find("ul",{"class":"forecast"})
    dan2_noć = dan2_noć.find("li",{"class":"temp"})
    dan2_noć = dan2_noć.find("span",{"class":"val"}).text.replace("°","")
    dan2_noć = int(dan2_noć)
    cursor.execute("UPDATE vrijeme_dan2 SET noc = {} WHERE mjesto = '{}'".format(dan2_noć,gradovi_list[brojac]))
    #####################################################################################################################################################################

    #Treći dan - jutro
    dan3_jutro = tablica.find_all("tr")[0]
    dan3_jutro = dan3_jutro.find_all("td")[2]
    dan3_jutro = dan3_jutro.find("ul",{"class":"forecast"})
    dan3_jutro = dan3_jutro.find("li",{"class":"temp"})
    dan3_jutro = dan3_jutro.find("span",{"class":"val"}).text.replace("°","")
    dan3_jutro = int(dan3_jutro)
    cursor.execute("UPDATE vrijeme_dan3 SET jutro = {} WHERE mjesto = '{}'".format(dan3_jutro,gradovi_list[brojac]))

    #Treći dan - popodne
    dan3_popodne = tablica.find_all("tr")[1]
    dan3_popodne = dan3_popodne.find_all("td")[2]
    dan3_popodne = dan3_popodne.find("ul",{"class":"forecast"})
    dan3_popodne = dan3_popodne.find("li",{"class":"temp"})
    dan3_popodne = dan3_popodne.find("span",{"class":"val"}).text.replace("°","")
    dan3_popodne = int(dan3_popodne)
    cursor.execute("UPDATE vrijeme_dan3 SET popodne = {} WHERE mjesto = '{}'".format(dan3_popodne,gradovi_list[brojac]))

    #Treći dan - večer
    dan3_večer = tablica.find_all("tr")[2]
    dan3_večer = dan3_večer.find_all("td")[2]
    dan3_večer = dan3_večer.find("ul",{"class":"forecast"})
    dan3_večer = dan3_večer.find("li",{"class":"temp"})
    dan3_večer = dan3_večer.find("span",{"class":"val"}).text.replace("°","")
    dan3_večer = int(dan3_večer)
    cursor.execute("UPDATE vrijeme_dan3 SET vecer = {} WHERE mjesto = '{}'".format(dan3_večer,gradovi_list[brojac]))

    #Treći dan - noć
    dan3_noć = tablica.find_all("tr")[3]
    dan3_noć = dan3_noć.find_all("td")[2]
    dan3_noć = dan3_noć.find("ul",{"class":"forecast"})
    dan3_noć = dan3_noć.find("li",{"class":"temp"})
    dan3_noć = dan3_noć.find("span",{"class":"val"}).text.replace("°","")
    dan3_noć = int(dan3_noć)
    cursor.execute("UPDATE vrijeme_dan3 SET noc = {} WHERE mjesto = '{}'".format(dan3_noć,gradovi_list[brojac]))



#funkcija za dohvaćanje podataka o vremenu
def vrijeme_sada(grad):
    url = "http://www.vrijeme.net/hrvatska/{}".format(grad)
    respone = requests.get(url)

    vrijeme_tri_dana(respone)

    soup = BeautifulSoup(respone.content,"html5lib")

    temperatura = soup.find("li", attrs = {"class":"temp"})
    temperatura = temperatura.find("span",attrs = {"class":"val"}).text
    temperatura = temperatura.replace("°","")

    vlaznost = soup.find("li",attrs = {"class":"humidity alt-01"})
    vlaznost = vlaznost.find("span",attrs= {"class":"val"}).text
    vlaznost = vlaznost.replace("%","") 

    tlak = soup.find("li",attrs = {"class":"pressure alt-01"})
    tlak = tlak.find("span",attrs= {"class":"val"}).text
    tlak = tlak.replace("hPa","").strip()

    try:
        stanje = soup.find("p",attrs={"class":"desc alt-01"}).text
    except:
        stanje = soup.find("p",attrs={"class":"desc alt-02"}).text
    return temperatura,vlaznost,tlak,stanje




#Petlja za dohvaćanje podataka za svako mjesto i ažuriranje podataka u BP

for grad in gradovi_web:

    brojac += 1
    try:
        temperatura,vlaznost,tlak,stanje = vrijeme_sada(grad)
    except:
        print("Mjesto {} ne postoji u bazi podataka!".format(gradovi_list[brojac]))
        continue
    if temperatura == "-":
        temperatura = "NULL"

    if vlaznost == "-":
        vlaznost = "NULL"

    if tlak == "-":
        tlak = "NULL"


    print("Ažuriranje podataka za ",gradovi_list[brojac])

    cursor.execute('''
                UPDATE vrijeme_sada
                SET temperatura = {}
                WHERE naziv = '{}'

                '''.format(temperatura,gradovi_list[brojac]))
    
    cursor.execute('''
                UPDATE vrijeme_sada
                SET vlaznost = {}
                WHERE naziv = '{}'

                '''.format(vlaznost,gradovi_list[brojac]))

    cursor.execute('''
                UPDATE vrijeme_sada
                SET tlak = {}
                WHERE naziv = '{}'

                '''.format(tlak,gradovi_list[brojac]))

    cursor.execute('''
                UPDATE vrijeme_sada
                SET stanje = '{}'
                WHERE naziv = '{}'

                '''.format(stanje,gradovi_list[brojac]))

    
    cursor.commit()

def bioprognoza():
    print("Ažuriranje bioprognoze...")
    url = "http://www.vrijeme.net/bioprognoza"
    respone = requests.get(url)
    soup = BeautifulSoup(respone.content,"html5lib")   

    uvjeti = soup.find("ul",{"class":"bio-regions"})
    uvjeti = uvjeti.find_all("li")

    #Regija - "Središnja Hrvatska"
    sredisnja_hrvatska = uvjeti[0].text.strip().replace("Sjeverozapadna unutrašnjost - ","")

    #Regija - "Slavonija"
    slavonija = uvjeti[1].text.strip().replace("Posavina i Slavonija - ","")

    #Regija - "Istra i Kvarner"
    istra_i_kvarner = uvjeti[2].text.strip().replace("Gorski kotar i Lika - ","")

    #Regija -"Središnja Dalmacija"
    sredisnja_dalmacija = uvjeti[3].text.strip().replace("Dalmatinsko zaleđe - ","")

    #Regija - "Južna Dalmacija"
    juzna_dalmacija = uvjeti[5].text.strip().replace("Srednja i južna Dalmacija - ","")


    regije = [sredisnja_hrvatska,slavonija,istra_i_kvarner,sredisnja_dalmacija,juzna_dalmacija]
    regije_string= ["Središnja Hrvatska","Slavonija","Istra i Kvarner","Središnja Dalmacija","Južna Dalmacija"]

    bioprognoza = {"Povoljni uvjeti":"1",
                "Neutralno":"2",
                "Nepovoljni uvjeti":"3"}

    brojac = -1
    for regija in regije:
        if regija in bioprognoza:
            brojac += 1
            cursor.execute("UPDATE regija SET bioprognoza = {} WHERE naziv = '{}'".format(bioprognoza[regija],regije_string[brojac]))
            
            cursor.commit()


bioprognoza()

