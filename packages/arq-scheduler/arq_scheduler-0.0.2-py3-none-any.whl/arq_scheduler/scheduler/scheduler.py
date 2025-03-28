from arq.utils import import_string


class Scheduler(object):
    def __init__(self, arq_worker_settings: str, job_store: str, interval: float):
        self.worker_settings = import_string(arq_worker_settings)
        self.job_store = import_string(job_store)

    async def run(self):
        pass
