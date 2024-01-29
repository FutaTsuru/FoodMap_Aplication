import json
import boto3
from store_info import StoreInfo
from store_search import NearestStoreSearch
from near_action_log import NearActionLog


def lambda_handler(event, context):
    #eventから現在の緯度と経度を取得
    latitude, longtitude = event["val"]
    
    #S3からお店の情報を取得
    bucket = 'tsuruhara-testbucket'
    store_info_df = pd.read_csv('s3://' + bucket + '/store_info.csv')
    
    #取得した緯度経度から、近くに立ち寄ったお店を記録する
    threshold = 30
    near_action_log = NearActionLog(store_info_df, latitude, longtitude, threshold)
    store_info_df = near_action_log.near_Drop_by_log()
    store_info_df.to_csv('s3://' + bucket + '/store_info.csv')
    
    #お店の情報をStoreInfoクラスのインスタンスに格納
    instance_list = []
    for i in range(len(store_list)):
        store_info = StoreInfo(store_info_df['name'].to_list()[i],store_info_df['url'].to_list()[i], store_info_df['kind'].to_list()[i], store_info_df['image_url'].to_list()[i], store_info_df['latitude'].to_list()[i], store_info_df['longtitude'].to_list()[i], store_info_df['near_times'].to_list()[i])
        instance_list.append(store_info)
    
    #現在地から最も近い5つの店舗のインスタンスを抽出
    near_store_search = NearestStoreSearch(latitude, longtitude, instance_list, 5)
    output_list = near_store_search.get_near_store()
    
    #5つの店舗情報をS3に保存(更新)
    output_df = pd.DataFrame(columns = list(store_info_df.columns))
    for instance in output_list:
        output_df = pd.concat([output_df, store_info_df[store_info_df["name"] == instance.name]])
    
    output_df.to_csv('s3://' + bucket + '/nearest_store_df')
    
    #行動履歴から5つのお店をレコメンド、それらをS3に保存(更新)
    recommend_df = near_store_search.get_recommend_store(store_info_df)
    recommend_df.to_csv('s3://' + bucket + '/recommend_df.csv')
    
    output_df.to_csv('s3://' + bucket + '/nearest_store_info.csv')
    
    #経度緯度をS3に保存(蓄積)
    gps_info_df = pd.read_csv("s3://' + bucket + '/gps_info.csv")
    gps_info.df = pd.concat(gps_info_df, pd.DataFrame({"latitude" : latitude, "longtidue" : longtitude}))
    gps.to_csv('s3://' + bucket + 'gps_info.csv')
    
    return 0