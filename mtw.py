import json
from movie import Movie
import webbrowser
import os
import re
import random

page_head = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Movie Trailer Website</title>

    <!-- Bootstrap core CSS -->
    <!-- LOCAL RUNNING VERSION
    <link href="../../../../Dev/node_modules/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
    -->

    <!-- INTERNET CONNECTED VERSION -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    

    <!-- Custom styles for this template -->
    <link href="mtw.css" rel="stylesheet">
  </head>
'''

page_main_content = '''
<body>
    <!-- About Modal HTML -->
    <div id="aboutModal" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title">About</h4>
                </div>
                <div class="modal-body">
                    <p>This Movie Trailer Website was created by <strong>David Rowland</strong> for the Udacity Full Stack Web Developer Nanodegree.</p>
                    <p>Project 1 - submitted May 2015</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div> <!--/modal about-->

    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div> <!--/modal trailer -->

    <!-- Navigation Bar -->
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#"><span class="glyphicon glyphicon-facetime-video" aria-hidden="true" style="padding-right: 10px"></span>Movie Trailer Website</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="#">Home</a></li>
            <li><a href="#aboutModal" data-toggle="modal">About</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container starter-template">
      <h1>Your go to site for movie trailers</h1>
      <p class="lead">Welcome to the Movie Trailer Website, the fastest growing<br/>repository of movies trailers freely available for your viewing pleasure.</p>

      <div class="row">
        <div class="col-xs-6">
          <p class="center-block"><h4><span class="label label-success">NOW TRENDING</span></h4></p> 
          <!-- Carousel control -->
          <div id="popular-movies-carousel" class="carousel slide center-block" data-ride="carousel">
            <ol class="carousel-indicators">
              <li data-target="#popular-movies-carousel" data-slide-to="0" class="active"></li>
              <li data-target="#popular-movies-carousel" data-slide-to="1" class=""></li>
              <li data-target="#popular-movies-carousel" data-slide-to="2" class=""></li>
            </ol>
            <div class="carousel-inner" role="listbox">
              {carousel_content}
            </div>
            <a class="left carousel-control" href="#popular-movies-carousel" role="button" data-slide="prev">
              <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
              <span class="sr-only">Previous</span>
            </a>
            <a class="right carousel-control" href="#popular-movies-carousel" role="button" data-slide="next">
              <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
              <span class="sr-only">Next</span>
            </a>
          </div>
        </div>
        <div class="col-xs-6">
          <p class="center-block"><h4><span class="label label-primary">RECENTLY ADDED</span></h4></p> 
          <div class="panel panel-primary recently-added center-block">
            <div class="panel-body">
              {recently_added_content}
            </div>
          </div>
        </div>
      </div>
    </div><!-- /.container -->

    <div class="container starter-template main-movie-collection">
      {movie_tiles}
    </div>

    <div class="container starter-template">
      <nav>
        <ul class="pager">
          <li class="disabled"><a href="#">Previous</a></li>
          <li><a href="#">Next</a></li>
        </ul>
      </nav>
    </div>
'''

page_foot = '''
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <!-- LOCAL RUNNING VERSIONS 
    <script src="../../../..//Dev/jQuery/jquery-2.1.4.js"></script>
    <script src="../../../../Dev/node_modules/bootstrap/dist/js/bootstrap.min.js"></script>
    -->

    <!-- INTERNET CONNECTED VERSION -->
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>

    <script type="text/javascript">
      // Pause the video when the modal is closed
      $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
         $("#trailer-video-container").empty();
      });

      // Start playing the video whenever the trailer modal is opened
      $(document).on('click', '.movie-tile, .carousel_tile', function (event) {
          var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
          var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
          $("#trailer-video-container").empty().append($("<iframe></iframe>", {
            'id': 'trailer-video',
            'type': 'text-html',
            'src': sourceUrl,
            'frameborder': 0
          }));
      });

      // Animate in the movies when the page loads
      $(document).ready(function () {
        $('.movie-tile').hide().first().show("fast", function showNext() {
          $(this).next("div").show("fast", showNext);
        });
      });

      // Need to add a function so that when the About model is closed, focus doesn't remain
      // on the About button in the nav bar
      $('#aboutModal').on('hidden.bs.modal', function () {
        window.focus();
      });
    </script>
  </body>
</html>
'''

# a single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-3 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="165" height="256">
    <p><h6>{movie_title} <span class="label label-info">{rating}</span></h6></p>
</div>
'''

# single carousel html template
movie_carousel_content = '''
<div class="{item_active} carousel_tile carousel-image" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
  <img alt="{movie_title}" src="{poster_image_url}" class="img-responsive center-block carousel-image">
  <div class="carousel-caption">
      <h3>{movie_title}</h3>
      <p>{release_year}</p>
  </div>
</div>
'''

recently_added_content = '''
<p><h5>{movie_title} <span class="label label-primary">{release_year}</span></h5></p>
'''

def create_movie_showcase_content(movies):
  # loop through the movies collection and randomly pick a maximum of 3 movies for carousel
  # assumes at least 3 movies in collection
  content = ''
  first_time = True
  random_sample = random.sample(movies,3)
  for movie in random_sample:
    if first_time:
      set_class = "item active"
      first_time = False
    else:
      set_class = "item"

    content += movie_carousel_content.format(
      item_active=set_class,
      movie_title=movie.title,
      poster_image_url=movie.poster_image_url,
      trailer_youtube_id=get_youtube_url(movie),
      release_year=movie.release_year
    )
  return content

def create_movie_recent_content(movies):
  # loop through the movies collection and randomly pick a maximum of 3 movies for recently added
  # assumes at least 3 movies in collection
  content = ''
  random_sample = random.sample(movies,3)
  for movie in random_sample:
    content += recently_added_content.format(
      movie_title=movie.title,
      release_year=movie.release_year
    )
  return content

def create_movie_tiles_content(movies):
  # The HTML content for this section of the page
  content = ''
  for movie in movies:
      # Append the tile for the movie with its content filled in
      content += movie_tile_content.format(
          movie_title=movie.title,
          poster_image_url=movie.poster_image_url,
          trailer_youtube_id=get_youtube_url(movie),
          rating=movie.rating
      )
  return content

def get_youtube_url(movie):
  # Extract the youtube ID from the url
  youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
  youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
  trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None
  return trailer_youtube_id

def open_movies_page(movies):
  # Create or overwrite the output file
  output_file = open('mtw.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = page_main_content.format(
    movie_tiles=create_movie_tiles_content(movies),
    carousel_content=create_movie_showcase_content(movies),
    recently_added_content=create_movie_recent_content(movies)
  )

  # Output the file
  output_file.write(page_head + rendered_content + page_foot)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible

def json_to_movie(d):
  args = dict((key.encode('ascii'), value) for key, value in d.items())
  return Movie(**args)

if __name__ == "__main__":
  with open('movies.json') as movie_file:
    movie_list = json.load(movie_file, object_hook=json_to_movie)

  open_movies_page(movie_list)
