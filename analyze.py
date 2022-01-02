import sys
import time
from random import randint
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

movieNames = [] # Movie Names
# years = [] # Release Years
# genres = [] # Movie Genres
# imdbRatings = [] # IMDB Ratings
imdbPoster = [] # Movie Poster
imdbLink = [] # URL for movie page

# For monitoring request frequency
startTime = time.time()
reqNum = 0

print("Fetching Webpages...")

for i in range(1, 50 + 1, 50):
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
		movieNames.append(name)
		print(name)

		#IMDB Link
		link = container.a
		imdbLink.append(link['href'])

		for i in range(1):

			url = ('https://www.imdb.com' + link['href'])
			print(url)

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
			linkContainers = imdbSoup.find_all('div', \
				class_ = 'ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img',)

			for container in linkContainers:
				# Poster
				poster = container.img
				imdbPoster.append(poster['src'])
				print(imdbPoster)	

		# # Release Year
		# year = container.h3.find('span', class_ = 'lister-item-year').text
		# years.append(int(year[-5:-1]))

		

print()

# Create DataFrame of Movie Data
movieRatings = pd.DataFrame({
'Movie': movieNames,
# 'Year': years,
# 'Genre': genres,
# 'IMDB Rating': imdbRatings,
# 'Poster': imdbPoster,
'Link': imdbLink,
})

# Export data to .csv
movieRatings.to_csv('movieRatings.csv', encoding = 'utf-8', index = True)
print("Data Exported to movieRatings.csv")
