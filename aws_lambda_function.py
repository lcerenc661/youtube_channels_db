## AWS Lambda script, to be correctly executed remember to configure the enviroment variables

import pandas as pd
import time 
import requests 
import random
import os
import boto3


s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


def get_stats(api_key, channel_id):
    
    url_channel_stats = 'https://youtube.googleapis.com/youtube/v3/channels?part=statistics&id='+channel_id+'&key='+api_key
    channel_stats_raw = requests.get(url_channel_stats).json()
    channel_stats = channel_stats_raw['items'][0]['statistics']
    date = pd.to_datetime('today').strftime("%Y-%m-%d")
    channel_data = {
        'Date': [date],
        'Total_Views':[int(float(channel_stats['viewCount']))],
        'Subcribers':[int(float(channel_stats['subscriberCount']))],
        'Video_count':[int(float(channel_stats['videoCount']))],
    }
    channel_data = pd.DataFrame.from_dict(channel_data)
    
    return channel_data
    
    
def get_data_df(channels_df, developer_key):
    
    tiempo = [1,2,5,4]
    data_dfs=pd.DataFrame(columns=['Channel','Total_Views','Subcribers','Video_count','Date'])
    for channel in range(len(channels_df.index)):
        
        df = get_stats(developer_key, channels_df['Ch_id'][channel])
        df.insert(0,'Channel',channels_df['Name'][channel])
        data_dfs = pd.concat([data_dfs, df], axis=0)
        time.sleep(random.choice(tiempo))
        
    return data_dfs
    

def lambda_handler(event, context):
    
    bucket_input = os.environ['BUCKET_INPUT']
    bucket_output = os.environ['BUCKET_OUTPUT']
    file_name = os.environ['FILE_CHANNELS']
    developer_key = os.environ['APIKEY']
    
    print('bucket_input')
    #get Object
    csv_obj = s3_client.get_object(Bucket=bucket_input, Key =file_name)
    channels_df = pd.read_csv(csv_obj['Body'], delimiter=';')
    print(channels_df)
    
    #transfrom data
    results = get_data_df(channels_df, developer_key)
    date = pd.to_datetime('today').strftime("%Y%m%d")
    
    #load data
    results.to_csv(f'/tmp/youtube_stats_{date}.csv', index=False)
    #s3_resource.Object(bucket_output).upload_file(f'/tmp/youtube_stats_{date}.csv', Key=f'youtube_stats_{date}.csv')
    s3_client.upload_file(f'/tmp/youtube_stats_{date}.csv', bucket_output, f'youtube_stats_{date}.csv')
    os.remove(f'/tmp/youtube_stats_{date}.csv')
    

    return f'/tmp/youtube_stats_{date}.csv ==> file succeed'
