import pandas as pd

class StoreStatus:
    def __init__(self,path):
        self.path=path
        self.store_status_df = pd.read_csv(path)
        self.store_status_df['timestamp_utc'] = pd.to_datetime(self.store_status_df['timestamp_utc'], utc=True)

    def get_max_timestamp(self) -> pd.Timestamp:
        return self.store_status_df['timestamp_utc'].max()