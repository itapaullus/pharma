import logging


level = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}
DEBUG_LEVEL = 'DEBUG'


class Logger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)
        self.setLevel(level[DEBUG_LEVEL])
        sh = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh.setFormatter(fmt=formatter)
        self.addHandler(sh)
