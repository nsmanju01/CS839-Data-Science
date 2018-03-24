Python modules used: Beautiful Soup(bs4), pandas

data_science_stage2_imdb.py: code written to loop through list page of imdb.com for movies rankings i.e 'best movies of all time'.
Each list web page contains 50 movies, so iterated over 60 web pages to scrape 3000+ movie data.

data_science_stage2_metacritic.py: code written to iterate over movie listing 'best movies of all time' ranking. Each web page provided just limited info for 100 movies per page. So first made list of all movie urls and then iterated over each movie specific web page to scrape the required data.

Data generated for schema: [name,release_year,certificate,runtime,genre,director,gross,actors,production_house]