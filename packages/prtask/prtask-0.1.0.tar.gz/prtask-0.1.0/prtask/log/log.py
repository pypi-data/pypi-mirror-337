from loguru import logger
import os
import sys


class LoguruLogger:
    """
    Loguru日志工具类封装
    """

    def __init__(self):
        # 移除默认的控制台输出
        logger.remove()

        # 设置控制台输出格式和级别
        self._file_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<level>{message}</level>"
        )

        # 默认配置
        self._log_path = "logs"
        self._log_file = "app.log"
        self._rotation = "10 MB"  # 日志文件大小达到10MB时轮转
        self._retention = "7 days"  # 保留7天的日志
        self._compression = "zip"  # 日志轮转时压缩为zip格式
        self._level = "DEBUG"  # 默认日志级别
        self.add_level()

    def init_logger(
            self,
            log_path: str = "logs",
            log_file: str = "app.log",
            rotation: str = "10 MB",
            retention: str = "7 days",
            compression: str = "zip",
            level: str = "DEBUG",
            console_output: bool = True,
            file_output: bool = True
    ):
        """
        初始化日志配置

        :param log_path: 日志目录路径
        :param log_file: 日志文件名
        :param rotation: 日志轮转条件
        :param retention: 日志保留时间
        :param compression: 日志压缩格式
        :param level: 日志级别
        :param console_output: 是否输出到控制台
        :param file_output: 是否输出到文件
        """
        self._log_file = log_file
        self._rotation = rotation
        self._retention = retention
        self._compression = compression
        self._level = level
        self.add_level("Start")
        self.add_level("Complete")
        self.add_level("State")

        # 确保日志目录存在
        os.makedirs(self._log_path, exist_ok=True)

        # 移除所有现有的handler
        logger.remove()

        # 添加控制台输出
        if console_output:
            logger.add(
                sys.stdout,
                level=self._level,
                format=self._file_format,
                colorize=True,
                backtrace=True,
                diagnose=True
            )

        # 添加文件输出
        if file_output:
            log_file_path = os.path.join(log_path, self._log_file)
            logger.add(
                log_file_path,
                rotation=self._rotation,
                retention=self._retention,
                compression=self._compression,
                format=self._file_format,
                level=self._level,
                enqueue=True  # 异步安全
            )

    def get_logger(self):
        """
        获取logger实例
        """
        return logger

    @staticmethod
    def add_level(name: str = "CONFIG", level: int = 25, **kwargs):
        """添加自定义的CONFIG日志级别"""
        try:
            level_name = name
            level_value = level
            logger.level(level_name, level_value, **kwargs)
        except:
            pass


global_logger = LoguruLogger()


# 快捷方法
def init_logger(*args, **kwargs):
    """初始化日志配置"""
    LoguruLogger().init_logger(*args, **kwargs)


class AioLogger:
    @staticmethod
    def debug(msg: str, *args, **kwargs):
        """DEBUG级别日志"""
        global_logger.get_logger().debug(msg, *args, **kwargs)

    @staticmethod
    def info(msg: str, *args, **kwargs):
        """INFO级别日志"""
        global_logger.get_logger().info(msg, *args, **kwargs)

    @staticmethod
    def success(msg: str, *args, **kwargs):
        """INFO级别日志"""
        global_logger.get_logger().success(msg, *args, **kwargs)

    @staticmethod
    def warning(msg: str, *args, **kwargs):
        """WARNING级别日志"""
        global_logger.get_logger().warning(msg, *args, **kwargs)

    @staticmethod
    def error(msg: str, *args, **kwargs):
        """ERROR级别日志"""
        global_logger.get_logger().error(msg, *args, **kwargs)

    @staticmethod
    def exception(msg: str, *args, **kwargs):
        """EXCEPTION级别日志"""
        global_logger.get_logger().exception(msg, *args, **kwargs)

    @staticmethod
    def critical(msg: str, *args, **kwargs):
        """CRITICAL级别日志"""
        global_logger.get_logger().critical(msg, *args, **kwargs)

    @staticmethod
    def config(msg: str, *args, **kwargs):
        """CRITICAL级别日志"""
        global_logger.get_logger().log("CONFIG", msg, *args, **kwargs)

    @staticmethod
    def start(msg: str, *args, **kwargs):
        """CRITICAL级别日志"""
        global_logger.get_logger().log("Start", msg, *args, **kwargs)

    @staticmethod
    def complete(msg: str, *args, **kwargs):
        """CRITICAL级别日志"""
        global_logger.get_logger().log("Complete", msg, *args, **kwargs)

    @staticmethod
    def state(msg: str, *args, **kwargs):
        """CRITICAL级别日志"""
        global_logger.get_logger().log("State", msg, *args, **kwargs)

    @staticmethod
    def log(level: str, msg: str, *args, **kwargs):
        """自定义级别日志"""
        global_logger.get_logger().log(level, msg, *args, **kwargs)
