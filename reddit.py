import ConfigParser

import urllib
import urllib2
import json

import youtube

config = ConfigParser.ConfigParser()
config.read('app.cfg')

app_name = config.get('app', 'name', '')
username = config.get('reddit', 'username', '')

THREADS_URL = "https://api.reddit.com/submit"
COMMENTS_URL = "https://api.reddit.com/comments/{}"

headers = {'User-Agent': '{} by /u/{}'.format(app_name, username)
          ,'Method': 'GET'}

# A function that returns all of the threads for a given url
def get_threads(url):
  params = {'url': url}
  data = urllib.urlencode(params)
  request = urllib2.Request(THREADS_URL+'?'+data, headers=headers)

  try:
    response = urllib2.urlopen(request)
    result = json.load(response)
    return [item['data'] for item in result['data']['children']]
  except urllib2.HTTPError, e:
    return []

# A function that gets all comments in a thread
def get_comments(thread_id):
  url = COMMENTS_URL.format(thread_id)
  request = urllib2.Request(url, headers=headers)

  try:
    response = urllib2.urlopen(request)
    result = json.load(response)
    return [item['data'] for item in walk_comment_tree(result[1])]
  except urllib2.HTTPError, e:
    return []

# A function to return a top-bottom list of comments in the comment tree
def walk_comment_tree(comment_tree):
  for child in comment_tree['data'].get('children', []):
    yield child
    if child.get('replies'):
      yield walk_comment_tree(child['replies'])

if __name__ == '__main__':
  for channel in youtube.channels:
    print channel
    for video in youtube.get_videos(channel):
      id = video['resourceId']['videoId']
      print video['title'], youtube.video_url(id)
      for thread in get_threads(youtube.video_url(id)):
        for comment in get_comments(thread['id']):
          print comment['author'], '--', comment['body']
      print
  print
