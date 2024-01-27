import os
import pandas as pd
from tqdm import tqdm

current_path = os.getcwd()
current_path = current_path.split('movie-pre-buzz-to-box-office')
path = current_path[0] + 'movie-pre-buzz-to-box-office'

videoIds = pd.read_csv(path + "/Data/Trailer Ids/youtube trailer Ids.csv")

def videoDetails(videoId, apiKey):
    import googleapiclient.discovery
    import googleapiclient.errors

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    credentials = apiKey
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=credentials)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics", 
        id=videoId
    )
    response = request.execute()

    return response

videoIds = list(videoIds['Video Id'])
key = input("Enter the API Key:")
for i in tqdm(range(len(videoIds))):
    data = []
    row=[]
    row.append(videoIds[i])
    response = videoDetails(videoIds[i], apiKey=key)

    try: 
        row.append(response['etag']) 
    except (IndexError, KeyError) as error: 
        row.append(None)
    
    try:
        row.append(response['items'][0]['snippet']['publishedAt']) 
    except (IndexError, KeyError) as error:
        row.append(None)
    
    try:
        row.append(response['items'][0]['snippet']['title']) 
    except (IndexError, KeyError) as error:
        row.append(None)
    
    try:
        row.append(response['items'][0]['snippet']['description']) 
    except (IndexError, KeyError) as error:
        row.append(None)
    
    try:
        row.append(response['items'][0]['snippet']['channelTitle']) 
    except (IndexError, KeyError) as error:
        row.append(None)
    
    try:
        row.append(response['items'][0]['snippet']['categoryId']) 
    except (IndexError, KeyError) as error:
        row.append(None)

    try:
        row.append(response['items'][0]['snippet']['defaultAudioLanguage'])
    except (IndexError, KeyError) as error:
        row.append(None)
    
    try:
        row.append(response['items'][0]['contentDetails']['duration']) 
    except (IndexError, KeyError) as error:
        row.append(None)
    
    try:
        row.append(response['items'][0]['contentDetails']['definition']) 
    except (IndexError, KeyError) as error:
        row.append(None)
    
    try:
        row.append(response['items'][0]['contentDetails']['caption']) 
    except (IndexError, KeyError) as error:
        row.append(None)
    
    try:
        row.append(response['items'][0]['contentDetails']['licensedContent']) 
    except (IndexError, KeyError) as error:
        row.append(None)
    
    try:
        row.append(response['items'][0]['statistics']['viewCount']) 
    except (IndexError, KeyError) as error:
        row.append(None)
    
    try:
        row.append(response['items'][0]['statistics']['likeCount']) 
    except (IndexError, KeyError) as error:
        row.append(None)
    
    try:
        row.append(response['items'][0]['statistics']['commentCount'])
    except (IndexError, KeyError) as error:
        row.append(None)
    
    data.append(row)

    cols = ['videoId', 'etag', 'publishedAt', 'title', 'description', 'channelTitle', 'categoryId', \
            'defaultAudioLanguage', 'duration', 'definition', 'caption', 'licensedContent', \
                'viewCount', 'likeCount', 'commentCount'] 
    data = pd.DataFrame(data, columns=cols)
    
    if i==0:
        data.to_csv(path + '/Data/Video Description/videoDescription.csv', index=False, header=True)
    else:
        data.to_csv(path + '/Data/Video Description/videoDescription.csv', mode='a', index=False, header=False)