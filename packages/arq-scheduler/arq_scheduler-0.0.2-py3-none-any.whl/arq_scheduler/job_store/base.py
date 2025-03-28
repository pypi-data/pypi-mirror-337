from abc import ABCMeta, abstractmethod


class BaseJobStore(metaclass=ABCMeta):
    @abstractmethod
    def lookup_job(self, job_id):
        """

        :param job_id:
        :return:
        """

    @abstractmethod
    def get_due_jobs(self, now):
        """

        :param now:
        :return:
        """


    @abstractmethod
    def get_all_jobs(self):
        """

        :return:
        """

    @abstractmethod
    def add_job(self, job):
        """

        :param job:
        :return:
        """

    @abstractmethod
    def update_job(self, job):
        """

        :param job:
        :return:
        """

    @abstractmethod
    def remove_job(self, job_id):
        """

        :param job_id:
        :return:
        """

    @abstractmethod
    def remove_all_jobs(self):
        """

        :return:
        """
