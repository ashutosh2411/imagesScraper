from __future__ import print_function
from time import sleep 
import wget
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import urllib2
from bs4 import BeautifulSoup

def scraper (browser, username, file):
	browser.get('https://www.instagram.com/'+username)
	container = browser.find_element_by_class_name('_mesn5')
	infos = container.find_elements_by_class_name('_t98z6')
	num_of_posts = int(infos[0].text.split(' ')[0].replace(',', ''))
	prev_divs = browser.find_elements_by_class_name('_70iju')
	i = 0
	if num_of_posts > 12: 
		try: 
			body = browser.find_element_by_tag_name('body')
			button = body.find_element_by_xpath('//a[contains(@class, "_1cr2e _epyes")]')
			body.send_keys(Keys.END)
			sleep(1.5)
			button.click()
			body.send_keys(Keys.HOME)
			sleep(1.5)
			while len(browser.find_elements_by_class_name('_70iju')) > len(prev_divs):
				i = i + 12
				if i % 240 == 0:
					print ('found about '+str(i)+' images so far.')
				prev_divs = browser.find_elements_by_class_name('_70iju')
				body.send_keys(Keys.END)
				sleep(1.7)
				if len(browser.find_elements_by_class_name('_70iju')) <= len(prev_divs):
					sleep (3)
					if len(browser.find_elements_by_class_name('_70iju')) <= len(prev_divs):
						sleep (5)
						if len(browser.find_elements_by_class_name('_70iju')) <= len(prev_divs):
							sleep (5)
							if len(browser.find_elements_by_class_name('_70iju')) <= len(prev_divs):
								sleep (5)
								if len(browser.find_elements_by_class_name('_70iju')) <= len(prev_divs):
									sleep (10)
									if len(browser.find_elements_by_class_name('_70iju')) <= len(prev_divs):
										sleep (10)

				body.send_keys(Keys.HOME)
				sleep(.01)
		except NoSuchElementException as err:
			print ('-Post not found')

	links_elems = [div.find_elements_by_tag_name('a') for div in prev_divs]
	links = sum([[link_elem.get_attribute('href') for link_elem in elems] for elems in links_elems], [])
	driver.quit()
	f = open('temp.txt','w')
	f.write(str(links))
	f.close()
	i=0
	j = 0
	l=len(links)
	print ('Found '+str(l)+' Images. Saving links in '+file )
	f = open(file, 'w')
	for link in links:
		i = i + 1
		if (i==l/10):
			i = 0
			j = j + 1
			print('['+'==='*j+'   '*(12-j)+']')
		try: 
			soup = urllib2.urlopen(link).read()
			for line in soup.splitlines():
				if '<meta property=\"og:image\" content=\"' in line: 
					f.write( line[39:-4]+'\n')
					break;
		except : 
			f.flush()
			print ('-Image src not found for '+link)
	print('[====================================]')
	f.close()

u = raw_input()
f = u + '.txt'
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
#driver = webdriver.Firefox()
scraper (driver, u, f)