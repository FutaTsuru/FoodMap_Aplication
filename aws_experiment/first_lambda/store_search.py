import pandas as pd

class NearestStoreSearch():
  def __init__(self, latitude, longtitude, store_info_df, choose_num):
    self.latitude = latitude
    self.longtitude = longtitude
    self.choose_num = choose_num
    self.store_info_df = store_info_df

  def get_near_store(self):
    distance_list = []
    for i in range(len(self.store_info_df)):
      store_latitude = self.store_info_df[i : i+1]["latitude"].to_list()[0]
      store_longtitude = self.store_info_df[i : i+1]["longtitude"].to_list()[0]
      distance = (store_latitude - self.latitude) ** 2 + (store_longtitude - self.longtitude) ** 2
      distance_list.append(distance)
    
    output_df = pd.DataFrame(columns = list(self.store_info_df.columns))
    sort_distance = list(sorted(distance_list))
    for i in range(self.choose_num):
        tmp = sort_distance[i]
        index = distance_list.index(tmp)
        target_df = self.store_info_df[index : index + 1]
        output_df = pd.concat([output_df, target_df])
    return output_df
  
  def get_recommend_store(self, store_info_df):
    return store_info_df.sort_values('near_times', ascending=False)[0 : self.choose_num]