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
		

		# # Release Year
		# year = container.h3.find('span', class_ = 'lister-item-year').text
		# years.append(int(year[-5:-1]))

		# # Movie Genre
		# genre = container.p.find('span', class_ = 'genre') \
		# 	.text.strip('\n').strip()
		# genres.append(genre.split(', '))

		# # IMDB Rating
		# rating = container.strong.text
		# imdbRatings.append(float(rating))

		# # IMDB Poster
		# poster = container.a.img.find('span', class_= 'lister-item-image float-left')
		# imdbPoster.append(poster)

# NEED TO USE THE LOOP THAT SCRAPES THE TOP 250 PAGE TO SCRAPE THE DIRECT IMDB PAGE OF EACH MOVIE AND 
# GRAB THE URL (IMG / SRC) OF THE POSTER.		
	
	posterContainers = imdbSoup.find_all('td', \
		class_ = 'posterColumn',)
	
	for container in posterContainers:

		# IMDB Poster
		poster = container.find('img')
		imdbPoster.append(poster['src'])

print()

# Create DataFrame of Movie Data
movieRatings = pd.DataFrame({
'Movie': movieNames,
# 'Year': years,
# 'Genre': genres,
# 'IMDB Rating': imdbRatings,
'Poster': imdbPoster,
})

# Export data to .csv
movieRatings.to_csv('movieRatings.csv', encoding = 'utf-8', index = True)
print("Data Exported to movieRatings.csv")
