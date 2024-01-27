import os
import pandas as pd
from tqdm import tqdm
import json
from datetime import datetime

current_path = os.getcwd()
current_path = current_path.split('movie-pre-buzz-to-box-office')
path = current_path[0] + 'movie-pre-buzz-to-box-office'


def process_prompt(prompt):
        import openai
        from openai.error import ServiceUnavailableError, APIError, Timeout, AuthenticationError

        openai_key = ''
        openai.api_key = openai_key

        try:
            # @backoff.on_exception(backoff.expo, (ServiceUnavailableError, APIError))
            def chat_completion(prompt):
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": prompt},
                    ]
                )

                response = response['choices'][0]['message']['content']
                return response
            
            response = chat_completion(prompt)
            return response, 200
        except (ServiceUnavailableError, APIError, Timeout) as error:
            return 'error', 400

videoIds = pd.read_csv(path + "/Data/Trailer Ids/youtube trailer Ids.csv")

videodescriptions = pd.read_csv(path + "/Data/Video Description/videoDescription.csv")

videodescriptions_dict = {}
for videoId, description in zip(videodescriptions['videoId'], videodescriptions['description']):
    videodescriptions_dict[videoId] = description

videoIds = list(videoIds['Video Id'])
for videoId in (pbar:= tqdm(videoIds)):
    pbar.set_description(f"Generating video description for {videoId}")
    final_data = []
    with open((path + f"/Data/Video Indexes/JSON/{videoId}.json"), 'r') as fp:
        data = json.load(fp)

        keywords = []
        for keyword in data['summarizedInsights']['keywords']:
            keywords.append(keyword['name'])

        sentiments = []
        for sentiment in data['summarizedInsights']['sentiments']:
            if sentiment['sentimentKey'] != 'Neutral':
                sentiments.append([sentiment['sentimentKey'], sentiment['seenDurationRatio']])
        
        emotions = []
        for emotion in data['summarizedInsights']['emotions']:
            emotions.append([emotion['type'], emotion['seenDurationRatio']])
        
        audioeffects = []
        for audioeffect in data['summarizedInsights']['audioEffects']:
            audioeffects.append([audioeffect['audioEffectKey'], audioeffect['seenDurationRatio']])
        
        labels = []
        for label in data['summarizedInsights']['labels']:
            labels.append([label['name'], len(label['appearances'])])
        
        framepatters = []
        for pattern in data['summarizedInsights']['framePatterns']:
            sum = 0
            for appearence in pattern['appearances']:
                sum = sum + float(appearence['endSeconds']) - float(appearence['startSeconds'])
            sum = round(sum, 2)
            framepatters.append([pattern['name'], len(pattern['appearances']), sum])
        
        topics = []
        for topic in data['summarizedInsights']['topics']:
            topics.append(topic['name'])


    i = 0
    sentiment_passer = sentiments.copy()
    for sentiment in sentiments:
        sentiments[i] = f'"{sentiment[0]}" seen for {round(sentiment[1]*100, 2)}%'
        i += 1

    i = 0
    for emotion in emotions:
        emotions[i] = f'"{emotion[0]}" seen for {round(emotion[1]*100, 2)}%'
        i += 1

    i = 0
    for audioeffect in audioeffects:
        audioeffects[i] = f'"{audioeffect[0]}" seen for {round(audioeffect[1]*100, 2)}%'
        i += 1

    i = 0
    for label in labels:
        labels[i] = f'"{label[0]}" seen {label[1]} times'
        i += 1

    i = 0
    for framepatter in framepatters:
        framepatters[i] = f'"{framepatter[0]}" frame seen {framepatter[1]} times for a total of {framepatter[2]} seconds'
        i += 1
    
    prompt = f'''Create a humanized description of a movie trailer which has the followind identified attributes:
    1. Keywords indentified in the video: {', '.join(keywords)}
    2. Sentiments observed in the video: {', '.join(sentiments)}
    3. Emotions seen in the video: {', '.join(emotions)}
    4. Audio Effects present in the video: {', '.join(audioeffects)}
    5. Attributes/Objects sighted in the video: {', '.join(labels)}
    6. Frame Patterns: {', '.join(framepatters)}
    7. Topics inferred: {', '.join(topics)}
    8. Trailer description: "{videodescriptions_dict[videoId]}"

Make sure there are not links in the result.'''

    description, code = process_prompt(prompt=prompt)
    # description = description.strip()
    
    current_datetime = datetime.utcnow()
    final_data.append([videoId, code, prompt.replace('\n', ''), description, ','.join(sentiment_passer), current_datetime])
    
    cols = ['VideoId', 'Code', 'Prompt', 'OpenAIGeneratedDescription', 'CreatedTime']
    final_data = pd.DataFrame(final_data, columns=cols)
    final_data.to_csv(path+'/Data/Processed/ProcessedVideoDescription.csv', index=False, sep='|', header=False, mode='a', lineterminator='%')

generated_description = pd.read_csv(path+'/Data/Processed/ProcessedVideoDescription.csv', sep='|', lineterminator='%')

videoIds = list(videoIds['Video Id'])
# videoIds = ['iBgubizv64g','XKeNWUsC_Nw','BoNynvcG7Ok','b6qSGKN42Gc','tSkv_sEyPSc','gSMxBLlA8qY','Na6gA1RehsU','09zYzvKkCOA']
for videoId in (pbar:= tqdm(videoIds)):
    pbar.set_description(f"Generating video description for {videoId}")
    final_data = []
    with open((path + f"/Data/Video Indexes/JSON/{videoId}.json"), 'r') as fp:
        data = json.load(fp)

        keywords = []
        for keyword in data['summarizedInsights']['keywords']:
            keywords.append(keyword['name'])

        sentiments = []
        for sentiment in data['summarizedInsights']['sentiments']:
            if sentiment['sentimentKey'] != 'Neutral':
                sentiments.append([sentiment['sentimentKey'], sentiment['seenDurationRatio']])
        
        emotions = []
        for emotion in data['summarizedInsights']['emotions']:
            emotions.append([emotion['type'], emotion['seenDurationRatio']])
        
        audioeffects = []
        for audioeffect in data['summarizedInsights']['audioEffects']:
            audioeffects.append([audioeffect['audioEffectKey'], audioeffect['seenDurationRatio']])
        
        labels = []
        for label in data['summarizedInsights']['labels']:
            labels.append([label['name'], len(label['appearances'])])
        
        framepatters = []
        for pattern in data['summarizedInsights']['framePatterns']:
            sum = 0
            for appearence in pattern['appearances']:
                sum = sum + float(appearence['endSeconds']) - float(appearence['startSeconds'])
            sum = round(sum, 2)
            framepatters.append([pattern['name'], len(pattern['appearances']), sum])
        
        topics = []
        for topic in data['summarizedInsights']['topics']:
            topics.append(topic['name'])

    description = 'None'
    
    current_datetime = datetime.utcnow()
    j = ','
    for kj in sentiment_passer:
        for mj in kj:
            j += str(mj)
    final_data.append([videoId, j, current_datetime])
    
cols = ['VideoId', 'Sentiment', 'CreatedTime']
final_data = pd.DataFrame(final_data, columns=cols)
final_data.to_csv(path+'/Data/Processed/ProcessedVideoDescription-Sent.csv', index=False, header=True)