import os
from celery import Celery
from app.job_store import job_store
from app.video_utils import split_video_into_chunks
from app.gemini_api import summarize_video_chunk

# using redis
celery_app = Celery('worker', broker='redis://localhost:6379/0')

# celery task for splitting video into chunks and summarizing 
@celery_app.task
def process_video_job(job_id, video_path):
    try:
        job_store.update_status(job_id, 'PROCESSING')
        chunk_dir = os.path.join('chunks', job_id)
        chunks = split_video_into_chunks(video_path, chunk_dir)
        summaries = []
        for chunk in chunks:
            # summarize each chunk
            summary = summarize_video_chunk(chunk)
            summaries.append(summary)
        report = '\n\n'.join(summaries)
        job_store.set_report(job_id, report)
    except Exception as e:
        job_store.set_error(job_id, str(e)) 