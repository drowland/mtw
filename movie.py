import json
from video import Video

class Movie(Video):
	"""Specific implemention of a Movie based on parent class Video"""
	def __init__(self, title, story_line, poster_image_url,
				 trailer_youtube_url, rating, duration, release_year):

		# Call base class init with appropriate init variables
		Video.__init__(self, title, story_line, poster_image_url, trailer_youtube_url)
		
		self.rating = rating
		self.duration = duration
		self.release_year = release_year

	def show_info(self):
		print("Title: "+self.title)
		print("Storyline: "+self.storyline)