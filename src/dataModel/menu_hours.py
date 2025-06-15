from typing import Dict
import pandas as pd
from datetime import datetime

import pytz

class MenuHours:
    def __init__(self,path):
        self.path=path
        self.menu_hours_df= pd.read_csv(path)

    def get_menu_hours(self,store_id: int, date: datetime):
        day = date.weekday()
        mh = self.menu_hours_df[(self.menu_hours_df['store_id'] == store_id) & (self.menu_hours_df['dayOfWeek'] == day)]
        if mh.empty:
            return [datetime(date.year, date.month, date.day, 0, 0), datetime(date.year, date.month, date.day, 23, 59)]
        start = mh.iloc[0]['start_time_local']
        end = mh.iloc[0]['end_time_local']
        return [start, end]
    
    def to_utc(self, timezone_map: dict, store_id: str, time_field: str):
        tz_name = timezone_map.get(store_id, "UTC")
        tz = pytz.timezone(tz_name)
        dt = pd.to_datetime(time_field, format='%H:%M:%S')
        localized = tz.localize(dt)
        return localized.astimezone(pytz.utc)
    
    def add_utc_columns(self, timezone_df: pd.DataFrame):
        timezone_map = pd.Series(timezone_df.timezone_str.values, index=timezone_df.store_id).to_dict()
        self.menu_hours_df['start_time_utc'] = self.menu_hours_df.apply(lambda row: self.to_utc(timezone_map, row['store_id'], row['start_time_local']), axis=1)
        self.menu_hours_df['end_time_utc'] = self.menu_hours_df.apply(lambda row: self.to_utc(timezone_map, row['store_id'], row['end_time_local']), axis=1)
        self.menu_hours_df.to_csv(self.path, index=False)