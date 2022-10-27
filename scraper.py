from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
#from selenium.webdriver.common.keys import Keys

class ScrapeSeatgeek:
    def __init__(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        url = 'https://seatgeek.com/venues/the-sylvee/tickets'
        driver.get(url)
        arrayOfConcerts = []
        prices = []

        eventList = driver.find_elements(By.TAG_NAME, 'ul')
        events = eventList[3].find_elements(By.TAG_NAME, 'li')
        
        for event in events:
            ps = event.find_elements(By.TAG_NAME, 'p')
            concertName = "(" + ps[0].text + ") " + ps[1].text
            arrayOfConcerts.append(concertName)
            spans = event.find_elements(By.TAG_NAME, 'span')
            try:
                prices.append(int(''.join(filter(str.isdigit, spans[len(spans) - 1].text))))
            except:
                print("No price found for " + concertName)
                prices.append(0)
        #time.sleep(2)
        driver.quit()

        self.concerts = arrayOfConcerts
        self.prices = prices

def startScrape():
    return ScrapeSeatgeek()


csvfile = open('SeatgeekScrapeResults.csv', 'r+', newline='')
reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
results = startScrape()
#if (",".join(next(reader)) != ','.join(results.concerts):


writer = csv.writer(csvfile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
writer.writerow(results.concerts)
writer.writerow(results.prices)


print(results.concerts)
print(len(results.concerts))
print(results.prices)
print(len(results.prices))

print(','.join(results.concerts))
