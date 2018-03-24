from requests import get
from bs4 import BeautifulSoup as soup
from pprint import pprint
import re
import pandas as pd

'''
Helper Functions
'''

# Function to concatenate multiple names
def concatenate_strings_by_underscore(listOfNames):
	concatenatedString = ""
	for string in listOfNames:
		concatenatedString = concatenatedString +'_'+ string.text.encode('utf-8')

	return concatenatedString

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

	#IMDB web page has 50 movies per page. So iterate 60 times 
	for pageIndex in range(1,62):		
		
		#Page URL formation
		urlBegin = 'https://www.imdb.com/search/title?title_type=feature&languages=en&sort=num_votes,desc&page='
		urlEnd	 = '&ref_=adv_nxt'
		imdbUrl  = urlBegin + str(pageIndex) + urlEnd

		# debug
		# print "index: ", pageIndex
		# print "\n",imdbUrl

		#Obtain webpage response 
		response = get(imdbUrl)

		# debug
		# print(response.text[:500])

		#Get soup object from webpage response
		webpage_soup = soup(response.text, 'html.parser')
		movieContainers = webpage_soup.find_all('div', class_ = 'lister-item mode-advanced')

		#debug
		#print(type(movieContainers))
		#print(len(movieContainers))

		# Extract data from individual movie container
		for container in movieContainers:

			#debug
			# print "========================="
			
			#movie name
			mName = container.h3.a.text
			names.append(mName)
			
			#debug
			# print mName.encode('utf-8')

			#Release Year
			releaseYear = container.h3.find('span', class_ = 'lister-item-year').text
			if releaseYear == None:
				years.append("None")
			else:
				years.append(releaseYear.replace("(I)","").strip('()'))

			#Movie Certificate
			mCertificate = container.find('span', class_ = 'certificate')
			if mCertificate == None:
				certs.append("None")
			else:
				certs.append(mCertificate.text)

			#Movie Run Time
			runtime = container.find('span', class_ = 'runtime').text	
			if runtime == None:
				rts.append("None")
			else:
				rts.append(int(remove_min_from_runtime(runtime)))	

			#Movie Genre
			genre = container.find('span', class_ = 'genre').text
			genres.append(genre.replace(", ","_").strip())
			
			#Movie Directors
			mDirector =  container.find_all('a', {'href': re.compile('adv_li_dr')})		
			
			#In case of multiple Directors
			if len(mDirector) > 1:
				dirs = concatenate_strings_by_underscore(mDirector)
				
				#debug
				# print "dirs ", dirs

				dts.append(dirs)
			else:
				dts.append(mDirector[0].text.encode('utf-8'))
			
			#movie actors
			actor = container.find_all('a', {'href': re.compile('adv_li_st')})			

			#Multiple Actors
			if len(actor) > 1:
				concatActors = concatenate_strings_by_underscore(actor)

				#debug
				#print concatActors

				acts.append(concatActors)
			else:
				acts.append(actor[0].text)
			
			#Movie Box Office Collection
			boxOfficeGross = container.find_all('span', attrs = {'name':'nv'})

			#debug		
			#print "len boxOfficeGross ", len(boxOfficeGross)	

			#Check if Box Office info NOT Present
			if len(boxOfficeGross) <= 1:
				#debug
				#print "GROSS NONE"
				gross.append(int(-1000))
			else:
				#debug
				#print "gross",int(boxOfficeGross[1]['data-value'].replace(',', ''))
				gross.append(int(boxOfficeGross[1]['data-value'].replace(',', '')))  

			#Production House
			phouse.append('NA')


	# debug			
	# print "---------------------------\n"
	# for i in range(len(names)):
	# 	print "------ {} -----\n name: {}  year: {}  cert: {}  runtime: {}  genre: {} director: {}  gross: {} actors: {} phouse: {}".format(\
	# 	i, names[i].encode('utf-8'), years[i], certs[i], rts[i], genres[i], dts[i], gross[i], acts[i], phouse[i])			


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
	df.to_csv('imdb_data_1.csv', encoding='utf-8')