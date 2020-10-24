import pyodbc
import requests
from bs4 import BeautifulSoup
import os

path = os.path.dirname(__file__)

print("Ažuriranje podataka za Europu")

#spajanje na Access bazu
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' + "DBQ={}\projekt.accdb;".format(path)
    )
connection = pyodbc.connect(conn_str)
cursor = connection.cursor()

gradovi_list = []

#Funkcija za dohvaćanje gradova koji se nalaze na vrijeme.net/europa
def gradovi():
    url = "http://www.vrijeme.net/europa"
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html5lib")

    grad = soup.find("ul",attrs={"id":"locations-list"})

    for li in grad.find_all("li"):
        try:

            ime = li.find("span",attrs={"class":"location-name"}).text
            gradovi_list.append(ime)
        except:
            continue
    

gradovi()

#Insertanje gradova u bazu podataka(POKRENUTI JEDNOM!)
#for grad in gradovi_list:
#    cursor.execute("INSERT INTO vrijeme_europa (grad) VALUES ('{}')".format(grad))

#cursor.commit()



#Funkcija za dohvaćanje podataka o temperaturi, tlaku i vlažnosti za svaki grad
def temperatura():
    url = "http://www.vrijeme.net/europa"
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html5lib")

    grad = soup.find("ul",attrs={"class":"type-01"})

    brojac = -1
    for li in grad.find_all("li"):
        temperatura = li.find("a")
        try:
            temperatura = temperatura.find("span",{"class":"container"})
            
        except:
            continue
    
        temperatura = temperatura.find("ul",{"class":"forecast location-detail cf"})
        
        temperatura = temperatura.find("li",{"class":"temp alt-01"})

        temperatura = temperatura.find("span",{"class":"val"}).text.replace("°","")
        
        vlaznost = li.find("a")
        try:
            vlaznost = vlaznost.find("span",{"class":"container"})
        except:
            continue
        vlaznost = vlaznost.find("ul",{"class":"forecast location-detail cf"})
        vlaznost = vlaznost.find("li",{"class":"humidity alt-01"})
        vlaznost = vlaznost.find("span",{"class":"val"}).text.replace("%","")


        tlak = li.find("a")
        try:
            tlak = tlak.find("span",{"class":"container"})
        except:
            continue
        tlak = tlak.find("ul",{"class":"forecast location-detail cf"})
        tlak = tlak.find("li",{"class":"pressure alt-01"})
        tlak = tlak.find("span",{"class":"val"}).text
        tlak = tlak.replace(" hPa","")


        brojac += 1

        cursor.execute('''
                UPDATE vrijeme_europa
                SET temperatura = {}
                WHERE grad = '{}'

                '''.format(temperatura,gradovi_list[brojac]))

        cursor.execute('''
                UPDATE vrijeme_europa
                SET vlaznost = {}
                WHERE grad = '{}'

                '''.format(vlaznost,gradovi_list[brojac]))

        cursor.execute('''
                UPDATE vrijeme_europa
                SET tlak = {}
                WHERE grad = '{}'

                '''.format(tlak,gradovi_list[brojac]))

        cursor.execute('''
                UPDATE vrijeme_europa
                SET tlak = NULL
                WHERE tlak = 0 

                ''')
        cursor.commit()

temperatura()