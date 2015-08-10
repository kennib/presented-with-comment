# Presented with comment

The code above is a series of scripts for downloading Youtube and Reddit comments for Youtube videos.
It was inspired by the Achievement Hunter series [Presented with comment](http://achievementhunter.com/episode/achievement-hunter-season-2-presented-with-comment-1-week-of-july-26-th).

To use this code:

  0. Clone the code `git clone https://github.com/kennib/presented-with-comment`
  1. Go to the directory with the code in it `cd presented with comment`
  1. Get a [Youtube API key](https://developers.google.com/youtube/v3/getting-started)
  2. Paste the API key into [app.cfg](app.cfg)
  3. Add your reddit username into [app.cfg](app.cfg)
  4. Add the names of the Youtube channels you're interested in to [app.cfg](app.cfg) e.g. `channels = letsplay,achievementhunter`
  5. Install the libraries that the code uses `pip install -r requirements.txt`
  6. Run the script `python main.py`
  7. The comments are in the `comments.db` database now and can be queried `sqlite3 comments.db`
  8. You can retrieve the past week's comments from the database with `sqlite3 < list_comments.sql comments.db > comments.csv`
