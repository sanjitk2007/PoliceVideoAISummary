from pydantic import BaseModel
from typing import Optional

class AnalyzeResponse(BaseModel):
    jobId: str
    status_url: str

class StatusResponse(BaseModel):
    jobId: str
    status: str  
    report: Optional[str] = None
    error: Optional[str] = None 