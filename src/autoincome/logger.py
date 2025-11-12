
import logging, os, sys, pathlib

def setup_logger():
    logs = pathlib.Path(os.getcwd()) / "logs"
    logs.mkdir(exist_ok=True)
    logger = logging.getLogger("autoincome")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    fh = logging.FileHandler(logs / "run.log")
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    ch.setFormatter(fmt); fh.setFormatter(fmt)
    if not logger.handlers:
        logger.addHandler(ch); logger.addHandler(fh)
    return logger

logger = setup_logger()
