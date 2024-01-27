import os
import pandas as pd
import time
from tqdm import tqdm
from datetime import datetime
import json

current_path = os.getcwd()
current_path = current_path.split('movie-pre-buzz-to-box-office')
path = current_path[0] + 'movie-pre-buzz-to-box-office'


def get_accessToken(account_id):
    import urllib.request, json

    try:
        url = "https://api.videoindexer.ai/Auth/trial/Accounts/"+ account_id +"/AccessToken?allowEdit=true"

        hdr ={
        'Ocp-Apim-Subscription-Key': 'c26d838400a54208963e98d0064342fa',
        }

        req = urllib.request.Request(url, headers=hdr)

        req.get_method = lambda: 'GET'
        response = urllib.request.urlopen(req)
        code = response.getcode()
        response = response.read()
        accessToken = json.loads(response)
        return accessToken, code
    except Exception as error:
        code = error.getcode()
        error = error.read()
        error = json.loads(error)
        return error, code
    

def VideoIndex(account_id, videoid, accessToken, language='en-US', retranslate='false', includeStreamingUrls='true', includeSummarizedInsights='true'):
    import urllib.request, json

    try:
        base = "https://api.videoindexer.ai/trial/Accounts/"
        get_url = base + account_id + "/Videos/" + videoid + "/Index?language=" + language + "&reTranslate=" + retranslate + "&includeStreamingUrls=" + includeStreamingUrls + "&includeSummarizedInsights=" + includeSummarizedInsights + "&accessToken=" + accessToken

        hdr ={
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': 'c26d838400a54208963e98d0064342fa',
        }

        req = urllib.request.Request(get_url, headers=hdr)

        req.get_method = lambda: 'GET'
        response = urllib.request.urlopen(req)
        code = response.getcode()
        response = response.read()
        response = json.loads(response)
        return response, code, get_url, accessToken
    except Exception as error:
        code = error.getcode()
        error = error.read()
        error = json.loads(error)
        return error, code, get_url, accessToken
    

uploads = pd.read_csv(path+'/Data/Upload Data/uploadData.csv', sep='|').sort_values("CreatedTime", ascending=False)
uploads = uploads.loc[uploads['ResponseCode'] == 200]
uploads = uploads.drop_duplicates(['VideoId'], keep='first')
videoIds = {}
for videoId, fileId in zip(uploads['VideoId'], uploads['Id']):
    videoIds[fileId] = videoId
fileIds = list(uploads['Id'])

recieved = pd.read_csv(path+'/Data/Video Indexes/Raw Data.csv', sep='|').sort_values("CreatedTime", ascending=False)
recieved = recieved.loc[recieved['ResponseCode'] == 200]
recieved = recieved.drop_duplicates(['VideoId'], keep='first')
recieved = set(recieved['FileId'])
left = set(fileIds) - recieved
left = list(left)

while len(left) != 0:
    account_id = "7a8b1d65-2c64-4a2d-a275-eb72026881c9"
    access_token, sas_code = get_accessToken(account_id=account_id)
    for i in (pbar := tqdm(range(len(left)))):
        data = []
        row = []
        row.append(videoIds[left[i]])

        pbar.set_description(f"Recieving {left[i]}")
        file_id = left[i]
        row.append(file_id)

        response, code, get_url, access_token = VideoIndex(account_id=account_id, videoid=file_id, accessToken=access_token)
        row.append(code)
        row.append(get_url)
        
        if code == 200:
            obj = json.dumps(response, indent=3)
            with open(f"{path}/Data/Video Indexes/JSON/{videoIds[left[i]]}.json", "w") as fp:
                fp.write(obj) 
            row.append('saved')
        else:
            row.append('failed')

        current_datetime = datetime.utcnow()
        row.append(current_datetime)

        data.append(row)
        cols = ['VideoId', 'FileId', 'ResponseCode', 'GetUrl', 'Response', 'CreatedTime']
        data = pd.DataFrame(data, columns=cols)
        data.to_csv(path+'/Data/Video Indexes/Raw Data.csv', index=False, sep='|', header=False, mode='a')
        
        if code != 200:
            time.sleep(61)
        
    recieved = pd.read_csv(path+'/Data/Video Indexes/Raw Data.csv', sep='|').sort_values("CreatedTime", ascending=False)
    recieved = recieved.loc[recieved['ResponseCode'] == 200]
    recieved = recieved.drop_duplicates(['VideoId'], keep='first')
    recieved = set(recieved['FileId'])
    left = set(fileIds) - recieved
    left = list(left)


video_indices = pd.read_csv(path+'/Data/Video Indexes/Raw Data.csv', sep='|').sort_values("CreatedTime", ascending=False)
video_indices = video_indices.loc[video_indices['ResponseCode'] == 200]
video_indices = video_indices.drop_duplicates(['VideoId'], keep='first')

