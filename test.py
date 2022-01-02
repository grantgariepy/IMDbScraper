import sys
import time
from random import randint
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


imdbPoster = [] # Movie Poster


# For monitoring request frequency
startTime = time.time()
reqNum = 0

print("Fetching Webpages...")





for i in range(1,50 + 1, 50):

			url = ('https://www.imdb.com/title/tt0111161/')

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


print()

# Create DataFrame of Movie Data
tester = pd.DataFrame({
'Poster': imdbPoster,
})

# Export data to .csv
tester.to_csv('tester.csv', encoding = 'utf-8', index = True)
print("Data Exported to tester.csv")
