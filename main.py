import sqlite3
from datetime import datetime

import youtube
import reddit

from pprint import pprint

# This function creates database tables
def create_tables(conn):
  conn.execute("""PRAGMA foreign_keys = 1""")

  conn.execute("""
  CREATE TABLE IF NOT EXISTS video
  (id TEXT PRIMARY KEY,
   channel TEXT,
   date TEXT, title TEXT, url TEXT)
  """)

  conn.execute("""
  CREATE TABLE IF NOT EXISTS comment
  (id TEXT, site TEXT, video TEXT,
   date TEXT, author TEXT,
   comment TEXT, url TEXT,
   up_votes INTEGER, down_votes INTEGER,
   PRIMARY KEY (id, site))
  """)

# This function stores a single comment
def store_comment(comment):
  try:
    conn.execute("""INSERT INTO comment
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (comment['id'], comment['site'], comment['video'],
          comment['date'], comment['author'], comment['comment'],
          comment['url'], comment['up_votes'], comment['down_votes']))
  except sqlite3.IntegrityError, e:
    pass

# This function fetches all types of comments
# and stores them in the database
def fetch_store_comments(conn):
  for channel in youtube.channels:
    for video in youtube.get_videos(channel):
      # Video data
      video_id = video['resourceId']['videoId']
      video_url = youtube.video_url(video_id)
      video = {
        'id': video_id,
        'channel': video['channelTitle'],
        'date': video['publishedAt'],
        'title': video['title'],
        'url': video_url,
      }

      try:
        conn.execute("""INSERT INTO video
        VALUES (?, ?, ?, ?, ?)
        """, (video['id'], video['channel'], video['date'],
              video['title'], video['url']))
      except sqlite3.IntegrityError, e:
        pass

      # Youtube comment data
      for comment in youtube.get_comments(video_id):
        comment = {
          'id': comment['id'],
          'site': 'youtube',
          'video': video_id,
          'date': comment['updatedAt'],
          'author': comment['authorDisplayName'],
          'comment': comment['textDisplay'],
          'url': comment['authorGoogleplusProfileUrl'],
          'up_votes': comment['likeCount'],
          'down_votes': 0,
        }
        store_comment(comment)

      # Reddit comment data
      for thread in reddit.get_threads(video_url):
        for comment in reddit.get_comments(thread['id']):
          date = datetime.utcfromtimestamp(comment['created_utc']).isoformat() if 'created_utc' in comment else None
          if 'body' in comment:
            comment = {
              'id': comment['id'],
              'site': 'reddit',
              'video': video_id,
              'date': date,
              'author': comment['author'],
              'comment': comment['body'],
              'url': 'https://reddit.com/r/{}/comments/{}/{}/{}'.format(comment['subreddit'], thread['id'], comment['author'], comment['id']),
              'up_votes': comment['ups'],
              'down_votes': comment['downs'],
            }
            store_comment(comment)

    conn.commit()
  conn.close()

if __name__ == '__main__':
  conn = sqlite3.connect('comments.db')
  create_tables(conn)
  fetch_store_comments(conn)
