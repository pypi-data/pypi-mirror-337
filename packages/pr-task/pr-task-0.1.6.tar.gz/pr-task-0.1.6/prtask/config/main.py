import os
from typing import Optional
from prtask.log.log import init_logger


class LogConfig:
    log_file = "aioRedis.log"  # 日志文件名
    log_size = "100 MB"  # 每100MB轮转一次
    log_days = "30 days"  # 保留30天日志
    log_level = "DEBUG"  # 日志级别
    log_save = False  # 输出到文件
    log_console = True  # 输出到控制台
    log_compression = "zip"  # 使用zip压缩
    work_dir: Optional[str] = os.getcwd()  # 工作目录


    def __init__(self):
        init_logger(
            log_path=self.work_dir,
            log_file=self.log_file,
            rotation=self.log_size,
            retention=self.log_days,
            compression=self.log_compression,
            level=self.log_level,
            console_output=self.log_console,
            file_output=self.log_save
        )


class DefaultConfig:
    key: str = "prtask:tasks"
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 8
    qps: int = 100
    delay: int = 1.314
    initLog: bool = True
    lua_script = """
            local min_score = ARGV[1]
            local max_score = ARGV[2]
            local set_score = ARGV[3]
            local count = ARGV[4]

            local real_datas = {}
            if count ~= '' then
                for i = 1, count do
                    local data_with_score = redis.call('zrangebyscore', 
                        KEYS[1], min_score, max_score, 'withscores', 'limit', 0, 1)
                    if #data_with_score > 0 then
                        local data = data_with_score[1]
                        table.insert(real_datas, data)
                        redis.call('zincrby', KEYS[1], set_score - data_with_score[2], data)
                    end
                end
            else
                local datas = redis.call('zrangebyscore', 
                    KEYS[1], min_score, max_score, 'withscores')
                for i=1, #datas, 2 do
                    table.insert(real_datas, datas[i])
                    redis.call('zincrby', KEYS[1], set_score - datas[i+1], datas[i])
                end
            end
            return real_datas
            """
    work_dir: Optional[str] = os.getcwd()  # 工作目录
    from_url = f"redis://{redis_host}"
