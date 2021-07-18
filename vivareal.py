import os
import datetime
import csv
import time
import random
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import undetected_chromedriver as uc

class Vivareal:

    timestamp = str(datetime.datetime.now()).replace(".","").replace("-","").replace(":","")
    filename = "results_{}".format(timestamp)+".csv"
    chromeOptions = uc.ChromeOptions()
        #chromeOptions.add_argument('--headless')
    driver = uc.Chrome(options=chromeOptions)

    def __init__(self):
        
        self.csvCreater()
        url = "https://www.vivareal.com.br/aluguel"
        self.driver.get(url)
        
        while True:
            # driver.implicitly_wait(10)
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.property-card__title.js-cardLink.js-card-title')))
            self.ScrollPage()
            result_div = self.driver.find_element_by_css_selector(".results-list.js-results-list")
            result_cards_list = result_div.find_elements_by_css_selector("article.property-card__container.js-property-card")
            
            for item in result_cards_list:
                try:
                    title = item.find_element_by_css_selector("span.property-card__title.js-cardLink.js-card-title").text
                except NoSuchElementException:
                    title = "-"
                try:
                    address = item.find_element_by_css_selector("span.property-card__address").text
                except NoSuchElementException:
                    address = "-"    
                try:
                    price = item.find_element_by_css_selector(".property-card__price.js-property-card-prices.js-property-card__price-small").text
                except:
                    price = "-"
                try:
                    price_details = item.find_element_by_css_selector(".property-card__price-details--condo")
                    price_details = str(price_details.text).replace("Condomínio:","").strip()
                except NoSuchElementException:
                    price_details = "-"
                try:
                    area = item.find_element_by_css_selector("li.property-card__detail-item.property-card__detail-area")
                    area = str(area.text).replace("  ","").strip()
                except NoSuchElementException:
                    area = "-"
                try:
                    rooms = item.find_element_by_css_selector("li.property-card__detail-item.property-card__detail-room.js-property-detail-rooms")
                    rooms = str(rooms.text).replace(" Quarto","").replace("s","").strip()
                except NoSuchElementException:
                    rooms = "-"
                try:
                    garages = item.find_element_by_css_selector("li.property-card__detail-item.property-card__detail-garage.js-property-detail-garages")
                    garages = str(garages.text).replace("Vaga","").replace("s","").strip()
                except NoSuchElementException:
                    garages = "-"
                try:
                    bathrooms = item.find_element_by_css_selector("li.property-card__detail-item.property-card__detail-bathroom.js-property-detail-bathroom")
                    bathrooms = str(bathrooms.text).replace(" Banheiro","").replace("s","").strip()
                except NoSuchElementException:
                    bathrooms = "-"
                    
                self.csvupdate(title,address,price,price_details,area,rooms,bathrooms,garages)
                print(title,"\n",address,"\n",price,"\n",price_details,"\n",area,"\n",rooms,"\n",bathrooms,"\n",garages,"\n\n")

            self.driver.find_element_by_xpath("//a[@class='js-change-page' and contains(text(), 'Próxima página')]").click()
            
            time.sleep(5)

    def csvCreater(self):
        with open(self.filename,'w' ,newline='') as file:
            fieldNames = ['Title','Address','Rent','Admin Fee','Area','Rooms','Bathrooms','Parking']
            thewriter = csv.DictWriter(file, fieldnames=fieldNames)
            thewriter.writeheader()

    def csvupdate(self,title,address,price,price_details,area,rooms,bathrooms,garages):
        with open(self.filename,'a' ,newline='') as file:
            fieldNames = ['Title','Address','Rent','Admin Fee','Area','Rooms','Bathrooms','Parking']
            thewriter = csv.DictWriter(file, fieldnames=fieldNames)
            thewriter.writerow({'Title': str(title),'Address': str(address),'Rent': price,'Admin Fee': price_details,'Area': area,'Rooms':rooms,'Bathrooms': bathrooms,'Parking': garages})
    
    def ScrollPage(self):
        lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                lastCount = lenOfPage
                sleep(3)
                lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                    match=True
bot = Vivareal()