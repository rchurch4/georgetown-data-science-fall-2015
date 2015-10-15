# trip advisor scraper

import os
import sys
import time
import logging
import requests
from bs4 import BeautifulSoup
import re
import python_message as pm
import datetime
import json
import traceback

datadir = 'data/'
base_url = "http://www.tripadvisor.com/"
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.0 Safari/537.36'
regex = re.compile('[^A-Za-z0-9\s]')
money_re = re.compile('[^0-9]')
city_list = ['Washington_DC_District_of_Columbia', 'Nashville_Tennessee']
code_list = ['g28970', 'g55229']

# BEGIN YEAR PAGE SCRAPING
def get_city_page(c,index):
	url = base_url + 'Restaurants-'+str(code_list[c])+'-oa'+str(index)+'-'+city_list[c]+'.html'
	headers = {'User-Agent': user_agent}
	response = requests.get(url, headers=headers)
	html = response.text.encode('utf-8')
	return html

def parse_city_page(html):
	soup = BeautifulSoup(html)
	restaurants = soup.find_all('div', {'class':'listing'})
	new_restaurants = []
	for r in restaurants:
		# from htmly mess, get title and rating boxes
		title = r.find('h3', {'class':'title'}).find('a')
		rating = r.find('div',{'class':'rating'})

		# from title box, get link to review page and restaurant name
		rest_link = title.get('href')
		rest_name = title.get_text().strip()

		# from rating box, get review count and restaurant rating
		rev_count = rating.find('span', {'class':'reviewCount'}).find('a').get_text().strip()
		rest_rating = rating.find('span',{'class':'rate'}).find('img').get('alt')
		rest_rev_count = int(rev_count.split(' ')[0].replace(',',''))
		rest_rating = float(rest_rating.split(' ')[0])
		
		#create restaurant object and add to list of new_restaurants
		r = [rest_link, rest_name, rest_rev_count, rest_rating]
		new_restaurants.append(r)
	return new_restaurants

# END YEAR PAGE SCRAPING

#BEGIN REVIEW PAGE SCRAPING
def get_review_page(rest_url):
	url = base_url + rest_url[1:]
	#print url
	headers = {'User-Agent': user_agent}
	response = requests.get(url, headers=headers)
	html = response.text.encode('utf-8')
	return html

#returns (budget, revenue)
def parse_review_page(html, offset):
	soup = BeautifulSoup(html)
	try:
		next_url = soup.find('div',{'class':'pageNumbers'}).find('a',{'class':'pageNum taLnk','data-offset':offset}).get('href')
	except:
		next_url = None

	review_boxes = soup.find('div',id='REVIEWS').find_all('div',{'class':'reviewSelector'})
	reviews = []
	cnt = offset-10
	for rb in review_boxes:
		cnt += 1
		reviewer_info = rb.find('div',{'class':'col1of2'})
		review_details = rb.find('div',{'class':'col2of2'})

		if review_details is None:
			return (reviews, None)
		# from review details
		english = review_details.find('div', {'class':'googleTranslation'})
		if english is None:
			title = review_details.find('div',{'class':'quote'}).find('span').get_text().strip()
			entry = review_details.find('div',{'class':'entry'}).find('p').get_text().strip()

			rate_info = review_details.find('div',{'class':'rating'})
			rating = None
			rating_date = None
			try:
				rating = float(rate_info.find('span',{'class':'rate'}).find('img').get('alt').split(' ')[0])
			except:
				pass
			try:
				rating_date = rate_info.find('span', {'class':'ratingDate'}).get_text().strip().split(' ',1)[1].split('\n')[0]
			except:
				pass

			# from reviewer info
			member_info = reviewer_info.find('div', {'class':'member_info'})
			reviewer_name = member_info.find('div', {'class':'username'}).get_text().strip()
			reviewer_location = None
			try:
				reviewer_location = member_info.find('div', {'class':'location'}).get_text().strip()
			except:
				pass
			if reviewer_location == '':
				reviewer_location = None

			member_badging = reviewer_info.find('div', {'class':'memberBadging'})
			reviewer_num_reviews = 1
			try:
				reviewer_num_reviews = int(member_badging.find('div',{'class':'reviewerBadge'}).get_text().strip().split(' ')[0].replace(',',''))
			except:
				pass
			reviewer_num_helpful = 0
			try:
				reviewer_num_helpful = int(member_badging.find('div',{'class':'helpfulVotesBadge'}).get_text().strip().split(' ')[0].replace(',',''))
			except:
				pass

			review = [title, rating, rating_date, reviewer_name, reviewer_location, reviewer_num_reviews, reviewer_num_helpful, entry]
			reviews.append(review)
		else:
			return (reviews,None)
	return (reviews, next_url)
#END REVIEW PAGE SCRAPING

def parse_trip_advisor(datadir,step_cleared):
	if step_cleared < 1:
		for c in range(0,len(city_list)):
			city_restaurants = []
			index = 0
			while index < 1000:
				if index %120 == 0:
					print index
				city_restaurants += parse_city_page(get_city_page(c, index))
				index += 30
				time.sleep(2)
			with open(datadir+city_list[c]+'_basic_list.json','w') as f:
				json.dump(city_restaurants, f)
			print 'Done Basic List for '+city_list[c]
	if step_cleared < 2:
		for c in range(0,len(city_list)):
			city_restaurants = []
			with open(datadir+city_list[c]+'_basic_list.json','r') as f:
				city_restaurants = json.load(f)
			restaurant_reviews = []
			num_files = 1
			completed = (num_files*20) +1
			for r in city_restaurants[completed:]:
				print r[1]
				if len(restaurant_reviews) == 20:
					print 'WRITING TO FILE'
					with open(datadir+city_list[c]+'_review_list'+str(num_files)+'.json','w') as f:
						json.dump(restaurant_reviews, f)
					num_files += 1
					restaurant_reviews = []
				rest_url = r[0]
				review_count = r[2]
				offset = 10
				reviews = []
				while offset <= review_count+10 and rest_url is not None:
					(new_reviews, next_url) = parse_review_page(get_review_page(rest_url), offset)
					reviews += new_reviews
					rest_url = next_url
					offset += 10
					time.sleep(2)
				r = [r[1], reviews]
				restaurant_reviews.append(r)
			with open(datadir+city_list[c]+'_review_list'+str(num_files)+'.json','w') as f:
				json.dump(restaurant_reviews, f)
			num_files+=1
			restaurant_reviews = []
			print 'Done Review List for '+city_list[c]
	return

start_time = time.time()
try:
	parse_trip_advisor(datadir,1)
	msg = 'Finished in '+str(datetime.timedelta(seconds = time.time() - start_time))+'.'
	print msg
except:
	#this error handling thanks to http://stackoverflow.com/questions/1278705/python-when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
	traceback.print_exc()
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	e= str(exc_type)+', '+str(fname)+', '+str(exc_tb.tb_lineno)+', '+str(exc_obj)
	e += '. Finished with an Error in '+str(datetime.timedelta(seconds = time.time() - start_time))+'.'
	print e
	msg = e
finally:
	pass#pm.send(msg)