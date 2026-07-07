from datetime import datetime
from uuid import UUID


class Job:

    def __init__(
        self,
        job_id: UUID,
        filename: str,
        status: str = "RECEIVED"
    ):
        self.job_id = job_id
        self.filename = filename
        self.status = status
        self.created_at = datetime.now()