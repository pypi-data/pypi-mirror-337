import asyncio

import click

from arq_scheduler import __version__
from arq_scheduler.scheduler import Scheduler
from arq_scheduler.utils import setup_logging


@click.command('arq_scheduler')
@click.version_option(__version__, '-V', '--version', prog_name='arq')
@click.option('--worker-settings', type=str, required=True)
@click.option('--job-store', type=str, required=True)
@click.option('--verbose', is_flag=True, required=False, help="DEBUG")
@click.option('--quiet', is_flag=True, required=False, help="WARNING")
@click.option('--interval', type=float, required=False,
              help="How often the scheduler checks for new jobs to add to the queue (in seconds)")
def cli(*,
        worker_settings: str,
        job_store: str,
        verbose: bool,
        quiet: bool,
        interval: float):
    if verbose:
        log_level = "DEBUG"
    elif quiet:
        log_level = "WARNING"
    else:
        log_level = "INFO"
    setup_logging(log_level)

    asyncio.run(run(worker_settings=worker_settings, job_store=job_store, interval=interval))


async def run(worker_settings: str, job_store: str, interval: float):
    scheduler = Scheduler(arq_worker_settings=worker_settings, job_store=job_store, interval=interval)
