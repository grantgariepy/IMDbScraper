import sys
import time
from random import randint
from numpy import array
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

df = pd.DataFrame(columns = ['Name', 'Poster', 'Link'])

movieName = '' # Movie Names
moviePoster = '' # Movie Poster
movieLink = '' # URL for movie page

# years = [] # Release Years

# For monitoring request frequency
startTime = time.time()
reqNum = 0

print("Fetching Webpages...")

for i in range(1, 20):
	url = ('https://www.imdb.com/chart/top/')

	# Make a get request
	try:
		response = requests.get(url, headers = {"Accept-Language": "en-US, \
			en;q=0.5"})
		response.raise_for_status()
	# Throw warning in case of errors
	except requests.exceptions.RequestException as excep:
		print(f'\nThere was a problem:\n{excep}')
		sys.exit()

	# Pause the loop
	time.sleep(randint(1,4))

	# Monitor the request frequency
	reqNum += 0
	elapsedTime = time.time() - startTime
	print(f"Requesting...")

	# Parse the HTML Contents
	imdbSoup = bs(response.text, 'lxml')
	movieContainers = imdbSoup.find_all('td', \
		class_ = 'titleColumn',)

	for container in movieContainers:

		# Movie Name
		name = container.a.text
		movieName = name
		
		#IMDB Link
		link = container.a
		movieLink = link['href']
		
		url = ('https://www.imdb.com' + link['href'])
		
		try:
			response = requests.get(url, headers = {"Accept-Language": "en-US, \
				en;q=0.5"})
			response.raise_for_status()

		# Throw warning in case of errors
		except requests.exceptions.RequestException as excep:
			print(f'\nThere was a problem:\n{excep}')
			sys.exit()

		# Pause the loop
		time.sleep(randint(1,4))

		# Parse the HTML Contents
		imdbSoup = bs(response.text, 'lxml')
		linkContainers = imdbSoup.find_all('div', \
			class_ = 'ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img',)

		for containerTwo in linkContainers:
			# Poster
			poster = containerTwo.img
			moviePoster = poster['src']
			print(moviePoster)
			print(movieName)

		df2 = pd.DataFrame([[movieName, moviePoster, movieLink]], columns=['Name', 'Poster', 'Link'])
		df = df.append(df2, ignore_index=True)
		df.to_json('movieRatings.json')
		print(df)


		# # Release Year
		# year = container.h3.find('span', class_ = 'lister-item-year').text
		# years.append(int(year[-5:-1]))

print()





