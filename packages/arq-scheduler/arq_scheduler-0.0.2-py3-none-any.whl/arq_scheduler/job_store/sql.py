from arq_scheduler.job_store.base import BaseJobStore


class SQLJobStore(BaseJobStore):
    def __init__(self, table_name: str, engine_uri: str):
        self.table = self._table_definition()
        self.name = table_name
        self.engine_uri = engine_uri

    def _table_definition(self):
        from sqlalchemy import Table, Column, MetaData, String, JSON, TIMESTAMP, func
        meta = MetaData()
        columns = (Column("job_id", String(50), primary_key=True),
                   Column("job_data", JSON, nullable=False, server_default="{}"),
                   Column("updated_at", TIMESTAMP, nullable=False, server_default=func.now()),
                   Column("updated_at", TIMESTAMP, nullable=False, server_default=func.now()))

        return Table(self.name, meta, *columns)

    async def _execute(self, *args, **kwargs):
        from sqlalchemy.ext.asyncio import create_async_engine

        engine = create_async_engine(self.engine_uri, echo=True)
        async with engine.begin() as conn:
            await conn.execute(*args)

        await engine.dispose()

    async def _fetch_all(self, *args, **kwargs):
        from sqlalchemy.ext.asyncio import create_async_engine

        engine = create_async_engine(self.engine_uri, echo=True)
        async with engine.connect() as conn:
            response = await conn.execute(*args)
            results = response.fetchall()
        await engine.dispose()
        return results

    async def lookup_job(self, job_id):
        from sqlalchemy import select
        return await self._fetch_all(select(self.table).where(self.table.c.job_id == job_id))

    async def get_due_jobs(self, now):
        pass

    async def get_all_jobs(self):
        from sqlalchemy import select
        return await self._fetch_all(select(self.table))

    async def add_job(self, job):
        # TODO: convert job to  correct format to be inserted [{job_id: 123, ... etc]
        await self._execute(self.table.insert(), job)

    def update_job(self, job):
        pass

    def remove_job(self, job_id):
        pass

    def remove_all_jobs(self):
        pass
