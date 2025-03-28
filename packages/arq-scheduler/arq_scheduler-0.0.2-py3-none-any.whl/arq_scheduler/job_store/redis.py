from arq_scheduler.job_store.base import BaseJobStore


class RedisJobStore(BaseJobStore):
    def __init__(self):
        pass

    def lookup_job(self, job_id):
        pass

    def get_due_jobs(self, now):
        pass

    def get_all_jobs(self):
        pass

    def add_job(self, job):
        pass

    def update_job(self, job):
        pass

    def remove_job(self, job_id):
        pass

    def remove_all_jobs(self):
        pass
