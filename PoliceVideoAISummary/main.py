import os
import uuid
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from app.models import AnalyzeResponse, StatusResponse
from app.job_store import job_store
from app.worker import process_video_job

app = FastAPI()

UPLOAD_DIR = '/Users/sanjitkakarla/Desktop/uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

#endpoint for analyzing video
@app.post('/v1/analyze', response_model=AnalyzeResponse)
def analyze_video(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    video_path = os.path.join(UPLOAD_DIR, f'{job_id}_{file.filename}')
    with open(video_path, 'wb') as f:
        f.write(file.file.read())
    job_store.create_job(job_id)
    process_video_job.delay(job_id, video_path)
    status_url = f'/v1/analyze/status/{job_id}'
    return AnalyzeResponse(jobId=job_id, status_url=status_url)

# endpoint for getting job status
@app.get('/v1/analyze/status/{job_id}', response_model=StatusResponse)
def get_status(job_id: str):
    job = job_store.get_job(job_id)
    if not job:
        # handle no status found
        return JSONResponse(status_code=404, content={'detail': 'Job not found'})
    return StatusResponse(jobId=job_id, status=job['status'], report=job['report'], error=job['error']) 