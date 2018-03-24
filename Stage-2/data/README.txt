imdb_data: CSV file containing 3000+ movies data from 'https://www.imdb.com'. 
Attributes [name,release_year,certificate,runtime,genre,director,gross,actors,production_house]
NOTE: Production House name not taken from imdb.com, but to match the schema with metacritic.com its added. And 'NA' in the production_house coloumn means 'Not Available'.

metacritic_data: CSV file containing 3000+ movies data from 'http://www.metacritic.com'.
Attributes [name,release_year,certificate,runtime,genre,director,gross,actors,production_house]
NOTE: Box Office collection 'gross' value not taken from metacritic.com, but to match the schema with imdb.com its added. And 'NA' in the gross coloumn means 'Not Available'.
