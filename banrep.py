## DataFunction in Python for Use in Spotfire
## You moust define an output as DataTable with name "dfbanrep"
## Install selenium and put de chromedriver.exe in the especified path.


from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup

#options = Options()
chrome_path = r"xxxxxxxxx\chromedriver_win32\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# open it, go to a website, and get results
driver = webdriver.Chrome(chrome_path, options=options)

driver.get("https://totoro.banrep.gov.co/analytics/saw.dll?Go&NQUser=publico&NQPassword=publico123&Action=prompt&path=%2Fshared%2FSeries%20Estad%C3%ADsticas_T%2F1.%20Tasa%20de%20Cambio%20Peso%20Colombiano%2F1.1%20TRM%20-%20Disponible%20desde%20el%2027%20de%20noviembre%20de%201991%2F1.1.12.TCM_Serie%20historica%20promedio%20mensual&Options=rdf")

time.sleep(5)

soup=BeautifulSoup(driver.page_source, 'html.parser' )

driver.quit()

results = []
dfbanrep=pd.DataFrame()


def scrap_trm (clase):
    results=[]
    for elemento in soup.findAll(attrs={'class': clase}):
        mes = elemento.get_text()
        results.append(mes)
    return results

clase = 'mPTHC PTRHC0 OOLT'
dfbanrep['mes']=scrap_trm(clase)

clase = 'mPTDC PTDC OORT'
dfbanrep['mes_avg']=scrap_trm(clase)
dfbanrep["mes_avg"] = [float(str(i).replace(",", "")) for i in dfbanrep["mes_avg"]]
dfbanrep['mes_avg'].astype(float)

clase = 'mPTDC PTDC mPTLC PTLC OORT'
dfbanrep['mes_ending']=scrap_trm(clase)
dfbanrep["mes_ending"] = [float(str(i).replace(",", "")) for i in dfbanrep["mes_ending"]]
dfbanrep['mes_ending'].astype(float)
