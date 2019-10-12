from loguru import logger


# self-rule format
class Formatter:
    def __init__(self):
        self.padding = 0

    def format0(self, record):
        prefix = "{name}:{function}:{line}".format(**record)
        self.padding = max(self.padding, len(prefix))
        prefix = "{0: <{1}}".format(prefix, self.padding)
        fmt = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | " + prefix + " | {message}\n{exception}"
        return fmt

    def format(self, record):
        prefix = "{name}".format(**record)
        self.padding = max(self.padding, len(prefix))
        prefix = "{0: <{1}}".format(prefix, self.padding)
        fmt = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | " + prefix + " | {message}\n{exception}"
        return fmt


log = logger


def log_init(console_out=False):
    if console_out:
        # built-in logging output
        logger.remove()

    formatter = Formatter()

    info_path = './kline_filler/logs/info_logs/info.log'
    log.add(info_path, format=formatter.format0, rotation="64 MB",
            filter=lambda record: record["level"].no == 20,
            backtrace=False)

    request_path = './kline_filler/logs/info_logs/request.log'
    log.add(request_path, format=formatter.format, rotation="64 MB",
            filter=lambda record: record["level"].no == 10,
            backtrace=False)

    err_path = './kline_filler/logs/error_logs/error.log'
    log.add(err_path, format=formatter.format, rotation="64 MB",
            filter=lambda record: record["level"].no >= 40, backtrace=False)

    log.info('log module loaded')
