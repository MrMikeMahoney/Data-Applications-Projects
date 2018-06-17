# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 21:51:00 2018

@author: Mike aka DrMantisToboggan 

This is an attempt to scrape coinmarketcap.com >> To get historical data for a select
list of cryptocurrencies from 02/23/2014 to 02/23/2018

Note: This is done out of spite beacuse of the "Kaggle isn't a primary source but a secondary source of data." 
Comments a large portion of the class received!! I am doing this to merely check my data!!
"""

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
#import re
import urllib.request
#from datetime import datetime
from time import sleep
import random


def get_source(my_url):
    #open the connection and grabbing the page
    req=urllib.request.Request(my_url, headers={'User-Agent': 'Googlebot/1.0 (googlebot@googlebot.com http://googlebot.com/)'}) #to fool the API into thinking we are a browser
    uClient=uReq(req) #sends GET request to URL
    page_html=uClient.read() #reads returned data and puts it in a variable
    uClient.close() #close the connection
    page_soup = soup(page_html, "html.parser") ## does the HTML parsing
    return [page_soup, page_html]


# This is the URL we want to use >> "bitcoin" can be replaced >> Using our list
# Good Start = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20140223&end=20180224"
#This is the first part of the URL we want to use to scrape the page
url_head = "https://coinmarketcap.com/currencies/"

#This is the ending of the URL we want to scrape
#url_tail = "/historical-data/?start=20140223&end=20180224"

# 1 day Tail >> For a 1 day scrape, to test our loop
#url_tail = "/historical-data/?start=20180223&end=20180224"

# 2 day Tail >> For a 2 day scrape, to check "cryp_slug" is being added corecctly 
#url_tail = "/historical-data/?start=20180222&end=20180224"

# Whole year Tail >> For the beginning of the year scrape >> 02180101
#url_tail = "/historical-data/?start=20180101&end=20180224"

# Till 2017 >> Getting everything until 2017/01/01
#url_tail = "/historical-data/?start=20170101&end=20180224"

# Getting a final list to check our model
url_tail = "/historical-data/?start=20180227&end=20180228"


#list of crypto currencies we want to scrape
#cryp_list = ["bitcoin", "dogecoin", "ethereum", "ripple", "litecoin", "neo", "maker", "tether"]
# We got our premission denies, temporarily but we chamged User Agents >> Back to the remandier 
#>> Minus the rest of ripple
#cryp_list = ["litecoin", "neo", "maker", "tether"]
# Getting our scraped data >> To check our models
cryp_list = ["bitcoin", "dogecoin", "ethereum", "maker", "tether"]

# Thether is one of the least viotile stocks ; Maker has a high price


#Testing just Bitcoin
#cryp_list = ["bitcoin"]

#file we want to write parsed data to
# Our test file name >> Until it worked
#filename="Cyrpto_Scraped_test.csv" #csv file parsing scraped data to
#filename="Crypto_Scraped_Data.csv"
# Another test run writing to a CSV will more data
#filename="Crypto_Better_Scrape.csv"
#Test our predictions
#filename="Crypto_Test_Model.csv"

filename="C:/Users/Mike/Documents/Conda Scripts/Created Datasets/floppy_mctest.csv"

f=open(filename, "w") 
headers= "Slug,Date,Open,High,Low,Close,Volume,Market Cap\n" # headers for each column
f.write(headers)
"""
#file we want to write parsed data to
filename="Mahoney_HW4_ScrapedData_01.csv" #csv file parsing scraped data to
f=open(filename, "w") #opening the file
headers = "Date,Location,Description,Price\n" #Headers for each column
f.write(headers) #writting headers to file
"""


# Creating the loop to to set up URL to scrape
for crypto in cryp_list:
    #we are going to loop through each crypto currency
    my_url = url_head + crypto + url_tail
    
    #Original User Agent
    #req = urllib.request.Request (my_url, headers={
    #'#User-Agent': 'Googlebot/1.0 (googlebot@googlebot.com http://googlebot.com/)'})  # to fool the API into thinking we are a browser
    # Another User Agent >> They wont suspect a mac
    req = urllib.request.Request (my_url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'})
    
    uClient = uReq (req)  # sends GET request to URL
    page_html = uClient.read ()  # reads returned data and puts it in a variable
    uClient.close ()  # close the connection
    page_soup = soup(page_html, "html.parser")

    containers = page_soup.findAll("tr", {"class":"text-right" }) 

    contain = containers[0]
    container = containers[0]

    for container in containers: #initializing for loop >> to loop through each post
        pagedata = get_source(my_url) #utilizing our "user-agent" to webscrape
    
        slug = crypto
        #Creating the Date Container
        date_container = container.findAll("td", {"class":"text-left"})
        date = date_container[0].text # Selects the first element of the date container (the text only)
        #best_date = date.strftime("%m-%d-%y")
        #ate_format = datetime.strptime(date, "%m-%d-%y")
        #best_date = datetime.datetime(date, "%m-%d-%y")
        
        #Creating the  OHLC (Open[1], High[2], Low[3], CLose[4]) Container >> Note this will pull four different elements
        OHLC_container = container.findAll("td") #, {"data-format-fiat="" data-format-value"})
        #OHLC_container = container.td
        Open = OHLC_container[1].text
        #Open = OHLC_container["data-format-value"]
        #Open = OHLC_container[1].text # Grabs the 2nd "td" which is open in this case
    
        High = OHLC_container[2].text # Grabs the 3nd "td" which is high
        Low = OHLC_container[3].text # Grabs the 4th "td" which is Low
        Close = OHLC_container[4].text # Grabs the 5th "td" which is Close
    
        #Creating the Volume and Market Cap Container
        #Vol_Mkt_Cap_container = container.td
        Volume = OHLC_container[5].text
        Market_Capitalization = OHLC_container[6].text
        # <td data-format-fiat="" data-format-value="9937.07">9,937.07</td>
        f.write(str(slug)+"," +str(date.replace(",", "/"))+"," 
            +str(Open.replace(",", "")) +","+str(High.replace(",", "")) 
            +","+str(Low.replace(",", ""))
            +","+str(Close.replace(",", "")) +","+ str(Volume.replace(",", "")) +"," 
            + str(Market_Capitalization.replace(",", "")) +"\n")
        # setting a random intiger
        nap_time = random.uniform(0.3, 2.5)
        # just to be kind to the server >> its my good deed of the week
        sleep(nap_time)
f.close()