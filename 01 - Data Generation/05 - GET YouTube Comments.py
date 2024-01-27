import os
import pandas as pd
from tqdm import tqdm

current_path = os.getcwd()
current_path = current_path.split('movie-pre-buzz-to-box-office')
path = current_path[0] + 'movie-pre-buzz-to-box-office'

def get_comments(videoId, pageToken=False):
    import os
    import googleapiclient.discovery
    import json

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = ""

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    if pageToken == False:
        request = youtube.commentThreads().list(
            part="id,snippet,replies",
            maxResults=100,
            order="time",
            textFormat="html",
            videoId=videoId
        )
    else:
        request = youtube.commentThreads().list(
            part="id,snippet,replies",
            maxResults=100,
            order="time",
            videoId=videoId,
            textFormat="html",
            pageToken=pageToken
        )
    
    try:
        response = request.execute()
        code = 200
    except Exception as error:
        code = error.status_code
        response = error.content.decode("utf-8").replace("\n  ","")
        response = json.loads(response)
    return response, code

def remove_tags(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
 
    for data in soup(['style', 'script']):
        data.decompose()
    
    text = ' '.join(soup.stripped_strings)
    text = text.split("\n")
    text = ' '.join(text) 
    text = text.strip()
    text = text.replace("|", "")
    
    return text
 
videoIds = pd.read_csv(path + "/Data/Trailer Ids/youtube trailer Ids.csv")

videoIds = list(videoIds['Video Id'])[203:]
for videoId in (pbar:= tqdm(videoIds)):
    pbar.set_description(f"Fetching comments from {videoId}")
    response, code = get_comments(videoId=videoId)
    if code != 200:
        data = []
        error_reason = response['error']['errors'][0]['reason']
        data.append([videoId, code, error_reason, None, None, None, None])

        cols = ['videoId', 'code', 'error_reason', 'id', 'replies', 'comment', 'publishedAt']
        data = pd.DataFrame(data, columns=cols)
        data.to_csv(path+'/Data/Comments/Video Comments.csv', index=False, header=False, mode='a', sep='|')
    else:
        start = True
        while start:
            try:
                pageToken = response['nextPageToken']
                for item in response['items']:
                    data = []
                    id = item['id']
                    replies = item['snippet']['totalReplyCount']
                    
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    # comment = remove_tags(comment)
                    try:
                        for reply in item['replies']['comments']:
                            reply = reply['snippet']['textDisplay']
                            # reply = remove_tags(reply)
                            comment = comment + ' ' + reply
                    except KeyError:
                        comment = comment
                    
                    comment = remove_tags(comment)
                    
                    publishedAt = item['snippet']['topLevelComment']['snippet']['publishedAt']
                    
                    data.append([videoId, code, None, id, replies, comment, publishedAt])

                    cols = ['videoId', 'code', 'error_reason', 'id', 'replies', 'comment', 'publishedAt']
                    data = pd.DataFrame(data, columns=cols)
                    data.to_csv(path+'/Data/Comments/Video Comments.csv', index=False, header=False, mode='a', sep='|')
            except KeyError:
                start = False
                for item in response['items']:
                    data = []
                    id = item['id']
                    replies = item['snippet']['totalReplyCount']
                    
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    # comment = remove_tags(comment)
                    try:
                        for reply in item['replies']['comments']:
                            reply = reply['snippet']['textDisplay']
                            # reply = remove_tags(reply)
                            comment = comment + ' ' + reply
                    except KeyError:
                        comment = comment
                    
                    comment = remove_tags(comment)
                    
                    publishedAt = item['snippet']['topLevelComment']['snippet']['publishedAt']
                    
                    data.append([videoId, code, None, id, replies, comment, publishedAt])

                    cols = ['videoId', 'code', 'error_reason', 'id', 'replies', 'comment', 'publishedAt']
                    data = pd.DataFrame(data, columns=cols)
                    data.to_csv(path+'/Data/Comments/Video Comments.csv', index=False, header=False, mode='a', sep='|')
            
            response, code = get_comments(videoId=videoId, pageToken=pageToken)

comments = pd.read_csv(path+'/Data/Comments/Video Comments.csv', sep='|', lineterminator='\n')