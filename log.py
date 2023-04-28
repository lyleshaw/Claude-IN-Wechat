import logging


def _get_logger(name):
    logger_ = logging.getLogger(name)
    logger_.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger_.addHandler(ch)
    return logger_


logger = _get_logger(__name__)
