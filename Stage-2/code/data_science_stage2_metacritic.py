import requests
from bs4 import BeautifulSoup as soup
from pprint import pprint
import re
import pandas as pd
from time import sleep
from random import randint

#metacritic url
metaHome = 'http://www.metacritic.com/'

#header to access metacritic as a user
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

'''
Helper Functions
'''

# Function to concatenate multiple names
def concatenate_strings_by_underscore(listOfNames):
	concatenatedString = ""
	for string in listOfNames:
		concatenatedString = concatenatedString +'_'+ string.text.encode('utf-8')

	return concatenatedString

#Function to remove 'min' string from the runtime	
def remove_min_from_runtime(runtime):
	rt = runtime.split()

	return rt[0]

'''
MAIN
'''
if __name__ == "__main__":

	'''
	Scrapping IMDB
	'''

	#Initialize attribute lists
	names = []
	years = []
	certs = []
	rts   = []
	genres= []
	ptags = []
	dts   = []
	acts  = []
	gross = []
	phouse= []

	#Metacritic web page has 100 movies per page. So iterate 30 times 
	for pageIndex in range(0,32):

		sleep(randint(1,5))
		#Page URL formation
		urlBegin = 'http://www.metacritic.com/browse/movies/score/metascore/all/filtered?page='		
		metaUrl  = urlBegin + str(pageIndex)

		# debug
		# print "index: ", pageIndex
		# print "\n",metaUrl

		result = requests.get(metaUrl, headers=headers)
		
		#debug
		#print(result.text[:500])

		page_soup = soup(result.text, 'html.parser')

		#Obtain each movie name div section
		movie_containers = page_soup.find_all('div', class_ = 'title')
		
		#list to store individual movie urls
		movie_urls = []

		#Iterate over all movies in the list and get 
		for movie_div_containers in movie_containers:
			ahref = movie_div_containers.find('a', {'href': re.compile('/movie/')})
			movie_urls.append(ahref['href'])


		#Iterate over all movie lists
		#and scrape individual movie web page
		for murl in movie_urls:
			mov_url = metaHome + murl

			#debug
			# print "================"
			# print "mov url ", mov_url
			'''
			PER PAGE SCRAPPING
			'''
			mresult = requests.get(mov_url , headers=headers)
			if mresult.status_code == 404:
				continue
				
			#debug
			#print(mresult.text[:500])
		
			mpage_soup = soup(mresult.text, 'html.parser')  

			#Movie Name
			movie_name_div = mpage_soup.find('div', class_ = 'product_page_title')
			if type(movie_name_div) == 'NoneType':
				continue
			else:
				names.append(movie_name_div.h1.text)

				#debug				
				# print(movie_name_div.h1.text)

			#Movie Release Year
			movie_year_div = mpage_soup.find('span', class_ ='release_year lighter')
			if movie_year_div == None:
				years.append("None")
			else:	
				years.append(movie_year_div.text)
				#debug
				# print(movie_year_div.text)

			#Movie Production House
			movie_distributor_div = mpage_soup.find('span', class_ = 'distributor')
			if movie_distributor_div == None:
				phouse.append("None")
			else:
				phouse.append(movie_distributor_div.a.text)
				#debug
				# print (movie_distributor_div.a.text)

			#Movie Actors
			movie_actor_div = mpage_soup.find('div', class_ = 'summary_cast details_section')
			if movie_actor_div == None:
				acts.append("None")
			else:
				movie_actor_anchor = movie_actor_div.find_all('a', {'href': re.compile('/person/')})
				
				#Concatenate Actor names with '_'
				if len(movie_actor_anchor) > 1:
					actors = concatenate_strings_by_underscore(movie_actor_anchor)				
					#debug
					# print "actors ", actors

					acts.append(actors)
				else:
					acts.append(movie_actor_anchor[0].text.encode('utf-8'))		
					#debug
					# print(movie_actor_anchor)

			#Movie Director
			movie_dir_div = mpage_soup.find('div', class_ = 'director')
			if movie_dir_div == None:
				dts.append("None")
			else:
				movie_dir_anchor = movie_dir_div.find_all('a', {'href': re.compile('/person/')})

				#In case of multiple Directors
				if len(movie_dir_anchor) > 1:
					dirs = concatenate_strings_by_underscore(movie_dir_anchor)					
					#debug
					# print "dirs ", dirs

					dts.append(dirs)
				else:
					dts.append(movie_dir_anchor[0].text.encode('utf-8'))			
					#debug	
					# print(movie_dir_anchor)

			#Movie Runtime
			movie_rt_div = mpage_soup.find('div', class_ = 'runtime')
			if movie_rt_div == None:
				rts.append("None")
			else:			
				movie_rt_span = movie_rt_div.find_all('span')
				rts.append(remove_min_from_runtime(movie_rt_span[1].text))
				#debug
				# print(movie_rt_span[1].text)

			#Movie genres
			movie_genres_div = mpage_soup.find('div', class_ = 'genres')
			if movie_genres_div == None:
				genres.append("None")
			else:
				
				movie_genres_span = movie_genres_div.find_all('span', class_ = None)

				for gen in range(1, len(movie_genres_span)):
					if movie_genres_span[gen].has_attr("class") == False:
						concatenate_genre = ""
						concatenate_genre = concatenate_genre + '_' + movie_genres_span[gen].text.strip('\n')

				genres.append(concatenate_genre)
				#debug
				# print concatenate_genre

			#movie certificate / rating
			movie_cert_div = mpage_soup.find('div', class_ = 'rating')
			if movie_cert_div == None:
				certs.append("None")
			else:				
				movie_certs_span = movie_cert_div.find('span', class_ = None)
				certs.append(movie_certs_span.text.rstrip().replace(' ','').replace('\n',''))
			
			#Movie Box Office Cross
			gross.append('NA')
			#debug
			# print movie_certs_span.text.rstrip().replace(' ','').replace('\n','')

			
	#	debug
	# 	print "---------------------------\n"
	# 	for i in range(len(names)):
	# 		print "------ {} -----\n name: {}  year: {}  cert: {}  runtime: {}  genre: {} director: {}  gross: {} actors: {}".format(\
	# 		i, names[i].encode('utf-8'), years[i], certs[i], rts[i], genres[i], dts[i], gross[i], acts[i])		

	# debug
	# print "------LENGTH-----\n name: {}  year: {}  cert: {}  runtime: {}  genre: {} director: {}  gross: {} actors: {}".format(\
	# 		 len(names), len(years), len(certs), len(rts), len(genres), len(dts), len(gross), len(acts))		
	

	#Raw data for pandas data frame
	rawData = { 'name': names,
				'release_year': years,
				'certificate': certs,
				'runtime': rts,
				'genre': genres,
				'director': dts,
				'gross': gross,
				'actors': acts,
				'production_house': phouse
			}

	df = pd.DataFrame(rawData, columns = ['name', 'release_year', 'certificate', 'runtime', 'genre', 'director', 'gross', 'actors', 'production_house'])
	df.to_csv('metacriticDataFinal3049.csv', encoding='utf-8')	

		





	
