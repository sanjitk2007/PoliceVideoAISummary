import threading

class JobStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.jobs = {}

    def create_job(self, job_id):
        with self.lock:
            self.jobs[job_id] = {
                'status': 'PENDING',
                'report': None,
                'error': None
            }

    def update_status(self, job_id, status):
        with self.lock:
            if job_id in self.jobs:
                self.jobs[job_id]['status'] = status

    def set_report(self, job_id, report):
        with self.lock:
            if job_id in self.jobs:
                self.jobs[job_id]['report'] = report
                self.jobs[job_id]['status'] = 'COMPLETE'

    def set_error(self, job_id, error):
        with self.lock:
            if job_id in self.jobs:
                self.jobs[job_id]['error'] = error
                self.jobs[job_id]['status'] = 'FAILED'

    def get_job(self, job_id):
        with self.lock:
            return self.jobs.get(job_id)

job_store = JobStore() 