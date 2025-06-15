import pandas as pd
import pytz

class TimeZone:
    def __init__(self,path):
        self.path=path
        self.timezones_df = pd.read_csv(path)
        self.timezones_df.fillna("America/Chicago", inplace=True)

    def get_timezone(self, store_id: int):
        tz_row = self.timezones_df[self.timezones_df['store_id'] == store_id]
        if tz_row.empty:
            return pytz.timezone("America/Chicago")
        return pytz.timezone(tz_row.iloc[0]['timezone_str'])