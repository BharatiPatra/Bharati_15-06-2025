# Bharati_15-06-2025

# Store Monitoring Backend

This project implements a backend API for monitoring restaurant store uptime and downtime, as described in the take-home interview prompt.

## Problem Overview

Loop monitors several restaurants in the US and needs to track if a store is online during its business hours. Restaurant owners require reports on how often their stores were inactive during business hours in the past.

## Data Sources

- **store_status.csv**: Hourly polling data for each store (`store_id, timestamp_utc, status`)
- **menu_hours.csv**: Business hours for each store (`store_id, dayOfWeek, start_time_local, end_time_local`)
- **timezones.csv**: Timezone for each store (`store_id, timezone_str`)

## Features

- **Dynamic Data**: Reads from CSVs that are updated regularly.
- **Business Hours Logic**: Handles missing business hours (assumes 24/7) and missing timezones (defaults to America/Chicago).
- **Uptime/Downtime Calculation**: Interpolates between polling intervals to estimate uptime/downtime during business hours.
- **API Endpoints**:
  - `POST /trigger_report`: Triggers report generation and returns a `report_id`.
  - `GET /get_report?report_id=...`: Polls for report status or returns the completed CSV report.
  - `GET /get_report_file/{report_id}`: Downloads the generated report CSV.

## API Usage

1. **Trigger Report**

   ```
   POST /trigger_report
   Response: { "report_id": "<id>" }
   ```

2. **Check Report Status**

   ```
   GET /get_report?report_id=<id>
   Response: { "status": "Running" }
   or
   Response: { "status": "Complete", "download_url": "<url>" }
   ```

3. **Download Report**
   ```
   GET /get_report_file/<report_id>
   Returns: CSV file
   ```

## Output

The report CSV contains:

```
store_id, uptime_last_hour(in minutes), uptime_last_day(in hours), uptime_last_week(in hours), downtime_last_hour(in minutes), downtime_last_day(in hours), downtime_last_week(in hours)
```

Sample output is available in [`output/report_2ffbeea8.csv`](output/report_2ffbeea8.csv).

## Running the Project

1. Install dependencies:
   ```
   pip install fastapi uvicorn pandas pytz
   ```
2. Start the server:
   ```
   uvicorn main:app --reload
   ```
3. Use the API as described above.

## Ideas for Improvement

- **Database Integration**: Move from CSV-based storage to a relational database for scalability and reliability.
- **Efficient Interpolation**: Improve the interpolation logic for more accurate uptime/downtime estimation between polls.
- **Authentication**: Add authentication and authorization for API endpoints.
- **Error Handling**: Enhance error handling and logging for production readiness.
- **Unit Tests**: Add comprehensive unit and integration tests.
- **Async Processing**: Use async I/O for faster report generation on large datasets.

## Demo

A sample output CSV is included in the [`output/`](output/) directory.

---

**Author:** [E Bharati Patra]  
**Date:** [15-06-2025]
