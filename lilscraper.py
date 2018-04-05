# import libraries
import urllib2
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import numpy as np
import pandas as pd
from lxml import etree
from urllib2 import Request, urlopen, URLError, HTTPError
import io

#https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
#https://medium.com/@kasiarachuta/importing-and-exporting-csv-files-in-python-7fa6e4d9f408
#https://stackoverflow.com/questions/11465555/can-we-use-xpath-with-beautifulsoup

#quote_page = ['http://www.bloomberg.com/quote/SPX:IND', 'http://www.bloomberg.com/quote/CCMP:IND']

scrape_pages = 'csv_of_urls.csv'

dframe = pd.read_table(scrape_pages, sep=',')

# for loop
data = []
for pg in dframe[0:10]:

	url =  pg

	try:
		response = urlopen(url)
	except HTTPError as e:
		print 'The server couldn\'t fulfill the request.'
		print 'Error code: ', e.code
		name = 'Error code: ', e.code
		event = 'Error code: ', e.code
		badges = 'Error code: ', e.code
	except URLError as e:
		print 'We failed to reach a server.'
		print 'Reason: ', e.reason
		name = 'Reason: ', e.reason
		event = 'Reason: ', e.reason
		badges = 'Reason: ', e.reason
	else:
    	# everything is fine
		print 'scrape that bitch'


		response = urllib2.urlopen(url)
		htmlparser = etree.HTMLParser()
		tree = etree.parse(response, htmlparser)
		

		
		# query the website and return the html to the variable 'page'
		page = urllib2.urlopen(pg)
		# parse the html using beautiful soap and store in variable `soup`
		soup = BeautifulSoup(page, 'html.parser')


		# Take out the <div> of name and get its value
		name_box = soup.find('h1', {'class', 'event-name'})
		name_name = pg.replace("https://schedule.example.com/2018/events/","")
		name = name_box.encode('utf-8').strip() # strip() is used to remove starting and trailing


		name_file = str(name_name)
		print name_name
		
		# get the date and time
		event_date = soup.find('div', {'class', 'event-date'})
		event_date = str(event_date)
		
		#primary badge
		badge_items = tree.xpath('''//div[@class='row description']/div[@class='large-4 small-12 columns']/div[1]/text()''')
		badges = badge_items
		#secondary badge
		badge_items_secondary = tree.xpath('''//div[@class='row description']/div[@class='large-4 small-12 columns']/div[2]/text()''')
		badges_secondary = badge_items_secondary


		#venue
		#venue address
		#tags
		#speakers = soup.find('div', {'class', 'speaker-listing'})

		speakers_list = soup.find('div', {'class', 'speaker-listing'})

		if speakers_list:
			speakers = speakers_list.findAll('h4')
			speaker_all = str(speakers)
			
			#xpath
			speakers_xpath = tree.xpath('''//div[@class='speaker-listing']/h4/a''')

		else:
			speaker_all = "no speakers listed"
			#print "no speakers listed"
		
		
		# from BeautifulSoup import BeautifulSoup as bs
		# soup = bs(html)
		# div = soup.find("div",{"id":"fbbuzzresult"})
		# post_buzz = div.findAll("div",{"class":"postbuzz"})




		#description



		
		#todo Generate uniqure file names
		file = open("example_pages/" + "%s" % name_file + ".html" , 'w') 
		file.write(str(soup))


	# save the data in tuple
	data.append((name, event_date, badges, badges_secondary, speaker_all))

	# open a csv file with append, so old data will not be erased
	with open('example_dump.csv', 'a') as csv_file:
		writer = csv.writer(csv_file)
		# The for loop
		for name, event_date, badges, badges_secondary, speaker_all in data:
			writer.writerow([name, event_date, badges, badges_secondary, speaker_all])




