# DROP TABLE
# Yelp Data
#
# I used the following resources:
# -http://stackoverflow.com/questions/11205386/python-beautifulsoup-get-an-attribute-value-based-on-the-name-attribute
#  for help with exracting star rating from the meta tag
# -https://www.quora.com/For-the-Python-requests-get-method-how-can-I-while-loop-the-function-to-ensure-it-goes-forever-until-a-connection-is-made
#  for help diagnosing ConnectionError and exponential backoff solution
# -Rob Churchill HW 2
# 

from bs4 import BeautifulSoup
import requests
import json
import time
import re

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
headers = {'User-Agent': user_agent}
base_url = "http://www.yelp.com"
regex = re.compile('[^A-Za-z0-9\s]')
money_re = re.compile('[^0-9]+')
# class for number of reviews by a reviewer
experience_class = 'i-18x18_review_c-common_sprite-wrap'
 
def get_text(tags):
    return [tag.get_text() for tag in tags]

def get_review_page(url, offset):
    url = url + '?start=' + str(offset)
    delay = 0.5
    while True:
        try:
            time.sleep(delay)
            response = requests.get(url, headers=headers)
            break
        except requests.exceptions.ConnectionError:
            wait *= 2
            print 'Connection Error, backing off for', delay, 'seconds'
    html = response.text.encode('utf-8')
    return html

def parse_review_page(html):
    soup = BeautifulSoup(html, 'lxml')
    review_feed = soup.find('div', class_='feed')
    names = get_text(review_feed.find_all('li', class_='user-name'))
    locations = get_text(review_feed.find_all('li', class_='user-location'))
    experience = get_text(review_feed.find_all('span', class_=experience_class))
    date_tags = review_feed.find_all('meta', itemprop='datePublished')
    dates = [tag['content'] for tag in date_tags]
    star_tags = review_feed.find_all('meta', itemprop='ratingValue')
    stars = [tag['content'] for tag in star_tags]
    reviews = get_text(review_feed.find_all('p', lang='en'))
    return map(review_dict_entry, names, locations, experience, dates, stars, reviews)

def review_dict_entry(name, location, experience, date, rating, review):
    return {'name':name, 'location':location, 'exp':experience, 'date':date, 'rating':rating, 'review':review}

# get the number of English reviews as classified by Yelp
def get_num_reviews(url):
    html = get_review_page(url, 0)
    soup = BeautifulSoup(html, 'lxml')
    eng_tab = soup.find('span', {'data-lang':'en'}).find('span', class_='tab-link_count')
    num_reviews = eng_tab.get_text().strip('()')
    return int(num_reviews)
    
def get_all_reviews(url):
    reviews = []
    offset = 0
    num_reviews = get_num_reviews(url)
    print "num_reviews:", num_reviews
    while offset < num_reviews:
        html = get_review_page(url, offset)
        reviews += parse_review_page(html)
        offset = len(reviews)
        print offset
    return num_reviews, reviews


# ROB HW2
def get_search_page(offset, location):
	url = base_url + '/search?find_loc=' + location + '&cflt=restaurants&start=' + str(offset)
	response = requests.get(url, headers=headers)
	html = response.text.encode('utf-8')
	return html

def parse_search_page(html, ctr):
	restaurants = []
	soup = BeautifulSoup(html, 'lxml')
	wrappers = soup.findAll('div', {'class':'search-result natural-search-result'})
	for w in wrappers:
		main_wrapper = w.find('div', {'class':'biz-listing-large'})
		info_wrapper = main_wrapper.find('div', {'class':'main-attributes'})
		phone_wrapper = main_wrapper.find('div', {'class':'secondary-attributes'})
		address = main_wrapper.find('address').get_text()
		phone = str(money_re.sub('', phone_wrapper.find('span', {'class':'biz-phone'}).find(text=True)))
		info = info_wrapper.find('div', {'class':'media-story'})
		title_stuff = info.find('h3', {'class':'search-result-title'}).find('span', {'class':'indexed-biz-name'}).find('a', href=True)
		url = title_stuff['href']
                name = title_stuff.get_text()
		rating = float(money_re.sub('', info.find('div', {'class':'rating-large'}).find('i')['title']))/10.0
		num_reviews, reviews = get_all_reviews(base_url + url)
		restaurants.append({'name':name, 'address':address, 'url':url, 'rating':rating, 'num_reviews':num_reviews, 'phone':phone, 'reviews':reviews})
		ctr += 1
		print name, ctr
	return restaurants

def write_data(restaurants, file_prefix, file_ctr):
    filename = '../data/yelp_' + file_prefix + '_' + str(file_ctr) + '.json'
    with open(filename, 'w') as f:
        f.write(json.dumps(restaurants))
    print 'saved ' + filename
    
def get_restaurants(location_code, size):
    location = 'Washington,+DC,+USA' if location_code == 'dc' else 'Nashville,+TN,+USA'
    offset = 0
    # done up to dc_9, start at 10, need to go back for dc_0, nsh_0-9
    saved = 500
    file_ctr = 10
    restaurants = []
    while offset + saved < size:
        html = get_search_page(offset+saved, location)
        restaurants += parse_search_page(html, offset, saved)
        offset = len(restaurants)
        if offset % 50 == 0:
            write_data(restaurants, location_code, file_ctr)
            saved += len(restaurants)
            restaurants = []
            file_ctr += 1
            offset = 0

get_restaurants('dc', 1000)
get_restaurants('nsh', 1000)
