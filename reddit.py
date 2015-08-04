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

# A function that returns all of the threads for a given url
def get_threads(url):
  headers = {'User-Agent': '{} by /u/{}'.format(app_name, username)
            ,'Method': 'GET'}
  params = {'url': url}
  data = urllib.urlencode(params)
  request = urllib2.Request(THREADS_URL+'?'+data, headers=headers)

  try:
    response = urllib2.urlopen(request)
    result = json.load(response)
    return [item['data'] for item in result['data']['children']]
  except urllib2.HTTPError, e:
    return []

if __name__ == '__main__':
  for channel in youtube.channels:
    for video in youtube.get_videos(channel):
      id = video['resourceId']['videoId']
      print video['title'], youtube.video_url(id)
      for thread in get_threads(youtube.video_url(id)):
        print thread['id']
