# trip advisor scraper

import os
import sys
import time
import logging
import requests
from bs4 import BeautifulSoup
import re
#import python_message as pm
import datetime
import json
import traceback

#defines random stuff needed for the program to run
	#datadir says what folder output files will go into
	#city_list and code_list are used to generate urls for scraping
datadir = 'data/'
base_url = "http://www.tripadvisor.com/"
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.0 Safari/537.36'
regex = re.compile('[^A-Za-z0-9\s]')
money_re = re.compile('[^0-9]')
city_list = ['Washington_DC_District_of_Columbia']#, 'Nashville_Tennessee']
code_list = ['g28970']#, 'g55229']

# BEGIN YEAR PAGE SCRAPING
# get_city_page takes c as in the index of the city from city_list you want to scrape
	# and index, as in the starting restaurant rank you want to scrape (used to iterate over pages)
def get_city_page(c,index):
	url = base_url + 'Restaurants-'+str(code_list[c])+'-oa'+str(index)+'-'+city_list[c]+'.html'
	headers = {'User-Agent': user_agent}
	response = requests.get(url, headers=headers)
	html = response.text.encode('utf-8')
	return html

# parse_city_page takes html generated from get_city_page and turns it into a list of restuarants
def parse_city_page(html):
	soup = BeautifulSoup(html)
	#gets all restaurant listings
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
# uses the restaurant url that we got while scraping to get the reviews page
def get_review_page(rest_url):
	url = base_url + rest_url[1:]
	headers = {'User-Agent': user_agent}
	response = requests.get(url, headers=headers)
	html = response.text.encode('utf-8')
	return html

#returns (budget, revenue)
def parse_review_page(html, offset):
	soup = BeautifulSoup(html)
	
	# gets the next review page url, if there is one
	try:
		next_url = soup.find('div',{'class':'pageNumbers'}).find('a',{'class':'pageNum taLnk','data-offset':offset}).get('href')
	except:
		next_url = None

	# gets the reviews on this page, if there are any (oddly there exist pages without reviews)
	review_boxes = []
	try:
		review_boxes = soup.find('div',id='REVIEWS').find_all('div',{'class':'reviewSelector'})
	except:
		pass
	reviews = []
	cnt = offset-10
	for rb in review_boxes:
		cnt += 1
		# splits the html into the restaurant review info and the reviewer info
		reviewer_info = rb.find('div',{'class':'col1of2'})
		review_details = rb.find('div',{'class':'col2of2'})

		if review_details is None:
			return (reviews, None)
		# from review details, get whether the review is in english
		english = review_details.find('div', {'class':'googleTranslation'})
		if english is None: #english is None means there was no google translate box > english review
			# from htmly mess, get title and review text
			title = review_details.find('div',{'class':'quote'}).find('span').get_text().strip()
			entry = review_details.find('div',{'class':'entry'}).find('p').get_text().strip()

			# from htmly mess, get rating info that is still a mess
			rate_info = review_details.find('div',{'class':'rating'})
			rating = None
			rating_date = None

			# from htmly mess, get rating and date
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

			# from htmly mess, get reviewer name and location if it exists
			reviewer_name = member_info.find('div', {'class':'username'}).get_text().strip()
			reviewer_location = None
			try:
				reviewer_location = member_info.find('div', {'class':'location'}).get_text().strip()
			except:
				pass
			if reviewer_location == '':
				reviewer_location = None

			# from htmly mess, get reviewer's num_reviews and num_helpful_reviews
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

			# create review list item and add it to the list of reviews
			review = [title, rating, rating_date, reviewer_name, reviewer_location, reviewer_num_reviews, reviewer_num_helpful, entry]
			reviews.append(review)
		else:
			# if theres no reviews on this page for some reason, return an empty list, and no pointer to a next page
			return (reviews,None)
	return (reviews, next_url)
#END REVIEW PAGE SCRAPING

# pulls everything together
# step_cleared = 0 or 1. if 0, scrape city pages and then review pages. if 1, pull city pages list and scrape review pages only.
def parse_trip_advisor(datadir,step_cleared):
	# if we haven't scraped the list of restaurants, do so
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
	# if we have scraped the list of restaurants, scrape the reviews
	if step_cleared < 2:
		for c in range(0,len(city_list)):
			city_restaurants = []
			with open(datadir+city_list[c]+'_basic_list.json','r') as f:
				city_restaurants = json.load(f)
			restaurant_reviews = []
			# change the number of files to relflect where in the restaurant list you should start scraping reviews.
			# used to stop/start scraping in the middle. default 0.
			num_files = 0
			completed = 0
			if num_files > 0:
				completed = (num_files*20) +1
			# scrape reviews for unscraped restaurants
			for r in city_restaurants[completed:]:
				print r[1]
				# write to file after 20 restaurants have been scraped
				if len(restaurant_reviews) == 20:
					print 'WRITING TO FILE'
					with open(datadir+city_list[c]+'_review_list'+str(num_files)+'.json','w') as f:
						json.dump(restaurant_reviews, f)
					num_files += 1
					restaurant_reviews = []
				# get needed info from the restaurant list
				rest_url = r[0]
				review_count = r[2]
				offset = 10
				reviews = []
				# scrape the reviews from the restaurant page
				while offset <= review_count+10 and rest_url is not None:
					(new_reviews, next_url) = parse_review_page(get_review_page(rest_url), offset)
					reviews += new_reviews
					rest_url = next_url
					offset += 10
					# sleep so that you don't get caught scraping.
					time.sleep(2)
				r = [r[1], reviews]
				# add restaurant's review list to the list of restaurants' reviews
				restaurant_reviews.append(r)
			# if this is the last file, write it
			with open(datadir+city_list[c]+'_review_list'+str(num_files)+'.json','w') as f:
				json.dump(restaurant_reviews, f)
			num_files+=1
			restaurant_reviews = []
			print 'Done Review List for '+city_list[c]
	return

# keep track of the ungodly amount of time this takes
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
	#option to have the program text you when it's done scraping
	pass#pm.send(msg)