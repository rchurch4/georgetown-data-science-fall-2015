# imdb scraper

import os
import sys
import time
import logging
import requests
from BeautifulSoup import BeautifulSoup
import re
import python_message as pm
import datetime

datadir = 'data/'
base_url = "http://www.tripadvisor.com/"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36"
regex = re.compile('[^A-Za-z0-9\s]')
money_re = re.compile('[^0-9]')
city_list = ['Washington_DC_District_of_Columbia', 'Nashville_Tennessee']
code_list = ['g28970', 'g55229']

# BEGIN YEAR PAGE SCRAPING
def get_city_page(c,index):
	url = base_url + 'Restaurants-'+str(city_list[c])+'-oa'+str(index)+'-'+city_list[c]+'.html'
	headers = {'User-Agent': user_agent}
	response = requests.get(url, headers=headers)
	html = response.text.encode('utf-8')
	return html

def parse_city_page(html):
	return
# END YEAR PAGE SCRAPING

#BEGIN REVIEW PAGE SCRAPING
def get_review_page(rest_id):
	url = base_url
	headers = {'User-Agent': user_agent}
	response = requests.get(url, headers=headers)
	html = response.text.encode('utf-8')
	return html

#returns (budget, revenue)
def parse_review_page(rest_id):
	return
#END REVIEW PAGE SCRAPING

def parse_trip_advisor(datadir):
	return

start_time = time.time()
try:
	#parse_trip_advisor(datadir)
	msg = 'Finished in '+str(datetime.timedelta(seconds = time.time() - start_time))+'.'
	print msg
except:
	#this error handling thanks to http://stackoverflow.com/questions/1278705/python-when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	e= str(exc_type)+', '+str(fname)+', '+str(exc_tb.tb_lineno)+', '+str(exc_obj)
	e += '. Finished in '+str(datetime.timedelta(seconds = time.time() - start_time))+'.'
	print e
	msg = e
finally:
	pm.send(msg)