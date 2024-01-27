import os
import pandas as pd
import time
from tqdm import tqdm
from datetime import datetime

current_path = os.getcwd()
current_path = current_path.split('movie-pre-buzz-to-box-office')
path = current_path[0] + 'movie-pre-buzz-to-box-office'
print(path)

def videoURL(fileName, path, filetype, sasToken):
    cont_path = 'https://moviebuzz.blob.core.windows.net/moviebuzztrailers'
    path = cont_path + path + fileName + filetype + sasToken
    return path


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


def postVideo(videoURL, fileName, account_id, accessToken, privacy='Private', language='auto'):
    import urllib.request, json
    import time
    
    name = fileName

    base = 'https://api.videoindexer.ai/trial/Accounts/'
    post_url = base + account_id + '/Videos?name=' + name + '&privacy=' + privacy + '&language=' + language + '&videoUrl=' + \
        videoURL + '&fileName=' + fileName + '&accessToken=' + accessToken

    try:
        hdr ={
        'Cache-Control': 'no-cache',
        }

        req = urllib.request.Request(post_url, headers=hdr)

        req.get_method = lambda: 'POST'
        response = urllib.request.urlopen(req)
        code = response.getcode()
        response = response.read()
        response = json.loads(response)
        return response, code, post_url, accessToken
    except Exception as error:
        code = error.getcode()
        if code == 401:
            time.sleep(3)
            accessToken, _ = get_accessToken(account_id=account_id)

            post_url = base + account_id + '/Videos?name=' + name + '&privacy=' + privacy + '&language=' + language + '&videoUrl=' + \
                        videoURL + '&fileName=' + fileName + '&accessToken=' + accessToken
            
            try:
                hdr = {
                    'Cache-Control': 'no-cache',
                }

                req = urllib.request.Request(post_url, headers=hdr)

                req.get_method = lambda: 'POST'
                response = urllib.request.urlopen(req)
                code = response.getcode()
                response = response.read()
                response = json.loads(response)
                return response, code, post_url, accessToken
            except Exception as error:
                code = error.getcode()
                error = error.read()
                error = json.loads(error)
                return error, code, post_url, accessToken
        else:
            error = error.read()
            error = json.loads(error)
            return error, code, post_url, accessToken
        

videoIds = pd.read_csv(path + '/Data/Trailer Ids/youtube trailer Ids.csv')

videoIds = list(videoIds['Video Id'])
sasToken = ''
account_id = ""
access_token, sas_code = get_accessToken(account_id=account_id)
for i in (pbar := tqdm(range(len(videoIds)))):
    data = []
    row = []
    
    videoId = videoIds[i]
    pbar.set_description(f"Uploading {videoId}")
    row.append(videoId)
    
    video_url = videoURL(fileName=videoId, path='/trailers/', filetype='.mp4', sasToken=sasToken)
    row.append(video_url)

    # Change videURL to use real one
    response, code, post_url, access_token = postVideo(videoURL=video_url, fileName=videoId, account_id=account_id, accessToken=access_token)
    row.append(code)
    row.append(post_url)
    row.append(response)
    try:
        row.append(response['id'])
    except:
        row.append(None)
    
    try:
        row.append(response['created'])
    except:
        row.append(None)
    
    current_datetime = datetime.utcnow()
    row.append(current_datetime)

    data.append(row)
    cols = ['VideoId', 'VideoUrl', 'ResponseCode', 'PostUrl', 'Response', 'Id', 'UploadTime', 'CreatedTime']
    data = pd.DataFrame(data, columns=cols)
    if i==0:
        data.to_csv(path+'/Data/Upload Data/uploadData.csv', index=False, sep='|', header=False, mode='a')
    else:
        data.to_csv(path+'/Data/Upload Data/uploadData.csv', index=False, sep='|', mode='a', header=False)
    time.sleep(5)


left_uploads = ['0']
while len(left_uploads) != 0:
    uploads = pd.read_csv(path+'/Data/Upload Data/uploadData.csv', sep='|').sort_values("CreatedTime", ascending=False)
    uploads = uploads.loc[uploads['ResponseCode'] == 200]
    uploads = uploads.drop_duplicates(['VideoId'], keep='first')
    uploads = set(uploads['VideoId'])
    left_uploads = set(videoIds) - uploads
    left_uploads = list(left_uploads)
    sasToken = ''
    account_id = ""
    access_token, sas_code = get_accessToken(account_id=account_id)
    for i in (pbar := tqdm(range(len(left_uploads)))):
        data = []
        row = []
        
        videoId = left_uploads[i]
        pbar.set_description(f"Uploading {videoId}")
        row.append(videoId)
        
        video_url = videoURL(fileName=videoId, path='/trailers/', filetype='.mp4', sasToken=sasToken)
        row.append(video_url)

        # Change videURL to use real one
        response, code, post_url, access_token = postVideo(videoURL=video_url, fileName=videoId, account_id=account_id, accessToken=access_token)
        row.append(code)
        row.append(post_url)
        row.append(response)
        try:
            row.append(response['id'])
        except:
            row.append(None)
        
        try:
            row.append(response['created'])
        except:
            row.append(None)
        
        current_datetime = datetime.utcnow()
        row.append(current_datetime)

        data.append(row)
        cols = ['VideoId', 'VideoUrl', 'ResponseCode', 'PostUrl', 'Response', 'Id', 'UploadTime', 'CreatedTime']
        data = pd.DataFrame(data, columns=cols)
        data.to_csv(path+'/Data/Upload Data/uploadData.csv', index=False, sep='|', header=False, mode='a')
        
        if code != 200:
            time.sleep(50)

    uploads = pd.read_csv(path+'/Data/Upload Data/uploadData.csv', sep='|').sort_values("CreatedTime", ascending=False)
    uploads = uploads.loc[uploads['ResponseCode'] == 200]
    uploads = uploads.drop_duplicates(['VideoId'], keep='first')
    uploads = set(uploads['VideoId'])
    left_uploads = set(videoIds) - uploads
    left_uploads = list(left_uploads)


uploads = pd.read_csv(path+'/Data/Upload Data/uploadData.csv', sep='|').sort_values("CreatedTime", ascending=False)
uploads = uploads.loc[uploads['ResponseCode'] == 200]
uploads = uploads.drop_duplicates(['VideoId'], keep='first')

print(uploads)