import asyncio
import random
import aioredis
from typing import List
from prtask.config.main import LogConfig, DefaultConfig
from prtask.log.log import AioLogger as logger

class AioRedis(LogConfig, DefaultConfig):
    log_save = True

    def __init__(self):
        """
        Redis 异步任务队列处理器
        """
        super().__init__()
        self.init()
        self.redis_client = aioredis.from_url(url=self.from_url, port=self.redis_port, db=self.redis_db)
        self._poll_script = self.redis_client.register_script(self.lua_script)

    def init(self):
        if self.initLog:
            default_len = 48
            logger.start(f"\n+{'-' * (default_len - 2)}+\n"
                         f"|{'prtask Service'.center(default_len - 2)}|\n"
                         f"|{'key => {}'.format(self.key).center(default_len - 2)}|\n"
                         f"|{'qps => {}'.format(self.qps).center(default_len - 2)}|\n"
                         f"|{'delay => {}'.format(self.delay).center(default_len - 2)}|\n"
                         f"+{'-' * (default_len - 2)}+")

    async def execute_task(self, task) -> None:
        """执行单个任务"""
        task = task.decode('utf-8')
        try:
            await self.main(task)
        except Exception as e:
            logger.error(f"[Task Failed] {task}: {str(e)}")
        finally:
            await self.redis_client.zadd(self.key, {task: 1})

    async def _control_concurrency(self) -> None:
        """并发控制"""
        while len(asyncio.all_tasks()) - 2 >= self.qps:
            await asyncio.sleep(1)

    @staticmethod
    def get_all_tasks():
        return len(asyncio.all_tasks()) - 2

    async def listing(self):
        active_tasks = self.get_all_tasks()
        if active_tasks >= self.qps:
            logger.state(f"Tasks Running => {active_tasks}/{self.qps}")
        await asyncio.sleep(5)

    async def _monitor_status(self) -> None:
        """系统状态监控"""
        while True:
            await self.listing()

    async def _fetch_tasks(self, batch_size: int = 10) -> List[str]:
        """获取待处理任务"""
        return await self._poll_script(
            keys=[self.key],
            args=[-1, -1, 0, batch_size]
        )

    async def start(self) -> None:
        """启动任务处理系统"""
        logger.info("prtask Listing...")
        asyncio.create_task(self._monitor_status())

        while True:
            tasks = await self._fetch_tasks()
            for task_id in tasks:
                await self._control_concurrency()
                asyncio.create_task(self.execute_task(task_id))
            await asyncio.sleep(self.delay)

    async def main(self, task):
        logger.start(task)
        await asyncio.sleep(random.randint(1, 5))
        logger.complete(task)
