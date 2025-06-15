from datetime import timedelta

import pandas as pd

from src.dataModel.menu_hours import MenuHours
from src.dataModel.store_status import StoreStatus
from src.dataModel.timezone import TimeZone

REPORT_STATUS = {}

class ReportGeneration:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.timezone = TimeZone("data/timezones.csv")
        self.menu_hours = MenuHours("data/menu_hours.csv")
        self.menu_hours.add_utc_columns(self.timezone.timezones_df)  # Add UTC columns to menu hours
        self.store_status = StoreStatus("data/store_status.csv")

    def calculate_uptime(self, store_id: str, start: pd.Timestamp, end: pd.Timestamp):
        statuses = self.store_status.store_status_df[
            (self.store_status.store_status_df['store_id'] == store_id) & 
            (self.store_status.store_status_df['timestamp_utc'] >= start) & 
            (self.store_status.store_status_df['timestamp_utc'] <= end)
        ]
        if statuses.empty:
            return 0, 0
        
        hours = self.menu_hours.menu_hours_df[self.menu_hours.menu_hours_df['store_id'] == store_id]

        if hours.empty:
            return 0, 0
        
        def is_within_hours(status):
            day = status['timestamp_utc'].weekday()
            day_hours = hours[(hours['dayOfWeek'] == day)]

            if day_hours.empty:
                return False

            for _, dh in day_hours.iterrows():
                if pd.to_datetime(dh['start_time_local'], format='%H:%M:%S').time() <= status['timestamp_utc'].time(): #<= pd.to_datetime(dh['end_time_local'], format='%H:%M:%S').time():
                    return True
            
            return False
        
        filtered = statuses[statuses.apply(is_within_hours, axis=1)]

        if filtered.empty:
            return 0, 0

        filtered = filtered.sort_values('timestamp_utc')

        uptime = 0
        downtime = 0

        for idx, row in filtered.iterrows():
            duration = 60
            if row['status'] == 'active':
                uptime += duration
            else:
                downtime += duration
                
        return round(uptime), round(downtime)

    def generate_report(self, report_id: str):
        now = self.store_status.get_max_timestamp() 
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        week_ago = now - timedelta(days=7)

        result = []
        for store_id in self.store_status.store_status_df['store_id'].unique():
            up1, down1 = self.calculate_uptime(store_id, hour_ago, now)
            up24, down24 = self.calculate_uptime(store_id, day_ago, now)
            up7, down7 = self.calculate_uptime(store_id, week_ago, now)

            result.append({
                "store_id": store_id,
                "uptime_last_hour(in minutes)": up1,
                "uptime_last_day(in hours)": up24/60,
                "downtime_last_hour(in minutes)": down1,
                "uptime_last_week(in hours)": up7/60,
                "downtime_last_day(in hours)": down24/60,
                "downtime_last_week(in hours)": down7/60,
            })

        df = pd.DataFrame(result)
        out_path = f"{self.output_dir}/report_{report_id}.csv"
        df.to_csv(out_path, index=False)
        REPORT_STATUS[report_id] = "Complete"