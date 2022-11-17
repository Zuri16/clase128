from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# Enlace a NASA Exoplanet
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Controlador web
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

#guardar la informacion de la mini tabla
new_planets_data = []

#hyperlink=link de cada exoplaneta
def scrape_more_data(hyperlink):
    print(hyperlink)
    
    try:

        page=requests.get(hyperlink)
        page_soup=BeautifulSoup(page.content,"html.parser")
        listita=[]
        
        for ul_tag in page_soup.find_all("tr", attrs={"class": "fact_row"}):
                li_tags = ul_tag.find_all("td")
                for li_tag in enumerate(li_tags):
                     try:
                         listita.append(li_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                     except:
                         listita.append("")
    
        new_planets_data.append(listita)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

planet_df_1 = pd.read_csv("updated_scraped_data.csv")

# Llamar al método
for index, row in planet_df_1.iterrows():

    print(row["hyperlink"])

    # Llama a scrape_more_data(<hyperlink>)
    scrape_more_data(row["hyperlink"])

    print(f"La extracción de datos del hipervínculo {index+1} se ha completado")

print("estas son las comas",new_planets_data)

# Remover el carácter '\n' de los datos extraídos
scraped_data = []

for row in new_planets_data:
    replaced = []
    ## AGREGAR EL CÓDIGO AQUÍ ##
    for n in row:
        n=n.replace("\n"," ")
        replaced.append(n)
    
    scraped_data.append(replaced)

print(scraped_data)

headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]

new_planet_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convertir a CSV
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")
