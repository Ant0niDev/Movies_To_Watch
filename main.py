from dotenv import load_dotenv
from ui import PosterCanvas
from best_100_imdb_movies import imdb_top_100
from movie_recommend import MovieRecommendation

load_dotenv()

#UI SETUP
# ui_setup = PosterCanvas()
movie_of_the_week = MovieRecommendation(imdb_top_100)
