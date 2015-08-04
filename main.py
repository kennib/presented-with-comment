import ConfigParser

from apiclient.discovery import build

config = ConfigParser.ConfigParser()
config.read('app.cfg')

API_KEY = config.get('youtube', 'api_key', 'REPLACE_ME')
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
FREEBASE_SEARCH_URL = "https://www.googleapis.com/freebase/v1/search?%s"

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
  videos = []

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
        videos.append(playlist_item['snippet'])
        
      next_page_token = playlistitems_response.get('tokenPagination', {}).get(
        'nextPageToken')
      
      if len(videos) > 100:
        break
  
    return videos

# A function to get a video's comments
def get_comments(video_id):
  comments = []
  next_page_token = ''

  while next_page_token is not None:
    comments_response = youtube.commentThreads().list(
      videoId=video_id,
      part='snippet,id',
        maxResults=50,
        pageToken=next_page_token
    ).execute()
    
    for comment_item in comments_response['items']:
      comments.append(comment_item['snippet']['topLevelComment']['snippet'])

    next_page_token = comments_response.get('nextPageToken')

    if len(comments) > 100:
      break

  return comments


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
