import webbrowser

class Video():
	"""High level class definition defining a video"""

	def __init__(self, title, story_line, poster_image_url, trailer_youtube_url):
		self.title = title
		self.storyline = story_line
		self.poster_image_url = poster_image_url
		self.trailer_youtube_url = trailer_youtube_url

	def show_trailer(self):
		webbrowser.open(self.trailer_url)