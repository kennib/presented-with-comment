import ConfigParser

from apiclient.discovery import build

config = ConfigParser.ConfigParser()
config.read('app.cfg')

channels = config.get('youtube', 'channels', '').split(',')

API_KEY = config.get('youtube', 'api_key', 'REPLACE_ME')
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
FREEBASE_SEARCH_URL = "https://www.googleapis.com/freebase/v1/search?%s"
WATCH_URL = "https://www.youtube.com/watch?v="

# Service for calling the YouTube API
youtube = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=API_KEY)

# A function to get a channel's videos
def get_videos(channel):
  channels_response = youtube.channels().list(
    forUsername=channel,
    part='snippet,contentDetails'
  ).execute()

  channel_name = ''

  for channel in channels_response['items']:
    uploads_list_id = channel['contentDetails']['relatedPlaylists']['uploads']
    channel_name = channel['snippet']['title']
    
    next_page_token = ''
    while next_page_token is not None:
      playlistitems_response = youtube.playlistItems().list(
        playlistId=uploads_list_id,
        part='snippet',
        maxResults=50,
        pageToken=next_page_token
      ).execute()

      for playlist_item in playlistitems_response['items']:
        yield playlist_item['snippet']
        
      next_page_token = playlistitems_response.get('tokenPagination', {}).get(
        'nextPageToken')
      
      

# A function to get a video's comments
def get_comments(video_id):
  next_page_token = ''

  while next_page_token is not None:
    comments_response = youtube.commentThreads().list(
      videoId=video_id,
      part='snippet,id',
        maxResults=50,
        pageToken=next_page_token
    ).execute()
    
    for comment_item in comments_response['items']:
      comment_raw = comment_item['snippet']['topLevelComment']
      comment = comment_raw['snippet']
      comment['id'] = comment_raw['id']
      yield comment

    next_page_token = comments_response.get('nextPageToken')

def video_url(video_id):
  return WATCH_URL+video_id


if __name__ == '__main__':
  channels = config.get('youtube', 'channels', '').split(',')
  for channel in channels:
    print channel
    videos = get_videos(channel)
    for video in videos:
      id = video['resourceId']['videoId']
      print video['title'], id
      comments = get_comments(id)
      for comment in comments:
        print comment['authorDisplayName'], '--', comment['textDisplay']
      print
    print
