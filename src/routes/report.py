import uuid
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from src.dataModel.report_generation import REPORT_STATUS, ReportGeneration

OUTPUT_DIR = "output"  


report = APIRouter()


@report.post("/trigger_report")
def trigger_report(background_tasks: BackgroundTasks):
    report_id = str(uuid.uuid4())[:8]
    REPORT_STATUS[report_id] = "Running"

    def background_task(id):
        generator = ReportGeneration(output_dir=OUTPUT_DIR)
        generator.generate_report(id)

    background_tasks.add_task(background_task, report_id)
    return {"report_id": report_id}
    
@report.get("/get_report")
def get_report(report_id: str = Query(...)):
    
    if report_id not in REPORT_STATUS:
        raise HTTPException(404, "Invalid report_id")

    if REPORT_STATUS[report_id] == "Running":
        return {"status": "Running"}
    elif REPORT_STATUS[report_id] == "Complete":
        return {
            "status": "Complete",
            "download_url": f"http://127.0.0.1:8000/get_report_file/{report_id}"  
        }
    else:
        raise HTTPException(500, "Report not found or report generation failed.")
    

@report.get("/get_report_file/{report_id}")
def get_report_file(report_id: str):
    if report_id not in REPORT_STATUS or REPORT_STATUS[report_id] != "Complete":
        raise HTTPException(404, "Report not ready.")
    file_path = f"{OUTPUT_DIR}/report_{report_id}.csv"
    return FileResponse(file_path, media_type='text/csv', filename=f'report_{report_id}.csv')
