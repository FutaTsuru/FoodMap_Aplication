import json
import boto3
import pandas as pd
import os
from io import StringIO
from store_info import StoreInfo
from store_search import NearestStoreSearch
from near_action_log import NearActionLog


def lambda_handler(event, context):
    #eventから現在の緯度と経度を取得
    latitude = float(event["latitude"])
    longtitude = float(event["longtitude"])
    
    #S3からお店の情報を取得
    bucket = 'gps-bucket'
    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    key = 'store_info_df.csv'
    obj = s3.get_object(Bucket=bucket, Key=key)
    data = obj['Body'].read().decode('utf-8')
    store_info_df = pd.read_csv(StringIO(data))
    
    #取得した緯度経度から、近くに立ち寄ったお店を記録する
    threshold = 0.0004
    near_action_log = NearActionLog(store_info_df, latitude, longtitude, threshold)
    store_info_df = near_action_log.near_Drop_by_log()
    csv_buffer = StringIO()
    store_info_df.to_csv(csv_buffer, index = False)
    s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())
    
    
    #現在地から最も近い5つの店舗のインスタンスを抽出
    near_store_search = NearestStoreSearch(latitude, longtitude, store_info_df, 5)
    output_df = near_store_search.get_near_store()
    
    key = 'nearest_store_df.csv'
    csv_buffer = StringIO()
    output_df.to_csv(csv_buffer, index = False)
    s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())
    
    #行動履歴から5つのお店をレコメンド、それらをS3に保存(更新)
    recommend_df = near_store_search.get_recommend_store(store_info_df)
    key = 'recommend_store_df.csv'
    csv_buffer = StringIO()
    recommend_df.to_csv(csv_buffer, index = False)
    s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())
    
    #経度緯度をS3に保存(蓄積)
    key = 'gps_info.csv'
    obj = s3.get_object(Bucket=bucket, Key=key)
    data = obj['Body'].read().decode('utf-8')
    gps_info_df = pd.read_csv(StringIO(data))
    
    gps_info_df = pd.concat([gps_info_df, pd.DataFrame({"latitude" : [latitude], "longtitude" : [longtitude]})])
    csv_buffer = StringIO()
    gps_info_df.to_csv(csv_buffer, index = False)
    s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())
    
    return 0