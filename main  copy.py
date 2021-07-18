import requests
from bs4 import BeautifulSoup
import os
import datetime
import csv

from selenium import webdriver
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
options = webdriver.ChromeOptions()
# options.headless = True
# options.add_argument(f'user-agent={user_agent}')
# options.add_argument("--window-size=1920,1080")
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--allow-running-insecure-content')
# options.add_argument("--disable-extensions")
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")
# options.add_argument("--start-maximized")
# options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')


options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

class Vivareal:

    timestamp = str(datetime.datetime.now()).replace(".","").replace("-","").replace(":","")
    filename = "results_{}".format(timestamp)+".csv"

    def __init__(self):
        self.driver = webdriver.Chrome('chromedriver.exe',options=options)
        # self.csvCreater()
        # i = 0
        url = "https://www.vivareal.com.br/aluguel"
        self.driver.implicitly_wait(30)
        self.driver.get(url)

        titles = self.driver.find_elements_by_css_selector(".js-card-title .js-card-title")
        self.driver.implicitly_wait(30)
        nextbutton = self.driver.find_element_by_css_selector(".pagination__item:nth-child(9) .js-change-page").click()
           
        print(nextbutton)
        # print(len(titles))
        # for title in titles:
        #     print(title.text)
        # while True:
        #     print("Page Number: {}".format(i+1))
        #     # print(url.format(str(i+1)))
        #     self.start()
            # self.driver.find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]/a').click()
        #     i = i+1


    def start(self):
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]/a')))
        # response = requests.get(url)
        # print(response.content)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        results = soup.select_one(".results-list.js-results-list")
        data_lists = results.select("article.property-card__container.js-property-card")

        for item in data_lists:
            title = item.select_one("span.property-card__title.js-cardLink.js-card-title")
            if title is not None:
                title = title.text
            else:
                title = ""
            address = item.select_one("span.property-card__address")
            if address is not None:
                address = address.text
            else:
                address = ""
            
            price_div = item.select_one(".property-card__price.js-property-card-prices.js-property-card__price-small")
            price = price_div.find("p")
            if price or price_div is not None:
                price = str(price.text).strip()
            else:
                price = ""
                

            price_details = item.select_one(".property-card__price-details--condo")
            if price_details is not None:
                price_details = str(price_details.text).replace("Condomínio:","").strip()
            else:
                price_details = ""

            area = item.select_one("li.property-card__detail-item.property-card__detail-area")
            if area is not None:
                area = str(area.text).replace("  ","").strip()
            else:
                area = ""

            rooms = item.select_one("li.property-card__detail-item.property-card__detail-room.js-property-detail-rooms")
            if rooms is not None:
                rooms = str(rooms.text).replace(" Quarto","").replace("s","").strip()
            else:
                rooms = ""

            bathrooms = item.select_one("li.property-card__detail-item.property-card__detail-bathroom.js-property-detail-bathroom")
            if bathrooms is not None:
                bathrooms = str(bathrooms.text).replace(" Banheiro","").replace("s","").strip()
            else:
                bathrooms = ""
            garages = item.select_one("li.property-card__detail-item.property-card__detail-garage.js-property-detail-garages")
            if garages is not None:
                garages = str(garages.text).replace("   Vaga","").replace("s","").strip()
            else:
                garages = ""
            print(title,address,price,price_details,area,rooms,bathrooms,garages)
            self.csvupdate(title,address,price,price_details,area,rooms,bathrooms,garages)


    def csvCreater(self):
        
        with open(self.filename,'w' ,newline='') as file:
            fieldNames = ['Title','Address','Rent','Admin Fee','Area','Rooms','Bathrooms','Parking']
            thewriter = csv.DictWriter(file, fieldnames=fieldNames)
            thewriter.writeheader()

    def csvupdate(self,title,address,price,price_details,area,rooms,bathrooms,garages):
        with open(self.filename,'a' ,newline='') as file:
            fieldNames = ['Title','Address','Rent','Admin Fee','Area','Rooms','Bathrooms','Parking']
            thewriter = csv.DictWriter(file, fieldnames=fieldNames)
            thewriter.writerow({'Title': title,'Address': address,'Rent': price,'Admin Fee': price_details,'Area': area,'Rooms':rooms,'Bathrooms': bathrooms,'Parking': garages})

bot = Vivareal()