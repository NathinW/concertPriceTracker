from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from enum import Enum
#from selenium.webdriver.common.keys import Keys

class Calendar(Enum):
    Jan = 1
    Feb = 2
    Mar = 3
    Apr = 4
    May = 5
    Jun = 6
    Jul = 7
    Aug = 8
    Sep = 9
    Oct = 10
    Nov = 11
    Dec = 12

class Concert:
    concertName = ""
    concertDate = None 
    
    def __init__(self, concertNameDate):
        self.concertName = concertNameDate[1]
        self.concertDate = parseDate(concertNameDate[0])
        self.prices = [] 

    def __eq__(self, other):
        if isinstance(other, Concert):
            return self.concertName == other.concertName
        else:
            return False

    def addPrice(self, newPrice):
        dateCollected = datetime.datetime.now()
        self.prices.append([dateCollected, newPrice])

    def __str__(self):
        output = self.concertName + " |DATE: " + self.concertDate.strftime("%x") + "| PRICES: ["
        for price in self.prices:
            output += "(" + price[0].strftime("%x") + " $"
            output += str(price[1]) + ") "
        return output + "]"

def parseDate(concertNameDate):
        now = datetime.datetime.now()
        day = 0
        month = 0

        monthCode = concertNameDate[0:3]
        dayCode = concertNameDate[4:]
        for item in Calendar:
            if monthCode == item.name:
                month = item.value

        if month == 0 | day == 0:
            raise Exception("Error with collecting concert date")
        if len(dayCode) < 8:
            day = int(dayCode)
            return datetime.datetime(now.year, month, day)
        else:
            day = int(dayCode[0:2])
            year = int(dayCode[-4]) 
            return datetime.datetime(year, month, day)
  
class ScrapeSeatgeek:
    def parseArrays(concertsAndPrices, previousConcertArray):
        concertsArray = []
        concertNames = concertsAndPrices[0]
        concertPrices = concertsAndPrices[1]
        if previousConcertArray:
            i = 0
            while i < len(concertNames):
                concert = Concert(concertNames[i])
                if concert in previousConcertArray:
                    index = previousConcertArray.index(concert)
                    previousConcertArray[index].addPrice(concertPrices[i])
                else:
                    concert.addPrice(concertPrices[i])
                    concertsArray.append(concert)
                i += 1
            concertsArray = previousConcertArray
        else:
                i = 0
                while i < len(concertNames):
                    newConcert = Concert(concertNames[i])
                    newConcert.addPrice(concertPrices[i])
                    concertsArray.append(newConcert)
                    i+=1
        return concertsArray

    def runScrape():
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
            concertNameDate = []
            concertNameDate.append(ps[0].text)
            concertNameDate.append(ps[1].text)
            arrayOfConcerts.append(concertNameDate)
            spans = event.find_elements(By.TAG_NAME, 'span')
            try:
                prices.append(int(''.join(filter(str.isdigit, spans[len(spans) - 1].text))))
            except:
                print("No price found for " + concertNameDate[1])
                prices.append(0)
        #time.sleep(2)
        driver.quit()
        if len(arrayOfConcerts) == len(prices):
            returnArray = [arrayOfConcerts, prices]
        else:
            raise Exception("Array of concerts lengeth doesn't match prices")
        return returnArray

class ConcertStorage:
    def __init__(self):
        self.CONCERT_AND_PRICES = ScrapeSeatgeek.parseArrays(ScrapeSeatgeek.runScrape(), [])

    def newScrape(self):
        self.CONCERT_AND_PRICES = ScrapeSeatgeek.parseArrays(ScrapeSeatgeek.runScrape(), self.CONCERT_AND_PRICES)
    
    def clear(self):
        self.CONCERT_AND_PRICES = []

    def __str__(self):
        output = ""
        for concert in self.CONCERT_AND_PRICES:
            output += str(concert) + "\n"
        return output

data = ConcertStorage()
print(data)

data.newScrape()
print(data)