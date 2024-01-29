import pandas as pd

class NearActionLog():
    def __init__(self, store_info_df, latitude, longtitude, threshold):
        self.store_info_df = store_info_df
        self.latitude = latitude
        self.longtitude = longtitude
        self.threshold = threshold
    
    def near_Drop_by_log(self):
        for i in range(len(self.store_info_df)):
            near_times = self.store_info_df[i:i+1]["near_times"].to_list()[0]
            target_latitude = self.store_info_df[i:i+1]["latitude"].to_list()[0]
            target_longtitude = self.store_info_df[i:i+1]["longtitude"].to_list()[0]
            if ((self.latitude - target_latitude)**2 + (self.longtitude - target_longtitude)**2)**0.5  < self.threshold:
                self.store_info_df[i:i+1] = self.store_info_df[i:i+1].replace(near_times, near_times + 1)
        
        return self.store_info_df